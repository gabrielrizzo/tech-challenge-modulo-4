import json
import requests
from flask import jsonify
from langchain_core.prompts import PromptTemplate
from clients.openrouter import get_openrouter_client
from agents.prompts import PSYCOLOGICAL_ANALYSIS

def analyse_psicological_issue(text, emotion):
    """
    Agent to understand the text based on a person context.

    It should analyse and indicate the confiability of the analysis
    """
    prompt = PromptTemplate.from_template(PSYCOLOGICAL_ANALYSIS)

    llm = get_openrouter_client(temperature=0.5, model_kwargs={"response_format": {"type": "json_object"}})
    chain = prompt | llm
    result = chain.invoke({"text_to_analyse": text, "emotion_to_analyse": emotion})

    return jsonify(json.loads(result.content))