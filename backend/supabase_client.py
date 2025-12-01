"""
Cliente para usar a API REST do Supabase
Alternativa à conexão direta ao PostgreSQL
"""
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Obtém o diretório do arquivo atual (backend/)
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / '.env'

# Carrega variáveis de ambiente
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE)
else:
    load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL', 'txrkcdweknuxdbwaoekz.supabase.co')
SUPABASE_API_KEY = os.getenv('SUPABASE_API_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4cmtjZHdla251eGRid2FvZWt6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5OTc1ODIsImV4cCI6MjA3ODU3MzU4Mn0.lXFmJVdA4WsDuOndDnXMIQTHMTfLLK1eJaWz6BluB9c')

# URL completa da API
if not SUPABASE_URL.startswith('http'):
    SUPABASE_URL = f'https://{SUPABASE_URL}'

API_BASE_URL = f'{SUPABASE_URL}/rest/v1'

# Headers para requisições
HEADERS = {
    'apikey': SUPABASE_API_KEY,
    'Authorization': f'Bearer {SUPABASE_API_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
}

def get_tarefas():
    """Lista todas as tarefas"""
    try:
        url = f'{API_BASE_URL}/tarefa'
        print(f"🔍 Fazendo requisição GET para: {url}")
        response = requests.get(
            url,
            headers=HEADERS,
            params={'order': 'id_tarefas.desc'},
            timeout=10
        )
        print(f"📊 Status code: {response.status_code}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro ao buscar tarefas: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            error_msg += f" | Status: {e.response.status_code} | Response: {e.response.text[:200]}"
        print(f"❌ {error_msg}")
        raise Exception(error_msg)

def criar_tarefa(titulo, descricao, id_usuario=1):
    """Cria uma nova tarefa"""
    try:
        # Primeiro, verifica se o usuário existe
        usuario_existe = verificar_usuario(id_usuario)
        if not usuario_existe:
            criar_usuario_padrao()
        
        data = {
            'titulo': titulo,
            'descricao': descricao or '',
            'completa': False,
            'id_usuario': id_usuario
        }
        
        response = requests.post(
            f'{API_BASE_URL}/tarefa',
            headers=HEADERS,
            json=data,
            timeout=10
        )
        response.raise_for_status()
        resultado = response.json()
        # A API retorna uma lista, pega o primeiro item
        if isinstance(resultado, list) and len(resultado) > 0:
            return resultado[0]
        return resultado
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao criar tarefa: {str(e)}")

def marcar_concluida(id_tarefa):
    """Marca uma tarefa como concluída"""
    try:
        data = {'completa': True}
        response = requests.patch(
            f'{API_BASE_URL}/tarefa?id_tarefas=eq.{id_tarefa}',
            headers=HEADERS,
            json=data,
            timeout=10
        )
        response.raise_for_status()
        resultado = response.json()
        if isinstance(resultado, list) and len(resultado) > 0:
            return resultado[0]
        return resultado
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao marcar tarefa como concluída: {str(e)}")

def editar_tarefa(id_tarefa, titulo=None, descricao=None, completa=None):
    """Edita uma tarefa existente"""
    try:
        # Monta o objeto de dados apenas com os campos fornecidos
        data = {}
        if titulo is not None:
            data['titulo'] = titulo
        if descricao is not None:
            data['descricao'] = descricao
        if completa is not None:
            data['completa'] = completa
        
        # Se não houver dados para atualizar, retorna erro
        if not data:
            raise Exception("Nenhum campo fornecido para atualização")
        
        response = requests.patch(
            f'{API_BASE_URL}/tarefa?id_tarefas=eq.{id_tarefa}',
            headers=HEADERS,
            json=data,
            timeout=10
        )
        response.raise_for_status()
        resultado = response.json()
        if isinstance(resultado, list) and len(resultado) > 0:
            return resultado[0]
        return resultado
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao editar tarefa: {str(e)}")

def deletar_tarefa(id_tarefa):
    """Deleta uma tarefa"""
    try:
        response = requests.delete(
            f'{API_BASE_URL}/tarefa?id_tarefas=eq.{id_tarefa}',
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao deletar tarefa: {str(e)}")

def verificar_usuario(id_usuario):
    """Verifica se um usuário existe"""
    try:
        response = requests.get(
            f'{API_BASE_URL}/usuario?id_usuario=eq.{id_usuario}',
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        resultado = response.json()
        return isinstance(resultado, list) and len(resultado) > 0
    except:
        return False

def criar_usuario_padrao():
    """Cria um usuário padrão se não existir"""
    try:
        data = {
            'nome': 'Usuário Padrão',
            'email': 'usuario@padrao.com',
            'senha': 'senha123'
        }
        response = requests.post(
            f'{API_BASE_URL}/usuario',
            headers=HEADERS,
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except:
        pass  # Se falhar, continua mesmo assim

