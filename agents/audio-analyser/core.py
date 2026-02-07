import json
from flask import jsonify
from clients.openrouter import get_openrouter_audio_client

from langchain_core.messages import HumanMessage
from typing import Dict, Any

PSYCOLOGICAL_ANALYSIS = """
        You are an assistant performing NON-DIAGNOSTIC psychological text analysis for a certified psychologist.

        TASK
        Analyze the following text written by a woman. Identify emotional/mental-health *signals* strictly based on the text. Do NOT diagnose. Provide a reliability ("confiability") score and justify it.

        NON-NEGOTIABLE RULES
        1) Always include a disclaimer stating: this is only an analysis and must be used by a certified psychologist to provide any diagnosis.
        2) Do NOT output a diagnosis or definitive disorder label. Avoid claims like “she has X”. Use cautious language: “may indicate”, “could be consistent with”, “signals suggest”.
        3) Evidence-first order: (a) observed cues with quotes/paraphrases → (b) cautious interpretations → (c) alternative explanations/limitations → (d) conclusion for psychologist.
        If any user-provided example places conclusions first, reverse the order and keep evidence-first.
        4) Risk handling: If the text suggests self-harm/suicidality/violence/imminent danger as possible or likely, include an urgent recommended action to seek immediate professional help (without diagnosing).
        5) Output MUST be valid JSON ONLY (no markdown, no extra text).
        6) Should remove any sensitive data about the woman, that could lead to privacy or identificate the woman
        7) ALWAYS ANSWER IN PORTUGUESE

        OUTPUT FORMAT (JSON ONLY; follow this schema exactly)
        {{
        "disclaimer": "string (must mention certified psychologist and non-diagnostic nature)",
        "text_summary": "string (1-3 sentences, neutral)",
        "observed_cues": [
            {{
            "cue": "string (direct quote or close paraphrase from the text)",
            "category": "string (e.g., mood/anxiety/stress/trauma/self-esteem/sleep/thought patterns)",
            "why_it_matters": "string (brief, non-diagnostic)"
            }}
        ],
        "possible_interpretations": [
            {{
            "interpretation": "string (cautious, non-diagnostic)",
            }}
        ],
        "alternative_explanations_and_limitations": [
            "string (at least 3 items)"
        ],
        "risk_screening": {{
            "self_harm_or_suicide_signals": "none | unclear | possible | likely",
            "violence_or_imminent_danger_signals": "none | unclear | possible | likely",
            "recommended_action_if_risk": "string (only if possible/likely; otherwise empty string)"
        }},
        "conclusion_for_psychologist": "string (3–6 sentences, cautious summary; no diagnosis)",
        "confiability_score": {{
            "score": "number (0-100)",
            "rating_label": "low | medium | high",
            "justification": [
            "string (specific reasons tied to text quality and evidence)"
            ]
        }},
        "follow_up_questions_for_clinician": [
            "string (3–8 questions a psychologist could ask)"
        ]
        }}

        COMPLETENESS CHECK (DO INTERNALLY BEFORE OUTPUT)
        - Did you include the disclaimer?
        - Did you avoid diagnosis?
        - Did you include cues, interpretations, limitations, risk screening, conclusion, confiability score + justification?
        - Is the output valid JSON only?

        INPUT TEXT (analyze this):
        <<<{text_to_analyse}>>>
    """

def transcribe_audio(audio_data: str, audio_format: str = "wav") -> Dict[str, Any]:
    """
    Transcribes audio using OpenRouter's GPT-4o Audio Preview model via ChatOpenAI.
    """
    client = get_openrouter_audio_client(temperature=0.0)
    message = HumanMessage(
        content=[
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