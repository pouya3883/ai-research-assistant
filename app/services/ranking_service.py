from app.models.hybrid_search import HybridSearchResult


def normalize_by_max(scores: list[float]) -> list[float]:
    max_score = max(scores)

    if max_score == 0:
        return scores

    return [score / max_score for score in scores]


def normalize_scores(results: list[HybridSearchResult]) -> list[HybridSearchResult]:
    semantic_scores = [result.semantic_score for result in results]
    bm25_scores = [result.bm25_score for result in results]

    normalized_semantic = normalize_by_max(semantic_scores)
    normalized_bm25 = normalize_by_max(bm25_scores)

    for index, result in enumerate(results):
        result.normalized_semantic_score = normalized_semantic[index]
        result.normalized_bm25_score = normalized_bm25[index]

    return results


def rank_results(results: list[HybridSearchResult]) -> list[HybridSearchResult]:
    SEMANTIC_WEIGHT = 0.7
    BM25_WEIGHT = 0.3

    for result in results:
        result.hybrid_score = (
            result.normalized_semantic_score * SEMANTIC_WEIGHT
            + result.normalized_bm25_score * BM25_WEIGHT
        )

    results.sort(key=lambda result: result.hybrid_score, reverse=True)

    return results
