# app/nlp/ner_and_skills.py
import re
from typing import Dict, List
from dateutil import parser as dateparser
from datetime import datetime

try:
    import spacy
    _NLP = spacy.load("en_core_web_sm")
except Exception:
    _NLP = None

# ------------------------
# Domain-specific skill banks
# ------------------------
HR_SKILLS = [
    "hr", "human resources", "recruitment", "talent acquisition", "onboarding",
    "payroll", "payroll management", "employee relations", "hr operations",
    "compensation", "benefits", "excel", "advanced excel", "vlookup", "pivot",
    "hris", "hrms", "attendance", "policies", "performance management",
    "interviewing", "employee engagement"
]

IT_SKILLS = [
    "python", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "nlp", "natural language processing", "sql", "aws", "azure", "docker",
    "flask", "django", "rest", "java", "c++", "git", "linux", "spark", "hadoop",
    "react", "node", "javascript", "typescript", "kubernetes"
]

FINANCE_SKILLS = [
    "accounting", "gst", "tax", "auditing", "finance", "ledger", "tally",
    "financial analysis", "reconciliation", "payables", "receivables",
    "ms-excel", "advanced excel", "pivot", "budgeting", "forecasting"
]

GENERAL_SKILLS = sorted(list(set(HR_SKILLS + IT_SKILLS + FINANCE_SKILLS)))

# Map domain keys to banks
DOMAIN_BANKS = {
    "HR": HR_SKILLS,
    "IT": IT_SKILLS,
    "FINANCE": FINANCE_SKILLS,
    "GENERAL": GENERAL_SKILLS
}

# ------------------------
# Helpers: email / phone
# ------------------------
def _find_email(text: str):
    m = re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text)
    return m.group(0) if m else ""

def _find_phone(text: str):
    m = re.search(r'(\+?\d{1,3})?[\s\-\.\(]?\d{2,4}[\s\-\.\)]?\d{3,5}[\s\-\.\)]?\d{3,5}', text)
    return m.group(0) if m else ""

# ------------------------
# Experience extractor (robust)
# ------------------------
def _round_to_half(years_float: float) -> float:
    return round(years_float * 2) / 2.0

def extract_years(text: str):
    if not text:
        return 0.0
    txt = text.lower()

    # 1) Explicit "Total work experience" pattern
    m = re.search(
        r'total(?:\s+work)?\s+experience[:\s\-]*([0-9]+)\s*(?:years|yrs)?'
        r'(?:[,\/\s]*(\d+)\s*(?:months|mos)?)?',
        txt
    )
    if m:
        try:
            years = int(m.group(1))
            months = int(m.group(2)) if m.group(2) else 0
            val = years + (months / 12.0)
            return _round_to_half(val)
        except:
            pass

    # 2) Patterns like "3 years 5 months"
    m = re.search(r'(\d+)\s*(?:years|yrs)\s*(\d+)\s*(?:months|mos)', txt)
    if m:
        years = int(m.group(1))
        months = int(m.group(2))
        val = years + (months / 12.0)
        return _round_to_half(val)

    # 3) Single "X years" (take largest)
    matches = re.findall(r'(\d+(?:\.\d+)?)\s*\+?\s*(?:years|yrs)', txt)
    if matches:
        floats = [float(x) for x in matches]
        if floats:
            return _round_to_half(max(floats))

    # 4) Date ranges like "Jan 2018 to Mar 2021" or "2018-2021"
    range_matches = re.findall(
        r'([A-Za-z]{3,9}\s*\d{4}|\d{4})\s*(?:to|-|–|—)\s*([A-Za-z]{3,9}\s*\d{4}|\d{4})',
        text
    )
    for start_str, end_str in range_matches:
        try:
            start = dateparser.parse(start_str, default=datetime(1, 1, 1))
            end = dateparser.parse(end_str, default=datetime(1, 1, 1))
            if end > start:
                delta_years = (end - start).days / 365.0
                return _round_to_half(delta_years)
        except:
            continue

    return 0.0

# ------------------------
# Domain detection from job description
# ------------------------
def detect_domain(text: str) -> str:
    """
    Simple heuristic to detect JD domain.
    Returns one of: "HR", "IT", "FINANCE", "GENERAL"
    """
    if not text:
        return "GENERAL"
    txt = text.lower()
    # HR signals
    hr_signals = ["hr", "human resources", "recruit", "talent", "onboard", "payroll", "employee relations", "hris"]
    if any(sig in txt for sig in hr_signals):
        return "HR"
    # IT signals
    it_signals = ["developer", "engineer", "software", "python", "java", "machine learning", "ml", "devops", "frontend", "backend", "react", "node"]
    if any(sig in txt for sig in it_signals):
        return "IT"
    # Finance signals
    fin_signals = ["account", "gst", "tax", "finance", "audit", "auditor", "tally", "accounts payable", "accounts receivable"]
    if any(sig in txt for sig in fin_signals):
        return "FINANCE"
    return "GENERAL"

# ------------------------
# Skill extraction using chosen bank
# ------------------------
def extract_skills(text: str, bank: List[str]) -> List[str]:
    found = set()
    lower = text.lower()
    # match longer phrases first
    bank_sorted = sorted(bank, key=lambda s: -len(s))
    for skill in bank_sorted:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, lower):
            found.add(skill.lower())
    return sorted(found)

# ------------------------
# Name & education extractors (simple heuristics + spaCy)
# ------------------------
def extract_name(text: str):
    if _NLP:
        doc = _NLP(text[:2000])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
    # fallback heuristics
    m = re.search(r'name[:\s\-]{1,5}([A-Za-z ]{2,40})', text)
    if m:
        return m.group(1).strip()
    m = re.match(r'^\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+){0,2})', text)
    if m:
        return m.group(1).strip()
    return ""

def extract_education(text: str):
    text_l = text.lower()
    if "m.b.a" in text_l or "mba" in text_l or "master" in text_l:
        return "Master"
    if "b.tech" in text_l or "bachelor" in text_l or "b.sc" in text_l:
        return "Bachelor"
    if "phd" in text_l or "doctorate" in text_l:
        return "PhD"
    return ""

# ------------------------
# Main parser: returns structured candidate
# ------------------------
def parse_resume(text: str, filename: str = "") -> Dict:
    """
    Returns structured candidate dict using GENERAL_SKILLS as fallback.
    """
    return {
        "candidate_id": filename,
        "name": extract_name(text) or "",
        "email": _find_email(text) or "",
        "phone": _find_phone(text) or "",
        "skills": extract_skills(text, GENERAL_SKILLS),
        "experience_years": extract_years(text),
        "education": extract_education(text),
        "raw_text": text
    }
