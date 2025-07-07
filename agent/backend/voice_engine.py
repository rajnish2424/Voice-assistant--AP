import os
from TTS.api import TTS
from datetime import datetime

# Load TTS model once
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

def generate_response_audio(text: str, output_dir="audio") -> str:
    """
    Generate speech audio from text using Coqui TTS and save it to a .wav file.

    Returns:
        Full path to the generated audio file
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{output_dir}/greeting_{timestamp}.wav"
    tts.tts_to_file(text=text, file_path=filename)
    return filename

def call_via_agora(phone_number: str, audio_path: str) -> bool:
    """
    Placeholder function to trigger a voice call using Agora and play audio.

    This should:
    1. Initiate call via Agora SDK or SIP Gateway
    2. Stream the .wav file as audio

    Currently not implemented.
    """
    print(f"[🔔] Call to {phone_number} would be placed here.")
    print(f"[🔊] Audio to play: {audio_path}")
    return True
