from fastapi import APIRouter
from app.services.document_registry import load_documents, get_document, delete_document
from fastapi import HTTPException
from app.services.chunk_service import get_document_chunks
from app.services.chunk_service import search_chunks, search_document_chunks
from app.services.embedding_service import semantic_search_document
from app.services.llm_service import answer_question

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


@router.get("/documents/{document_id}/search")
def search_document(document_id: str, query: str, limit: int = 5):
    document = get_document(document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return search_document_chunks(document_id, query, limit)


@router.delete("/documents/{document_id}")
def remove_document(document_id: str):
    deleted = delete_document(document_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": "Document deleted"}


@router.get("/documents/{document_id}/semantic-search")
def semantic_search(document_id: str, query: str, limit: int = 5):
    results = semantic_search_document(
        document_id=document_id, query=query, limit=limit
    )

    return results


@router.get("/search")
def search(query: str, limit: int = 5):
    return search_chunks(query, limit)


@router.get("/documents/{document_id}/ask")
def ask_question(document_id: str, question: str):
    answer = answer_question(document_id=document_id, question=question)

    return {"answer": answer}
