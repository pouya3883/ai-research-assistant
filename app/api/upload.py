from fastapi import APIRouter, UploadFile
from pathlib import Path
from fastapi import HTTPException
from app.services.pdf_service import extract_text
from app.services.text_chunker import chunk_text
import uuid
from app.services.document_registry import load_documents, save_documents

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    document_id = str(uuid.uuid4())

    stored_filename = f"{document_id}_{file.filename}"
    file_path = upload_dir / stored_filename

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

    documents = load_documents()

    documents.append(
        {
            "document_id": document_id,
            "filename": file.filename,
            "characters": len(text),
            "chunks": len(chunks),
        }
    )

    save_documents(documents)

    return {
        "document_id": document_id,
        "filename": file.filename,
        "characters": len(text),
        "chunks": len(chunks),
    }
