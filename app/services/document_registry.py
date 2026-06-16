import json
from pathlib import Path

REGISTRY_FILE = Path("data/metadata/documents.json")


def load_documents():
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_documents(documents):
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=4)


def get_document(document_id: str):
    documents = load_documents()

    for document in documents:
        if document["document_id"] == document_id:
            return document

    return None
