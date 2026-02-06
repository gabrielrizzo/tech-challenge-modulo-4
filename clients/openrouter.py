import requests
import json
import os
from typing import Dict, Any


def get_openrouter_client():
    """
    Returns a configured OpenRouter client for API requests.
    
    Returns:
        dict: Configuration dictionary for OpenRouter API
    """
    return {
        "base_url": "https://openrouter.ai/api/v1/chat/completions",
        "headers": {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv('SITE_URL', ''),
            "X-Title": os.getenv('SITE_NAME', 'Tech Challenge Modulo 4'),
        }
    }


def transcribe_audio(audio_data: str, audio_format: str = "wav") -> Dict[str, Any]:
    """
    Transcribes audio using OpenRouter's GPT-4o Audio Preview model.
    
    Args:
        audio_data (str): Base64 encoded audio data
        audio_format (str): Audio format (default: "wav")
        
    Returns:
        dict: Transcription response from the API
    """
    client_config = get_openrouter_client()
    
    payload = {
        "model": "openai/gpt-4o-audio-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Transcreva este áudio para texto. Se o áudio estiver em português, mantenha o texto em português. Se estiver em outro idioma, transcreva no idioma original."
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": audio_data,
                            "format": audio_format
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(
        url=client_config["base_url"],
        headers=client_config["headers"],
        data=json.dumps(payload)
    )

    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        error_detail = response.json() if response.content else {"error": "No content"}
        raise Exception(f"Erro na API OpenRouter: {e}. Detalhes: {error_detail}")
    except Exception as e:
        raise Exception(f"Erro ao transcrever áudio: {str(e)}")


def analyze_audio_content(audio_data: str, audio_format: str = "wav") -> Dict[str, Any]:
    """
    Analyzes audio content for psychological signals using OpenRouter's GPT-4o Audio Preview model.
    
    Args:
        audio_data (str): Base64 encoded audio data
        audio_format (str): Audio format (default: "wav")
        
    Returns:
        dict: Analysis response from the API
    """
    client_config = get_openrouter_client()
    
    payload = {
        "model": "openai/gpt-4o-audio-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
                        Você é um assistente realizando análise psicológica de texto NÃO-DIAGNÓSTICA para um psicólogo certificado.

                        TAREFA:
                        Analise o conteúdo deste áudio (transcrito automaticamente). Identifique sinais emocionais/de saúde mental estritamente baseados no conteúdo. NÃO faça diagnóstico. Forneça um score de confiabilidade e justifique.

                        REGRAS FUNDAMENTAIS:
                        1) Sempre inclua um disclaimer informando que isto é apenas uma análise e deve ser usada por um psicólogo certificado para qualquer diagnóstico.
                        2) NÃO forneça diagnóstico ou rótulo definitivo. Use linguagem cautelosa: "pode indicar", "pode ser consistente com", "sinais sugerem".
                        3) Ordem baseada em evidências: (a) pistas observadas com citações -> (b) interpretações cautelosas -> (c) explicações alternativas/limitações -> (d) conclusão para psicólogo.
                        4) Triagem de risco: Se o texto sugerir auto-harm/suicídio/violência/perigo iminente, inclua recomendação urgente de busca de ajuda profissional.
                        5) Responda em português.

                        FORMATO DE SAÍDA (JSON apenas):
                        {
                            "disclaimer": "string",
                            "transcription": "string",
                            "text_summary": "string",
                            "observed_cues": [
                                {
                                    "cue": "string",
                                    "category": "string",
                                    "why_it_matters": "string"
                                }
                            ],
                            "possible_interpretations": [
                                {
                                    "interpretation": "string"
                                }
                            ],
                            "alternative_explanations_and_limitations": ["string"],
                            "risk_screening": {
                                "self_harm_or_suicide_signals": "none | unclear | possible | likely",
                                "violence_or_imminent_danger_signals": "none | unclear | possible | likely",
                                "recommended_action_if_risk": "string"
                            },
                            "conclusion_for_psychologist": "string",
                            "confiability_score": {
                                "score": "number (0-100)",
                                "rating_label": "low | medium | high",
                                "justification": ["string"]
                            },
                            "follow_up_questions_for_clinician": ["string"]
                        }
                        """
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": audio_data,
                            "format": audio_format
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(
        url=client_config["base_url"],
        headers=client_config["headers"],
        data=json.dumps(payload)
    )

    response.raise_for_status()
    return response.json()