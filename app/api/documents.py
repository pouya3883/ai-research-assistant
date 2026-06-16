from fastapi import APIRouter
from app.services.document_registry import load_documents

router = APIRouter()


@router.get("/documents")
def get_documents():
    return load_documents()
