from pydantic import BaseModel


class DocumentChunk(BaseModel):
    document_id: str
    filename: str

    chunk_index: int
    total_chunks: int

    content: str
