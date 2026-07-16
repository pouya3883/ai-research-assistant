import pytest

from app.models.chunk import DocumentChunk


@pytest.fixture
def sample_chunks() -> list[DocumentChunk]:
    return [
        DocumentChunk(
            document_id="doc-1",
            filename="test.pdf",
            chunk_index=0,
            total_chunks=3,
            content="Linux uses the GRUB bootloader.",
        ),
        DocumentChunk(
            document_id="doc-1",
            filename="test.pdf",
            chunk_index=1,
            total_chunks=3,
            content="Python is a programming language.",
        ),
        DocumentChunk(
            document_id="doc-1",
            filename="test.pdf",
            chunk_index=2,
            total_chunks=3,
            content="Network interfaces are configured using ip.",
        ),
    ]
