# Máscara Sintética (Synthetic Masker)

> Projeto simples para gerar e mascarar dados sintéticos.

Uma aplicação leve (Flask + SQLite) que importa um `seed.json`, salva em banco, treina um modelo estatístico simples e gera registros sintéticos parecidos com os reais. Útil para testes, ensino e experimentos com preservação de privacidade.

---

## Funcionalidades principais
- Importa um `data/seed.json` com registros iniciais.
- Persiste em `data.db` (SQLite).
- Treina um modelo simples (Gaussian Mixture) para **idade** e **renda**.
- Gera registros sintéticos coerentes (nome, CPF formatado, idade, cidade, renda).
- Endpoint para **mascarar CPFs** reais (substituir por sintéticos).
- Exporta registros sintéticos para `synthetics_export.csv`.
- Interface web mínima para operações (botões para importar, treinar, gerar, exportar, resetar).

---

## Aviso importante
- Faça backup do `data.db` antes de operações destrutivas (reset).

---

## Estrutura do projeto
```
mascara-sintetica/
├─ data/
│  └─ seed.json
├─ templates/
│  └─ index.html
├─ app.py
├─ requirements.txt
└─ README.md
```

---

## Quickstart (passo a passo)

1. De git clone neste projeto
2. Descompacte o projeto
3.  Abra o terminal e entre na pasta do projeto:
```powershell
cd na pasta respectiva
```

2. Crie e ative o ambiente virtual:
```powershell
python -m venv venv
# cmd:
venv\Scripts\activate.bat

```

3. Atualize pip e instale dependências:
```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

4. Inicie a aplicação:
```bash
python app.py
```

5. Abra no navegador:
```
http://127.0.0.1:5000/
```

> Se tiver problemas com `numpy` / `scikit-learn` no Windows, considerar usar **Miniconda** (conda cria ambientes com dependências binárias prontas).

---

## Endpoints (API)
- `GET /` — interface web.
- `POST /import_seed` — importa `data/seed.json` para o banco.
- `GET /users` — lista todos os usuários (JSON).
- `POST /users` — cria novo usuário (JSON body).
- `PUT /users/<id>` — atualiza usuário.
- `DELETE /users/<id>` — deleta usuário.
- `POST /train` — treina modelo (gera `synth_model.joblib`).
- `POST /generate` — gera registros sintéticos (body: `{"n": <numero>}`).
- `POST /mask_cpfs` — substitui CPFs reais por CPFs sintéticos (marca como `synthetic=1`).
- `GET /export_synthetics` — exporta registros sintéticos para `synthetics_export.csv`.
- `POST /reset_db` — reseta (apaga) o banco local `data.db` e recria a tabela.

---

## Banco de dados
- Arquivo: `data.db` (SQLite).
- Tabela `users` (esquema):
```sql
id INTEGER PRIMARY KEY,
nome TEXT,
cpf TEXT,
idade INTEGER,
cidade TEXT,
renda REAL,
synthetic INTEGER DEFAULT 0
```
- `synthetic = 0` → registro original; `synthetic = 1` → registro gerado/mascarado.

---

## Exemplo rápido de uso (via UI)
1. `Importar seed.json` → popula o banco.  
2. `Treinar modelo` → aprende padrões.  
3. `Gerar 5 sintéticos` → cria registros falsos (marcados).  
4. `Exportar sintéticos` → gera `synthetics_export.csv`.  
5. `Mascarar CPFs` → substitui CPFs reais por sintéticos (opcional).  
6. `Resetar DB` → cuidado: apaga tudo.

---

## Arquivo seed.json de exemplo
Coloque em `data/seed.json` com um array de objetos. Exemplo mínimo:
```json
[
  {"id": 1, "nome": "Lucas Silva", "cpf": "12345678909", "idade": 28, "cidade": "São Paulo", "renda": 3500.0, "synthetic": 0},
  {"id": 2, "nome": "Mariana Souza", "cpf": "98765432100", "idade": 34, "cidade": "Campinas", "renda": 4800.0, "synthetic": 0},
  {"id": 3, "nome": "Pedro Costa", "cpf": "11122233344", "idade": 22, "cidade": "Santos", "renda": 2100.0, "synthetic": 0},
  {"id": 4, "nome": "Ana Pereira", "cpf": "55566677788", "idade": 41, "cidade": "Ribeirão Preto", "renda": 6200.0, "synthetic": 0},
  {"id": 5, "nome": "Matheus Oliveira", "cpf": "22233344455", "idade": 30, "cidade": "Sorocaba", "renda": 4100.0, "synthetic": 0}
]

```

---
##  Contribuição
- Nair Santos de Sousa;
- Marcela Aparecida Almeida;
- Raissa Santos Ramos.

---
