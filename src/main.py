import os
import textwrap

from src import audio_downloader, audio_transcriber, transcription_summarizer

if __name__ == "__main__":
    video_url = "https://youtu.be/EIXhvkOS7k4"

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")
    audio_path = audio_downloader.download_audio(video_url, output_dir)
    txt_path = audio_transcriber.transcribe("tiny", audio_path, os.path.dirname(audio_path))
    final_summary = transcription_summarizer.summarize(txt_path, os.path.dirname(audio_path))
    print("\n\n\n" + "=" * 80)
    print(textwrap.fill(final_summary, width=80))
