import json
from flask import jsonify
from clients.openrouter import get_openrouter_audio_client

from langchain_core.messages import HumanMessage
from typing import Dict, Any
from agents.prompts import PSYCOLOGICAL_ANALYSIS

def transcribe_audio(audio_data: str, audio_format: str = "wav") -> Dict[str, Any]:
    """
    Transcribes audio using OpenRouter's GPT-4o Audio Preview model via ChatOpenAI.
    """
    client = get_openrouter_audio_client(temperature=0.0)
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "Transcribe the audio to text. Transcribe in the same language as the audio."
            },
            {
                "type": "input_audio",
                "input_audio": {
                    "data": audio_data,
                    "format": audio_format
                }
            }
        ]
    )
    try:
        response = client.invoke([message])
        return {"choices": [{"message": {"content": response.content}}]}
    except Exception as e:
        raise Exception(f"Erro ao transcrever áudio: {str(e)}")


def analyze_audio_content(audio_data: str, audio_format: str = "wav") -> Dict[str, Any]:
    """
    Analyzes audio content for psychological signals using OpenRouter's GPT-4o Audio Preview model via ChatOpenAI.
    """
    client = get_openrouter_audio_client(temperature=0.1)
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": PSYCOLOGICAL_ANALYSIS
            },
            {
                "type": "input_audio",
                "input_audio": {
                    "data": audio_data,
                    "format": audio_format
                }
            }
        ]
    )
    response = client.invoke([message])
    return {"choices": [{"message": {"content": response.content}}]}

def transcribe_audio_file(audio_data: str, audio_format: str = "wav"):
    """
    Transcribes audio file using OpenRouter's GPT-4o Audio Preview model.

    Args:
        audio_data (str): Base64 encoded audio data
        audio_format (str): Audio format (default: "wav")

    Returns:
        flask.Response: JSON response with transcribed text
    """
    try:
        result = transcribe_audio(audio_data, audio_format)
        
        # Extract the transcribed text from the response
        if 'choices' in result and len(result['choices']) > 0:
            transcription = result['choices'][0]['message']['content']
        else:
            transcription = "Não foi possível transcrever o áudio."
        
        return jsonify({
            "transcription": transcription,
            "success": True
        })
    
    except Exception as e:
        return jsonify({
            "error": f"Erro na transcrição do áudio: {str(e)}",
            "success": False
        }), 500


def analyse_audio_psicological_issue(audio_data: str, audio_format: str = "wav"):
    """
    Analyzes audio content for psychological signals using OpenRouter.

    Args:
        audio_data (str): Base64 encoded audio data
        audio_format (str): Audio format (default: "wav")

    Returns:
        flask.Response: JSON response with psychological analysis
    """
    try:
        result = analyze_audio_content(audio_data, audio_format)
        
        # Extract the analysis from the response
        if 'choices' in result and len(result['choices']) > 0:
            analysis_content = result['choices'][0]['message']['content']
            
            # Try to parse as JSON
            try:
                analysis = json.loads(analysis_content)
            except json.JSONDecodeError:
                # If not valid JSON, return as raw text
                analysis = {
                    "raw_analysis": analysis_content,
                    "disclaimer": "Esta é uma análise automática e deve ser revisada por um psicólogo certificado."
                }
        else:
            analysis = {
                "error": "Não foi possível analisar o conteúdo do áudio.",
                "disclaimer": "Esta é uma análise automática e deve ser revisada por um psicólogo certificado."
            }
        
        return jsonify(analysis)
    
    except Exception as e:
        return jsonify({
            "error": f"Erro na análise do áudio: {str(e)}",
            "disclaimer": "Esta é uma análise automática e deve ser revisada por um psicólogo certificado."
        }), 500