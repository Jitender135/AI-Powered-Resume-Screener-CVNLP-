# app/planner.py
from typing import List, Dict, Tuple

# Small static mapping of common job titles -> required skills (tunable & extendable)
JOB_SKILL_BANK = {
    "data scientist": [
        "python", "pandas", "numpy", "sql", "machine learning", "scikit-learn",
        "statistics", "data visualization", "deep learning"
    ],
    "hr executive": [
        "hr", "recruitment", "onboarding", "payroll", "employee relations", "excel"
    ],
    "software engineer": [
        "python", "java", "git", "rest", "docker", "kubernetes", "react"
    ],
    # add more as needed
}

# Simple mapping of skills -> recommended short courses (static)
SKILL_TO_COURSES = {
    "python": ["Python for Everybody (Coursera)", "Complete Python Bootcamp (Udemy)"],
    "pandas": ["Data Manipulation with pandas (DataCamp)"],
    "machine learning": ["Machine Learning by Andrew Ng (Coursera)"],
    "deep learning": ["Deep Learning Specialization (Coursera)"],
    "sql": ["SQL for Data Science (Coursera)"],
    "excel": ["Excel Skills for Business (Coursera)"],
    "payroll": ["Payroll Management Essentials (Udemy)"],
    "recruitment": ["Recruiting Foundations (LinkedIn Learning)"],
    # add domain-specific suggestions...
}

def get_required_skills_for_job(title: str) -> List[str]:
    t = title.strip().lower()
    # exact match or simple fallback: if title contains keyword
    if t in JOB_SKILL_BANK:
        return JOB_SKILL_BANK[t]
    for key in JOB_SKILL_BANK:
        if key in t:
            return JOB_SKILL_BANK[key]
    # fallback: return a generic set (or empty)
    return []

def evaluate_readiness(candidate_skills: List[str], required_skills: List[str]) -> Dict:
    cand = {s.lower() for s in (candidate_skills or [])}
    req = [s.lower() for s in required_skills]
    if not req:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "readiness_pct": 0.0
        }
    matched = [s for s in req if s in cand]
    missing = [s for s in req if s not in cand]
    readiness = round((len(matched) / len(req)) * 100, 2)
    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "readiness_pct": readiness
    }

def recommend_courses_for_skills(skills: List[str], top_n: int = 3) -> Dict[str, List[str]]:
    recs = {}
    for s in skills:
        name = s.lower()
        if name in SKILL_TO_COURSES:
            recs[s] = SKILL_TO_COURSES[name][:top_n]
        else:
            recs[s] = ["No specific course mapped — search Coursera/Udemy for " + s]
    return recs
