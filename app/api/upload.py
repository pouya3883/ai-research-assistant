from fastapi import APIRouter, UploadFile
from pathlib import Path
from fastapi import HTTPException
from app.services.pdf_service import extract_text

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

    return {"filename": file.filename, "characters": len(text)}
