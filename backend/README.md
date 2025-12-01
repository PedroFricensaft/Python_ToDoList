# Backend - ToDoList

Backend simples em Flask conectado ao PostgreSQL.

## Como usar:

### 1. Recriar ambiente virtual (se o venv foi criado no Linux):
```powershell
# Remove o venv antigo (opcional)
Remove-Item -Recurse -Force venv

# Cria novo venv para Windows
python -m venv venv

# Ativa o venv
venv\Scripts\Activate.ps1

# Instala dependências
pip install -r requirements.txt
```

### 2. Configurar banco de dados:
Crie um arquivo `.env` na pasta backend (opcional):
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=todo_list
DB_USER=postgres
DB_PASSWORD=root
```

Ou edite `db_config.py` diretamente.

### 3. Iniciar servidor:

**Opção A - Script PowerShell:**
```powershell
.\start.ps1
```

**Opção B - Manual:**
```powershell
python app.py
```

**Opção C - Com venv ativado:**
```powershell
venv\Scripts\Activate.ps1
python app.py
```

O servidor estará rodando em: http://localhost:5000

## Endpoints:

- `GET /` - Teste do servidor
- `GET /tarefas` - Lista todas as tarefas
- `POST /tarefas` - Cria nova tarefa
- `PUT /tarefas/<id>/concluir` - Marca tarefa como concluída
- `DELETE /tarefas/<id>` - Deleta tarefa

