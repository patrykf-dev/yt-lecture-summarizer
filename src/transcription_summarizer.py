import os.path

import requests
import sys


def summarize(txt_path, output_path):
    chunk_summaries = _generate_chunk_summaries(txt_path, output_path)

    if not chunk_summaries:
        print("Error: Could not generate chunk summaries.", file=sys.stderr)
        return

    return _create_final_summary(chunk_summaries, output_path)


def _generate_chunk_summaries(txt_path, output_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        lecture_text = f.read()
    total_chars = len(lecture_text)
    print(f"Transcription loaded ({total_chars} characters)")

    chunks = _chunk_text(lecture_text, 5000, 200)
    print(f"Split transcription into {len(chunks)} chunks")
    chunk_summaries = []
    for i, chunk_text in enumerate(chunks):
        print(f"\tProcessing chunk {i + 1}/{len(chunks)} ({len(chunk_text)} chars)...")
        chunk_summary = _summarize_chunk(chunk_text)
        chunk_summaries.append(chunk_summary)

    chunks_path = os.path.join(output_path, "summary_chunks.txt")
    with open(chunks_path, 'w', encoding='utf-8') as file:
        file.write("\n\n".join(chunk_summaries))

    return chunk_summaries


def _chunk_text(text, chunk_size, overlap):
    chunks = []
    start = 0
    end = 0

    while start < len(text) and end < len(text):
        end = start + chunk_size
        if end > len(text):
            end = len(text)
        else:
            sentence_end = text.rfind('.', end - overlap, end)
            if sentence_end != -1:
                end = sentence_end + 1

        chunk = text[start:end]
        chunks.append(chunk)
        start = max(end - overlap, start + 1)

    return chunks


def _summarize_chunk(chunk):
    prompt = f"""
    Below is a portion of a lecture transcript. Please provide a concise summary that captures the key points, main ideas, and important details from this section. Focus on extracting the most valuable information.

    LECTURE EXCERPT:
    {chunk}

    SUMMARY:
    """

    return _call_ollama(prompt)


def _create_final_summary(chunk_summaries, output_path):
    print("Creating final summary...")
    combined_summaries = "\n\n".join(chunk_summaries)

    prompt = f"""
    Below are summaries of different sections of a long lecture. Please create a cohesive, well-organized final summary that captures the key points and themes of the entire lecture based on these section summaries. The final summary should be concise yet comprehensive.

    SECTION SUMMARIES:
    {combined_summaries}

    FINAL LECTURE SUMMARY:
    """

    final_summary = _call_ollama(prompt)

    summary_path = os.path.join(output_path, "summary.txt")
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(final_summary)

    return final_summary


def _call_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "temperature": 0.1,
                "stream": False
            },
            timeout=180
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except Exception as e:
        print(f"Error communicating with Ollama: {e}", file=sys.stderr)
        return ""
