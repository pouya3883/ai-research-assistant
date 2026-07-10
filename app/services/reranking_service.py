from sentence_transformers import CrossEncoder
from app.models.hybrid_search import HybridSearchResult

reranking_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank_results(
    query: str, results: list[HybridSearchResult]
) -> list[HybridSearchResult]:
    """
    Score each search result against the query using a CrossEncoder
    and return the results sorted by rerank score.
    """
    pairs = [(query, result.content) for result in results]

    scores = reranking_model.predict(pairs)

    for result, score in zip(results, scores):
        result.rerank_score = float(score)

    results.sort(key=lambda result: result.rerank_score, reverse=True)

    return results
