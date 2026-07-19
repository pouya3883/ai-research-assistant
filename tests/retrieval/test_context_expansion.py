from unittest.mock import patch

from app.models.chunk import DocumentChunk
from app.services.chunk_service import get_context_chunks


def test_get_context_chunks_returns_neighbors(
    sample_chunks: list[DocumentChunk],
) -> None:
    with patch(
        "app.services.chunk_service.get_document_chunks", return_value=sample_chunks
    ):
        chunks = get_context_chunks(document_id="doc-1", chunk_index=1, window=1)

    assert len(chunks) == 3
    assert [chunk.chunk_index for chunk in chunks] == [0, 1, 2]


def test_get_context_chunks_handles_first_chunk(
    sample_chunks: list[DocumentChunk],
) -> None:
    with patch(
        "app.services.chunk_service.get_document_chunks", return_value=sample_chunks
    ):
        chunks = get_context_chunks(document_id="doc-1", chunk_index=0, window=1)

    assert [chunk.chunk_index for chunk in chunks] == [0, 1]


def test_get_context_chunks_handles_last_chunk(
    sample_chunks: list[DocumentChunk],
) -> None:
    with patch(
        "app.services.chunk_service.get_document_chunks", return_value=sample_chunks
    ):
        chunks = get_context_chunks(document_id="doc-1", chunk_index=2, window=1)

    assert [chunk.chunk_index for chunk in chunks] == [1, 2]


def test_get_context_chunks_returns_empty_for_negative_index(
    sample_chunks: list[DocumentChunk],
) -> None:
    with patch(
        "app.services.chunk_service.get_document_chunks", return_value=sample_chunks
    ):
        chunks = get_context_chunks(document_id="doc-1", chunk_index=-1)

    assert chunks == []


def test_get_context_chunks_returns_empty_for_invalid_index(
    sample_chunks: list[DocumentChunk],
) -> None:
    with patch(
        "app.services.chunk_service.get_document_chunks", return_value=sample_chunks
    ):
        chunks = get_context_chunks(document_id="doc-1", chunk_index=10)

    assert chunks == []


def test_get_context_chunks_large_window_returns_all_chunks(
    sample_chunks: list[DocumentChunk],
) -> None:
    with patch(
        "app.services.chunk_service.get_document_chunks", return_value=sample_chunks
    ):
        chunks = get_context_chunks(document_id="doc-1", chunk_index=1, window=10)

    assert len(chunks) == len(sample_chunks)
