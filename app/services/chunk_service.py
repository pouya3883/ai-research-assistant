from pathlib import Path
from app.models.search import SearchResult
from app.models.chunk import DocumentChunk

CHUNKS_DIR = Path("data/chunks")


def get_chunk_number(file_path: Path) -> int:
    return int(file_path.stem.split("_chunk_")[-1])


def get_document_chunks(document_id: str) -> list[DocumentChunk]:
    chunks = []

    files = sorted(
        CHUNKS_DIR.glob(f"{document_id}_*_chunk_*.txt"), key=get_chunk_number
    )

    total_chunks = len(files)

    for chunk_index, file in enumerate(files):
        with open(file, "r", encoding="utf-8") as f:
            chunks.append(
                DocumentChunk(
                    document_id=document_id,
                    filename=file.name,
                    chunk_index=chunk_index,
                    total_chunks=total_chunks,
                    content=f.read(),
                )
            )

    return chunks


def get_context_chunks(
    document_id: str, chunk_index: int, window: int = 1
) -> list[DocumentChunk]:
    """
    Return the requested chunk together with its neighboring chunks.
    """
    chunks = get_document_chunks(document_id)

    if chunk_index < 0 or chunk_index >= len(chunks):
        return []

    start = max(0, chunk_index - window)
    end = min(len(chunks), chunk_index + window + 1)

    return chunks[start:end]


def expand_context_chunks(
    results: list[SearchResult], window: int = 1
) -> list[DocumentChunk]:
    expanded_chunks: dict[tuple[str, int], DocumentChunk] = {}

    for result in results:
        context_chunks = get_context_chunks(
            document_id=result.document_id,
            chunk_index=result.chunk_index,
            window=window,
        )

        for chunk in context_chunks:
            expanded_chunks[(chunk.document_id, chunk.chunk_index)] = chunk

    return list(expanded_chunks.values())


def limit_context_chunks(
    chunks: list[DocumentChunk], max_chunks: int
) -> list[DocumentChunk]:
    if len(chunks) <= max_chunks:
        return chunks

    return chunks[:max_chunks]


def count_matches(content: str, query: str) -> int:
    return content.lower().count(query.lower())


def search_document_chunks(
    document_id: str, query: str, limit: int = 5
) -> list[SearchResult]:
    results = []
    chunks = get_document_chunks(document_id)

    for chunk in chunks:
        if query.lower() in chunk.content.lower():
            results.append(
                SearchResult(
                    document_id=chunk.document_id,
                    filename=chunk.filename,
                    chunk_index=chunk.chunk_index,
                    total_chunks=chunk.total_chunks,
                    content=chunk.content,
                    score=count_matches(chunk.content, query),
                )
            )

    results.sort(key=lambda result: result.score, reverse=True)

    return results[:limit]


def delete_document_chunks(document_id: str) -> None:
    for file in CHUNKS_DIR.glob("*.txt"):
        if file.name.startswith(document_id):
            file.unlink()
