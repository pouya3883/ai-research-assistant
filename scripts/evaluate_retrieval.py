# Evaluation for LPI-Learning-Material-101-500-en
from app.services.hybrid_search_service import hybrid_search_document

DOCUMENT_ID = ""
TEST_QUERIES = [
    "grub boot",
    "linux permissions",
    "network interface",
    "filesystem hierarchy",
    "kernel modules",
]


def main() -> None:
    for query in TEST_QUERIES:
        results = hybrid_search_document(document_id=DOCUMENT_ID, query=query, limit=5)

        print("=" * 80)
        print(f"Query: {query}")
        print("=" * 80)

        for index, result in enumerate(results, start=1):
            print(f"\nResult #{index}")
            print(f"Hybrid Score : {result.hybrid_score:.4f}")
            print(f"Semantic : {result.semantic_score:.4f}")
            print(f"BM25 : {result.bm25_score:.4f}")
            print(f"File : {result.filename}")

            print("-" * 80)
            print(result.content)
            print("=" * 80)


if __name__ == "__main__":
    main()
