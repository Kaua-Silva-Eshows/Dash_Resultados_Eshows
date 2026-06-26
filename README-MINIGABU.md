# README-MINIGABU — Dashboard Eshows

> Arquivo local do Mini_Gabu. Preservado pelo `sync_dashboard_eshows.py` — nunca sobrescrito pelo upstream.

## Setup local

```powershell
$dash = "c:\Users\user\OneDrive\FGV-SP\Claude\Mini_Gabu\brands\eshows\dashboard_eshows"

# Criar venv com Python 3.14
py -3.14 -m venv "$dash\.venv"

# Instalar dependências
& "$dash\.venv\Scripts\pip.exe" install --prefer-binary -r "$dash\requirements.txt"

# Rodar o dashboard
& "$dash\.venv\Scripts\streamlit.exe" run "$dash\main.py"
```

**Nota Python:** O dashboard usa Python 3.12 em produção (Streamlit Cloud). O venv local roda 3.14.
Se alguma lib não tiver wheel para 3.14, instalar via `--prefer-binary` ou fixar versão compatível.

## Secrets

O arquivo `.streamlit/secrets.toml` contém as credenciais dos três bancos:
- `[mysql_eshows]` — DB de faturamento (eshows-3.czzecscahytf.us-east-2.rds.amazonaws.com)
- `[mysql_grupoe]` — DB de custos Eshows (homolog.cvuwkhnpr3rt.us-east-2.rds.amazonaws.com / EPM_GRUPOE)
- `[mysql_blueme]` — DB de custos BlueME (homolog.cvuwkhnpr3rt.us-east-2.rds.amazonaws.com / EPM_FB)

Nunca commitado — protegido por `.gitignore` local e por `brands/**/.streamlit/secrets.toml` no `.gitignore` raiz do Mini_Gabu.

## Protocolo de atualização

```powershell
# Para fazer mudanças no dashboard:
cd brands\eshows\dashboard_eshows
git checkout main
git pull origin main
git checkout -b fix/descricao-da-mudanca

# ... editar arquivos específicos ...

git status               # secrets.toml NÃO pode aparecer aqui
git add <arquivos-específicos>
git commit -m "fix: descrição"
git push origin fix/descricao-da-mudanca
# ... abrir PR no GitHub ...
# ... após merge ...

cd ..\..\..   # volta para raiz do Mini_Gabu
git submodule update --remote brands/eshows/dashboard_eshows
git add brands/eshows/dashboard_eshows
git commit -m "chore: atualiza submodule dashboard_eshows"
```

**NUNCA usar `git add .` ou `git add -A`** — sempre adicionar arquivos específicos.

## Atualizar sem mudanças (puxar upstream)

```powershell
# Opção 1: via submodule (preferencial — atualiza o ponteiro no Mini_Gabu)
git submodule update --remote brands/eshows/dashboard_eshows
git add brands/eshows/dashboard_eshows
git commit -m "chore: atualiza submodule dashboard_eshows"

# Opção 2: via sync script (espelhamento de arquivos, sem atualizar ponteiro)
python scripts/sync_dashboard_eshows.py
```

## Queries no Mini_Gabu

As queries SQL derivadas do dashboard estão em `brands/eshows/queries/`.
Arquitetura de 3 bancos — usar `db_query.py` com o brand correto para cada banco:

```bash
# Faturamento (banco eshows)
python scripts/db_query.py --brand eshows --file brands/eshows/queries/01_faturamento.sql

# Custos Eshows (banco grupoe)
python scripts/db_query.py --brand eshows-grupoe --file brands/eshows/queries/02_custos_eshows.sql

# Custos BlueME (banco blueme/EPM_FB)
python scripts/db_query.py --brand eshows-blueme --file brands/eshows/queries/03_custos_blueme.sql
```
