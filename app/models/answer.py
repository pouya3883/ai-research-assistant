from pydantic import BaseModel


class Citation(BaseModel):
    id: int

    source: str

    chunk_index: int

    preview: str


class AnswerResponse(BaseModel):
    answer: str
    citations: list[Citation]
