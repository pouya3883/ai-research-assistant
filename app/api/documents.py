from fastapi import APIRouter
from app.services.document_registry import load_documents, get_document
from fastapi import HTTPException

router = APIRouter()


@router.get("/documents")
def get_documents():
    return load_documents()


@router.get("/documents/{document_id}")
def get_document_by_id(document_id: str):
    document = get_document(document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return document
