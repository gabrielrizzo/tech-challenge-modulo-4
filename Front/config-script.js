// Configuração da API
const API_BASE_URL = 'http://localhost:5001';

// Elementos DOM
const statusCard = document.getElementById('statusCard');
const configForm = document.getElementById('configForm');
const openaiKeyInput = document.getElementById('openaiKey');
const openrouterKeyInput = document.getElementById('openrouterKey');
const saveBtn = document.getElementById('saveBtn');
const testResults = document.getElementById('testResults');

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    checkEnvStatus();
    
    configForm.addEventListener('submit', handleSaveConfig);
});

/**
 * Verifica o status do arquivo .env
 */
async function checkEnvStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/config/check`);
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        const data = await response.json();
        displayEnvStatus(data);
        
        // Se existir, carrega as configurações atuais
        if (data.exists) {
            await loadCurrentConfig();
        }

    } catch (error) {
        console.error('Erro ao verificar .env:', error);
        statusCard.innerHTML = `
            <div class="alert alert-error">
                ❌ Erro ao verificar configurações: ${error.message}
                <br><small>Verifique se a API está rodando em ${API_BASE_URL}</small>
            </div>
        `;
    }
}

/**
 * Exibe o status do arquivo .env
 */
function displayEnvStatus(data) {
    let statusClass = 'status-card';
    let statusHTML = '';

    if (data.exists) {
        statusClass += ' status-exists';
        statusHTML = `
            <div class="alert alert-success">
                ✅ Arquivo .env encontrado!
            </div>
            <div style="margin-top: 15px;">
                <p><strong>Chaves configuradas:</strong></p>
                <ul style="list-style: none; padding: 10px 0;">
                    <li style="padding: 5px 0;">
                        ${data.has_openai_key ? '✅' : '❌'} OpenAI API Key
                        ${data.has_openai_key ? '<span style="color: var(--success-color);">(Configurada)</span>' : '<span style="color: var(--warning-color);">(Não configurada)</span>'}
                    </li>
                    <li style="padding: 5px 0;">
                        ${data.has_openrouter_key ? '✅' : '❌'} OpenRouter API Key
                        ${data.has_openrouter_key ? '<span style="color: var(--success-color);">(Configurada)</span>' : '<span style="color: var(--danger-color);">(Não configurada - OBRIGATÓRIA!)</span>'}
                    </li>
                </ul>
                <p style="margin-top: 15px; color: var(--text-secondary);">
                    💡 Você pode atualizar as chaves abaixo. Deixe em branco para manter a chave atual.
                </p>
            </div>
        `;
    } else {
        statusClass += ' status-warning';
        statusHTML = `
            <div class="alert alert-warning">
                ⚠️ Arquivo .env não encontrado!
            </div>
            <p style="margin-top: 15px; color: var(--text-secondary);">
                Um novo arquivo .env será criado quando você salvar as configurações abaixo.
            </p>
        `;
    }

    statusCard.className = `card ${statusClass}`;
    statusCard.innerHTML = statusHTML;
}

/**
 * Carrega as configurações atuais
 */
async function loadCurrentConfig() {
    try {
        const response = await fetch(`${API_BASE_URL}/config/get`);
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        const data = await response.json();
        
        // Preenche os campos com as chaves existentes (parcialmente ocultas)
        if (data.openai_key) {
            openaiKeyInput.placeholder = maskKey(data.openai_key);
        }
        
        if (data.openrouter_key) {
            openrouterKeyInput.placeholder = maskKey(data.openrouter_key);
        }

    } catch (error) {
        console.error('Erro ao carregar configurações:', error);
    }
}

/**
 * Mascara a chave para exibição
 */
function maskKey(key) {
    if (!key || key.length < 10) return '••••••••••••';
    const start = key.substring(0, 8);
    const end = key.substring(key.length - 4);
    return `${start}••••${end}`;
}

/**
 * Manipula o salvamento das configurações
 */
async function handleSaveConfig(event) {
    event.preventDefault();
    
    const openaiKey = openaiKeyInput.value.trim();
    const openrouterKey = openrouterKeyInput.value.trim();

    // Validação
    if (!openaiKey && !openrouterKey) {
        showAlert('Por favor, preencha pelo menos uma chave!', 'warning');
        return;
    }

    // Validação do formato OpenRouter
    if (openrouterKey && !openrouterKey.startsWith('sk-or-v1-')) {
        showAlert('A chave do OpenRouter deve começar com "sk-or-v1-"', 'error');
        return;
    }

    // Validação do formato OpenAI
    if (openaiKey && !openaiKey.startsWith('sk-')) {
        showAlert('A chave da OpenAI deve começar com "sk-"', 'error');
        return;
    }

    // Desabilita o botão durante o salvamento
    saveBtn.disabled = true;
    saveBtn.textContent = '⏳ Salvando...';

    try {
        const response = await fetch(`${API_BASE_URL}/config/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                openai_key: openaiKey || null,
                openrouter_key: openrouterKey || null
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
        }

        const data = await response.json();
        
        showAlert(`✅ ${data.message}`, 'success');
        
        // Mostra alerta de reinicialização
        setTimeout(() => {
            showAlert('⚠️ IMPORTANTE: Reinicie o servidor Flask para aplicar as mudanças!', 'warning');
        }, 1500);
        
        // Limpa os campos
        clearForm();
        
        // Recarrega o status
        setTimeout(() => {
            checkEnvStatus();
        }, 2000);

    } catch (error) {
        console.error('Erro ao salvar configurações:', error);
        showAlert(`❌ Erro ao salvar: ${error.message}`, 'error');
    } finally {
        saveBtn.disabled = false;
        saveBtn.textContent = '💾 Salvar Configurações';
    }
}

/**
 * Alterna visibilidade do campo de senha
 */
function toggleVisibility(inputId) {
    const input = document.getElementById(inputId);
    if (input.type === 'password') {
        input.type = 'text';
    } else {
        input.type = 'password';
    }
}

/**
 * Limpa o formulário
 */
function clearForm() {
    openaiKeyInput.value = '';
    openrouterKeyInput.value = '';
}

/**
 * Testa a chave do OpenRouter
 */
async function testOpenRouterKey() {
    testResults.classList.add('visible');
    testResults.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Testando chave do OpenRouter...</p>
        </div>
    `;

    try {
        const response = await fetch(`${API_BASE_URL}/config/test-openrouter`);
        const data = await response.json();

        if (data.success) {
            testResults.innerHTML = `
                <div class="test-result-item test-result-success">
                    <strong>✅ OpenRouter está funcionando!</strong>
                    <p style="margin-top: 10px;">Chave válida e conectada.</p>
                </div>
            `;
        } else {
            testResults.innerHTML = `
                <div class="test-result-item test-result-error">
                    <strong>❌ Erro ao testar OpenRouter</strong>
                    <p style="margin-top: 10px;">${data.error || 'Chave inválida ou não configurada'}</p>
                </div>
            `;
        }
    } catch (error) {
        testResults.innerHTML = `
            <div class="test-result-item test-result-error">
                <strong>❌ Erro ao conectar com a API</strong>
                <p style="margin-top: 10px;">${error.message}</p>
            </div>
        `;
    }
}

/**
 * Testa o health check da API
 */
async function testHealthCheck() {
    testResults.classList.add('visible');
    testResults.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Verificando saúde da API...</p>
        </div>
    `;

    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        let resultHTML = `
            <div class="test-result-item ${data.status === 'healthy' ? 'test-result-success' : 'test-result-warning'}">
                <strong>${data.status === 'healthy' ? '✅' : '⚠️'} Status: ${data.status.toUpperCase()}</strong>
                <div style="margin-top: 15px;">
                    <p><strong>Dependências:</strong></p>
                    <ul style="list-style: none; padding: 10px 0;">
                        <li>OpenAI: ${data.dependencias.openai_configured ? '✅' : '❌'}</li>
                        <li>OpenRouter: ${data.dependencias.openrouter_configured ? '✅' : '❌'}</li>
                        <li>Flask: ${data.dependencias.flask_operacional ? '✅' : '❌'}</li>
                        <li>LangChain: ${data.dependencias.langchain_operacional ? '✅' : '❌'}</li>
                    </ul>
                </div>
            </div>
        `;

        if (data.warnings && data.warnings.length > 0) {
            resultHTML += `
                <div class="test-result-item test-result-warning" style="margin-top: 10px;">
                    <strong>⚠️ Avisos:</strong>
                    <ul style="margin-top: 10px; padding-left: 20px;">
                        ${data.warnings.map(w => `<li>${w}</li>`).join('')}
                    </ul>
                </div>
            `;
        }

        testResults.innerHTML = resultHTML;

    } catch (error) {
        testResults.innerHTML = `
            <div class="test-result-item test-result-error">
                <strong>❌ Erro ao conectar com a API</strong>
                <p style="margin-top: 10px;">${error.message}</p>
            </div>
        `;
    }
}

/**
 * Exibe mensagem de alerta
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const container = document.querySelector('main');
    container.insertBefore(alertDiv, container.firstChild);

    // Remove o alerta após 5 segundos
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        alertDiv.style.transition = 'opacity 0.5s ease';
        setTimeout(() => alertDiv.remove(), 500);
    }, 5000);
}

// Torna funções globais para serem chamadas pelos botões inline
window.toggleVisibility = toggleVisibility;
window.loadCurrentConfig = loadCurrentConfig;
window.clearForm = clearForm;
window.testOpenRouterKey = testOpenRouterKey;
window.testHealthCheck = testHealthCheck;
