import os
import re

import yt_dlp
import moviepy


def download_audio(youtube_url):
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")

    os.makedirs(output_dir, exist_ok=True)

    download_config = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
        'extract_flat': 'in_playlist',
    }

    with yt_dlp.YoutubeDL(download_config) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        title = info.get('title', 'Unknown Title')
        downloaded_file = ydl.prepare_filename(info)

    if downloaded_file.endswith('.mp3'):
        mp3_path = downloaded_file
    else:
        parent_path = os.path.join(output_dir, _make_string_safe(title))
        os.makedirs(parent_path, exist_ok=True)
        mp3_path = os.path.join(parent_path, "audio.mp3")
        audio_clip = moviepy.AudioFileClip(downloaded_file)
        audio_clip.write_audiofile(mp3_path)
        audio_clip.close()
        os.remove(downloaded_file)

    return os.path.abspath(mp3_path)


def _make_string_safe(input_string):
    ascii_string = input_string.encode('ascii', 'ignore').decode('ascii')
    underscored_string = ascii_string.replace(' ', '_')
    lowercase_string = underscored_string.lower()
    clean_string = re.sub(r'[^a-z0-9_]', '', lowercase_string)
    single_underscore_string = re.sub(r'_+', '_', clean_string)[:40]
    final_string = single_underscore_string.strip('_')
    return final_string
