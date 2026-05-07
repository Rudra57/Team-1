import os
import json
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional


load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


class EvidenceRow(BaseModel):
    study_title: str
    year: str
    population: str
    sample_size: str
    sepsis_type: str
    biomarker: str
    outcome: str
    main_finding: str
    statistical_method: str
    odds_ratio: str
    auc: str
    p_value: str
    source_quote: str
    chunk_id: str


EXTRACTION_PROMPT = """
You are a clinical evidence extraction system.

Your task is to read a medical research text chunk and extract structured clinical evidence.

SOURCE CHUNK ID:
{chunk_id}

SOURCE TEXT:
\"\"\"
{chunk_text}
\"\"\"

Return ONLY valid JSON.

Return a JSON list of evidence rows.

Each row must follow this exact schema:

[
  {{
    "study_title": "",
    "year": "",
    "population": "",
    "sample_size": "",
    "sepsis_type": "",
    "biomarker": "",
    "outcome": "",
    "main_finding": "",
    "statistical_method": "",
    "odds_ratio": "",
    "auc": "",
    "p_value": "",
    "source_quote": "",
    "chunk_id": ""
  }}
]

What to extract:
- biomarkers
- clinical scores
- predictors
- mortality outcomes
- sample size
- study design / statistical method
- odds ratios
- AUC values
- p-values
- main clinical findings

Rules:
1. Extract only information explicitly stated in the source text.
2. Do not invent medical facts.
3. If a field is missing, write "not reported".
4. source_quote must be copied exactly from the source text.
5. chunk_id must be "{chunk_id}".
6. Return [] if the chunk has no relevant clinical evidence.
7. Return JSON only. No markdown. No explanation.
"""


def clean_json_response(text: str) -> str:
    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def call_gpt_for_chunk(chunk_text: str, chunk_id: str) -> list[dict]:
    prompt = EXTRACTION_PROMPT.format(
        chunk_text=chunk_text,
        chunk_id=chunk_id
    )

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    content = clean_json_response(content)

    return json.loads(content)


def load_chunks(path: str) -> list[dict]:
    """
    Supports your current format:
    [
      "chunk text 1",
      "chunk text 2"
    ]

    Converts it into:
    [
      {"chunk_id": "chunk_0", "text": "..."},
      {"chunk_id": "chunk_1", "text": "..."}
    ]
    """

    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    chunks = []

    for i, item in enumerate(raw):
        if isinstance(item, str):
            chunks.append({
                "chunk_id": f"chunk_{i}",
                "text": item
            })

        elif isinstance(item, dict):
            chunks.append({
                "chunk_id": item.get("chunk_id", f"chunk_{i}"),
                "text": item.get("text", "")
            })

    return chunks


def validate_rows(rows: list[dict], chunk_text: str) -> list[dict]:
    validated = []

    for row in rows:
        quote = row.get("source_quote", "")

        row["quote_found_in_source"] = (
            quote != "not reported"
            and quote in chunk_text
        )

        try:
            valid_row = EvidenceRow(**row)
            row["schema_valid"] = True

        except Exception as e:
            row["schema_valid"] = False
            row["schema_error"] = str(e)

        validated.append(row)

    return validated


def extract_all_chunks(
    chunks_path: str,
    output_json: str = "data/output/evidence_rows.json",
    output_csv: str = "data/output/evidence_rows.csv",
    max_chunks: Optional[int] = None
):
    chunks = load_chunks(chunks_path)

    if max_chunks is not None:
        chunks = chunks[:max_chunks]

    all_rows = []

    for i, chunk in enumerate(chunks, start=1):
        print(f"Processing {i}/{len(chunks)}: {chunk['chunk_id']}")

        try:
            rows = call_gpt_for_chunk(
                chunk_text=chunk["text"],
                chunk_id=chunk["chunk_id"]
            )

            rows = validate_rows(rows, chunk["text"])
            all_rows.extend(rows)

        except Exception as e:
            print(f"Failed on {chunk['chunk_id']}: {e}")

    Path(output_json).parent.mkdir(parents=True, exist_ok=True)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_rows, f, indent=2, ensure_ascii=False)

    df = pd.DataFrame(all_rows)
    df.to_csv(output_csv, index=False)

    print(f"Saved JSON: {output_json}")
    print(f"Saved CSV: {output_csv}")
    print(f"Extracted rows: {len(all_rows)}")


if __name__ == "__main__":
    extract_all_chunks(
        chunks_path="data/Baloch_2022_clean_chunks.json",
            max_chunks=None    
    )