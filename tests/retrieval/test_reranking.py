from unittest.mock import MagicMock, patch

from app.models.hybrid_search import HybridSearchResult
import app.services.reranking_service as reranking_service


def test_reranking_returns_results_sorted_by_rerank_score(
    sample_hybrid_results: list[HybridSearchResult],
) -> None:
    mock_model = MagicMock()
    mock_model.predict.return_value = [0.30, 0.95, 0.60]

    with patch(
        "app.services.reranking_service.get_reranking_model",
        return_value=mock_model,
    ):
        results = reranking_service.rerank_results(
            query="python", results=sample_hybrid_results
        )

    scores = [result.rerank_score for result in results]

    assert scores == sorted(scores, reverse=True)
    assert results[0].chunk_index == 1


def test_reranking_assigns_rerank_scores(
    sample_hybrid_results: list[HybridSearchResult],
) -> None:
    mock_model = MagicMock()
    mock_model.predict.return_value = [0.10, 0.20, 0.30]

    with patch(
        "app.services.reranking_service.get_reranking_model",
        return_value=mock_model,
    ):
        results = reranking_service.rerank_results(
            query="python", results=sample_hybrid_results
        )

    assert results[0].rerank_score == 0.30
    assert results[1].rerank_score == 0.20
    assert results[2].rerank_score == 0.10


def test_reranking_preserves_number_of_results(
    sample_hybrid_results: list[HybridSearchResult],
) -> None:
    mock_model = MagicMock()
    mock_model.predict.return_value = [0.30, 0.95, 0.60]

    with patch(
        "app.services.reranking_service.get_reranking_model",
        return_value=mock_model,
    ):
        results = reranking_service.rerank_results(
            query="python", results=sample_hybrid_results
        )

    assert len(results) == len(sample_hybrid_results)


def test_reranking_handles_empty_results() -> None:
    mock_model = MagicMock()
    mock_model.predict.return_value = []

    with patch(
        "app.services.reranking_service.get_reranking_model", return_value=mock_model
    ):
        results = reranking_service.rerank_results(query="python", results=[])

    assert results == []


def test_reranking_builds_query_content_pairs(
    sample_hybrid_results: list[HybridSearchResult],
) -> None:
    mock_model = MagicMock()
    mock_model.predict.return_value = [0.30, 0.95, 0.60]

    with patch(
        "app.services.reranking_service.get_reranking_model",
        return_value=mock_model,
    ):
        reranking_service.rerank_results(query="python", results=sample_hybrid_results)

    mock_model.predict.assert_called_once_with(
        [
            ("python", "Linux uses the GRUB bootloader."),
            ("python", "Python is a programming language."),
            ("python", "Network interfaces are configured using ip."),
        ]
    )


def test_get_reranking_model_loads_model_only_once() -> None:
    reranking_service.reranking_model = None

    with patch("app.services.reranking_service.CrossEncoder") as mock_cross_encoder:
        mock_model = MagicMock()
        mock_cross_encoder.return_value = mock_model

        model1 = reranking_service.get_reranking_model()
        model2 = reranking_service.get_reranking_model()

    assert model1 is model2
    mock_cross_encoder.assert_called_once_with("cross-encoder/ms-marco-MiniLM-L-6-v2")
