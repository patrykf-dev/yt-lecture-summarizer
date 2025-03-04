# YouTube lecture summarizer

This project generates a brief summary of a YouTube video lecture.

## Prerequisites

Before you begin, ensure you have installed all required components:

* [Ollama](https://ollama.ai/) running with at least one LLM installed (`llama3.2:3b` is recommended)
* [Python 3.7+](https://www.python.org/downloads/) with required packages listed in [requirements.txt](requirements.txt)

## Usage

To use the YouTube Lecture Summarizer, follow these steps:

1. Clone this repository to your local machine.
```commandline
git clone https://github.com/patrykf-dev/yt-lecture-summarizer
```
2. Navigate to the project directory.
```commandline
cd yt-lecture-summarizer
```
3. [optional] Make sure you have all required packages installed
```commandline
pip install -r requirements.txt 
```
4. Run the main script, providing the YouTube url to your lecture:

```commandline
python src/main.py "https://youtu.be/EIXhvkOS7k4"
```

If you need to configure how the script works, feel free to modify the [config.json](config.json) file contents. 

## How it works

1. The script downloads the audio from the specified YouTube video.
2. It uses the Whisper model to transcribe the audio to text.
3. The transcription is divided into smaller chunks (~5000 characters long).
4. Each chunk is summarized by the model of your choice.
5. All chunk summaries are joined and shortened once again by the model of your choice.
6. The final summary is presented to you.

## Costs

All AI models in this project run locally on your machine. This means:

* No API keys or subscriptions are required.
* You can use this tool for free without usage limits.
