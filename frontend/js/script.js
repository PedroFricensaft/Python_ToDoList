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

// Variável para armazenar todas as tarefas e filtro atual
let todasTarefas = [];
let filtroAtual = 'todas'; // 'todas', 'pendentes', 'concluidas'

// Função para carregar tarefas do backend
async function carregarTarefas(filtro = 'todas') {
    try {
        const response = await fetch(`${API_URL}/tarefas`);
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        todasTarefas = await response.json();
        
        // Aplicar filtro
        aplicarFiltro(filtro);
    } catch (error) {
        console.error('Erro ao carregar tarefas:', error);
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            taskList.innerHTML = '<li style="color: red; padding: 20px;">⚠️ Erro: Não foi possível conectar ao servidor. Verifique se o backend está rodando em http://localhost:5000</li>';
        }
    }
}

// Função para aplicar filtro nas tarefas
function aplicarFiltro(filtro) {
    filtroAtual = filtro;
    
    // Filtrar tarefas baseado no filtro selecionado
    let tarefasFiltradas = [];
    
    switch(filtro) {
        case 'pendentes':
            tarefasFiltradas = todasTarefas.filter(tarefa => !tarefa.completa);
            break;
        case 'concluidas':
            tarefasFiltradas = todasTarefas.filter(tarefa => tarefa.completa);
            break;
        case 'todas':
        default:
            tarefasFiltradas = todasTarefas;
            break;
    }
    
    // Limpar lista atual
    taskList.innerHTML = '';
    
    // Renderizar tarefas filtradas
    if (tarefasFiltradas.length === 0) {
        let mensagem = '';
        switch(filtro) {
            case 'pendentes':
                mensagem = 'Nenhuma tarefa pendente';
                break;
            case 'concluidas':
                mensagem = 'Nenhuma tarefa concluída';
                break;
            default:
                mensagem = 'Nenhuma tarefa cadastrada';
        }
        taskList.innerHTML = `<li style="color: #666; padding: 20px; text-align: center;">${mensagem}</li>`;
    } else {
        tarefasFiltradas.forEach(tarefa => {
            adicionarTarefaNaLista(tarefa);
        });
    }
    
    // Adicionar event listeners após renderizar
    adicionarEventListeners();
    
    // Atualizar estado visual dos botões do menu
    atualizarMenuAtivo(filtro);
}

// Função para atualizar o estado visual do menu
function atualizarMenuAtivo(filtro) {
    // Remove classe active de todos os itens
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Adiciona classe active no item selecionado
    const itemAtivo = document.querySelector(`[data-filtro="${filtro}"]`);
    if (itemAtivo) {
        itemAtivo.classList.add('active');
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
        
        // Recarregar lista de tarefas mantendo o filtro atual
        await carregarTarefas(filtroAtual);
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
                    // Recarregar tarefas mantendo o filtro atual
                    await carregarTarefas(filtroAtual);
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
                    // Recarregar tarefas mantendo o filtro atual
                    await carregarTarefas(filtroAtual);
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

// Event listeners para os botões do menu
document.addEventListener('DOMContentLoaded', () => {
    // Carregar tarefas iniciais
    carregarTarefas('todas');
    
    // Adicionar event listeners nos botões do menu
    const menuTodas = document.getElementById('menuTodas');
    const menuPendentes = document.getElementById('menuPendentes');
    const menuConcluidas = document.getElementById('menuConcluidas');
    
    if (menuTodas) {
        menuTodas.addEventListener('click', (e) => {
            e.preventDefault();
            aplicarFiltro('todas');
        });
    }
    
    if (menuPendentes) {
        menuPendentes.addEventListener('click', (e) => {
            e.preventDefault();
            aplicarFiltro('pendentes');
        });
    }
    
    if (menuConcluidas) {
        menuConcluidas.addEventListener('click', (e) => {
            e.preventDefault();
            aplicarFiltro('concluidas');
        });
    }
});