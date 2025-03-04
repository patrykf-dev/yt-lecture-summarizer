import os
import sys
import textwrap

from src import audio_downloader, audio_transcriber, transcription_summarizer

if __name__ == "__main__":
    video_url = sys.argv[1]

    audio_path = audio_downloader.download_audio(video_url)
    txt_path = audio_transcriber.transcribe(audio_path, os.path.dirname(audio_path))
    final_summary = transcription_summarizer.summarize(txt_path, os.path.dirname(audio_path))
    print("\n\n\n" + "=" * 80)
    print(textwrap.fill(final_summary, width=80))
