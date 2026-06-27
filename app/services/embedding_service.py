from app.models.embedding import DocumentEmbedding
from sentence_transformers import SentenceTransformer
from app.services.chunk_service import get_document_chunks
from app.services.vector_store import add_embedding, get_document_embeddings
from sentence_transformers import util

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(document_id: str, chunk_filename: str, content: str):
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
            chunk_filename=chunk["filename"],
            content=chunk["content"],
        )

        add_embedding(embedding)


def create_query_embedding(query: str):
    return embedding_model.encode(query).tolist()


def calculate_similarity(query_embedding, chunk_embedding):
    similarity = util.cos_sim(query_embedding, chunk_embedding)

    return similarity.item()


def semantic_search_document(document_id, query, limit: int = 5):
    results = []
    query_embedding = create_query_embedding(query)
    document_embeddings = get_document_embeddings(document_id)
    chunks = get_document_chunks(document_id)

    chunk_map = {chunk["filename"]: chunk["content"] for chunk in chunks}

    for embedding in document_embeddings:
        score = calculate_similarity(query_embedding, embedding["embedding"])

        results.append(
            {
                "chunk_filename": embedding["chunk_filename"],
                "content": chunk_map[embedding["chunk_filename"]],
                "score": score,
            }
        )

    results.sort(key=lambda result: result["score"], reverse=True)

    return results[:limit]


def build_context(document_id: str, query: str, limit: int = 3):
    results = semantic_search_document(
        document_id=document_id, query=query, limit=limit
    )

    return [result["content"] for result in results]
