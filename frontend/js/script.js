// URL da API backend
const API_URL = 'http://localhost:5000';

const addButton = document.querySelector("#addTaskBtn");
const modalOverlay = document.querySelector("#modalOverlay");
const closeModal = document.querySelector("#closeModal");
const cancelBtn = document.querySelector("#cancelBtn");
const taskForm = document.querySelector("#taskForm");
const taskList = document.querySelector(".task-list");

// Abrir modal ao clicar no botão verde
addButton.addEventListener('click', () => {
    modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
});

// Fechar modal ao clicar no X
closeModal.addEventListener('click', () => {
    modalOverlay.classList.remove('active');
    document.body.style.overflow = 'auto';
    taskForm.reset();
});

// Fechar modal ao clicar em Cancelar
cancelBtn.addEventListener('click', () => {
    modalOverlay.classList.remove('active');
    document.body.style.overflow = 'auto';
    taskForm.reset();
});

// Fechar modal ao clicar fora dele (no overlay)
modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) {
        modalOverlay.classList.remove('active');
        document.body.style.overflow = 'auto';
        taskForm.reset();
    }
});

// Fechar modal com a tecla ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
        modalOverlay.classList.remove('active');
        document.body.style.overflow = 'auto';
        taskForm.reset();
    }
});

// Função para carregar tarefas do backend
async function carregarTarefas() {
    try {
        const response = await fetch(`${API_URL}/tarefas`);
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        const tarefas = await response.json();
        
        // Limpar lista atual
        taskList.innerHTML = '';
        
        // Renderizar cada tarefa
        tarefas.forEach(tarefa => {
            adicionarTarefaNaLista(tarefa);
        });
        
        // Adicionar event listeners após renderizar
        adicionarEventListeners();
    } catch (error) {
        console.error('Erro ao carregar tarefas:', error);
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            taskList.innerHTML = '<li style="color: red; padding: 20px;">⚠️ Erro: Não foi possível conectar ao servidor. Verifique se o backend está rodando em http://localhost:5000</li>';
        }
    }
}

// Função para criar tarefa no backend
async function criarTarefa(titulo, descricao) {
    try {
        const response = await fetch(`${API_URL}/tarefas`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                titulo: titulo,
                descricao: descricao || '',
                id_usuario: 1
            })
        });
        
        if (!response.ok) {
            const data = await response.json().catch(() => ({ erro: 'Erro desconhecido' }));
            throw new Error(data.erro || `Erro HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao criar tarefa:', error);
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            throw new Error('Não foi possível conectar ao servidor. Verifique se o backend está rodando em http://localhost:5000');
        }
        throw error;
    }
}

// Função para marcar tarefa como concluída
async function marcarConcluida(id) {
    try {
        const response = await fetch(`${API_URL}/tarefas/${id}/concluir`, {
            method: 'PUT'
        });
        
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('Erro ao marcar tarefa como concluída');
        }
    } catch (error) {
        console.error('Erro ao marcar como concluída:', error);
        throw error;
    }
}

// Função para deletar tarefa
async function deletarTarefa(id) {
    try {
        const response = await fetch(`${API_URL}/tarefas/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            return true;
        } else {
            throw new Error('Erro ao deletar tarefa');
        }
    } catch (error) {
        console.error('Erro ao deletar tarefa:', error);
        throw error;
    }
}

// Função para adicionar tarefa na lista (DOM)
function adicionarTarefaNaLista(tarefa) {
    const li = document.createElement('li');
    li.className = 'task-item';
    li.dataset.id = tarefa.id;
    
    if (tarefa.completa) {
        li.classList.add('completed');
    }
    
    li.innerHTML = `
        <div class="task-content">
            <input type="checkbox" class="task-checkbox" id="task-${tarefa.id}" ${tarefa.completa ? 'checked' : ''}>
            <label for="task-${tarefa.id}" class="task-checkbox-label"></label>
            <div class="task-title">${tarefa.titulo}</div>
            <button class="delete-btn" data-id="${tarefa.id}" title="Deletar tarefa">×</button>
        </div>
        <div class="task-description">${tarefa.descricao || ''}</div>
    `;
    
    taskList.appendChild(li);
}

// Submeter formulário
taskForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const taskTitle = document.querySelector("#taskTitle").value;
    const taskDescription = document.querySelector("#taskDescription").value;
    
    if (!taskTitle.trim()) {
        alert('Por favor, preencha o título da tarefa');
        return;
    }
    
    try {
        await criarTarefa(taskTitle, taskDescription);
        
        // Fechar modal após adicionar
        modalOverlay.classList.remove('active');
        document.body.style.overflow = 'auto';
        taskForm.reset();
        
        // Recarregar lista de tarefas
        await carregarTarefas();
    } catch (error) {
        alert('Erro ao criar tarefa: ' + error.message);
    }
});

// Função para adicionar event listeners nas tarefas
function adicionarEventListeners() {
    const taskItems = document.querySelectorAll('.task-item');
    const taskCheckboxes = document.querySelectorAll('.task-checkbox');
    const deleteButtons = document.querySelectorAll('.delete-btn');
    
    // Gerenciar checkboxes - marcar/desmarcar como concluída
    taskCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', async (e) => {
            e.stopPropagation();
            const taskItem = checkbox.closest('.task-item');
            const taskId = parseInt(taskItem.dataset.id);
            
            if (checkbox.checked) {
                try {
                    await marcarConcluida(taskId);
                    taskItem.classList.add('completed');
                } catch (error) {
                    checkbox.checked = false;
                    alert('Erro ao marcar tarefa como concluída');
                }
            }
        });
    });
    
    // Botões de deletar
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const taskId = parseInt(btn.dataset.id);
            
            if (confirm('Tem certeza que deseja deletar esta tarefa?')) {
                try {
                    await deletarTarefa(taskId);
                    btn.closest('.task-item').remove();
                } catch (error) {
                    alert('Erro ao deletar tarefa');
                }
            }
        });
    });
    
    // Mostrar/esconder descrição ao clicar na tarefa
    taskItems.forEach(item => {
        item.addEventListener('click', (e) => {
            // Não expandir se clicar no checkbox, label, ou botão de deletar
            if (e.target.classList.contains('task-checkbox') || 
                e.target.classList.contains('task-checkbox-label') ||
                e.target.classList.contains('delete-btn') ||
                e.target.closest('.task-checkbox-label') ||
                e.target.closest('.task-checkbox') ||
                e.target.closest('.delete-btn')) {
                return;
            }
            
            // Não expandir se clicar na descrição
            if (e.target.classList.contains('task-description')) {
                return;
            }
            
            // Fechar outras tarefas expandidas
            taskItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('expanded')) {
                    otherItem.classList.remove('expanded');
                }
            });
            
            // Alternar a tarefa clicada
            item.classList.toggle('expanded');
        });
    });
}

// Carregar tarefas quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    carregarTarefas();
});