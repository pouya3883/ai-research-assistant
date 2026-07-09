from app.models.embedding import DocumentEmbedding
from sentence_transformers import SentenceTransformer
from app.services.chunk_service import get_document_chunks
from app.services.vector_store import add_embedding, get_document_embeddings
from sentence_transformers import util
from app.models.search import SearchResult

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(
    document_id: str, chunk_filename: str, content: str
) -> DocumentEmbedding:
    embedding_vector = embedding_model.encode(content).tolist()

    return DocumentEmbedding(
        document_id=document_id,
        chunk_filename=chunk_filename,
        embedding=embedding_vector,
    )


def generate_document_embeddings(document_id: str):
    chunks = get_document_chunks(document_id)

    for chunk in chunks:
        embedding = create_embedding(
            document_id=document_id,
            chunk_filename=chunk.filename,
            content=chunk.content,
        )

        add_embedding(embedding)


def create_query_embedding(query: str) -> list[float]:
    return embedding_model.encode(query).tolist()


def calculate_similarity(
    query_embedding: list[float], chunk_embedding: list[float]
) -> float:
    similarity = util.cos_sim(query_embedding, chunk_embedding)

    return similarity.item()


def semantic_search_document(document_id, query, limit: int = 5):
    results = []
    query_embedding = create_query_embedding(query)
    document_embeddings = get_document_embeddings(document_id)
    chunks = get_document_chunks(document_id)

    chunk_map = {chunk.filename: chunk for chunk in chunks}

    for embedding in document_embeddings:
        score = calculate_similarity(query_embedding, embedding["embedding"])

        chunk = chunk_map[embedding["chunk_filename"]]

        results.append(
            SearchResult(
                document_id=chunk.document_id,
                filename=chunk.filename,
                chunk_index=chunk.chunk_index,
                total_chunks=chunk.total_chunks,
                content=chunk.content,
                score=score,
            )
        )

    results.sort(key=lambda result: result.score, reverse=True)

    return results[:limit]
