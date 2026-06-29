from pydantic import BaseModel


class Citation(BaseModel):
    id: int
    source: str


class AnswerResponse(BaseModel):
    answer: str
    citations: list[Citation]
