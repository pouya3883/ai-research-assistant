from app.models.embedding import DocumentEmbedding
from sentence_transformers import SentenceTransformer
from app.services.chunk_service import get_document_chunks
from app.services.embedding_registry import add_embedding

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
