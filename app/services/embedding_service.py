from app.models.embedding import DocumentEmbedding


def create_embedding(document_id: str, chunk_filename: str, content: str):
    return DocumentEmbedding(
        document_id=document_id, chunk_filename=chunk_filename, embedding=[]
    )
