def transcribe(model_size, audio_path, output_dir):
    import whisper
    import os

    """
    model_size options: "tiny", "base", "small", "medium", "large"
    """
    print(f"Starting to transcribe, estimated duration is {_estimate_time(audio_path, model_size)}")

    try:
        whisper_model = whisper.load_model(model_size)
        print(f"Whisper model loaded successfully")
    except Exception as e:
        print(f"Failed to load Whisper model: {e}")
        raise

    result = whisper_model.transcribe(audio_path)
    txt_path = os.path.join(output_dir, "transcription.txt")
    with open(txt_path, "w", encoding="utf8") as text_file:
        text_file.write(result["text"])
    return txt_path


def _estimate_time(file_path, model_size):
    import torch

    duration_seconds = 3386  # TODO: read real mp3 duration

    time_factors = {
        "tiny": 0.1,
        "base": 0.2,
        "small": 0.5,
        "medium": 1.0,
        "large": 2.0
    }
    time_factor = time_factors.get(model_size, 0.5)

    if torch.cuda.is_available():
        time_factor = time_factor * 0.2

    estimated_seconds = duration_seconds * time_factor

    minutes, seconds = divmod(int(estimated_seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"
