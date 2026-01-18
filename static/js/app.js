/**
 * Launcher V2 - JavaScript Frontend
 * Local com interface interativa
 */

const appsContainer = document.getElementById('apps-container');
const modalAdicionar = document.getElementById('modal-adicionar');
let debounceTimer = {};

/**
 * Abre o modal de adicionar app
 */
function abrirModalAdicionar() {
    modalAdicionar.style.display = 'block';
    document.getElementById('app-id').focus();
}

/**
 * Fecha o modal de adicionar app
 */
function fecharModalAdicionar() {
    modalAdicionar.style.display = 'none';
    document.getElementById('form-adicionar').reset();
}

/**
 * Envia o formulário de adicionar app
 */
async function enviarFormulario(event) {
    event.preventDefault();
    
    const dados = {
        id: document.getElementById('app-id').value.trim().toLowerCase(),
        nome: document.getElementById('app-nome').value.trim(),
        caminho: document.getElementById('app-caminho').value.trim(),
        processo: document.getElementById('app-processo').value.trim()
    };
    
    if (!dados.id || !dados.nome) {
        mostrarErro('ID e Nome sao obrigatorios!');
        return;
    }
    
    try {
        const response = await fetch('/api/apps', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });
        
        const data = await response.json();
        
        if (data.success) {
            mostrarSucesso(`✅ App '${dados.nome}' adicionado com sucesso!`);
            fecharModalAdicionar();
            setTimeout(carregarApps, 500);
        } else {
            mostrarErro(`❌ ${data.message}`);
        }
    } catch (error) {
        mostrarErro('Erro ao adicionar app: ' + error.message);
    }
}

/**
 * Carrega lista de apps
 */
async function carregarApps() {
    try {
        const response = await fetch('/api/apps');
        const data = await response.json();
        
        if (data.success) {
            renderizarApps(data.apps);
        } else {
            mostrarErro('Erro ao carregar apps');
        }
    } catch (error) {
        mostrarErro('Erro de conexão: ' + error.message);
    }
}

/**
 * Renderiza os cards dos apps
 */
function renderizarApps(apps) {
    appsContainer.innerHTML = '';
    
    if (apps.length === 0) {
        appsContainer.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1;">
                <div class="empty-state-icon">📭</div>
                <div class="empty-state-text">Nenhum app cadastrado. Clique em "Adicionar App" para começar!</div>
            </div>
        `;
        return;
    }
    
    apps.forEach(app => {
        const card = criarCard(app);
        appsContainer.appendChild(card);
    });
}

/**
 * Cria um card para um app
 */
function criarCard(app) {
    const card = document.createElement('div');
    card.className = 'app-card';
    card.innerHTML = `
        <button class="btn-delete" onclick="deletarApp('${escapeHtml(app.id)}', '${escapeHtml(app.nome)}')">✕</button>
        <div class="app-icon">🚀</div>
        <div class="app-name">${escapeHtml(app.nome)}</div>
        <div class="app-id">${escapeHtml(app.id)}</div>
        <div class="app-buttons">
            <button class="btn-open" onclick="abrirApp('${escapeHtml(app.id)}')">
                ▶️ Abrir
            </button>
            <button class="btn-close" onclick="fecharApp('${escapeHtml(app.id)}')">
                ⏹️ Fechar
            </button>
        </div>
    `;
    return card;
}

/**
 * Escapa caracteres especiais HTML
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

/**
 * Abre um app com debounce
 */
async function abrirApp(appId) {
    if (debounceTimer[appId]) return;
    
    debounceTimer[appId] = true;
    setTimeout(() => delete debounceTimer[appId], 2000);
    
    try {
        const response = await fetch(`/api/open/${appId}`, {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            mostrarSucesso(`✅ ${appId} aberto`);
        } else {
            mostrarErro(`❌ ${data.message || 'Erro ao abrir app'}`);
        }
    } catch (error) {
        mostrarErro('Erro: ' + error.message);
    }
}

/**
 * Fecha um app com debounce
 */
async function fecharApp(appId) {
    if (debounceTimer[appId]) return;
    
    debounceTimer[appId] = true;
    setTimeout(() => delete debounceTimer[appId], 2000);
    
    try {
        const response = await fetch(`/api/close/${appId}`, {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            mostrarSucesso(`✅ ${appId} fechado`);
        } else {
            mostrarErro(`❌ ${data.message || 'Erro ao fechar app'}`);
        }
    } catch (error) {
        mostrarErro('Erro: ' + error.message);
    }
}

/**
 * Deleta um app
 */
async function deletarApp(appId, appNome) {
    if (!confirm(`Tem certeza que deseja remover "${appNome}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/apps/${appId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            mostrarSucesso(`✅ ${appNome} removido`);
            setTimeout(carregarApps, 500);
        } else {
            mostrarErro(`❌ ${data.message}`);
        }
    } catch (error) {
        mostrarErro('Erro ao deletar app: ' + error.message);
    }
}

/**
 * Mostra mensagem de erro
 */
function mostrarErro(mensagem) {
    mostrarMensagem(mensagem, 'error');
}

/**
 * Mostra mensagem de sucesso
 */
function mostrarSucesso(mensagem) {
    mostrarMensagem(mensagem, 'success');
}

/**
 * Mostra mensagem genérica
 */
function mostrarMensagem(mensagem, tipo) {
    const div = document.createElement('div');
    div.className = `message ${tipo}`;
    div.innerHTML = mensagem;
    
    const container = document.querySelector('.container');
    container.insertBefore(div, container.querySelector('.btn-add-app').nextSibling);
    
    setTimeout(() => {
        div.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => div.remove(), 300);
    }, 4000);
}

/**
 * Fecha o modal quando clica fora dele
 */
window.onclick = function(event) {
    if (event.target == modalAdicionar) {
        fecharModalAdicionar();
    }
}

// Carrega apps ao iniciar
document.addEventListener('DOMContentLoaded', () => {
    carregarApps();
});

// Auto-refresh a cada 30 segundos
setInterval(carregarApps, 30000);
