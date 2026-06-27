from pydantic import BaseModel


class RetrievalResult(BaseModel):
    contexts: list[str]
    sources: list[str]
