from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase_client import get_tarefas, criar_tarefa, marcar_concluida, deletar_tarefa, editar_tarefa
import sys

# Cria o app Flask
app = Flask(__name__)

# Permite requisições do frontend (CORS)
CORS(app)

# Rota de teste
@app.route('/', methods=['GET'])
def teste():
    return jsonify({'mensagem': 'Servidor Flask está rodando!', 'status': 'ok'}), 200

# Listar todas as tarefas
@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    try:
        tarefas = get_tarefas()
        # Formata as tarefas para o formato esperado pelo frontend
        tarefas_formatadas = []
        for tarefa in tarefas:
            tarefas_formatadas.append({
                'id': tarefa.get('id_tarefas'),
                'titulo': tarefa.get('titulo', ''),
                'descricao': tarefa.get('descricao') or '',
                'completa': tarefa.get('completa', False),
                'id_usuario': tarefa.get('id_usuario')
            })
        return jsonify(tarefas_formatadas), 200
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Erro em listar_tarefas: {error_msg}")
        return jsonify({'erro': error_msg}), 500

# Criar nova tarefa
@app.route('/tarefas', methods=['POST'])
def criar_tarefa_route():
    try:
        data = request.get_json()
        titulo = data.get('titulo')
        descricao = data.get('descricao', '')
        id_usuario = data.get('id_usuario', 1)
        
        if not titulo:
            return jsonify({'erro': 'Título é obrigatório'}), 400
        
        tarefa = criar_tarefa(titulo, descricao, id_usuario)
        
        # Formata a resposta
        tarefa_formatada = {
            'id': tarefa.get('id_tarefas'),
            'titulo': tarefa.get('titulo', ''),
            'descricao': tarefa.get('descricao') or '',
            'completa': tarefa.get('completa', False),
            'id_usuario': tarefa.get('id_usuario')
        }
        
        return jsonify(tarefa_formatada), 201
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Erro em listar_tarefas: {error_msg}")
        return jsonify({'erro': error_msg}), 500

# Editar tarefa
@app.route('/tarefas/<int:id>', methods=['PUT'])
def editar_tarefa_route(id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'erro': 'Nenhum dado fornecido para atualização'}), 400
        
        # Extrai os campos que podem ser editados
        titulo = data.get('titulo')
        descricao = data.get('descricao')
        completa = data.get('completa')
        
        # Chama a função de edição
        tarefa = editar_tarefa(id, titulo=titulo, descricao=descricao, completa=completa)
        
        if not tarefa:
            return jsonify({'erro': 'Tarefa não encontrada'}), 404
        
        # Formata a resposta
        tarefa_formatada = {
            'id': tarefa.get('id_tarefas'),
            'titulo': tarefa.get('titulo', ''),
            'descricao': tarefa.get('descricao') or '',
            'completa': tarefa.get('completa', False),
            'id_usuario': tarefa.get('id_usuario')
        }
        
        return jsonify(tarefa_formatada), 200
    except Exception as e:
        error_msg = str(e)
        if "not found" in error_msg.lower() or "404" in error_msg:
            return jsonify({'erro': 'Tarefa não encontrada'}), 404
        return jsonify({'erro': error_msg}), 500

# Marcar tarefa como concluída
@app.route('/tarefas/<int:id>/concluir', methods=['PUT'])
def marcar_concluida_route(id):
    try:
        tarefa = marcar_concluida(id)
        
        if not tarefa:
            return jsonify({'erro': 'Tarefa não encontrada'}), 404
        
        # Formata a resposta
        tarefa_formatada = {
            'id': tarefa.get('id_tarefas'),
            'titulo': tarefa.get('titulo', ''),
            'descricao': tarefa.get('descricao') or '',
            'completa': tarefa.get('completa', False),
            'id_usuario': tarefa.get('id_usuario')
        }
        
        return jsonify(tarefa_formatada), 200
    except Exception as e:
        error_msg = str(e)
        if "not found" in error_msg.lower() or "404" in error_msg:
            return jsonify({'erro': 'Tarefa não encontrada'}), 404
        return jsonify({'erro': str(e)}), 500

# Deletar tarefa
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa_route(id):
    try:
        deletar_tarefa(id)
        return jsonify({'mensagem': 'Tarefa deletada com sucesso'}), 200
    except Exception as e:
        error_msg = str(e)
        if "not found" in error_msg.lower() or "404" in error_msg:
            return jsonify({'erro': 'Tarefa não encontrada'}), 404
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 SERVIDOR FLASK INICIANDO")
    print("=" * 60)
    
    # Testa conexão com API REST do Supabase
    try:
        print("🔍 Testando conexão com API REST do Supabase...")
        tarefas = get_tarefas()
        print(f"✅ Conexão com API REST OK (encontradas {len(tarefas)} tarefas)")
    except Exception as e:
        print(f"⚠️  AVISO: Erro ao conectar à API REST: {e}")
        print("⚠️  O servidor iniciará, mas pode não funcionar corretamente")
        print("⚠️  Verifique se a API Key está configurada corretamente")
    
    print("=" * 60)
    print("📍 URL: http://localhost:5000")
    print("📍 Teste: http://localhost:5000/")
    print("📍 API: http://localhost:5000/tarefas")
    print("=" * 60)
    print("📡 Aguardando requisições...")
    print("⚠️  MANTENHA ESTE TERMINAL ABERTO!")
    print("=" * 60)
    print()
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor parado pelo usuário (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERRO ao iniciar servidor: {e}")
        print("\nVerifique:")
        print("  1. Se a porta 5000 está livre")
        print("  2. Se todas as dependências estão instaladas")
        print("  3. Se a senha do banco está configurada no .env")
        sys.exit(1)

