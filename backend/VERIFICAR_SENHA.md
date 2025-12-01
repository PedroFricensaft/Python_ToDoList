# 🔍 Como Verificar se a Senha está Configurada

## Passo 1: Verificar se o arquivo .env existe

No PowerShell, execute:
```powershell
cd backend
Test-Path .env
```

Se retornar `False`, crie o arquivo:
```powershell
Copy-Item env.example .env
```

## Passo 2: Verificar o conteúdo do arquivo .env

Abra o arquivo `backend\.env` e verifique se a linha `DB_PASSWORD` está assim:

```env
DB_PASSWORD=sua_senha_real_aqui
```

**IMPORTANTE:** 
- ❌ NÃO deve estar: `DB_PASSWORD=sua_senha_aqui` (isso é placeholder)
- ❌ NÃO deve estar: `DB_PASSWORD=` (vazio)
- ✅ DEVE estar: `DB_PASSWORD=MinhaSenhaReal123!@#` (senha real)

## Passo 3: Obter a senha do Supabase

1. Acesse: **https://txrkcdweknuxdbwaoekz.supabase.co**
2. Faça login
3. Vá em **Settings** (ícone de engrenagem no menu lateral)
4. Clique em **Database**
5. Procure por uma das opções:
   - **Database Password** - copie a senha
   - **Connection string** - a senha está no formato: `postgresql://postgres.[PROJECT]:[SENHA]@...`
   - **Connection pooling** - pode ter a senha também
6. Se não encontrar, clique em **Reset database password** para definir uma nova

## Passo 4: Configurar no arquivo .env

1. Abra `backend\.env` no editor
2. Encontre a linha: `DB_PASSWORD=sua_senha_aqui`
3. Substitua `sua_senha_aqui` pela senha real que você copiou
4. **NÃO deixe espaços** antes ou depois do `=`
5. Salve o arquivo

## Passo 5: Testar a conexão

Execute o script de teste:
```powershell
cd backend
python test_connection.py
```

Se der erro de timeout, pode ser:
- Senha incorreta
- Firewall bloqueando (tente desabilitar temporariamente)
- Problema de rede

## Exemplo de arquivo .env correto:

```env
SUPABASE_URL=txrkcdweknuxdbwaoekz.supabase.co
DB_HOST=db.txrkcdweknuxdbwaoekz.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.txrkcdweknuxdbwaoekz
DB_PASSWORD=MinhaSenhaReal123!@#
DB_SSLMODE=require
```

