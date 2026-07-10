from pydantic import BaseModel


class HybridSearchResult(BaseModel):
    document_id: str

    filename: str

    chunk_index: int
    total_chunks: int

    content: str

    semantic_score: float = 0.0
    bm25_score: float = 0.0

    normalized_semantic_score: float = 0.0
    normalized_bm25_score: float = 0.0

    hybrid_score: float = 0.0

    rerank_score: float = 0.0
