def calculate_final_score(
    semantic_score: float,
    tfidf_score: float,
    keyword_score: float
) -> float:
    """
    Weighted combination of all three scores.
    Semantic carries most weight — most meaningful for NLP matching.
    """
    return round(
        (0.5 * semantic_score) +
        (0.3 * tfidf_score) +
        (0.2 * keyword_score),
        3
    )


def rank_candidates(candidates: list[dict]) -> list[dict]:
    """
    Takes a list of scored candidates and returns
    them sorted by final score with rank assigned.

    Each candidate dict must have:
        - filename        (str)
        - semantic_score  (float)
        - tfidf_score     (float)
        - keyword_score   (float)
    """

    for candidate in candidates:
        candidate["final_score"] = calculate_final_score(
            candidate["semantic_score"],
            candidate["tfidf_score"],
            candidate["keyword_score"]
        )

    # Sort highest to lowest
    candidates.sort(key=lambda x: x["final_score"], reverse=True)

    # Assign rank
    for i, candidate in enumerate(candidates, start=1):
        candidate["rank"] = i

    return candidates


def get_verdict(score: float) -> str:
    """
    Returns a human-readable verdict based on final score.
    No LLM needed — rule based.
    """
    if score >= 0.75:
        return "Strong Match — Recommended for Interview"
    elif score >= 0.55:
        return "Good Match — Consider for Interview"
    elif score >= 0.35:
        return "Weak Match — Skill Gaps Present"
    else:
        return "Poor Match — Does Not Meet Requirements"