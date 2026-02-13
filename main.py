from flask import request, Flask, jsonify, send_from_directory, send_file
from flask_cors import CORS
from dotenv import load_dotenv, set_key, find_dotenv
from agents import analyse_psicological_issue
import os
from datetime import datetime
import importlib
audio_analyser = importlib.import_module("agents.audio-analyser")
transcribe_audio_file = audio_analyser.transcribe_audio
analyse_audio_psicological_issue = audio_analyser.analyse_audio_psicological_issue
emotion_analyser = importlib.import_module("agents.emotion-analyser")
predict_emotion_from_base64 = emotion_analyser.predict_emotion_from_base64
load_dotenv()
app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir requisições do frontend

@app.route('/', methods=['GET'])
def home():
    """Rota raiz que retorna informações sobre a API"""
    return jsonify({
        "nome": "Tech Challenge Módulo 4 - API de Análise Psicológica",
        "versao": "0.1.0",
        "descricao": "API Flask com funcionalidades de análise de texto e áudio usando IA",
        "endpoints": {
            "textuais": {
                "POST /resume": "Resume textos usando IA",
                "POST /analyse-psycological-issue": "Análise psicológica NÃO-DIAGNÓSTICA de textos femininos"
            },
            "audio": {
                "POST /transcribe-audio": "Transcreve áudio para texto",
                "POST /analyse-audio-psycological-issue": "Análise psicológica de áudio"
            },
            "sistema": {
                "GET /health": "Verifica saúde da API e dependências"
            }
        },
        "tecnologias": ["Flask", "LangChain", "OpenAI", "OpenRouter", "GPT-4o"],
        "status": "operacional"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check da API"""
    try:
        # Verifica se as variáveis de ambiente estão configuradas
        openai_key = os.getenv('OPEN_AI_API_KEY')
        openrouter_key = os.getenv('OPENROUTER_API_KEY')
        
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "api": "Tech Challenge Módulo 4",
            "versao": "0.1.0",
            "dependencias": {
                "openai_configured": bool(openai_key and openai_key.startswith('sk-')),
                "openrouter_configured": bool(openrouter_key and openrouter_key.startswith('sk-or-v1')),
                "flask_operacional": True,
                "langchain_operacional": True
            }
        }
        
        # Adiciona warnings se alguma configuração estiver faltando
        warnings = []
        if not openai_key:
            warnings.append("OPEN_AI_API_KEY não configurada")
        if not openrouter_key:
            warnings.append("OPENROUTER_API_KEY não configurada")
            
        if warnings:
            health_status["warnings"] = warnings
            health_status["status"] = "degraded"
        
        return jsonify(health_status), 200 if health_status["status"] == "healthy" else 206
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }), 500

@app.route('/transcribe-audio', methods=['POST'])
def transcribe_audio():
    data = request.get_json()
    audio_data = data.get('audio_data')
    audio_format = data.get('audio_format', 'wav')

    if not audio_data:
        return jsonify({"error": "audio_data é obrigatório"}), 400

    result = transcribe_audio_file(audio_data, audio_format)
    return result

@app.route('/analyse-audio-psycological-issue', methods=['POST'])
def analyse_audio_psicological_issue_route():
    data = request.get_json()
    audio_data = data.get('audio_data')
    audio_format = data.get('audio_format', 'wav')

    if not audio_data:
        return jsonify({"error": "audio_data é obrigatório"}), 400

    result = analyse_audio_psicological_issue(audio_data, audio_format)
    return result

@app.route('/predict-emotion', methods=['POST'])
def predict_emotion():
    data = request.get_json()
    audio_data = data.get('audio_data')
    audio_format = data.get('audio_format', 'wav')

    if not audio_data:
        return jsonify({"error": "audio_data é obrigatório"}), 400
    result = predict_emotion_from_base64(audio_data, audio_format)
    return jsonify({ "emotion": result })

@app.route('/analyse-patient-psychological-issue', methods=['POST'])
def analyse_patient_psychological_issue():
    data = request.get_json()
    audio_data = data.get('audio_data')
    audio_format = data.get('audio_format', 'wav')

    if not audio_data:
        return jsonify({"error": "audio_data é obrigatório"}), 400

    result = transcribe_audio_file(audio_data, audio_format)
    # transcribe_audio_file returns a Flask Response or (Response, status_code) on error
    if isinstance(result, tuple):
        return result
    response_data = result.get_json()
    transcription = response_data.get('transcription', '') if isinstance(response_data, dict) else ''

    emotion_result = predict_emotion_from_base64(audio_data, audio_format)
    psychological_response = analyse_psicological_issue(transcription, emotion_result)
    psychological_data = psychological_response.get_json() if hasattr(psychological_response, 'get_json') else psychological_response

    return jsonify({
        "resume": psychological_data,
        "emotion": emotion_result,
        "transcription": transcription
    })

# Rotas para servir o frontend
@app.route('/frontend/<path:filename>')
def serve_frontend_files(filename):
    """Serve arquivos estáticos do frontend (CSS, JS, etc)"""
    return send_from_directory('Front', filename)

@app.route('/frontend')
@app.route('/frontend/')
def serve_frontend():
    """Serve o frontend HTML"""
    return send_from_directory('Front', 'index.html')

@app.route('/test-audio')
def test_audio():
    """Rota de teste para verificar se os áudios estão acessíveis"""
    audio_dir = os.path.join(os.path.dirname(__file__), 'audios')
    files = []
    for filename in os.listdir(audio_dir):
        if filename.lower().endswith(('.mp3', '.wav')):
            file_path = os.path.join(audio_dir, filename)
            files.append({
                'name': filename,
                'exists': os.path.exists(file_path),
                'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                'url': f'/audio/{filename}'
            })
    return jsonify({'files': files, 'audio_dir': audio_dir})

@app.route('/list-audios', methods=['GET'])
def list_audios():
    """Lista todos os arquivos de áudio disponíveis na pasta audios"""
    try:
        audio_dir = os.path.join(os.path.dirname(__file__), 'audios')
        
        if not os.path.exists(audio_dir):
            return jsonify({"error": "Diretório de áudios não encontrado"}), 404
        
        audio_files = []
        for filename in os.listdir(audio_dir):
            if filename.lower().endswith(('.mp3', '.wav')):
                file_path = os.path.join(audio_dir, filename)
                file_stats = os.stat(file_path)
                
                audio_files.append({
                    "name": filename,
                    "format": "mp3" if filename.lower().endswith('.mp3') else "wav",
                    "size": file_stats.st_size,
                    "modified": datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                })
        
        # Ordena por nome
        audio_files.sort(key=lambda x: x['name'])
        
        return jsonify({
            "audios": audio_files,
            "total": len(audio_files)
        })
    
    except Exception as e:
        return jsonify({"error": f"Erro ao listar áudios: {str(e)}"}), 500

@app.route('/audio/<path:filename>', methods=['GET'])
def serve_audio(filename):
    """Serve um arquivo de áudio específico"""
    try:
        audio_dir = os.path.join(os.path.dirname(__file__), 'audios')
        file_path = os.path.join(audio_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({"error": "Arquivo não encontrado"}), 404
        
        # Determina o mimetype
        mimetype = 'audio/mpeg' if filename.lower().endswith('.mp3') else 'audio/wav'
        
        response = send_file(file_path, mimetype=mimetype)
        response.headers['Accept-Ranges'] = 'bytes'
        response.headers['Cache-Control'] = 'public, max-age=3600'
        return response
    
    except Exception as e:
        return jsonify({"error": f"Erro ao servir áudio: {str(e)}"}), 500


# Rotas para configuração de chaves de API
@app.route('/config')
@app.route('/config/')
def serve_config_page():
    """Serve a página de configuração"""
    return send_from_directory('Front', 'config.html')

@app.route('/config/check', methods=['GET'])
def check_env_file():
    """Verifica se o arquivo .env existe e quais chaves estão configuradas"""
    try:
        env_path = find_dotenv()
        exists = bool(env_path and os.path.exists(env_path))
        
        if not exists:
            return jsonify({
                "exists": False,
                "has_openai_key": False,
                "has_openrouter_key": False
            })
        
        # Verifica se as chaves existem
        openai_key = os.getenv('OPEN_AI_API_KEY')
        openrouter_key = os.getenv('OPENROUTER_API_KEY')
        
        return jsonify({
            "exists": True,
            "has_openai_key": bool(openai_key and len(openai_key) > 0),
            "has_openrouter_key": bool(openrouter_key and len(openrouter_key) > 0),
            "env_path": env_path
        })
    
    except Exception as e:
        return jsonify({"error": f"Erro ao verificar .env: {str(e)}"}), 500

@app.route('/config/get', methods=['GET'])
def get_current_config():
    """Retorna as chaves atuais (parcialmente mascaradas)"""
    try:
        openai_key = os.getenv('OPEN_AI_API_KEY', '')
        openrouter_key = os.getenv('OPENROUTER_API_KEY', '')
        
        return jsonify({
            "openai_key": openai_key if openai_key else None,
            "openrouter_key": openrouter_key if openrouter_key else None
        })
    
    except Exception as e:
        return jsonify({"error": f"Erro ao obter configurações: {str(e)}"}), 500

@app.route('/config/save', methods=['POST'])
def save_config():
    """Salva ou atualiza as chaves no arquivo .env"""
    try:
        data = request.get_json()
        openai_key = data.get('openai_key')
        openrouter_key = data.get('openrouter_key')
        
        # Validação
        if not openai_key and not openrouter_key:
            return jsonify({"error": "Pelo menos uma chave deve ser fornecida"}), 400
        
        # Validação de formato
        if openrouter_key and not openrouter_key.startswith('sk-or-v1-'):
            return jsonify({"error": "Formato inválido para chave do OpenRouter"}), 400
        
        if openai_key and not openai_key.startswith('sk-'):
            return jsonify({"error": "Formato inválido para chave da OpenAI"}), 400
        
        # Encontra ou cria o arquivo .env
        env_path = find_dotenv()
        if not env_path:
            # Cria novo arquivo .env na raiz do projeto
            env_path = os.path.join(os.path.dirname(__file__), '.env')
            open(env_path, 'w').close()
        
        # Atualiza as chaves
        updated_keys = []
        
        if openai_key:
            set_key(env_path, 'OPEN_AI_API_KEY', openai_key)
            updated_keys.append('OPEN_AI_API_KEY')
        
        if openrouter_key:
            set_key(env_path, 'OPENROUTER_API_KEY', openrouter_key)
            updated_keys.append('OPENROUTER_API_KEY')
        
        return jsonify({
            "success": True,
            "message": f"Configurações salvas com sucesso! Chaves atualizadas: {', '.join(updated_keys)}",
            "updated_keys": updated_keys,
            "env_path": env_path,
            "warning": "Reinicie o servidor Flask para aplicar as mudanças"
        })
    
    except Exception as e:
        return jsonify({"error": f"Erro ao salvar configurações: {str(e)}"}), 500

@app.route('/config/test-openrouter', methods=['GET'])
def test_openrouter():
    """Testa se a chave do OpenRouter está funcionando"""
    try:
        openrouter_key = os.getenv('OPENROUTER_API_KEY')
        
        if not openrouter_key:
            return jsonify({
                "success": False,
                "error": "Chave do OpenRouter não configurada"
            })
        
        # Tenta fazer uma requisição simples para validar a chave
        from clients.openrouter import get_openrouter_client
        
        try:
            client = get_openrouter_client(temperature=0.0)
            # A inicialização bem-sucedida indica que a chave está no formato correto
            return jsonify({
                "success": True,
                "message": "Chave do OpenRouter configurada corretamente",
                "key_format": "sk-or-v1-****" + openrouter_key[-4:] if len(openrouter_key) > 4 else "****"
            })
        except Exception as client_error:
            return jsonify({
                "success": False,
                "error": f"Erro ao inicializar cliente: {str(client_error)}"
            })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro ao testar OpenRouter: {str(e)}"
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
