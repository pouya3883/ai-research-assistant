from unittest.mock import patch

from app.models.hybrid_search import HybridSearchResult
from app.models.search import SearchResult
from app.services.hybrid_search_service import hybrid_search_document


def test_hybrid_search_returns_ranked_results() -> None:
    semantic_results = [
        SearchResult(
            document_id="doc-1",
            filename="chunk-0",
            chunk_index=0,
            total_chunks=3,
            content="python",
            score=0.90,
        )
    ]

    bm25_results = [
        SearchResult(
            document_id="doc-1",
            filename="chunk-0",
            chunk_index=0,
            total_chunks=3,
            content="python",
            score=7.5,
        )
    ]

    hybrid_results = [
        HybridSearchResult(
            document_id="doc-1",
            filename="chunk-0",
            chunk_index=0,
            total_chunks=3,
            content="python",
            semantic_score=0.90,
            bm25_score=7.5,
            hybrid_score=0.95,
        )
    ]

    with (
        patch(
            "app.services.hybrid_search_service.semantic_search_document",
            return_value=semantic_results,
        ),
        patch(
            "app.services.hybrid_search_service.get_document_chunks", return_value=[]
        ),
        patch(
            "app.services.hybrid_search_service.bm25_search", return_value=bm25_results
        ),
        patch(
            "app.services.hybrid_search_service.normalize_scores",
            return_value=hybrid_results,
        ),
        patch(
            "app.services.hybrid_search_service.rank_results",
            return_value=hybrid_results,
        ),
        patch(
            "app.services.hybrid_search_service.rerank_results",
            return_value=hybrid_results,
        ),
    ):
        results = hybrid_search_document(document_id="doc-1", query="python")

    assert len(results) == 1
    assert results[0].filename == "chunk-0"


def test_hybrid_search_calls_pipeline_services() -> None:
    semantic_results = [
        SearchResult(
            document_id="doc-1",
            filename="chunk-0",
            chunk_index=0,
            total_chunks=3,
            content="python",
            score=0.90,
        )
    ]

    bm25_results = [
        SearchResult(
            document_id="doc-1",
            filename="chunk-0",
            chunk_index=0,
            total_chunks=3,
            content="python",
            score=7.5,
        )
    ]

    hybrid_results = [
        HybridSearchResult(
            document_id="doc-1",
            filename="chunk-0",
            chunk_index=0,
            total_chunks=3,
            content="python",
            semantic_score=0.90,
            bm25_score=7.5,
            hybrid_score=0.95,
        )
    ]

    with (
        patch(
            "app.services.hybrid_search_service.semantic_search_document",
            return_value=semantic_results,
        ) as mock_semantic,
        patch(
            "app.services.hybrid_search_service.get_document_chunks", return_value=[]
        ) as mock_chunks,
        patch(
            "app.services.hybrid_search_service.bm25_search", return_value=bm25_results
        ) as mock_bm25,
        patch(
            "app.services.hybrid_search_service.normalize_scores",
            return_value=hybrid_results,
        ) as mock_normalize,
        patch(
            "app.services.hybrid_search_service.rank_results",
            return_value=hybrid_results,
        ) as mock_rank,
        patch(
            "app.services.hybrid_search_service.rerank_results",
            return_value=hybrid_results,
        ) as mock_rerank,
    ):
        hybrid_search_document(document_id="doc-1", query="python")

    mock_semantic.assert_called_once_with(document_id="doc-1", query="python", limit=5)

    mock_chunks.assert_called_once_with("doc-1")

    mock_bm25.assert_called_once_with(chunks=[], query="python", limit=5)

    mock_normalize.assert_called_once()

    normalize_input = mock_normalize.call_args.args[0]

    assert len(normalize_input) == 1

    assert normalize_input[0].semantic_score == 0.90
    assert normalize_input[0].bm25_score == 7.5

    mock_rank.assert_called_once_with(hybrid_results)

    mock_rerank.assert_called_once_with(query="python", results=hybrid_results)


def test_hybrid_search_merges_results_from_both_retrievers() -> None:
    semantic_results = [
        SearchResult(
            document_id="doc-1",
            filename="chunk-0",
            chunk_index=0,
            total_chunks=3,
            content="linux",
            score=0.90,
        )
    ]

    bm25_results = [
        SearchResult(
            document_id="doc-1",
            filename="chunk-1",
            chunk_index=1,
            total_chunks=3,
            content="python",
            score=8.0,
        )
    ]

    with (
        patch(
            "app.services.hybrid_search_service.semantic_search_document",
            return_value=semantic_results,
        ),
        patch(
            "app.services.hybrid_search_service.get_document_chunks", return_value=[]
        ),
        patch(
            "app.services.hybrid_search_service.bm25_search", return_value=bm25_results
        ),
        patch(
            "app.services.hybrid_search_service.normalize_scores",
            side_effect=lambda results: results,
        ),
        patch(
            "app.services.hybrid_search_service.rank_results",
            side_effect=lambda results: results,
        ),
        patch(
            "app.services.hybrid_search_service.rerank_results",
            side_effect=lambda query, results: results,
        ),
    ):
        results = hybrid_search_document(document_id="doc-1", query="python")

    assert len(results) == 2

    filenames = {result.filename for result in results}

    assert filenames == {"chunk-0", "chunk-1"}


def test_hybrid_search_does_not_duplicate_same_chunk() -> None:
    semantic_results = [
        SearchResult(
            document_id="doc-1",
            filename="chunk-0",
            chunk_index=0,
            total_chunks=3,
            content="python",
            score=0.90,
        )
    ]

    bm25_results = [
        SearchResult(
            document_id="doc-1",
            filename="chunk-0",
            chunk_index=0,
            total_chunks=3,
            content="python",
            score=7.5,
        )
    ]

    with (
        patch(
            "app.services.hybrid_search_service.semantic_search_document",
            return_value=semantic_results,
        ),
        patch(
            "app.services.hybrid_search_service.get_document_chunks", return_value=[]
        ),
        patch(
            "app.services.hybrid_search_service.bm25_search", return_value=bm25_results
        ),
        patch(
            "app.services.hybrid_search_service.normalize_scores",
            side_effect=lambda results: results,
        ),
        patch(
            "app.services.hybrid_search_service.rank_results",
            side_effect=lambda results: results,
        ),
        patch(
            "app.services.hybrid_search_service.rerank_results",
            side_effect=lambda query, results: results,
        ),
    ):
        results = hybrid_search_document(document_id="doc-1", query="python")

    assert len(results) == 1

    assert results[0].filename == "chunk-0"
    assert results[0].semantic_score == 0.90
    assert results[0].bm25_score == 7.5
