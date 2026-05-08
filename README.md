# Sepsis Atlas — AI-Powered Clinical Evidence Extraction System

## Overview

Sepsis Atlas is an AI-powered medical evidence pipeline designed to transform unstructured sepsis research papers into structured, analysis-ready clinical evidence.

Instead of manually reading and extracting findings from dozens of medical papers, which can be slow, expensive, and difficult to scale, the system automatically processes PDFs, extracts clinically relevant evidence, validates outputs, and organizes results into structured datasets for downstream analysis.

The project focuses on:
- scalable medical literature processing
- evidence extraction
- structured clinical knowledge generation
- verifiable and source-grounded outputs

---

## Project Architecture

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/ff7cd9c3-d8ca-4917-8d36-5baa6971daff" />



## How to Use

1. Place all relevant PDFs inside the `data/pdfs/` folder.

2. Run the data pipeline notebook:

```bash
src/Data_pipeline.ipynb
```

3. Run the extraction script:

```bash
src/extract.py
```

4. Run the validation notebook:

```bash
src/data_validation.ipynb
```

5. Final validated outputs will be generated in:

```text
data/output/validated_output.csv
```

---

## Data Engineering / Pipeline Layer

### Responsibilities
- PDF ingestion pipeline
- automated text extraction
- text cleaning & normalization
- chunk generation
- schema design
- validation infrastructure
- evidence table generation
- CSV/database preparation

### Technologies Used
- Python
- Jupyter Notebook
- PyMuPDF
- pandas
- JSON
- Pydantic

---

## AI / LLM Extraction Layer

### Responsibilities
- GPT/LLM prompt engineering
- evidence extraction from chunks
- schema-based structured output generation

---

## Pipeline Stages

## 1. PDF Extraction

Research papers are processed using PyMuPDF to extract raw text from all pages.

## 2. Text Cleaning

The pipeline removes:
- broken line breaks
- duplicate spaces
- formatting noise
- page markers

## 3. Chunking

Large medical papers are divided into smaller AI-processable chunks.

### Output
chunks.json 

## 4. Evidence Schema

The extraction schema defines the structure AI must generate:

json {   "study_title": "",   "year": "",   "population": "",   "sample_size": "",   "sepsis_type": "",   "biomarker": "",   "outcome": "",   "main_finding": "",   "odds_ratio": "",   "auc": "",   "p_value": "",   "source_quote": "",   "paper_name": "",   "chunk_id": "" } 

## 5. AI-Based Evidence Extraction

The AI system processes chunks and extracts:
- biomarkers
- outcomes
- mortality findings
- statistical metrics
- source-grounded evidence

## 6. Validation Layer

Pydantic validates AI outputs before storage to ensure:
- correct datatypes
- structured outputs
- schema consistency
- reliable evidence formatting

## 7. Final Evidence Table

Validated outputs are stored inside:

```text
data/output/validated_output.csv
```

---

## Technologies

- Python
- Jupyter Notebook
- PyMuPDF
- pandas
- Pydantic
- JSON
- OpenAI / LLM APIs

---

## Repository Structure

```text
Team-1
├── data/
│   ├── pdfs/
│   └── output/
│       ├── output.csv
│       ├── output.json
│       └── validated_output.csv
│   ├── chunks.json
│   ├── evidence_schema.json
│   └── evidence_table.csv
│
├── src/
│   ├── Data_pipeline.ipynb
│   ├── data_validation.ipynb
│   └── extract.py
│
└── README.md
``` 

---

## Future Improvements

- Streamlit dashboard
- semantic search
- vector database integration
- RAG-based querying
- advanced clinical filtering
- SQL backend integration

---

## Final Goal

The final system enables clinicians and researchers to query large collections of sepsis literature and receive:

- structured evidence
- aggregated findings
- source-grounded results
- analysis-ready medical data

instead of manually reading hundreds of pages of research papers.
