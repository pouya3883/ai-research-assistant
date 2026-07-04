from app.models.hybrid_search import HybridSearchResult
from app.services.embedding_service import semantic_search_document
from app.services.chunk_service import get_document_chunks
from app.services.bm25_service import bm25_search
from app.services.ranking_service import normalize_scores, rank_results


def hybrid_search_document(
    document_id: str, query: str, limit: int = 5
) -> list[HybridSearchResult]:
    semantic_results = semantic_search_document(
        document_id=document_id, query=query, limit=limit
    )

    chunks = get_document_chunks(document_id)

    bm25_results = bm25_search(chunks=chunks, query=query, limit=limit)

    results_by_filename: dict[str, HybridSearchResult] = {}

    for result in semantic_results:
        results_by_filename[result.filename] = HybridSearchResult(
            filename=result.filename,
            content=result.content,
            semantic_score=result.score,
        )

    for result in bm25_results:
        if result.filename in results_by_filename:
            results_by_filename[result.filename].keyword_score = result.score
        else:
            results_by_filename[result.filename] = HybridSearchResult(
                filename=result.filename,
                content=result.content,
                keyword_score=result.score,
            )

    results = list(results_by_filename.values())

    results = normalize_scores(results)
    results = rank_results(results)

    return results[:limit]
