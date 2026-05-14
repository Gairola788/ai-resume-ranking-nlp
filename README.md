# AI-Based Resume Screening & Candidate Ranking System

A minor project built using NLP techniques to automatically screen resumes 
and rank candidates against a job description.

## Features
- Upload PDF, DOCX, or TXT resumes
- Three-layer NLP scoring: BERT Semantic + TF-IDF + Keyword Matching
- Multi-candidate ranking leaderboard
- Recruiter-friendly UI with skill gap analysis

## Tech Stack
- **Backend:** FastAPI, Python
- **NLP:** Sentence-Transformers (BERT), Scikit-learn (TF-IDF), Regex Keyword Matching
- **Frontend:** HTML, CSS, Vanilla JS
- **File Parsing:** pypdf, python-docx

## How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
Open `frontend/index.html` in your browser.

## Project Structure
```
ResumeScreener/
├── backend/
│   ├── main.py
│   ├── parser.py
│   ├── keyword_matcher.py
│   ├── semantic_similarity.py
│   ├── preprocessing.py
│   ├── matcher.py
│   └── ranker.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── sample_data/
```