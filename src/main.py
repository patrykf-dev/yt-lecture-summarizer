import os

from src import audio_downloader, audio_transcriber, transcription_summarizer

if __name__ == "__main__":
    video_url = "https://youtu.be/EIXhvkOS7k4"

    audio_path = audio_downloader.download_audio(video_url)
    txt_path = audio_transcriber.transcribe("tiny", audio_path, os.path.dirname(audio_path))
    transcription_summarizer.summarize(txt_path, os.path.dirname(audio_path))
