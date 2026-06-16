from pathlib import Path

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


def search_chunks(query: str, limit: int = 5):
    results = []

    for file in CHUNKS_DIR.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        if query.lower() in content.lower():
            results.append({"filename": file.name, "content": content})

    return results[:limit]
