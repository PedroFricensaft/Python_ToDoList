# Backend - ToDoList

Backend em Flask conectado ao Supabase (PostgreSQL).

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta no Supabase com banco de dados configurado

## 🚀 Como usar:

### 1. Instalar dependências

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configurar banco de dados Supabase

1. Crie um arquivo `.env` na pasta `backend` (copie do `.env.example`)
2. Obtenha a senha do banco de dados:
   - Acesse: https://txrkcdweknuxdbwaoekz.supabase.co
   - Vá em Settings > Database
   - Copie a senha do banco de dados
3. Edite o arquivo `.env` e configure:
   ```
   DB_PASSWORD=sua_senha_real_aqui
   ```

### 3. Iniciar servidor

```powershell
python app.py
```

Ou use o script:
```powershell
.\start.ps1
```

O servidor estará rodando em: **http://localhost:5000**

## 📡 Endpoints:

- `GET /` - Teste do servidor
- `GET /tarefas` - Lista todas as tarefas
- `POST /tarefas` - Cria nova tarefa
  ```json
  {
    "titulo": "Título da tarefa",
    "descricao": "Descrição (opcional)",
    "id_usuario": 1
  }
  ```
- `PUT /tarefas/<id>/concluir` - Marca tarefa como concluída
- `DELETE /tarefas/<id>` - Deleta tarefa

## 🗄️ Estrutura do Banco de Dados

### Tabela: usuario
- `id_usuario` (serial, primary key)
- `nome` (varchar(255), not null)
- `email` (varchar(255), not null, unique)
- `senha` (varchar(255), not null)
- `idade` (int)

### Tabela: tarefa
- `id_tarefas` (serial, primary key)
- `titulo` (varchar(255), not null)
- `descricao` (varchar(255))
- `completa` (boolean, default false)
- `id_usuario` (int, foreign key -> usuario.id_usuario)

## 🔧 Informações do Supabase

- **URL:** https://txrkcdweknuxdbwaoekz.supabase.co
- **API Key:** eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4cmtjZHdla251eGRid2FvZWt6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5OTc1ODIsImV4cCI6MjA3ODU3MzU4Mn0.lXFmJVdA4WsDuOndDnXMIQTHMTfLLK1eJaWz6BluB9c
