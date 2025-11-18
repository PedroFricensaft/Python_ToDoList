const addButton = document.querySelector("#addTaskBtn");
const modalOverlay = document.querySelector("#modalOverlay");
const closeModal = document.querySelector("#closeModal");
const cancelBtn = document.querySelector("#cancelBtn");
const taskForm = document.querySelector("#taskForm");

// Abrir modal ao clicar no botão verde
addButton.addEventListener('click', () => {
    modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Previne scroll do body quando modal está aberto
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

// Submeter formulário
taskForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const taskTitle = document.querySelector("#taskTitle").value;
    const taskDescription = document.querySelector("#taskDescription").value;
    const taskDate = document.querySelector("#taskDate").value;
    const taskTime = document.querySelector("#taskTime").value;
    const taskPriority = document.querySelector('input[name="priority"]:checked').value;
    
    // Aqui você pode adicionar a lógica para salvar a tarefa
    console.log('Nova tarefa:', { taskTitle, taskDescription, taskDate, taskTime, taskPriority });
    
    // Fechar modal após adicionar
    modalOverlay.classList.remove('active');
    document.body.style.overflow = 'auto';
    taskForm.reset();
    
    // Aqui você pode adicionar a tarefa à lista
    // Por exemplo: adicionarTarefa(taskTitle, taskDate, taskTime);
});

// Mostrar/esconder descrição ao clicar na tarefa e gerenciar status
document.addEventListener('DOMContentLoaded', () => {
    const taskItems = document.querySelectorAll('.task-item');
    const taskCheckboxes = document.querySelectorAll('.task-checkbox');
    
    // Gerenciar checkboxes - marcar/desmarcar como concluída
    taskCheckboxes.forEach(checkbox => {
        // Sincronizar estado inicial
        const taskItem = checkbox.closest('.task-item');
        if (checkbox.checked) {
            taskItem.classList.add('completed');
        }
        
        checkbox.addEventListener('change', (e) => {
            e.stopPropagation(); // Prevenir que expanda a descrição
            const taskItem = checkbox.closest('.task-item');
            
            if (checkbox.checked) {
                taskItem.classList.add('completed');
            } else {
                taskItem.classList.remove('completed');
            }
        });
    });
    
    // Mostrar/esconder descrição ao clicar na tarefa
    taskItems.forEach(item => {
        item.addEventListener('click', (e) => {
            // Não expandir se clicar no checkbox ou no label do checkbox
            if (e.target.classList.contains('task-checkbox') || 
                e.target.classList.contains('task-checkbox-label') ||
                e.target.closest('.task-checkbox-label') ||
                e.target.closest('.task-checkbox')) {
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
});