import os
from TTS.api import TTS
from datetime import datetime

# 🔁 Cache loaded models
loaded_models = {}

def get_tts_model(language: str) -> TTS:
    """
    Load the TTS model based on the specified language.
    Models are cached to avoid reloading every time.
    """
    lang = language.lower()

    if lang in loaded_models:
        return loaded_models[lang]

    if lang == "hindi":
        model_name = "tts_models/hi/cv/vakyansh-bert-350"
    else:
        model_name = "tts_models/en/ljspeech/tacotron2-DDC"

    print(f"🔊 Loading TTS model for language: {lang}")
    tts = TTS(model_name=model_name)
    loaded_models[lang] = tts
    return tts

def generate_response_audio(text: str, language="english", output_dir="audio") -> str:
    """
    Generate speech audio from text using Coqui TTS and save it to a .wav file.
    Returns:
        Full path to the generated audio file
    """
    tts = get_tts_model(language)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{output_dir}/greeting_{timestamp}.wav"
    tts.tts_to_file(text=text, file_path=filename)
    print(f"[✅] Audio generated at: {filename}")
    return filename

def call_via_agora(phone_number: str, audio_path: str) -> bool:
    """
    Placeholder function to trigger a voice call using Agora and play audio.
    """
    print(f"[🔔] Call to {phone_number} would be placed here.")
    print(f"[🔊] Audio to play: {audio_path}")
    return True
