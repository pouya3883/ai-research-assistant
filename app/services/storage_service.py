from pathlib import Path

UPLOADS_DIR = Path("data/uploads")
PROCESSED_DIR = Path("data/processed")


def delete_files(directory: Path, document_id: str) -> None:
    for file in directory.glob("*"):
        if file.name.startswith(document_id):
            file.unlink()
