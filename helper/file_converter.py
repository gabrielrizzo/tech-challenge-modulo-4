"""File conversion utilities."""

import base64
import os
import tempfile


def base64_to_temp_file(base64_data: str, file_extension: str = "wav") -> str:
    """
    Decode base64 data and write to a temporary file. Caller must unlink the file when done.

    Args:
        base64_data: Base64-encoded content (no data URL prefix).
        file_extension: Extension for the temp file, e.g. "wav", "mp3".

    Returns:
        Path to the temporary file.
    """
    raw = base64.b64decode(base64_data, validate=True)
    suffix = f".{file_extension}" if not file_extension.startswith(".") else file_extension
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        os.write(fd, raw)
    finally:
        os.close(fd)
    return path
