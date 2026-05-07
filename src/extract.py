import os
import json
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

input_file = Path("data/all_chunks.json")
output_json = Path("data/output/output.json")
output_csv = Path("data/output/output.csv")

model = "gpt-4o-mini"


EVIDENCE_SCHEMA = {
    "name": "evidence_row",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "study_title": {"type": "string"},
            "year": {"type": "string"},
            "population": {"type": "string"},
            "sample_size": {"type": "string"},
            "sepsis_type": {"type": "string"},
            "biomarker": {"type": "string"},
            "outcome": {"type": "string"},
            "main_finding": {"type": "string"},
            "odds_ratio": {"type": "string"},
            "auc": {"type": "string"},
            "p_value": {"type": "string"},
            "source_quote": {"type": "string"},
            "chunk_id": {"type": "string"}
        },
        "required": [
            "study_title",
            "year",
            "population",
            "sample_size",
            "sepsis_type",
            "biomarker",
            "outcome",
            "main_finding",
            "odds_ratio",
            "auc",
            "p_value",
            "source_quote",
            "chunk_id"
        ]
    }
}


def extract_from_chunk(chunk: dict) -> dict:
    prompt = f"""
You are extracting evidence from medical research paper chunks.

Return one JSON object using the required schema.

Rules:
- Only use information explicitly present in the chunk.
- Do not guess.
- If a value is missing, use an empty string.
- source_quote must be a short exact quote from the chunk supporting the extraction.
- chunk_id must be the given chunk_id.
- study_title should be the paper title if visible, otherwise use paper_name.

Paper name: {chunk.get("paper_name", "")}
Chunk ID: {chunk.get("chunk_id", "")}

Chunk text:
{chunk.get("text", "")}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You extract structured evidence from scientific text."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": EVIDENCE_SCHEMA
        },
        temperature=0
    )

    content = response.choices[0].message.content
    return json.loads(content)


def main():
    with open(input_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    rows = []

    for i, chunk in enumerate(chunks, start=1):
        print(f"Processing chunk {i}/{len(chunks)}: {chunk.get('paper_name')} #{chunk.get('chunk_id')}")

        try:
            row = extract_from_chunk(chunk)
            rows.append(row)
        except Exception as e:
            print(f"Error on chunk {chunk.get('chunk_id')}: {e}")

    output_json.parent.mkdir(parents=True, exist_ok=True)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)

    print(f"Saved JSON to {output_json}")
    print(f"Saved CSV to {output_csv}")


if __name__ == "__main__":
    main()