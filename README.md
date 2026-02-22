AI-Powered Resume Screener (CVNLP)

An intelligent resume parsing and ranking system that automates candidate shortlisting using hybrid semantic + keyword scoring with explainable AI outputs.

Overview

Manual resume screening is slow, inconsistent, and keyword-heavy systems miss contextual relevance.

CVNLP addresses this by combining:

Structured resume parsing

Semantic similarity modeling

Weighted ranking logic

Explainable suitability scoring

The system improves contextual matching between resumes and job descriptions while maintaining interpretability.

Core Architecture

Resume (PDF/DOCX)
→ Text Extraction (PyMuPDF / docx2txt)
→ NLP Preprocessing
→ Hybrid Scoring Engine
  • Keyword Matching
  • SentenceTransformer Embeddings
→ Weighted Ranking
→ GPT-based Explainability

Key Features

Automated PDF & DOCX resume parsing

Hybrid semantic + keyword scoring

Context-aware candidate ranking

Skill gap identification

Modular ML-ready architecture

Tech Stack

Python · NLP/NER · SentenceTransformers · GPT · PyMuPDF · docx2txt

Scoring Logic

Final Score = α(Keyword Score) + β(Semantic Similarity)

Hybrid scoring improves contextual relevance compared to keyword-only baselines.

Why This Matters

Reduces manual screening time

Improves ranking consistency

Captures semantic skill equivalence (e.g., “ML” ≈ “Machine Learning”)

Maintains explainability for recruiter trust

Future Extensions

FastAPI deployment

Batch ranking pipeline

Recruiter analytics dashboard

Fine-tuned domain-specific embeddings

Author: Jitender Singh
B.Tech CSE
