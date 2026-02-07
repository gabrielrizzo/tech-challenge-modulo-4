import os

import librosa
import numpy as np
import torch
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor

from helper import base64_to_temp_file

model_id = "firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3"
model = AutoModelForAudioClassification.from_pretrained(model_id)

feature_extractor = AutoFeatureExtractor.from_pretrained(model_id, do_normalize=True)
id2label = model.config.id2label


def preprocess_audio(audio_path, feature_extractor, max_duration=30.0):
    audio_array, sampling_rate = librosa.load(audio_path, sr=None)

    max_length = int(feature_extractor.sampling_rate * max_duration)
    if len(audio_array) > max_length:
        audio_array = audio_array[:max_length]
    else:
        audio_array = np.pad(audio_array, (0, max_length - len(audio_array)))

    inputs = feature_extractor(
        audio_array,
        sampling_rate=feature_extractor.sampling_rate,
        max_length=max_length,
        truncation=True,
        return_tensors="pt",
    )
    return inputs


def predict_emotion(audio_path, model, feature_extractor, id2label, max_duration=30.0):
    """Predict emotion from an audio file path."""
    inputs = preprocess_audio(audio_path, feature_extractor, max_duration)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_id = torch.argmax(logits, dim=-1).item()
    predicted_label = id2label[predicted_id]

    return predicted_label


def predict_emotion_from_base64(
    base64_audio: str,
    audio_format: str = "wav",
    max_duration: float = 30.0,
) -> str:
    """
    Predict emotion from base64-encoded audio.

    Args:
        base64_audio: Base64-encoded audio content (no data URL prefix).
        audio_format: Format of the audio, e.g. "wav", "mp3". Used for the temp file extension and librosa.
        max_duration: Max duration in seconds to process.

    Returns:
        Predicted emotion label.
    """
    temp_path = base64_to_temp_file(base64_audio, audio_format)
    try:
        return predict_emotion(
            temp_path,
            model,
            feature_extractor,
            id2label,
            max_duration=max_duration,
        )
    finally:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
