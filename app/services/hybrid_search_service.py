from app.models.hybrid_search import HybridSearchResult
from app.models.chunk import DocumentChunk
from app.services.embedding_service import semantic_search_document
from app.services.chunk_service import (
    get_document_chunks,
    expand_context_chunks,
    limit_context_chunks,
)
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
            document_id=result.document_id,
            filename=result.filename,
            chunk_index=result.chunk_index,
            total_chunks=result.total_chunks,
            content=result.content,
            semantic_score=result.score,
        )

    for result in bm25_results:
        if result.filename in results_by_filename:
            results_by_filename[result.filename].bm25_score = result.score
        else:
            results_by_filename[result.filename] = HybridSearchResult(
                document_id=result.document_id,
                filename=result.filename,
                chunk_index=result.chunk_index,
                total_chunks=result.total_chunks,
                content=result.content,
                bm25_score=result.score,
            )

    results = list(results_by_filename.values())

    results = normalize_scores(results)
    results = rank_results(results)

    return results[:limit]


def hybrid_search_context(
    document_id: str,
    query: str,
    limit: int = 5,
    window: int = 1,
    max_context_chunks: int = 15,
) -> list[DocumentChunk]:
    """
    Return context-expanded chunks around the highest-ranked retrieval results.
    """
    results = hybrid_search_document(document_id=document_id, query=query, limit=limit)

    expanded_chunks = expand_context_chunks(results=results, window=window)

    return limit_context_chunks(chunks=expanded_chunks, max_chunks=max_context_chunks)
