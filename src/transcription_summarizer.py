import os.path

import requests
import sys
import textwrap


def summarize(txt_path, output_path):
    args = {
        "chunk_size": 5000,
        "temperature": 0.1,
        "model": "llama3.2:3b",
    }

    with open(txt_path, 'r', encoding='utf-8') as f:
        lecture_text = f.read()

    total_chars = len(lecture_text)
    print(f"Transcription loaded ({total_chars} characters)")

    chunks = chunk_text(lecture_text, args['chunk_size'], 200)
    print(f"Split into {len(chunks)} chunks")

    print(f"Generating summaries using Ollama model '{args['model']}'...")
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)...")
        summary = summarize_chunk(chunk, model_name=args['model'], temperature=args['temperature'])
        if summary:
            chunk_summaries.append(summary)
            print(f"✓ Chunk {i + 1} summarized")
        else:
            print(f"✗ Failed to summarize chunk {i + 1}")

    if not chunk_summaries:
        print("Error: Could not generate any summaries.", file=sys.stderr)
        return

    print("Creating final summary...")
    final_summary = create_final_summary(chunk_summaries, model_name=args['model'], temperature=args['temperature'])

    if not final_summary:
        print("Error: Failed to create final summary.", file=sys.stderr)
        final_summary = "\n\n".join(chunk_summaries)
        print("Using individual chunk summaries instead.")

    summary_path = os.path.join(output_path, "summary.txt")
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(final_summary)

    print(f"\nSummary successfully generated and saved to {summary_path}")

    print("LECTURE SUMMARY" + "=" * 50)
    wrapped_summary = textwrap.fill(final_summary, width=80)
    print(wrapped_summary)
    print("=" * 50)


def chunk_text(text, chunk_size, overlap):
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


def summarize_chunk(chunk, model_name="llama3:latest", temperature=0.1):
    prompt = f"""
    Below is a portion of a lecture transcript. Please provide a concise summary that captures the key points, main ideas, and important details from this section. Focus on extracting the most valuable information.

    LECTURE EXCERPT:
    {chunk}

    SUMMARY:
    """

    return _call_ollama(model_name, prompt, temperature)


def create_final_summary(chunk_summaries, model_name, temperature):
    combined_summaries = "\n\n".join(chunk_summaries)

    prompt = f"""
    Below are summaries of different sections of a long lecture. Please create a cohesive, well-organized final summary that captures the key points and themes of the entire lecture based on these section summaries. The final summary should be concise yet comprehensive.

    SECTION SUMMARIES:
    {combined_summaries}

    FINAL LECTURE SUMMARY:
    """

    return _call_ollama(model_name, prompt, temperature)


def _call_ollama(model_name, prompt, temperature):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False
            },
            timeout=180
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}", file=sys.stderr)
        return ""
