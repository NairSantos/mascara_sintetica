SYNTHETIC-MASKER — README_RUN.txt
=================================

Resumo
------
Projeto demo que importa um JSON de seed, salva em um banco SQLite, treina um modelo simples para gerar dados sintéticos e expõe uma interface web mínima.

Pré-requisitos
--------------
- Python 3.8 — 3.11 recomendado (verifique com `python --version` ou `py -3 --version`)

Estrutura do projeto
--------------------
mascara sintetica/
├─ data/
│  └─ seed.json
├─ app.py
├─ requirements.txt
├─ templates/
│  └─ index.html
└─ README_RUN.txt

Passo a passo (cmd.exe)
-----------------------
1. Abra o Prompt de Comando (cmd.exe).
2. Navegue até a pasta do projeto (use aspas por causa dos espaços):
   cd na pasta

3. Criar virtualenv:
   python -m venv venv
   (se `python` não funcionar, tente `py -3 -m venv venv`)

4. Ativar o virtualenv:
   venv\Scripts\activate.bat
   (aparecerá (venv) no prompt)

5. Atualizar pip/setuptools/wheel (recomendado):
   venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel

6. Instalar dependências:
   venv\Scripts\python.exe -m pip install -r requirements.txt

7. Rodar a aplicação:
   python app.py
   (ou venv\Scripts\python.exe app.py)

8. Abra no navegador:
   http://127.0.0.1:5000/

Passo a passo (PowerShell)
--------------------------



Comandos principais da aplicação (APIs)
--------------------------------------
- Importar seed.json para o banco:
  POST http://127.0.0.1:5000/import_seed
  (no front há botão "Importar seed.json")

- Listar usuários:
  GET http://127.0.0.1:5000/users

- Criar usuário (body JSON):
  POST http://127.0.0.1:5000/users
  exemplo body:
  {"nome":"Fulano","cpf":"00011122233","idade":25,"cidade":"Cidade","renda":2000.0}

- Atualizar usuário:
  PUT http://127.0.0.1:5000/users/<id>

- Deletar usuário:
  DELETE http://127.0.0.1:5000/users/<id>

- Treinar modelo:
  POST http://127.0.0.1:5000/train

- Gerar N sintéticos:
  POST http://127.0.0.1:5000/generate
  body JSON: {"n": 5}

Front-end
---------
Abra `http://127.0.0.1:5000/` e use os botões:
- Importar seed.json
- Treinar modelo
- Gerar 5 sintéticos
- Atualizar lista

Solução de problemas comuns
---------------------------
1) Aviso de pip antigo:
   - Ignorar (apenas aviso) ou atualizar com:
     venv\Scripts\python.exe -m pip install --upgrade pip

2) Erro ao compilar `numpy` / `scikit-learn`:
   - Instalar Build Tools for Visual Studio (Visual C++ build tools).
     Link: procurar "Build Tools for Visual Studio" no site da Microsoft.
   - Alternativa: usar conda/miniconda (recomendada no Windows):
     * Instale Miniconda/Anaconda
     * crie um ambiente: conda create -n masker python=3.11 -y
     * conda activate masker
     * conda install numpy pandas scikit-learn joblib faker -y
     * pip install Flask
     * depois rode `python app.py` dentro do ambiente conda

3) Erro de permissão no PowerShell ao ativar:
   - Execute:
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
   - Então ative: .\venv\Scripts\Activate.ps1

4) Problema com paths que têm espaços:
   - Sempre use aspas ao `cd` (ex.: cd "C:\Users\FATEC ZONA LESTE\Downloads\mascara sintetica")

Considerações de segurança e uso
-------------------------------
- Este projeto é um **protótipo** educacional. Não use em produção sem:
  - aplicar políticas formais de anonimização (k-anon, differential privacy),
  - revisar conformidade LGPD/GDPR,
  - proteger endpoints com autenticação/autorização e TLS.

- Os CPFs no seed e gerados são apenas para demonstração. Em produção não gere CPFs reais sem cuidado legal.

Dicas extras
------------
- Para parar o servidor Flask no terminal: Ctrl+C
- Para desativar o virtualenv: deactivate
- Se quiser exportar dados sintéticos para CSV, eu posso adicionar um endpoint `/export_synthetics` que salva `synthetics.csv`.

Versões de teste
----------------
Testado com Python 3.10 / 3.11 e pacotes listados em requirements.txt. Em Windows, usar conda costuma reduzir problemas de build.

Fim do README
-------------
Se quiser, eu adapto esse README para:
- incluir comandos prontos para colar no terminal (cmd / PowerShell),
- criar um arquivo `run_windows.ps1` com todos os passos automatizados,
- ou adicionar um endpoint de exportação CSV automáticamente.


