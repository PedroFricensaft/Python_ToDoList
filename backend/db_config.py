import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

# Obtém o diretório do arquivo atual (backend/)
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / '.env'

# Carrega variáveis de ambiente do arquivo .env
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE)
else:
    load_dotenv()

# Configurações do Supabase
# URL: https://txrkcdweknuxdbwaoekz.supabase.co
# API Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4cmtjZHdla251eGRid2FvZWt6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5OTc1ODIsImV4cCI6MjA3ODU3MzU4Mn0.lXFmJVdA4WsDuOndDnXMIQTHMTfLLK1eJaWz6BluB9c

# Extrai o projeto ID da URL do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL', 'txrkcdweknuxdbwaoekz.supabase.co')
PROJECT_ID = SUPABASE_URL.replace('https://', '').replace('http://', '').replace('.supabase.co', '').strip()

# Configurações do banco de dados Supabase (PostgreSQL)
DB_CONFIG = {
    'host': os.getenv('DB_HOST', f'db.{PROJECT_ID}.supabase.co'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'postgres'),
    'user': os.getenv('DB_USER', f'postgres.{PROJECT_ID}'),
    'password': os.getenv('DB_PASSWORD', ''),
    'sslmode': os.getenv('DB_SSLMODE', 'require'),  # SSL obrigatório para Supabase
    'connect_timeout': 10  # Timeout de 10 segundos
}

def get_connection():
    """Cria e retorna uma conexão com o PostgreSQL do Supabase"""
    try:
        # Verifica se a senha está configurada
        if not DB_CONFIG['password']:
            raise ValueError(
                "Senha do banco de dados não configurada!\n"
                "Configure DB_PASSWORD no arquivo .env com a senha do Supabase.\n"
                "Obtenha a senha em: https://txrkcdweknuxdbwaoekz.supabase.co > Settings > Database"
            )
        
        print(f"🔍 Tentando conectar ao Supabase...")
        print(f"   Host: {DB_CONFIG['host']}")
        print(f"   User: {DB_CONFIG['user']}")
        
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Conexão estabelecida com sucesso!")
        return conn
    except ValueError as e:
        print(f"❌ Erro de configuração: {e}")
        raise
    except psycopg2.OperationalError as e:
        error_msg = str(e)
        if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
            print(f"❌ Erro: Timeout ao conectar ao banco de dados")
            print(f"   Verifique:")
            print(f"   1. Se a senha está correta no arquivo .env")
            print(f"   2. Se o firewall permite conexões na porta 5432")
            print(f"   3. Se o host está correto: {DB_CONFIG['host']}")
        elif "password" in error_msg.lower() or "authentication" in error_msg.lower():
            print(f"❌ Erro: Falha na autenticação")
            print(f"   Verifique se a senha no arquivo .env está correta")
        else:
            print(f"❌ Erro ao conectar ao banco de dados: {e}")
        raise
    except psycopg2.Error as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
        raise
