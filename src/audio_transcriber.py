from config import Config
from logger import log


def transcribe(audio_path, output_dir):
    import whisper
    import os

    model_size = Config.get("whisper_model")
    log(f"Starting to transcribe, it can take a few minutes depending on hardware, model size and audio length...")

    try:
        whisper_model = whisper.load_model(model_size)
        log(f"Whisper model ({model_size}) loaded successfully")
    except Exception as e:
        log(f"Failed to load Whisper model: {e}")
        raise

    whisper_result = whisper_model.transcribe(audio_path)

    txt_path = os.path.join(output_dir, "transcription.txt")
    with open(txt_path, "w", encoding="utf8") as text_file:
        text_file.write(whisper_result["text"])
    log(f"Successfully saved transcription in {txt_path}")

    return txt_path
