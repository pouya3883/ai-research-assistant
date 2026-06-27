from app.models.retrieval import RetrievalResult
from app.services.embedding_service import semantic_search_document


def retrieve_context(document_id: str, question: str) -> RetrievalResult:
    results = semantic_search_document(document_id=document_id, query=question)

    contexts = [result["content"] for result in results]

    sources = [result["chunk_filename"] for result in results]

    return RetrievalResult(contexts=contexts, sources=sources)
