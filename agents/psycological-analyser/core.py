import json
import requests
from flask import jsonify
from langchain_core.prompts import PromptTemplate
from clients import get_open_ai_client
from clients.openrouter import get_openrouter_client
from .prompts import PSYCOLOGICAL_ANALYSIS


def resume_text(text_to_resume):
    """
    Summarizes the provided text using an AI language model.

    This function creates a prompt template that instructs the AI to act as a
    text summarizer and generates a condensed version of the input text in the
    same language.

    Args:
        text_to_resume (str): The text content to be summarized.

    Returns:
        str: The summarized version of the input text.
    """
    prompt = PromptTemplate.from_template(
        """
        PERSONA:
        Act as a text resumer
        
        OBJECTIVE:
        Resume the text given in the same language from the text provided

        OUTPUT:
        Return the resumed text in the JSON KEY "resume"
        
        TEXT:
            {text_to_resume}
        """
    )

    llm = get_open_ai_client(temperature=0.5)
    chain = prompt | llm
    result = chain.invoke({"text_to_resume": text_to_resume})

    return jsonify(json.loads(result.content))

def analyse_woman_psicological_issue(text):
    """
    Agent to understand the text based on a woman context.

    It should analyse and indicate the confiability of the analysis
    """
    client_config = get_openrouter_client()

    prompt_text = PSYCOLOGICAL_ANALYSIS.replace("{text_to_analyse}", text)

    payload = {
        "model": "openai/gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": prompt_text
            }
        ],
        "response_format": {"type": "json_object"}
    }

    response = requests.post(
        url=client_config["base_url"],
        headers=client_config["headers"],
        data=json.dumps(payload)
    )

    response.raise_for_status()
    result = response.json()
    content = result["choices"][0]["message"]["content"]

    return jsonify(json.loads(content))