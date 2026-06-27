import os
import json

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

EMBEDDINGS_FILE = Path("data/metadata/embeddings.json")
VECTOR_STORE_BACKEND = os.getenv("VECTOR_STORE_BACKEND", "json")


def load_embeddings() -> list[dict]:
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_embeddings(embeddings) -> None:
    with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(embeddings, f, indent=4)


def add_embedding(embedding) -> None:
    if VECTOR_STORE_BACKEND != "json":
        raise ValueError(f"Unsupported vector store backend: {VECTOR_STORE_BACKEND}")

    embeddings = load_embeddings()
    for i in embeddings:
        if i["chunk_filename"] == embedding.chunk_filename:
            return
    embeddings.append(embedding.model_dump())
    save_embeddings(embeddings)


def get_document_embeddings(document_id: str) -> list[dict]:
    if VECTOR_STORE_BACKEND != "json":
        raise ValueError(f"Unsupported vector store backend: {VECTOR_STORE_BACKEND}")

    embeddings = load_embeddings()
    results = [
        embedding for embedding in embeddings if embedding["document_id"] == document_id
    ]
    return results


def delete_document_embeddings(document_id: str) -> None:
    embeddings = load_embeddings()

    updated = [
        embedding for embedding in embeddings if embedding["document_id"] != document_id
    ]

    save_embeddings(updated)
