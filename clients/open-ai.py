from langchain_openai import ChatOpenAI
import os


def get_open_ai_client(temperature):
    """
    Returns ChatOpenAI client from Langchain with the temperature passed.

    Args:
        temperature (float): The temperature for response randomness (0.0 to 1.0).

    Returns:
        ChatOpenAI: A configured ChatOpenAI client instance with JSON response format.
    """
    open_ai_client = ChatOpenAI(
        api_key=os.getenv('OPEN_AI_API_KEY'),
        temperature=temperature,
        model="gpt-3.5-turbo",
        model_kwargs={"response_format": {"type": "json_object"}}
    )

    return open_ai_client
