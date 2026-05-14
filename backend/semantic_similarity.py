from sentence_transformers import SentenceTransformer, util

# Load model lazily — only when first called
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def semantic_similarity(text1, text2):
    model = get_model()
    emb = model.encode([text1, text2], convert_to_tensor=True)
    score = util.cos_sim(emb[0], emb[1])
    return score.item()