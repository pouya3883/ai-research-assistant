from pydantic import BaseModel


class DocumentEmbedding(BaseModel):
    document_id: str
    chunk_filename: str
    embedding: list[float]
