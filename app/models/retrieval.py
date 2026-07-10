from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    source: str

    chunk_index: int

    content: str


class RetrievalResult(BaseModel):
    results: list[RetrievedChunk]
