# AI-Powered Resume Screener (CVNLP)

Automated resume parsing and candidate ranking using hybrid semantic + keyword scoring with explainable AI outputs.

---

## Problem

Manual resume screening is slow and inconsistent.  
Keyword-only systems miss contextual skill relevance.

---

## Solution

CVNLP combines structured parsing with semantic similarity modeling to produce context-aware, interpretable candidate rankings.

---

## Architecture

Resume (PDF/DOCX)  
→ Text Extraction (PyMuPDF / docx2txt)  
→ NLP Preprocessing  
→ Hybrid Scoring  
   • Keyword Matching  
   • SentenceTransformer Embeddings  
→ Weighted Ranking  
→ GPT-based Explainability  

---

## Core Features

- Automated PDF & DOCX parsing  
- Hybrid semantic + keyword scoring  
- Context-aware ranking  
- Skill gap identification  
- Modular ML-ready pipeline  

---

## Scoring Model

Final Score = α(Keyword Score) + β(Semantic Similarity)

Improves contextual relevance vs keyword-only baselines.

---

## Tech Stack

Python · PyMuPDF · docx2txt · NLP/NER  
SentenceTransformers · GPT  

---

## Impact

- Reduces screening time  
- Improves ranking consistency  
- Maintains explainability for recruiter trust  

---

**Author:** Jitender Singh  
B.Tech Computer Science & Engineering
