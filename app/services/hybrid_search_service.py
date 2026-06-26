# TODO:
# Implement weighted hybrid search after introducing a unified ranking strategy

from app.services.chunk_service import search_document_chunks
from app.services.embedding_service import semantic_search_document


def hybrid_search_document(document_id: str, query: str, limit: int = 5):
    keyword_results = search_document_chunks(
        document_id=document_id, query=query, limit=limit
    )

    semantic_results = semantic_search_document(
        document_id=document_id, query=query, limit=limit
    )

    combined_results = []

    combined_results.extend(semantic_results)

    for result in keyword_results:
        combined_results.append(
            {
                "chunk_filename": result.filename,
                "content": result.content,
                "score": result.score,
            }
        )

    seen_chunks = set()
    unique_results = []

    for result in combined_results:
        # print(result["score"])
        if result["chunk_filename"] not in seen_chunks:
            seen_chunks.add(result["chunk_filename"])
            unique_results.append(result)

    return unique_results[:limit]


# test = hybrid_search_document(
#     document_id="cbf4105b-90c1-46a1-8083-dae45ac8310b",
#     query="ps4",
#     limit=1000,
# )

# for t in test:
#     print(t["score"])
