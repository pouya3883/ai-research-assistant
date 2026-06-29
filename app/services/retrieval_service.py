from app.models.retrieval import RetrievalResult, RetrievedChunk
from app.services.embedding_service import semantic_search_document


def retrieve_context(document_id: str, question: str) -> RetrievalResult:
    search_results = semantic_search_document(document_id=document_id, query=question)

    retrieved_chunk = [
        RetrievedChunk(content=result.content, source=result.filename)
        for result in search_results
    ]

    return RetrievalResult(results=retrieved_chunk)
