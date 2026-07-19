import pytest

from app.models.chunk import DocumentChunk
from app.models.hybrid_search import HybridSearchResult


@pytest.fixture
def sample_chunks() -> list[DocumentChunk]:
    return [
        DocumentChunk(
            document_id="doc-1",
            filename="chunk-0",
            chunk_index=0,
            total_chunks=3,
            content="Linux uses the GRUB bootloader.",
        ),
        DocumentChunk(
            document_id="doc-1",
            filename="chunk-1",
            chunk_index=1,
            total_chunks=3,
            content="Python is a programming language.",
        ),
        DocumentChunk(
            document_id="doc-1",
            filename="chunk-2",
            chunk_index=2,
            total_chunks=3,
            content="Network interfaces are configured using ip.",
        ),
    ]


@pytest.fixture
def sample_hybrid_results() -> list[HybridSearchResult]:
    return [
        HybridSearchResult(
            document_id="doc-1",
            filename="chunk-0",
            chunk_index=0,
            total_chunks=3,
            content="Linux uses the GRUB bootloader.",
            semantic_score=0.91,
            bm25_score=0.52,
            hybrid_score=0.79,
        ),
        HybridSearchResult(
            document_id="doc-1",
            filename="chunk-1",
            chunk_index=1,
            total_chunks=3,
            content="Python is a programming language.",
            semantic_score=0.80,
            bm25_score=0.90,
            hybrid_score=0.84,
        ),
        HybridSearchResult(
            document_id="doc-1",
            filename="chunk-2",
            chunk_index=2,
            total_chunks=3,
            content="Network interfaces are configured using ip.",
            semantic_score=0.75,
            bm25_score=0.60,
            hybrid_score=0.71,
        ),
    ]
