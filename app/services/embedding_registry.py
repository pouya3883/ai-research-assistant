from pathlib import Path
import json

EMBEDDINGS_FILE = Path("data/metadata/embeddings.json")


def load_embeddings():
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_embeddings(embeddings):
    with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(embeddings, f, indent=4)
