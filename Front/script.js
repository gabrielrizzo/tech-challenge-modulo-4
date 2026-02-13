// Configuração da API
const API_BASE_URL = 'http://localhost:5001';

// Estado da aplicação
let currentAudioFile = null;
let currentAudioBase64 = null;
let currentAudioFormat = null;

// Elementos DOM
const audioFileInput = document.getElementById('audioFile');
const fileNameSpan = document.getElementById('fileName');
const audioPreview = document.getElementById('audioPreview');
const audioPlayer = document.getElementById('audioPlayer');
const transcribeBtn = document.getElementById('transcribeBtn');
const analyseBtn = document.getElementById('analyseBtn');
const emotionBtn = document.getElementById('emotionBtn');
const completeAnalysisBtn = document.getElementById('completeAnalysisBtn');
const resultSection = document.getElementById('resultSection');
const resultDiv = document.getElementById('result');
const loadingDiv = document.getElementById('loading');
const audioLibrary = document.getElementById('audioLibrary');
const libraryLoading = document.getElementById('libraryLoading');

// Event Listeners
audioFileInput.addEventListener('change', handleFileSelect);
transcribeBtn.addEventListener('click', () => handleAnalysis('transcribe'));
analyseBtn.addEventListener('click', () => handleAnalysis('analyse'));
emotionBtn.addEventListener('click', () => handleAnalysis('emotion'));
completeAnalysisBtn.addEventListener('click', () => handleAnalysis('complete'));

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    loadAudioLibrary();
});

/**
 * Manipula a seleção de arquivo
 */
function handleFileSelect(event) {
    const file = event.target.files[0];
    
    if (!file) {
        resetFileSelection();
        return;
    }

    // Valida o tipo de arquivo
    const validTypes = ['audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/wave', 'audio/x-wav'];
    if (!validTypes.includes(file.type) && !file.name.match(/\.(mp3|wav)$/i)) {
        showAlert('Por favor, selecione um arquivo MP3 ou WAV válido.', 'error');
        resetFileSelection();
        return;
    }

    currentAudioFile = file;
    fileNameSpan.textContent = file.name;
    
    // Determina o formato do áudio
    currentAudioFormat = file.name.toLowerCase().endsWith('.mp3') ? 'mp3' : 'wav';
    
    // Mostra preview do áudio
    const objectURL = URL.createObjectURL(file);
    audioPlayer.src = objectURL;
    audioPreview.style.display = 'block';
    
    // Converte para base64
    convertToBase64(file);
}

/**
 * Converte arquivo para base64
 */
function convertToBase64(file) {
    const reader = new FileReader();
    
    reader.onload = function(event) {
        // Remove o prefixo "data:audio/...;base64,"
        const base64String = event.target.result.split(',')[1];
        currentAudioBase64 = base64String;
        
    // Habilita os botões
    transcribeBtn.disabled = false;
    analyseBtn.disabled = false;
    emotionBtn.disabled = false;
    completeAnalysisBtn.disabled = false;
    };
    
    reader.onerror = function() {
        showAlert('Erro ao converter arquivo para base64.', 'error');
        resetFileSelection();
    };
    
    reader.readAsDataURL(file);
}

/**
 * Reset da seleção de arquivo
 */
function resetFileSelection() {
    currentAudioFile = null;
    currentAudioBase64 = null;
    currentAudioFormat = null;
    fileNameSpan.textContent = 'Escolher arquivo MP3 ou WAV';
    audioPreview.style.display = 'none';
    audioPlayer.src = '';
    transcribeBtn.disabled = true;
    analyseBtn.disabled = true;
    emotionBtn.disabled = true;
    completeAnalysisBtn.disabled = true;
    audioFileInput.value = '';
}

/**
 * Manipula as requisições de análise
 */
async function handleAnalysis(type) {
    if (!currentAudioBase64) {
        showAlert('Por favor, selecione um arquivo de áudio primeiro.', 'warning');
        return;
    }

    const endpoints = {
        'transcribe': '/transcribe-audio',
        'analyse': '/analyse-audio-psycological-issue',
        'emotion': '/predict-emotion',
        'complete': '/analyse-patient-psychological-issue'
    };

    const endpoint = endpoints[type];
    if (!endpoint) return;

    // Mostra loading
    resultSection.style.display = 'block';
    loadingDiv.style.display = 'flex';
    resultDiv.innerHTML = '';
    resultDiv.style.display = 'none';

    // Desabilita botões durante o processamento
    transcribeBtn.disabled = true;
    analyseBtn.disabled = true;
    emotionBtn.disabled = true;
    completeAnalysisBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                audio_data: currentAudioBase64,
                audio_format: currentAudioFormat
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
        }

        const data = await response.json();
        displayResult(data, type);

    } catch (error) {
        console.error('Erro na requisição:', error);
        showAlert(`Erro ao processar áudio: ${error.message}`, 'error');
        resultSection.style.display = 'none';
    } finally {
        loadingDiv.style.display = 'none';
        // Reabilita botões
        transcribeBtn.disabled = false;
        analyseBtn.disabled = false;
        emotionBtn.disabled = false;
        completeAnalysisBtn.disabled = false;
    }
}

/**
 * Exibe o resultado da análise
 */
function displayResult(data, type) {
    resultDiv.style.display = 'block';
    
    let resultHTML = '';

    if (type === 'transcribe') {
        resultHTML = formatTranscriptionResult(data);
    } else if (type === 'analyse') {
        resultHTML = formatAnalysisResult(data);
    } else if (type === 'emotion') {
        resultHTML = formatEmotionResult(data);
    } else if (type === 'complete') {
        resultHTML = formatCompleteAnalysisResult(data);
    }

    resultDiv.innerHTML = resultHTML;
}

/**
 * Formata resultado de transcrição
 */
function formatTranscriptionResult(data) {
    // Tenta extrair a transcrição de diferentes estruturas possíveis
    let transcription = null;
    
    // Estrutura 1: { transcription: "texto" }
    if (data.transcription) {
        transcription = data.transcription;
    }
    // Estrutura 2: { choices: [{ message: { content: "texto" } }] }
    else if (data.choices && data.choices[0] && data.choices[0].message) {
        transcription = data.choices[0].message.content;
    }
    
    if (transcription) {
        let resultHTML = '<div style="padding: 10px;">';
        resultHTML += '<strong style="font-size: 1.3rem; color: var(--primary-color);">📝 Transcrição do Áudio</strong>\n\n';
        
        // Card com a transcrição
        resultHTML += '<div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(99, 102, 241, 0.05)); padding: 20px; border-radius: 12px; border-left: 4px solid var(--primary-color); margin-top: 15px; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.1);">';
        resultHTML += '<div style="font-size: 1.05rem; line-height: 1.8; color: var(--text-color);">';
        
        // Remove \n\n extras e formata
        const formattedText = transcription
            .replace(/\\n\\n/g, '<br><br>')
            .replace(/\\n/g, '<br>')
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n/g, '<br>');
        
        resultHTML += formattedText;
        resultHTML += '</div></div>';
        
        // Estatísticas
        const cleanText = transcription.replace(/\\n/g, ' ').replace(/\n/g, ' ');
        const wordCount = cleanText.split(/\s+/).filter(w => w.length > 0).length;
        const charCount = cleanText.length;
        
        resultHTML += '<div style="margin-top: 20px; display: flex; gap: 15px; flex-wrap: wrap;">';
        resultHTML += '<div style="background: rgba(99, 102, 241, 0.1); padding: 10px 15px; border-radius: 8px; flex: 1; min-width: 150px;">';
        resultHTML += '<div style="font-size: 0.85rem; color: var(--text-secondary);">Palavras</div>';
        resultHTML += `<div style="font-size: 1.5rem; font-weight: bold; color: var(--primary-color);">${wordCount}</div>`;
        resultHTML += '</div>';
        resultHTML += '<div style="background: rgba(99, 102, 241, 0.1); padding: 10px 15px; border-radius: 8px; flex: 1; min-width: 150px;">';
        resultHTML += '<div style="font-size: 0.85rem; color: var(--text-secondary);">Caracteres</div>';
        resultHTML += `<div style="font-size: 1.5rem; font-weight: bold; color: var(--primary-color);">${charCount}</div>`;
        resultHTML += '</div></div>';
        
        resultHTML += '</div>';
        return resultHTML;
    }
    
    // Fallback: mostra JSON formatado
    return '<div style="padding: 10px;"><strong style="font-size: 1.3rem; color: var(--primary-color);">📝 Transcrição do Áudio</strong><pre style="background: rgba(99, 102, 241, 0.1); padding: 20px; border-radius: 12px; margin-top: 15px; overflow-x: auto; color: var(--text-color);">' + JSON.stringify(data, null, 2) + '</pre></div>';
}

/**
 * Formata resultado de análise psicológica
 */
function formatAnalysisResult(data) {
    // Tenta extrair o conteúdo de diferentes estruturas
    let content = null;
    
    // Estrutura 1: { choices: [{ message: { content: "..." } }] }
    if (data.choices && data.choices[0] && data.choices[0].message) {
        content = data.choices[0].message.content;
    }
    // Estrutura 2: Direto o objeto JSON da análise
    else if (typeof data === 'object' && !Array.isArray(data)) {
        content = data;
    }
    
    if (content) {
        let resultHTML = '<div style="padding: 10px;">';
        resultHTML += '<strong style="font-size: 1.3rem; color: var(--secondary-color);">🧠 Análise Psicológica</strong>\n\n';
        
        // Se content é string, tenta fazer parse
        let parsedContent = null;
        if (typeof content === 'string') {
            try {
                parsedContent = JSON.parse(content);
            } catch {
                // Não é JSON, usa como texto
                parsedContent = content;
            }
        } else {
            parsedContent = content;
        }
        
        if (typeof parsedContent === 'object' && parsedContent !== null) {
            // É um JSON estruturado
            resultHTML += '<div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(139, 92, 246, 0.05)); padding: 20px; border-radius: 12px; border-left: 4px solid var(--secondary-color); margin-top: 15px; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.1);">';
            resultHTML += formatPsychologicalAnalysisObject(parsedContent);
            resultHTML += '</div>';
        } else {
            // É texto simples
            resultHTML += '<div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(139, 92, 246, 0.05)); padding: 20px; border-radius: 12px; border-left: 4px solid var(--secondary-color); margin-top: 15px; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.1);">';
            resultHTML += '<div style="font-size: 1.05rem; line-height: 1.8; color: var(--text-color);">';
            
            // Formata parágrafos e listas
            const formattedContent = String(parsedContent)
                .replace(/\n\n/g, '</p><p style="margin: 15px 0;">')
                .replace(/\n/g, '<br>')
                .replace(/\*\*(.*?)\*\*/g, '<strong style="color: var(--secondary-color);">$1</strong>')
                .replace(/^\- (.*?)$/gm, '<li style="margin-left: 20px;">$1</li>');
            
            resultHTML += '<p style="margin: 0;">' + formattedContent + '</p>';
            resultHTML += '</div></div>';
        }
        
        // Badge informativo
        resultHTML += '<div style="margin-top: 20px; padding: 12px 18px; background: rgba(245, 158, 11, 0.1); border-radius: 8px; border: 1px solid var(--warning-color);">';
        resultHTML += '<div style="display: flex; align-items: center; gap: 10px;">';
        resultHTML += '<span style="font-size: 1.2rem;">⚠️</span>';
        resultHTML += '<div style="font-size: 0.9rem; color: var(--warning-color); line-height: 1.5;">';
        resultHTML += '<strong>Importante:</strong> Esta é uma análise NÃO-DIAGNÓSTICA gerada por IA. Não substitui avaliação profissional.';
        resultHTML += '</div></div></div>';
        
        resultHTML += '</div>';
        return resultHTML;
    }
    
    // Fallback: mostra JSON formatado
    return '<div style="padding: 10px;"><strong style="font-size: 1.3rem; color: var(--secondary-color);">🧠 Análise Psicológica</strong><pre style="background: rgba(139, 92, 246, 0.1); padding: 20px; border-radius: 12px; margin-top: 15px; overflow-x: auto; color: var(--text-color);">' + JSON.stringify(data, null, 2) + '</pre></div>';
}

/**
 * Formata resultado de detecção de emoção
 */
function formatEmotionResult(data) {
    if (data.emotion) {
        const emotionIcons = {
            'angry': '😠',
            'sad': '😢',
            'happy': '😊',
            'neutral': '😐',
            'fearful': '😨',
            'disgust': '🤢',
            'surprised': '😲'
        };
        
        const emotionNames = {
            'angry': 'Raiva',
            'sad': 'Tristeza',
            'happy': 'Felicidade',
            'neutral': 'Neutro',
            'fearful': 'Medo',
            'disgust': 'Nojo',
            'surprised': 'Surpresa'
        };
        
        const emotionColors = {
            'angry': '#ef4444',
            'sad': '#3b82f6',
            'happy': '#10b981',
            'neutral': '#6b7280',
            'fearful': '#f59e0b',
            'disgust': '#8b5cf6',
            'surprised': '#ec4899'
        };
        
        const emotion = data.emotion.toLowerCase();
        const icon = emotionIcons[emotion] || '😶';
        const emotionPt = emotionNames[emotion] || data.emotion;
        const color = emotionColors[emotion] || 'var(--accent-color)';
        
        let resultHTML = '<div style="padding: 10px;">';
        resultHTML += '<strong style="font-size: 1.3rem; color: var(--accent-color);">😊 Detecção de Emoção</strong>\n\n';
        
        // Card grande com a emoção
        resultHTML += `<div style="background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(236, 72, 153, 0.05)); padding: 30px; border-radius: 12px; border-left: 4px solid ${color}; margin-top: 15px; box-shadow: 0 4px 15px rgba(236, 72, 153, 0.1); text-align: center;">`;
        
        // Ícone grande
        resultHTML += `<div style="font-size: 4rem; margin-bottom: 15px;">${icon}</div>`;
        
        // Nome da emoção
        resultHTML += `<div style="font-size: 2rem; font-weight: bold; color: ${color}; margin-bottom: 10px;">${emotionPt}</div>`;
        resultHTML += `<div style="font-size: 1rem; color: var(--text-secondary);">${data.emotion}</div>`;
        
        resultHTML += '</div>';
        
        // Informação sobre o modelo
        resultHTML += '<div style="margin-top: 20px; padding: 12px 18px; background: rgba(99, 102, 241, 0.1); border-radius: 8px; border: 1px solid var(--primary-color);">';
        resultHTML += '<div style="display: flex; align-items: center; gap: 10px;">';
        resultHTML += '<span style="font-size: 1.2rem;">ℹ️</span>';
        resultHTML += '<div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.5;">';
        resultHTML += '<strong style="color: var(--primary-color);">Modelo Local:</strong> Detecção realizada com modelo Transformers (não requer API key)';
        resultHTML += '</div></div></div>';
        
        resultHTML += '</div>';
        return resultHTML;
    }
    return JSON.stringify(data, null, 2);
}

/**
 * Formata resultado de análise completa
 */
function formatCompleteAnalysisResult(data) {
    let resultHTML = '<div style="padding: 10px;">';
    
    // Cabeçalho
    resultHTML += '<strong style="font-size: 1.3rem;">🔬 Análise Completa do Áudio</strong>\n\n';
    resultHTML += '<div style="border-left: 4px solid var(--primary-color); padding-left: 15px; margin: 20px 0;">';
    
    // 1. Transcrição
    if (data.transcription) {
        resultHTML += '<div style="margin-bottom: 25px;">';
        resultHTML += '<strong style="color: var(--primary-color); font-size: 1.1rem;">📝 Transcrição:</strong>\n\n';
        resultHTML += `<div style="background: rgba(99, 102, 241, 0.05); padding: 15px; border-radius: 8px; margin-top: 10px;">${data.transcription}</div>`;
        resultHTML += '</div>';
    }
    
    // 2. Emoção
    if (data.emotion) {
        const emotionIcons = {
            'angry': '😠',
            'sad': '😢',
            'happy': '😊',
            'neutral': '😐',
            'fearful': '😨',
            'disgust': '🤢',
            'surprised': '😲'
        };
        
        const emotion = typeof data.emotion === 'string' ? data.emotion : data.emotion.emotion || 'unknown';
        const emotionLower = emotion.toLowerCase();
        const icon = emotionIcons[emotionLower] || '😶';
        
        resultHTML += '<div style="margin-bottom: 25px;">';
        resultHTML += '<strong style="color: var(--accent-color); font-size: 1.1rem;">😊 Emoção Detectada:</strong>\n\n';
        resultHTML += `<div style="background: rgba(236, 72, 153, 0.05); padding: 15px; border-radius: 8px; margin-top: 10px; font-size: 1.2rem;">${icon} <strong>${emotion}</strong></div>`;
        resultHTML += '</div>';
    }
    
    // 3. Análise Psicológica
    if (data.resume) {
        resultHTML += '<div style="margin-bottom: 15px;">';
        resultHTML += '<strong style="color: var(--secondary-color); font-size: 1.1rem;">🧠 Análise Psicológica:</strong>\n\n';
        resultHTML += '<div style="background: rgba(139, 92, 246, 0.05); padding: 15px; border-radius: 8px; margin-top: 10px;">';
        
        // Se resume for um objeto, tenta formatá-lo melhor
        if (typeof data.resume === 'object') {
            // Tenta extrair conteúdo de choices se existir
            if (data.resume.choices && data.resume.choices[0] && data.resume.choices[0].message) {
                const content = data.resume.choices[0].message.content;
                // Tenta fazer parse de JSON se o conteúdo for JSON
                try {
                    const parsedContent = JSON.parse(content);
                    resultHTML += formatPsychologicalAnalysisObject(parsedContent);
                } catch {
                    resultHTML += content;
                }
            } else {
                resultHTML += formatPsychologicalAnalysisObject(data.resume);
            }
        } else {
            resultHTML += data.resume;
        }
        
        resultHTML += '</div></div>';
    }
    
    resultHTML += '</div></div>';
    
    return resultHTML;
}

/**
 * Formata objeto de análise psicológica
 */
function formatPsychologicalAnalysisObject(obj) {
    let html = '';
    
    for (const [key, value] of Object.entries(obj)) {
        // Formata a chave (converte snake_case para Title Case)
        const formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        
        html += `<div style="margin-bottom: 15px;">`;
        html += `<strong style="color: var(--text-color);">${formattedKey}:</strong>\n`;
        
        if (typeof value === 'object' && value !== null) {
            if (Array.isArray(value)) {
                html += '<ul style="margin: 5px 0; padding-left: 20px;">';
                value.forEach(item => {
                    // Se o item for um objeto, formata recursivamente
                    if (typeof item === 'object' && item !== null) {
                        html += '<li style="margin-bottom: 10px;">';
                        html += '<div style="background: rgba(99, 102, 241, 0.05); padding: 10px; border-radius: 6px; margin-top: 5px;">';
                        html += formatPsychologicalAnalysisObject(item);
                        html += '</div>';
                        html += '</li>';
                    } else {
                        // Item é string ou número
                        html += `<li>${item}</li>`;
                    }
                });
                html += '</ul>';
            } else {
                // É um objeto, formata recursivamente com indentação
                html += '<div style="margin-left: 15px; padding-left: 10px; border-left: 2px solid rgba(139, 92, 246, 0.3);">';
                html += formatPsychologicalAnalysisObject(value);
                html += '</div>';
            }
        } else {
            html += `<span style="color: var(--text-secondary);">${value}</span>\n`;
        }
        
        html += '</div>';
    }
    
    return html;
}

/**
 * Carrega a biblioteca de áudios
 */
async function loadAudioLibrary() {
    // Lista estática de áudios conhecidos na pasta audios/
    const knownAudios = [
        { name: 'en-neutral.mp3', format: 'mp3' },
        { name: 'pt-br-angry.mp3', format: 'mp3' },
        { name: 'pt-br-angry-2.mp3', format: 'mp3' },
        { name: 'pt-br-fearful.mp3', format: 'mp3' },
        { name: 'pt-br-sad.mp3', format: 'mp3' }
    ];

    try {
        // Tenta buscar da API primeiro
        const response = await fetch(`${API_BASE_URL}/list-audios`);
        
        if (response.ok) {
            const data = await response.json();
            displayAudioLibrary(data.audios || knownAudios);
            return;
        }
    } catch (error) {
        console.log('API não disponível, usando lista estática de áudios');
    }
    
    // Se a API não estiver disponível, usa a lista estática
    displayAudioLibrary(knownAudios);
}

/**
 * Exibe a biblioteca de áudios
 */
function displayAudioLibrary(audios) {
    libraryLoading.style.display = 'none';
    
    if (audios.length === 0) {
        audioLibrary.innerHTML = '<p style="color: var(--text-secondary);">Nenhum áudio encontrado na pasta "audios".</p>';
        return;
    }

    audioLibrary.innerHTML = '';

    audios.forEach(audio => {
        const audioItem = createAudioItem(audio);
        audioLibrary.appendChild(audioItem);
    });
}

/**
 * Cria um item de áudio para a biblioteca
 */
function createAudioItem(audio) {
    const div = document.createElement('div');
    div.className = 'audio-item';

    const audioIcon = getAudioIcon(audio.name);

    div.innerHTML = `
        <div class="audio-item-header">
            <span class="audio-icon">${audioIcon}</span>
            <h3>${audio.name}</h3>
        </div>
        <audio controls preload="metadata" id="audio-${audio.name.replace(/[^a-zA-Z0-9]/g, '-')}">
            <source src="${API_BASE_URL}/audio/${encodeURIComponent(audio.name)}" type="audio/${audio.format}">
            Seu navegador não suporta o elemento de áudio.
        </audio>
        <div class="audio-actions">
            <button class="btn btn-primary btn-small" onclick="selectLibraryAudio('${audio.name}', '${audio.format}')">
                ✅ Selecionar Áudio
            </button>
        </div>
    `;

    // Adiciona listener para erro de carregamento
    const audioElement = div.querySelector('audio');
    const sourceElement = audioElement.querySelector('source');
    
    sourceElement.addEventListener('error', function() {
        // Tenta caminho alternativo
        const altPaths = [
            `../audios/${audio.name}`,
            `../../audios/${audio.name}`,
            `/audios/${audio.name}`
        ];
        
        let currentAttempt = 0;
        
        function tryNextPath() {
            if (currentAttempt < altPaths.length) {
                sourceElement.src = altPaths[currentAttempt];
                audioElement.load();
                currentAttempt++;
            } else {
                // Se todos os caminhos falharem, mostra mensagem
                const errorMsg = document.createElement('p');
                errorMsg.style.color = 'var(--warning-color)';
                errorMsg.style.fontSize = '0.85rem';
                errorMsg.style.marginTop = '10px';
                errorMsg.textContent = '⚠️ Inicie a API para reproduzir o áudio';
                audioElement.parentNode.insertBefore(errorMsg, audioElement.nextSibling);
            }
        }
        
        sourceElement.addEventListener('error', tryNextPath, { once: true });
        tryNextPath();
    });

    return div;
}

/**
 * Retorna ícone baseado no nome do arquivo
 */
function getAudioIcon(filename) {
    const name = filename.toLowerCase();
    if (name.includes('angry')) return '😠';
    if (name.includes('sad')) return '😢';
    if (name.includes('happy')) return '😊';
    if (name.includes('fearful')) return '😨';
    if (name.includes('neutral')) return '😐';
    return '🎵';
}

/**
 * Seleciona áudio da biblioteca e carrega na seção principal
 */
async function selectLibraryAudio(filename, format) {
    try {
        // Busca o áudio da API
        const response = await fetch(`${API_BASE_URL}/audio/${encodeURIComponent(filename)}`);
        
        if (!response.ok) {
            throw new Error(`Erro ao carregar áudio: ${response.status}`);
        }

        const blob = await response.blob();
        
        // Cria um File object a partir do blob
        const file = new File([blob], filename, { type: `audio/${format}` });
        
        // Define como arquivo atual
        currentAudioFile = file;
        currentAudioFormat = format;
        
        // Atualiza o nome do arquivo
        fileNameSpan.textContent = filename;
        
        // Mostra preview do áudio na seção principal
        const objectURL = URL.createObjectURL(blob);
        audioPlayer.src = objectURL;
        audioPreview.style.display = 'block';
        
        // Converte para base64
        const reader = new FileReader();
        
        reader.onload = function(event) {
            const base64String = event.target.result.split(',')[1];
            currentAudioBase64 = base64String;
            
            // Habilita os botões
            transcribeBtn.disabled = false;
            analyseBtn.disabled = false;
            emotionBtn.disabled = false;
            completeAnalysisBtn.disabled = false;
        };
        
        reader.readAsDataURL(blob);
        
        // Scroll suave para a seção de upload
        const uploadSection = document.querySelector('.upload-section');
        if (uploadSection) {
            uploadSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        
        // Mostra mensagem de sucesso
        showAlert(`✅ Áudio "${filename}" selecionado! Escolha uma ação acima.`, 'success');

    } catch (error) {
        console.error('Erro ao selecionar áudio da biblioteca:', error);
        showAlert(`Erro ao selecionar áudio: ${error.message}. Certifique-se de que a API está rodando.`, 'error');
    }
}

/**
 * Analisa áudio da biblioteca
 */
async function analyzeLibraryAudio(filename, type) {
    try {
        // Tenta buscar o áudio da API
        let audioUrl = `${API_BASE_URL}/audio/${encodeURIComponent(filename)}`;
        
        // Se a API não estiver disponível, tenta buscar diretamente da pasta audios
        let response = await fetch(audioUrl).catch(() => {
            // Fallback: tenta buscar do caminho relativo
            return fetch(`../audios/${encodeURIComponent(filename)}`);
        });
        
        if (!response.ok) {
            throw new Error(`Erro ao carregar áudio: ${response.status}. Certifique-se de que a API está rodando.`);
        }

        const blob = await response.blob();
        const reader = new FileReader();

        reader.onload = async function(event) {
            const base64String = event.target.result.split(',')[1];
            const format = filename.toLowerCase().endsWith('.mp3') ? 'mp3' : 'wav';

            // Define como áudio atual
            currentAudioBase64 = base64String;
            currentAudioFormat = format;

            // Scroll para a seção de resultados
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

            // Executa a análise
            await handleAnalysis(type);
        };

        reader.readAsDataURL(blob);

    } catch (error) {
        console.error('Erro ao analisar áudio da biblioteca:', error);
        showAlert(`Erro ao processar áudio: ${error.message}. A API precisa estar rodando para análises.`, 'error');
    }
}

/**
 * Exibe mensagem de alerta
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const container = document.querySelector('.container main');
    container.insertBefore(alertDiv, container.firstChild);

    // Remove o alerta após 5 segundos
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        alertDiv.style.transition = 'opacity 0.5s ease';
        setTimeout(() => alertDiv.remove(), 500);
    }, 5000);
}

// Torna as funções globais para serem chamadas pelos botões inline
window.analyzeLibraryAudio = analyzeLibraryAudio;
window.selectLibraryAudio = selectLibraryAudio;