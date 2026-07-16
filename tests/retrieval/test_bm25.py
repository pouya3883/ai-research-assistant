from app.models.chunk import DocumentChunk
from app.services.bm25_service import bm25_search


def test_bm25_returns_relevant_chunk(sample_chunks: list[DocumentChunk]) -> None:
    results = bm25_search(chunks=sample_chunks, query="grub")

    assert results
    assert results[0].chunk_index == 0


def test_bm25_respects_limit(sample_chunks: list[DocumentChunk]) -> None:
    results = bm25_search(chunks=sample_chunks, query="linux", limit=2)

    assert len(results) == 2


def test_bm25_returns_results_sorted_by_score(
    sample_chunks: list[DocumentChunk],
) -> None:
    results = bm25_search(chunks=sample_chunks, query="python")

    scores = [result.score for result in results]

    assert scores == sorted(scores, reverse=True)


def test_bm25_handles_unrelated_query(sample_chunks: list[DocumentChunk]) -> None:
    results = bm25_search(chunks=sample_chunks, query="quantum-entanglement")

    assert len(results) == len(sample_chunks)
    assert all(result.score == 0 for result in results)
