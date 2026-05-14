import re

# ---------------------------------------------
# 🧩 Step 1: Define Predefined Skill Weights
# ---------------------------------------------

skill_weights = {
    # Core Programming
    "python": 0.9,
    "java": 0.7,
    "javascript": 0.7,
    "c++": 0.7,
    "r": 0.6,

    # ML / AI
    "machine learning": 1.0,
    "deep learning": 0.85,
    "nlp": 0.8,
    "natural language processing": 0.8,
    "computer vision": 0.8,
    "reinforcement learning": 0.75,
    "large language models": 0.9,
    "llm": 0.9,
    "generative ai": 0.9,

    # Agentic AI / LLM Frameworks
    "langchain": 0.9,
    "langgraph": 0.9,
    "llamaindex": 0.85,
    "crewai": 0.8,
    "autogen": 0.8,
    "rag": 0.85,
    "vector database": 0.8,
    "chromadb": 0.75,
    "pinecone": 0.75,

    # ML Libraries
    "tensorflow": 0.9,
    "pytorch": 0.9,
    "scikit-learn": 0.8,
    "keras": 0.75,
    "hugging face": 0.85,
    "transformers": 0.85,
    "pandas": 0.65,
    "numpy": 0.65,
    "scipy": 0.6,
    "matplotlib": 0.5,

    # Web / API
    "fastapi": 0.8,
    "flask": 0.6,
    "django": 0.7,
    "rest api": 0.65,
    "api": 0.6,

    # Data
    "data science": 0.95,
    "data analysis": 0.75,
    "sql": 0.7,
    "mongodb": 0.65,
    "postgresql": 0.65,

    # DevOps / Tools
    "docker": 0.7,
    "git": 0.5,
    "linux": 0.55,
    "aws": 0.75,
    "gcp": 0.7,
    "azure": 0.7,

    # Soft Skills
    "communication": 0.4,
    "teamwork": 0.3,
    "problem solving": 0.4,
}

# ---------------------------------------------
# ⚙️ Step 2: Extract Skills from Text
# ---------------------------------------------
def extract_skills(text):
    """
    Extract skills mentioned in the text based on the skill_weights dictionary.
    Uses case-insensitive matching.
    """
    text = text.lower()
    found_skills = [skill for skill in skill_weights.keys() if re.search(r'\b' + re.escape(skill) + r'\b', text)]
    return found_skills

def weighted_skill_match(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    
    if not jd_skills:
        return {
            "keyword_score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "bonus_skills": [],
            "jd_skill_coverage": "0/0"
        }

    total_weight = sum(skill_weights[skill] for skill in jd_skills)
    matched_weight = sum(skill_weights[skill] for skill in resume_skills if skill in jd_skills)
    weighted_score = matched_weight / total_weight if total_weight > 0 else 0.0

    matched = [s for s in resume_skills if s in jd_skills]
    missing = [s for s in jd_skills if s not in resume_skills]
    bonus = [s for s in resume_skills if s not in jd_skills]

    return {
        "keyword_score": round(weighted_score, 2),
        "matched_skills": matched,
        "missing_skills": missing,
        "bonus_skills": bonus,
        "jd_skill_coverage": f"{len(matched)}/{len(jd_skills)}"
    }