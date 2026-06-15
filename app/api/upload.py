from fastapi import APIRouter, UploadFile
from pathlib import Path
from fastapi import HTTPException
from app.services.pdf_service import extract_text
from app.services.text_chunker import chunk_text

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    text = extract_text(str(file_path))

    chunks = chunk_text(text)

    chunks_dir = Path("data/chunks")
    chunks_dir.mkdir(parents=True, exist_ok=True)

    for index, chunk in enumerate(chunks):
        chunk_file = chunks_dir / f"{file_path.stem}_chunk_{index}.txt"

        with open(chunk_file, "w", encoding="utf-8") as f:
            f.write(chunk)

    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    text_file = processed_dir / f"{file_path.stem}.txt"

    with open(text_file, "w", encoding="utf-8") as f:
        f.write(text)

    return {
        "filename": file.filename,
        "characters": len(text),
        "chunks": len(chunks),
    }
