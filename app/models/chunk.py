from pydantic import BaseModel


class DocumentChunk(BaseModel):
    filename: str
    content: str
