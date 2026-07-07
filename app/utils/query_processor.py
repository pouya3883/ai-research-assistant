from app.utils.text_processing import tokenize

STOPWORDS = frozenset(
    {
        "a",
        "an",
        "the",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "what",
        "which",
        "who",
        "when",
        "where",
        "why",
        "how",
        "do",
        "does",
        "did",
        "of",
        "to",
        "for",
        "in",
        "on",
        "at",
        "by",
        "with",
        "from",
        "into",
        "about",
        "and",
        "or",
    }
)


def preprocess_query(query: str) -> list[str]:
    """
    Prepare a user query for BM25 retrieval.

    Operations:
    - Normalize and tokenize the query.
    - Remove common stopwords.
    - Fallback to the original tokens if every token is removed.
    """
    tokens: list[str] = tokenize(query)

    filtered_tokens: list[str] = [token for token in tokens if token not in STOPWORDS]

    return filtered_tokens if filtered_tokens else tokens
