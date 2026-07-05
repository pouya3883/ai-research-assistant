from pydantic import BaseModel


class HybridSearchResult(BaseModel):
    filename: str
    content: str

    semantic_score: float = 0.0
    bm25_score: float = 0.0

    normalized_semantic_score: float = 0.0
    normalized_bm25_score: float = 0.0

    hybrid_score: float = 0.0
