from pathlib import Path
import json

EMBEDDINGS_FILE = Path("data/metadata/embeddings.json")


def load_embeddings():
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_embeddings(embeddings):
    with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(embeddings, f, indent=4)


def add_embedding(embedding):
    embeddings = load_embeddings()

    for i in embeddings:
        if i["chunk_filename"] == embedding.chunk_filename:
            return

    embeddings.append(embedding.model_dump())

    save_embeddings(embeddings)


def get_document_embeddings(document_id: str):
    embeddings = load_embeddings()

    results = [
        embedding for embedding in embeddings if embedding["document_id"] == document_id
    ]

    return results
