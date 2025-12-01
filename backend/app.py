from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config import get_connection

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
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id_tarefas, titulo, descricao, completa, id_usuario 
            FROM tarefa 
            ORDER BY id_tarefas DESC
        """)
        
        tarefas = []
        for row in cursor.fetchall():
            tarefas.append({
                'id': row[0],
                'titulo': row[1],
                'descricao': row[2] or '',
                'completa': row[3],
                'id_usuario': row[4]
            })
        
        cursor.close()
        conn.close()
        
        return jsonify(tarefas), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# Criar nova tarefa
@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    try:
        data = request.get_json()
        titulo = data.get('titulo')
        descricao = data.get('descricao', '')
        id_usuario = data.get('id_usuario', 1)
        
        if not titulo:
            return jsonify({'erro': 'Título é obrigatório'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verifica se usuário existe, se não cria um padrão
        cursor.execute("SELECT id_usuario FROM usuario WHERE id_usuario = %s", (id_usuario,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO usuario (nome, email, senha) 
                VALUES (%s, %s, %s)
                RETURNING id_usuario
            """, ('Usuário Padrão', 'usuario@padrao.com', 'senha123'))
            id_usuario = cursor.fetchone()[0]
            conn.commit()
        
        # Cria a tarefa
        cursor.execute("""
            INSERT INTO tarefa (titulo, descricao, completa, id_usuario)
            VALUES (%s, %s, %s, %s)
            RETURNING id_tarefas, titulo, descricao, completa, id_usuario
        """, (titulo, descricao, False, id_usuario))
        
        row = cursor.fetchone()
        conn.commit()
        
        tarefa = {
            'id': row[0],
            'titulo': row[1],
            'descricao': row[2] or '',
            'completa': row[3],
            'id_usuario': row[4]
        }
        
        cursor.close()
        conn.close()
        
        return jsonify(tarefa), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# Marcar tarefa como concluída
@app.route('/tarefas/<int:id>/concluir', methods=['PUT'])
def marcar_concluida(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tarefa 
            SET completa = TRUE 
            WHERE id_tarefas = %s
            RETURNING id_tarefas, titulo, descricao, completa, id_usuario
        """, (id,))
        
        row = cursor.fetchone()
        
        if not row:
            cursor.close()
            conn.close()
            return jsonify({'erro': 'Tarefa não encontrada'}), 404
        
        conn.commit()
        
        tarefa = {
            'id': row[0],
            'titulo': row[1],
            'descricao': row[2] or '',
            'completa': row[3],
            'id_usuario': row[4]
        }
        
        cursor.close()
        conn.close()
        
        return jsonify(tarefa), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# Deletar tarefa
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM tarefa WHERE id_tarefas = %s", (id,))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({'erro': 'Tarefa não encontrada'}), 404
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'mensagem': 'Tarefa deletada com sucesso'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    import sys
    
    print("=" * 60)
    print("🚀 SERVIDOR FLASK INICIANDO")
    print("=" * 60)
    
    # Testa conexão com banco antes de iniciar
    try:
        print("🔍 Testando conexão com banco de dados...")
        conn = get_connection()
        conn.close()
        print("✅ Conexão com banco OK")
    except Exception as e:
        print(f"⚠️  AVISO: Erro ao conectar ao banco: {e}")
        print("⚠️  O servidor iniciará, mas pode não funcionar corretamente")
        print("⚠️  Verifique se o PostgreSQL está rodando e as credenciais estão corretas")
    
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
        print("  3. Se o PostgreSQL está rodando")
        sys.exit(1)

