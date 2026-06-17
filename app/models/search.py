from pydantic import BaseModel


class SearchResult(BaseModel):
    filename: str
    content: str
    score: int
