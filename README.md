# Sepsis Atlas — AI-Powered Clinical Evidence Extraction System

## Overview

Sepsis Atlas is an AI-powered medical evidence pipeline designed to transform unstructured sepsis research papers into structured, analysis-ready clinical evidence.

Instead of manually reading and extracting findings from dozens of medical papers, the system automatically processes PDFs, extracts clinically relevant evidence, validates outputs, and organizes results into structured datasets for downstream analysis.

The project focuses on:
- scalable medical literature processing
- evidence extraction
- structured clinical knowledge generation
- verifiable and source-grounded outputs

---

# Problem Statement

Thousands of clinically valuable findings are buried inside medical research papers. Traditional meta-analysis requires manual extraction and is slow, expensive, and difficult to scale.

Sepsis Atlas automates this process by converting:
text Research PDFs → Structured Clinical Evidence 

---

# Project Architecture

```text
Medical PDFs
      ↓
Text Extraction, Cleaning & Normalization
      ↓
Chunking Pipeline
      ↓
AI-Based Evidence Extraction
      ↓
Pydantic Validation
      ↓
Structured Evidence Table
```

---

# Team Responsibilities

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

# Pipeline Stages

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

# Technologies

- Python
- Jupyter Notebook
- PyMuPDF
- pandas
- Pydantic
- JSON
- OpenAI / LLM APIs

---

# Future Improvements

- Streamlit dashboard
- semantic search
- vector database integration
- RAG-based querying
- advanced clinical filtering
- SQL backend integration

---

# Final Goal

The final system enables clinicians and researchers to query large collections of sepsis literature and receive:

- structured evidence
- aggregated findings
- source-grounded results
- analysis-ready medical data

instead of manually reading hundreds of pages of research papers.
