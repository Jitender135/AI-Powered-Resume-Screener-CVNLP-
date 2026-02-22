# app/hybrid_matcher.py
import re
from typing import Dict, Set, List
# from app.Models.embeddings import cosine_similarity_score
from app.NLP.ner_and_skills import (
    detect_domain, DOMAIN_BANKS, extract_skills as extract_skills_with_bank
)

# weights (tune later)
WEIGHTS = {
    "skill": 0.50,
    "experience": 0.30,
    "education": 0.10,
    "semantic": 0.10
}

def _experience_score(candidate_years: float, jd_text: str) -> float:
    m = re.search(r'(\d+)\s*(?:\+)?\s*years?', jd_text.lower())
    if m:
        req = float(m.group(1))
        if candidate_years >= req:
            return 100.0
        else:
            return round(max(min((candidate_years / req) * 100.0, 100.0), 0.0), 2)
    return 100.0

def _education_score(candidate_edu: str, jd_text: str) -> float:
    jd_l = jd_text.lower()
    cand = candidate_edu.lower() if candidate_edu else ""
    if "master" in jd_l or "m.tech" in jd_l or "msc" in jd_l:
        return 100.0 if "master" in cand or "m" in cand else 50.0
    if "bachelor" in jd_l or "b.tech" in jd_l:
        return 100.0 if "bachelor" in cand or "b" in cand else 70.0
    return 100.0

def _extract_required_skills_from_jd(jd_text: str, domain: str) -> Set[str]:
    """
    Use detected domain to pick a relevant skill bank and extract skills from JD.
    """
    bank = DOMAIN_BANKS.get(domain, DOMAIN_BANKS["GENERAL"])
    jd_skills = set(extract_skills_with_bank(jd_text, bank=bank))
    return set([s.lower() for s in jd_skills])

def hybrid_match(candidate: Dict, jd_text: str) -> Dict:
    """
    candidate: dict from parse_resume(...)
    jd_text: job description text (cleaned)
    returns: dict with score, breakdown, reason, missing_skills, candidate
    """
    # 1) detect domain
    domain = detect_domain(jd_text)
    bank = DOMAIN_BANKS.get(domain, DOMAIN_BANKS["GENERAL"])

    # 2) required skills from JD using selected bank
    required_skills = set(extract_skills_with_bank(jd_text, bank=bank))
    required_skills = set([s.lower() for s in required_skills])

    # Fallback: if JD didn't contain any recognized skill from bank, fall back to GENERAL bank
    if not required_skills:
        required_skills = set(extract_skills_with_bank(jd_text, bank=DOMAIN_BANKS["GENERAL"]))
        required_skills = set([s.lower() for s in required_skills])

    # Candidate skills (lowercased)
    cand_skills = set([s.lower() for s in candidate.get("skills", [])])

    # Matched and missing
    matched_skills = required_skills & cand_skills
    missing_skills = sorted(list(required_skills - cand_skills))

    # Skill score (if no required skills found, default to 100)
    required_count = len(required_skills)
    if required_count == 0:
        skill_score = 100.0
    else:
        skill_score = round((len(matched_skills) / required_count) * 100.0, 2)

    # Experience and education scores
    exp_score = _experience_score(candidate.get("experience_years", 0.0), jd_text)
    edu_score = _education_score(candidate.get("education", ""), jd_text)

    # Semantic score
    try:
        semantic_score = cosine_similarity_score(candidate.get("raw_text", ""), jd_text)
    except Exception:
        semantic_score = 0.0

    # Combine weighted final score
    final_score = (
        WEIGHTS["skill"] * skill_score
        + WEIGHTS["experience"] * exp_score
        + WEIGHTS["education"] * edu_score
        + WEIGHTS["semantic"] * semantic_score
    )
    final_score = round(max(min(final_score, 100.0), 0.0), 2)

    # Build reason and breakdown
    reason_parts = [
        f"Domain: {domain}",
        f"Skill match: {len(matched_skills)}/{required_count} ({skill_score}%)",
        f"Experience score: {exp_score}% ({candidate.get('experience_years', 0.0)} yrs)",
        f"Education score: {edu_score}%",
        f"Semantic similarity: {semantic_score}%"
    ]
    reason_text = " | ".join(reason_parts)

    breakdown = {
        "skill_score": skill_score,
        "experience_score": exp_score,
        "education_score": edu_score,
        "semantic_score": semantic_score,
        "domain": domain
    }

    return {
        "score": final_score,
        "breakdown": breakdown,
        "reason": reason_text,
        "missing_skills": missing_skills,
        "candidate": candidate
    }
