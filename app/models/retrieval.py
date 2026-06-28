from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    content: str
    source: str


class RetrievalResult(BaseModel):
    results: list[RetrievedChunk]
