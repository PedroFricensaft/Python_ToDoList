"""
Script para testar a API REST do Supabase
Execute: python test_api.py
"""
from supabase_client import get_tarefas, criar_tarefa, marcar_concluida, deletar_tarefa

print("=" * 60)
print("TESTE DA API REST DO SUPABASE")
print("=" * 60)
print()

try:
    print("1. Testando listar tarefas...")
    tarefas = get_tarefas()
    print(f"✅ Sucesso! Encontradas {len(tarefas)} tarefas")
    if tarefas:
        print(f"   Primeira tarefa: {tarefas[0]}")
    print()
    
    print("2. Testando criar tarefa...")
    nova_tarefa = criar_tarefa("Tarefa de Teste", "Descrição de teste")
    print(f"✅ Tarefa criada: {nova_tarefa}")
    print()
    
    if nova_tarefa and 'id_tarefas' in nova_tarefa:
        tarefa_id = nova_tarefa['id_tarefas']
        print(f"3. Testando marcar tarefa {tarefa_id} como concluída...")
        tarefa_atualizada = marcar_concluida(tarefa_id)
        print(f"✅ Tarefa atualizada: {tarefa_atualizada}")
        print()
        
        print(f"4. Testando deletar tarefa {tarefa_id}...")
        deletar_tarefa(tarefa_id)
        print("✅ Tarefa deletada")
        print()
    
    print("=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
    
except Exception as e:
    print()
    print("=" * 60)
    print("❌ ERRO NOS TESTES")
    print("=" * 60)
    print(f"Erro: {e}")
    print()
    print("Possíveis causas:")
    print("1. API Key incorreta ou expirada")
    print("2. Tabelas não existem no Supabase")
    print("3. Problema de permissões na API")
    print("4. Problema de rede/firewall")

