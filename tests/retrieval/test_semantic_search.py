from unittest.mock import patch

from app.models.chunk import DocumentChunk
from app.services.embedding_service import semantic_search_document


def test_semantic_search_returns_most_relevant_chunk(
    sample_chunks: list[DocumentChunk],
) -> None:
    with (
        patch(
            "app.services.embedding_service.create_query_embedding",
            return_value=[0.1, 0.2],
        ),
        patch(
            "app.services.embedding_service.get_document_embeddings",
            return_value=[
                {"chunk_filename": "chunk-0", "embedding": [1]},
                {"chunk_filename": "chunk-1", "embedding": [2]},
                {"chunk_filename": "chunk-2", "embedding": [3]},
            ],
        ),
        patch(
            "app.services.embedding_service.get_document_chunks",
            return_value=sample_chunks,
        ),
        patch(
            "app.services.embedding_service.calculate_similarity",
            side_effect=[0.30, 0.95, 0.60],
        ),
    ):
        results = semantic_search_document(document_id="doc-1", query="python")

    assert results
    assert results[0].chunk_index == 1


def test_semantic_search_returns_results_sorted_by_score(
    sample_chunks: list[DocumentChunk],
) -> None:
    with (
        patch(
            "app.services.embedding_service.create_query_embedding",
            return_value=[0.1, 0.2],
        ),
        patch(
            "app.services.embedding_service.get_document_embeddings",
            return_value=[
                {"chunk_filename": "chunk-0", "embedding": [1]},
                {"chunk_filename": "chunk-1", "embedding": [2]},
                {"chunk_filename": "chunk-2", "embedding": [3]},
            ],
        ),
        patch(
            "app.services.embedding_service.get_document_chunks",
            return_value=sample_chunks,
        ),
        patch(
            "app.services.embedding_service.calculate_similarity",
            side_effect=[0.30, 0.95, 0.60],
        ),
    ):
        results = semantic_search_document(document_id="doc-1", query="python")

    scores = [result.score for result in results]

    assert scores == sorted(scores, reverse=True)


def test_semantic_search_respects_limit(sample_chunks: list[DocumentChunk]) -> None:
    with (
        patch(
            "app.services.embedding_service.create_query_embedding",
            return_value=[0.1, 0.2],
        ),
        patch(
            "app.services.embedding_service.get_document_embeddings",
            return_value=[
                {"chunk_filename": "chunk-0", "embedding": [1]},
                {"chunk_filename": "chunk-1", "embedding": [2]},
                {"chunk_filename": "chunk-2", "embedding": [3]},
            ],
        ),
        patch(
            "app.services.embedding_service.get_document_chunks",
            return_value=sample_chunks,
        ),
        patch(
            "app.services.embedding_service.calculate_similarity",
            side_effect=[0.30, 0.95, 0.60],
        ),
    ):
        results = semantic_search_document(document_id="doc-1", query="python", limit=2)

    assert len(results) == 2


def test_semantic_search_returns_empty_when_no_embeddings(
    sample_chunks: list[DocumentChunk],
) -> None:
    with (
        patch(
            "app.services.embedding_service.create_query_embedding",
            return_value=[0.1, 0.2],
        ),
        patch(
            "app.services.embedding_service.get_document_embeddings",
            return_value=[],
        ),
        patch(
            "app.services.embedding_service.get_document_chunks",
            return_value=sample_chunks,
        ),
    ):
        results = semantic_search_document(document_id="doc-1", query="python")

    assert results == []


def test_semantic_search_returns_all_results_when_exceeds_result_count(
    sample_chunks: list[DocumentChunk],
) -> None:
    with (
        patch(
            "app.services.embedding_service.create_query_embedding",
            return_value=[0.1, 0.2],
        ),
        patch(
            "app.services.embedding_service.get_document_embeddings",
            return_value=[
                {"chunk_filename": "chunk-0", "embedding": [1]},
                {"chunk_filename": "chunk-1", "embedding": [2]},
                {"chunk_filename": "chunk-2", "embedding": [3]},
            ],
        ),
        patch(
            "app.services.embedding_service.get_document_chunks",
            return_value=sample_chunks,
        ),
        patch(
            "app.services.embedding_service.calculate_similarity",
            side_effect=[0.30, 0.95, 0.60],
        ),
    ):
        results = semantic_search_document(
            document_id="doc-1", query="python", limit=10
        )

    assert len(results) == 3
