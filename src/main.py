import os
import sys

import audio_downloader
import audio_transcriber
import transcription_summarizer
from logger import log

if __name__ == "__main__":
    if len(sys.argv) == 1:
        log("Error: please provide url to the YouTube video lecture as sys arg")
        sys.exit(1)

    video_url = sys.argv[1]

    audio_path = audio_downloader.download_audio(video_url)
    txt_path = audio_transcriber.transcribe(audio_path, os.path.dirname(audio_path))
    final_summary = transcription_summarizer.summarize(txt_path, os.path.dirname(audio_path))
