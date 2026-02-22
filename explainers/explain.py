# app/explainers/explain.py
from typing import Dict

def make_short_explanation(breakdown: Dict, candidate: Dict) -> str:
    """
    Build a concise sentence explaining the main drivers of the score.
    Example result:
      "80% skill match (3/4 skills), 100% experience match (3.5 yrs), semantic similarity 78%."
    """
    if not breakdown:
        return ""

    # Extract components with safe defaults
    skill = breakdown.get("skill_score", None)
    exp = breakdown.get("experience_score", None)
    edu = breakdown.get("education_score", None)
    sem = breakdown.get("semantic_score", None)
    domain = breakdown.get("domain", "")

    parts = []
    if skill is not None:
        parts.append(f"{skill}% skill match")
    if exp is not None:
        # show experience years if present on candidate
        yrs = candidate.get("experience_years")
        if yrs is not None:
            parts.append(f"{exp}% experience match ({yrs} yrs)")
        else:
            parts.append(f"{exp}% experience match")
    if edu is not None:
        parts.append(f"{edu}% education match")
    if sem is not None:
        parts.append(f"semantic similarity {sem}%")
    if domain:
        parts.append(f"domain: {domain}")

    return ". ".join(parts) + "."

def make_recommendation(breakdown: Dict, missing_skills:list) -> str:
    """
    Create a short action recommendation:
      - 'Ready to interview' if score high
      - 'Consider for training: <skills>' if missing skills present
      - 'Not suitable' if score low
    This uses simple thresholds (tuneable).
    """
    skill = breakdown.get("skill_score", 0)
    final_score = breakdown.get("final_score", None)
    # if final_score was not stored, we expect caller to pass overall score separately.
    # We'll use skill as proxy if final_score is not provided.

    # Heuristics (tune these thresholds to your needs)
    if final_score is None:
        # fallback heuristic
        if skill >= 80:
            level = "high"
        elif skill >= 60:
            level = "medium"
        else:
            level = "low"
    else:
        if final_score >= 80:
            level = "high"
        elif final_score >= 60:
            level = "medium"
        else:
            level = "low"

    if level == "high":
        return "Recommendation: Candidate ready to interview."
    elif level == "medium":
        if missing_skills:
            return f"Recommendation: Consider after short training in {', '.join(missing_skills[:3])}."
        return "Recommendation: Consider for interview; minor gaps."
    else:
        if missing_skills:
            return f"Recommendation: Not suitable now — missing {', '.join(missing_skills[:3])}."
        return "Recommendation: Not suitable."

# convenience wrapper so we can add final_score into breakdown easily
def generate_explanation_payload(score: float, breakdown: Dict, candidate: Dict, missing_skills: list) -> Dict:
    # copy breakdown to avoid mutating caller
    payload = dict(breakdown or {})
    payload["final_score"] = score
    payload["domain"] = payload.get("domain", "")
    short = make_short_explanation(payload, candidate)
    rec = make_recommendation(payload, missing_skills)
    return {
        "explanation_text": short,
        "recommendation": rec
    }
