// URL da API backend
const API_URL = 'http://localhost:5000';

// Verificar se está na página de login ou cadastro
const isLoginPage = window.location.pathname.includes('login.html');
const isCadastroPage = window.location.pathname.includes('cadastro.html');

// Função para mostrar erro
function mostrarErro(mensagem) {
    const erroDiv = document.getElementById('erroMensagem');
    if (erroDiv) {
        erroDiv.textContent = mensagem;
        erroDiv.style.display = 'block';
    } else {
        alert(mensagem);
    }
}

// Função para esconder erro
function esconderErro() {
    const erroDiv = document.getElementById('erroMensagem');
    if (erroDiv) {
        erroDiv.style.display = 'none';
    }
}

// Função para fazer login
async function fazerLogin(email, senha) {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', // Importante para cookies/sessão
            body: JSON.stringify({
                email: email,
                senha: senha
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.erro || 'Erro ao fazer login');
        }
        
        // Redireciona para a página principal
        window.location.href = 'index.html';
    } catch (error) {
        mostrarErro(error.message);
        throw error;
    }
}

// Função para fazer cadastro
async function fazerCadastro(nome, email, senha, idade) {
    try {
        const response = await fetch(`${API_URL}/auth/cadastro`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', // Importante para cookies/sessão
            body: JSON.stringify({
                nome: nome,
                email: email,
                senha: senha,
                idade: idade || null
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.erro || 'Erro ao cadastrar');
        }
        
        // Redireciona para a página principal
        window.location.href = 'index.html';
    } catch (error) {
        mostrarErro(error.message);
        throw error;
    }
}

// Event listener para formulário de login
if (isLoginPage) {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            esconderErro();
            
            const email = document.getElementById('email').value;
            const senha = document.getElementById('senha').value;
            
            if (!email || !senha) {
                mostrarErro('Por favor, preencha todos os campos');
                return;
            }
            
            try {
                await fazerLogin(email, senha);
            } catch (error) {
                // Erro já foi mostrado na função
            }
        });
    }
}

// Event listener para formulário de cadastro
if (isCadastroPage) {
    const cadastroForm = document.getElementById('cadastroForm');
    if (cadastroForm) {
        cadastroForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            esconderErro();
            
            const nome = document.getElementById('nome').value;
            const email = document.getElementById('email').value;
            const senha = document.getElementById('senha').value;
            const idade = document.getElementById('idade').value;
            
            if (!nome || !email || !senha) {
                mostrarErro('Por favor, preencha todos os campos obrigatórios');
                return;
            }
            
            try {
                await fazerCadastro(nome, email, senha, idade ? parseInt(idade) : null);
            } catch (error) {
                // Erro já foi mostrado na função
            }
        });
    }
}

