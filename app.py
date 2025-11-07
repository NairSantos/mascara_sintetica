import os
import json
import sqlite3
from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import joblib
from collections import Counter
from faker import Faker

DB_PATH = "data.db"
MODEL_PATH = "synth_model.joblib"
SEED_JSON = "data/seed.json"

app = Flask(__name__, template_folder="templates")
fake = Faker("pt_BR")

# --- DB helpers ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        cpf TEXT,
        idade INTEGER,
        cidade TEXT,
        renda REAL,
        synthetic INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def insert_user(record):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (id, nome, cpf, idade, cidade, renda, synthetic)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (record.get("id"), record.get("nome"), record.get("cpf"),
              record.get("idade"), record.get("cidade"), record.get("renda"),
              record.get("synthetic", 0)))
    conn.commit()
    conn.close()

def update_user(uid, record):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE users SET nome=?, cpf=?, idade=?, cidade=?, renda=?, synthetic=?
        WHERE id=?
    """, (record.get("nome"), record.get("cpf"), record.get("idade"),
          record.get("cidade"), record.get("renda"), record.get("synthetic",0), uid))
    conn.commit()
    conn.close()

def delete_user(uid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (uid,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

# --- API endpoints ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/import_seed", methods=["POST"])
def import_seed():
    try:
        init_db()
        if not os.path.exists(SEED_JSON):
            return jsonify({"status": "error", "error": f"Arquivo {SEED_JSON} não encontrado."}), 404

        with open(SEED_JSON, "r", encoding="utf-8") as f:
            arr = json.load(f)

        if not isinstance(arr, list):
            return jsonify({"status": "error", "error": "Formato inválido: deve ser lista de registros."}), 400

        for r in arr:
            insert_user(r)
        return jsonify({"status": "ok", "imported": len(arr)})

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        df = get_all_users()
        return df.to_json(orient="records", force_ascii=False)
    else:
        rec = request.get_json()
        # create new id if not provided
        if "id" not in rec or rec["id"] is None:
            df = get_all_users()
            maxid = int(df["id"].max()) if not df.empty else 0
            rec["id"] = maxid + 1
        insert_user(rec)
        return jsonify({"status":"created","id": rec["id"]})

@app.route("/users/<int:uid>", methods=["PUT","DELETE"])
def user_modify(uid):
    if request.method == "PUT":
        rec = request.get_json()
        update_user(uid, rec)
        return jsonify({"status":"updated","id":uid})
    else:
        delete_user(uid)
        return jsonify({"status":"deleted","id":uid})

# --- Simple ML training and generation ---
def train_model():
    df = get_all_users()
    if df.empty:
        raise RuntimeError("No data to train on.")
    # numeric features: idade, renda
    numeric = df[["idade","renda"]].dropna().values
    # fit simple GMM
    gmm = GaussianMixture(n_components=min(3, max(1, len(numeric)//5)), random_state=0)
    gmm.fit(numeric)

    # categorical distributions
    cidade_counts = Counter(df["cidade"].astype(str).values)
    nome_counts = Counter(df["nome"].astype(str).values)

    # CPF digit distribution per position (assume 11 digits)
    cpfs = df["cpf"].astype(str).dropna().values
    cpf_digits = []
    for pos in range(11):
        pos_counts = Counter()
        for c in cpfs:
            s = "".join([ch for ch in c if ch.isdigit()])
            if len(s) < 11:
                # pad left with zeros if weird
                s = s.zfill(11)
            pos_counts.update(s[pos])
        cpf_digits.append(dict(pos_counts))

    model = {
        "gmm": gmm,
        "cidade_counts": dict(cidade_counts),
        "nome_counts": dict(nome_counts),
        "cpf_digits": cpf_digits
    }
    joblib.dump(model, MODEL_PATH)
    return model

def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)

def sample_from_counts(counts_dict):
    items = list(counts_dict.keys())
    weights = np.array(list(counts_dict.values()), dtype=float)
    weights = weights / weights.sum()
    return np.random.choice(items, p=weights)

def generate_cpf_from_digit_probs(cpf_digits_probs):
    s = ""
    for pos_probs in cpf_digits_probs:
        items = list(pos_probs.keys())
        weights = np.array(list(pos_probs.values()), dtype=float)
        if weights.sum() == 0:
            weights = np.ones(len(items))
        weights = weights / weights.sum()
        digit = np.random.choice(items, p=weights)
        s += digit
    return s

@app.route("/train", methods=["POST"])
def train_endpoint():
    try:
        model = train_model()
        return jsonify({"status":"trained"})
    except Exception as e:
        return jsonify({"status":"error","error": str(e)}), 400

@app.route("/generate", methods=["POST"])
def generate_endpoint():
    """
    Body: {"n": 10}
    Generates n synthetic records and inserts into DB with synthetic=1
    """
    data = request.get_json() or {}
    n = int(data.get("n", 1))

    # tenta carregar modelo treinado; se não houver, treina um novo
    model = load_model()
    if model is None:
        try:
            model = train_model()
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 400

    # extrai componentes do modelo
    gmm = model.get("gmm")
    if gmm is None:
        return jsonify({"status": "error", "error": "Modelo inválido: faltando GMM"}), 400

    # carrega usuários existentes para evitar CPFs repetidos
    df = get_all_users()
    existing_cpfs = set(df["cpf"].tolist()) if not df.empty else set()
    maxid = int(df["id"].max()) if not df.empty else 0

    generated = []
    for i in range(n):
        # amostra idade e renda do modelo GMM
        sample = gmm.sample(1)[0].reshape(-1)
        idade = int(max(16, min(90, round(sample[0]))))
        renda = float(max(0.0, round(sample[1], 2)))

        # escolhe cidade e nome
        cidade = sample_from_counts(model["cidade_counts"])
        if np.random.rand() < 0.6 and len(model["nome_counts"]) > 0:
            nome = sample_from_counts(model["nome_counts"])
        else:
            nome = fake.name()

        # gera CPF e evita duplicados
        cpf = generate_cpf_from_digit_probs(model["cpf_digits"])
        attempts = 0
        while cpf in existing_cpfs and attempts < 10:
            cpf = generate_cpf_from_digit_probs(model["cpf_digits"])
            attempts += 1
        if cpf in existing_cpfs:
            cpf = cpf[:-2] + f"{np.random.randint(0,100):02d}"  # garante unicidade

        existing_cpfs.add(cpf)
        maxid += 1

        rec = {
            "id": maxid,
            "nome": nome,
            "cpf": cpf,
            "idade": idade,
            "cidade": cidade,
            "renda": renda,
            "synthetic": 1
        }

        insert_user(rec)
        generated.append(rec)

    return jsonify({"status": "ok", "generated": generated})


##Exportar apenas registros sintéticos para CSV
@app.route("/export_synthetics", methods=["GET"])
def export_synthetics():
    import csv
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM users WHERE synthetic=1", conn)
    conn.close()
    out_path = "synthetics_export.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    return jsonify({"status":"ok","file": out_path, "rows": len(df)})

##resetar banco
@app.route("/reset_db", methods=["POST"])
def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
    return jsonify({"status":"reset"})

##Evita inserir CPF duplicado quando gerar sintéticos
def cpf_exists(cpf):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE cpf=? LIMIT 1", (cpf,))
    exists = c.fetchone() is not None
    conn.close()
    return exists




if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
