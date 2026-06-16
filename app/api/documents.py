from fastapi import APIRouter
from app.services.document_registry import load_documents, get_document, delete_document
from fastapi import HTTPException
from app.services.chunk_service import get_document_chunks

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


@router.get("/documents/{document_id}/chunks")
def get_chunks(document_id: str):
    document = get_document(document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return get_document_chunks(document_id)


@router.delete("/documents/{document_id}")
def remove_document(document_id: str):
    deleted = delete_document(document_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": "Document deleted"}
