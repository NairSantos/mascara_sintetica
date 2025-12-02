# Projeto Máscara Sintética 

Aplicação leve (Flask + SQLite) para **mascarar dados sensíveis** e **gerar dados sintéticos** que preservam padrões estatísticos dos dados originais, ajudando a proteger informações pessoais e permitindo uso seguro em testes, estudos e protótipos.

---

##  Ideia Geral

O objetivo do projeto é criar um sistema capaz de:

- **Mascarar dados sensíveis** (nome, CPF, renda, idade etc.);
- **Gerar registros sintéticos realistas**, mas não rastreáveis ao indivíduo original;
- Permitir visualização e exportação via **interface web simples**, feita sem frameworks pesados.

A proposta é proteger informações pessoais e facilitar experimentos envolvendo privacidade.

---

##  Planejamento do Projeto

O sistema possui três camadas principais:

### 1. Front-end (Interface do Usuário)

- Interface em **HTML, CSS e JavaScript puro**;
- Botões para:
  - Importar seed.json;
  - Treinar modelo;
  - Gerar registros sintéticos;
  - Exportar dados;
  - Mascarar CPFs reais;
  - Resetar banco;
- Tabela com destaque para registros sintéticos.

### 2. Back-end (API e Banco de Dados)

- API em **Python (Flask)**;
- Banco **SQLite (`data.db`)**;
- Rotas REST para manipulação dos dados;
- Armazenamento do modelo (`synth_model.joblib`).

### 3. Geração de Dados Sintéticos

- Modelo estatístico com **Gaussian Mixture (scikit-learn)**;
- Aprendizado de padrões de idade e renda;
- Uso opcional de **Faker** para nomes, cidades e CPFs falsos.

---

##  Tecnologias Utilizadas

| Camada | Tecnologias |
|--------|-------------|
| **Front-end** | HTML, CSS, JavaScript |
| **Back-end** | Python (Flask) |
| **Banco de Dados** | SQLite |
| **Machine Learning** | scikit-learn, numpy, pandas |
| **Geração de dados falsos** | Faker |

---

#  Funcionalidades Principais

- Importação de registros via `data/seed.json`;
- Persistência em `data.db`;
- Treinamento de modelo estatístico;
- Geração de dados sintéticos coerentes;
- Mascaramento de CPFs reais;
- Exportação para `synthetics_export.csv`;
- Interface web com botões de ação.

---

#  Estrutura do Projeto

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

#  Quickstart (Passo a Passo)

1. Clone o projeto  
```bash
git clone <link-do-repo>
```

2. Entre no diretório  
```bash
cd mascara-sintetica
```

3. Crie e ative o ambiente virtual  
```powershell
python -m venv venv
venv\Scripts\activate.bat
```

4. Instale dependências  
```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

5. Execute o projeto  
```bash
python app.py
```

6. Acesse no navegador  
```
http://127.0.0.1:5000/
```

---

#  Endpoints da API

| Método | Rota | Função |
|-------|------|--------|
| GET | `/` | Interface web |
| POST | `/import_seed` | Importar seed.json |
| GET | `/users` | Listar usuários |
| POST | `/users` | Criar usuário |
| PUT | `/users/<id>` | Atualizar usuário |
| DELETE | `/users/<id>` | Deletar usuário |
| POST | `/train` | Treinar modelo |
| POST | `/generate` | Gerar sintéticos |
| POST | `/mask_cpfs` | Mascarar CPFs |
| GET | `/export_synthetics` | Exportar CSV |
| POST | `/reset_db` | Resetar banco |

---

#  Banco de Dados

Tabela `users`:

```sql
id INTEGER PRIMARY KEY,
nome TEXT,
cpf TEXT,
idade INTEGER,
cidade TEXT,
renda REAL,
synthetic INTEGER DEFAULT 0
```

- `synthetic = 0` → dado original  
- `synthetic = 1` → dado sintético

---

#  Exemplo de Uso pela Interface

1. Clique em **Importar Seed**  
2. Clique em **Treinar Modelo**  
3. Clique em **Gerar Sintéticos**  
4. Clique em **Exportar**  
5. Clique em **Mascarar CPFs** (opcional)  
6. Clique em **Resetar DB** (cuidado!)  

---

#  Exemplo de seed.json

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

#  Contribuição

- **Nair Santos de Sousa**  
- **Marcela Aparecida Almeida**  
- **Raissa Santos Ramos**


---
