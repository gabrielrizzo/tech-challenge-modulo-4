import importlib

# Import module with hyphen in name
open_ai_module = importlib.import_module(".open-ai", package="clients")
openrouter_module = importlib.import_module(".openrouter", package="clients")
# Export the client function
get_open_ai_client = open_ai_module.get_open_ai_client
get_openrouter_client = openrouter_module.get_openrouter_client
get_openrouter_audio_client = openrouter_module.get_openrouter_audio_client
__all__ = ["get_open_ai_client", "get_openrouter_client", "get_openrouter_audio_client"]
