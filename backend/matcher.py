#✅ <-- put TF-IDF + Cosine code here

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume_to_jd(resumesform,job_description):
    """
   resumes: list of resume texts [str, str, ...]
    job_description: string
    returns: list of (resume_index, similarity_score)
    
    """
    
    
    documents = [resumesform, job_description]
 #Combines resumes + JD
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # last vector = JD, rest = resumes
    jd_vector = tfidf_matrix[-1]
    resume_vectors = tfidf_matrix[:-1]
    
    scores = cosine_similarity(resume_vectors, jd_vector)
    results = [(i, float(score[0])) for i, score in enumerate(scores)]
    results.sort(key=lambda x: x[1], reverse=True)  # rank by similarity
    return results