from flask import request, Flask, jsonify
from dotenv import load_dotenv
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
