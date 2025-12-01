"""
Script para testar a conexão com o Supabase
Execute: python test_connection.py
"""
import sys
from db_config import get_connection, DB_CONFIG, ENV_FILE

print("=" * 60)
print("TESTE DE CONEXÃO COM SUPABASE")
print("=" * 60)
print()

# Verifica se o arquivo .env existe
if not ENV_FILE.exists():
    print(f"❌ Arquivo .env não encontrado em: {ENV_FILE}")
    print("   Crie o arquivo .env copiando do env.example")
    sys.exit(1)
else:
    print(f"✅ Arquivo .env encontrado: {ENV_FILE}")

print()
print("📋 Configurações de conexão:")
print(f"   Host: {DB_CONFIG['host']}")
print(f"   Port: {DB_CONFIG['port']}")
print(f"   Database: {DB_CONFIG['database']}")
print(f"   User: {DB_CONFIG['user']}")
print(f"   SSL Mode: {DB_CONFIG.get('sslmode', 'not set')}")
print(f"   Password: {'✅ Configurada' if DB_CONFIG['password'] else '❌ NÃO CONFIGURADA'}")

if not DB_CONFIG['password']:
    print()
    print("=" * 60)
    print("❌ ERRO: Senha não configurada!")
    print("=" * 60)
    print("Para corrigir:")
    print("1. Abra o arquivo .env na pasta backend")
    print("2. Encontre a linha: DB_PASSWORD=sua_senha_aqui")
    print("3. Substitua 'sua_senha_aqui' pela senha real do Supabase")
    print("4. Obtenha a senha em: https://txrkcdweknuxdbwaoekz.supabase.co")
    print("   Settings > Database > Database Password")
    sys.exit(1)

print()
print("=" * 60)
print("🔍 Tentando conectar...")
print("=" * 60)

try:
    conn = get_connection()
    cursor = conn.cursor()
    
    # Testa uma query simples
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print(f"✅ Conexão estabelecida com sucesso!")
    print(f"   PostgreSQL Version: {version[:50]}...")
    
    # Testa se as tabelas existem
    print()
    print("🔍 Verificando tabelas...")
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name IN ('usuario', 'tarefa')
        ORDER BY table_name;
    """)
    tabelas = cursor.fetchall()
    
    if tabelas:
        print("✅ Tabelas encontradas:")
        for tabela in tabelas:
            print(f"   - {tabela[0]}")
    else:
        print("⚠️  Tabelas 'usuario' e 'tarefa' não encontradas")
        print("   Certifique-se de que as tabelas foram criadas no Supabase")
    
    cursor.close()
    conn.close()
    
    print()
    print("=" * 60)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    
except Exception as e:
    print()
    print("=" * 60)
    print("❌ ERRO NA CONEXÃO")
    print("=" * 60)
    print(f"Erro: {e}")
    print()
    print("Possíveis soluções:")
    print("1. Verifique se a senha no arquivo .env está correta")
    print("2. Verifique se o firewall permite conexões na porta 5432")
    print("3. Verifique se o host está correto")
    print("4. Tente desabilitar temporariamente o firewall/antivírus")
    sys.exit(1)

