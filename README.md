# AI-Based Candidate Ranking System Using NLP

## Overview

The AI-Based Candidate Ranking System is an NLP-driven recruitment assistance system designed to automate resume screening and candidate evaluation. The system analyzes candidate resumes, compares them with job descriptions, and generates candidate rankings based on semantic similarity and skill matching.

The project combines Natural Language Processing (NLP), TF-IDF vectorization, and Sentence-BERT semantic similarity techniques to improve candidate-job matching accuracy and reduce manual recruitment effort.

---

## Features

* Resume parsing and text extraction
* Job description analysis
* NLP preprocessing pipeline
* TF-IDF based keyword matching
* Sentence-BERT semantic similarity analysis
* Candidate scoring and ranking
* Skill matching and missing skill detection
* Automated recruiter assistance system

---

## System Workflow

1. Recruiter uploads the job description.
2. Candidate resumes are uploaded into the system.
3. Resume text is extracted and preprocessed.
4. TF-IDF and Sentence-BERT embeddings are generated.
5. Similarity between resumes and job description is calculated.
6. Candidates are ranked based on relevance scores.
7. Final ranked results are displayed to the recruiter.

---

## Technologies Used

| Category             | Technologies                           |
| -------------------- | -------------------------------------- |
| Programming Language | Python                                 |
| NLP Techniques       | Tokenization, TF-IDF, Stopword Removal |
| AI/ML Model          | Sentence-BERT (all-MiniLM-L6-v2)       |
| Similarity Methods   | Cosine Similarity                      |
| NLP Libraries        | NLTK, Scikit-learn                     |
| Transformer Library  | Sentence-Transformers                  |
| Resume Parsing       | PyPDF2, python-docx                    |
| Backend Framework    | FastAPI                                |
| Development Tools    | VS Code, GitHub                        |

---


---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/candidate-ranking-system.git
cd candidate-ranking-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Project

```bash
uvicorn app:app --reload
```

---

## Prototype Demonstration

The prototype demonstrates:

* Resume parsing
* NLP preprocessing
* Semantic similarity analysis
* Candidate ranking
* Skill matching and missing skill identification

---

## Future Scope

* Integration with real-world recruitment datasets
* Fine-tuned transformer models
* Bias reduction mechanisms
* Multi-language resume analysis
* ATS platform integration

---

## Conclusion

The proposed system automates resume screening and candidate ranking using NLP and semantic similarity techniques. It assists recruiters in identifying suitable candidates efficiently while reducing manual effort in the hiring process.

---

## Contributors

* Akshat Gairola,Saurabh Kaintura,Shubham Bhatt

---

