from app.models.retrieval import RetrievalResult, RetrievedChunk
from app.services.hybrid_search_service import hybrid_search_context


def retrieve_context(document_id: str, question: str) -> RetrievalResult:
    context_chunks = hybrid_search_context(document_id=document_id, query=question)

    retrieved_chunks = [
        RetrievedChunk(content=chunk.content, source=chunk.filename)
        for chunk in context_chunks
    ]

    return RetrievalResult(results=retrieved_chunks)
