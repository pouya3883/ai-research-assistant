from pydantic import BaseModel


class HybridSearchResult(BaseModel):
    filename: str
    content: str

    semantic_score: float = 0.0
    keyword_score: float = 0.0

    normalized_semantic_score: float = 0.0
    normalized_keyword_score: float = 0.0

    hybrid_score: float = 0.0
