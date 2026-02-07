import os
from langchain_openai import ChatOpenAI


def get_openrouter_client(temperature: float = 0.7, model_kwargs: dict = {}):
    """
    Returns a configured OpenRouter LangChain client for chat/chain usage (gpt-4o).
    """
    return ChatOpenAI(
        model="openai/gpt-4o",
        temperature=temperature,
        streaming=True,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        model_kwargs=model_kwargs,
        default_headers={
            "HTTP-Referer": "https://your-site.com",
            "X-Title": "My LangChain App"
        },
    )


def get_openrouter_audio_client(temperature: float = 0.0):
    """
    Returns a ChatOpenAI client configured for openai/gpt-4o-audio-preview (transcription, audio analysis).
    """
    return ChatOpenAI(
        model="openai/gpt-4o-audio-preview",
        temperature=temperature,
        streaming=False,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://your-site.com",
            "X-Title": "My LangChain App"
        },
    )