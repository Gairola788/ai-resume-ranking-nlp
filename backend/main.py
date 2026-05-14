import os
import nltk
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from parser import extract_text
from preprocessing import clean_text
from matcher import match_resume_to_jd
from semantic_similarity import semantic_similarity
from keyword_matcher import weighted_skill_match
from ranker import rank_candidates, get_verdict

# -------------------------------------------
# NLTK downloads (runs once)
# -------------------------------------------
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

app = FastAPI()

# -------------------------------------------
# CORS — allows frontend to talk to backend
# -------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------
# Health check — to verify server is running
# -------------------------------------------
@app.get("/")
def root():
    return {"status": "Resume Screener API is running"}


# -------------------------------------------
# Single resume screen endpoint
# -------------------------------------------
@app.post("/screen")
async def screen_resume(
    jd_text: str = Form(...),
    resume: UploadFile = File(...)
):
    # Read and extract text from resume
    resume_bytes = await resume.read()
    raw_text = extract_text(resume_bytes, resume.filename)
    clean_resume = clean_text(raw_text)
    clean_jd = clean_text(jd_text)

    # Score
    semantic_score = semantic_similarity(clean_resume, clean_jd)
    tfidf_result = match_resume_to_jd(clean_resume, clean_jd)
    tfidf_score = tfidf_result[0][1] if tfidf_result else 0.0
    keyword_result = weighted_skill_match(clean_resume, clean_jd)
    keyword_score = keyword_result.get("keyword_score", 0.0)

    # Final score
    from ranker import calculate_final_score
    final = calculate_final_score(semantic_score, tfidf_score, keyword_score)

    return {
        "filename": resume.filename,
        "semantic_score": round(semantic_score, 3),
        "tfidf_score": round(tfidf_score, 3),
        "keyword_score": keyword_score,
        "matched_skills": keyword_result.get("matched_skills", []),
        "missing_skills": keyword_result.get("missing_skills", []),
        "final_score": final,
        "verdict": get_verdict(final)
    }


# -------------------------------------------
# Multiple resumes ranking endpoint
# -------------------------------------------
@app.post("/rank")
async def rank_resumes(
    jd_text: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    clean_jd = clean_text(jd_text)
    candidates = []

    for resume in resumes:
        resume_bytes = await resume.read()

        try:
            raw_text = extract_text(resume_bytes, resume.filename)
        except ValueError as e:
            # Skip unreadable files, don't crash whole request
            candidates.append({
                "filename": resume.filename,
                "error": str(e),
                "final_score": 0.0,
                "rank": None
            })
            continue

        clean_resume = clean_text(raw_text)

        # Score each resume
        semantic_score = semantic_similarity(clean_resume, clean_jd)
        tfidf_result = match_resume_to_jd(clean_resume, clean_jd)
        tfidf_score = tfidf_result[0][1] if tfidf_result else 0.0
        keyword_result = weighted_skill_match(clean_resume, clean_jd)
        keyword_score = keyword_result.get("keyword_score", 0.0)

        candidates.append({
            "filename": resume.filename,
            "semantic_score": round(semantic_score, 3),
            "tfidf_score": round(tfidf_score, 3),
            "keyword_score": keyword_score,
            "matched_skills": keyword_result.get("matched_skills", []),
            "missing_skills": keyword_result.get("missing_skills", []),
        })

    # Rank valid candidates
    valid = [c for c in candidates if "error" not in c]
    failed = [c for c in candidates if "error" in c]

    ranked = rank_candidates(valid)

    # Add verdict to each
    for candidate in ranked:
        candidate["verdict"] = get_verdict(candidate["final_score"])

    return {
        "total": len(resumes),
        "ranked": ranked,
        "failed": failed
    }