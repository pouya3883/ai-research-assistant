from pathlib import Path
from app.models.search import SearchResult

CHUNKS_DIR = Path("data/chunks")


def get_chunk_number(file_path):
    return int(file_path.stem.split("_chunk_")[-1])


def get_document_chunks(document_id: str):
    chunks = []

    files = sorted(
        CHUNKS_DIR.glob(f"{document_id}_*_chunk_*.txt"), key=get_chunk_number
    )

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            chunks.append({"filename": file.name, "content": f.read()})

    return chunks


def count_matches(content: str, query: str):
    return content.lower().count(query.lower())


def search_chunks(query: str, limit: int = 5):
    results = []

    for file in CHUNKS_DIR.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        if query.lower() in content.lower():
            results.append(
                SearchResult(
                    filename=file.name,
                    content=content,
                    score=count_matches(content, query),
                )
            )

    results.sort(key=lambda result: result.score, reverse=True)

    return results[:limit]


def search_document_chunks(document_id: str, query: str, limit: int = 5):
    results = []
    chunks = get_document_chunks(document_id)

    for chunk in chunks:
        if query.lower() in chunk["content"].lower():
            results.append(
                SearchResult(
                    filename=chunk["filename"],
                    content=chunk["content"],
                    score=count_matches(chunk["content"], query),
                )
            )

    results.sort(key=lambda result: result.score, reverse=True)

    return results[:limit]


def delete_document_chunks(document_id: str) -> None:
    for file in CHUNKS_DIR.glob("*.txt"):
        if file.name.startswith(document_id):
            file.unlink()
