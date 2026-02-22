import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import get_resume_match_score
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise EnvironmentError("❌ GEMINI_API_KEY not found in .env file")

# --- Sample test data ---
resume_text = """
John Doe
Python Developer with 3 years of experience in AI and Data Science projects.
Skilled in FastAPI, Machine Learning, and NLP.
Bachelor's in Computer Science.
"""

job_description = """
Looking for a Python Developer with experience in FastAPI, REST APIs, and NLP.
Candidate should have 2+ years of experience and a background in Computer Science or related field.
"""

print("🔍 Testing Gemini API connection...")
result = get_resume_match_score(resume_text, job_description)

print("\n✅ API Test Result:")
print(result)
