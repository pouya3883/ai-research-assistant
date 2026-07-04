from app.models.chunk import DocumentChunk
from app.models.search import SearchResult
from collections import Counter
from app.utils.text_processing import tokenize
from math import log

K1 = 1.5
B = 0.75


def bm25_search(
    chunks: list[DocumentChunk], query: str, limit: int = 5
) -> list[SearchResult]:
    corpus = _build_corpus(chunks)

    idf, avg_document_length = _compute_idf(corpus)

    query_tokens = tokenize(query)

    results = []

    for chunk in chunks:
        document_tokens = corpus[chunk.filename]

        score = _score_document(
            query_tokens=query_tokens,
            term_frequencies=Counter(document_tokens),
            document_length=len(document_tokens),
            avg_document_length=avg_document_length,
            idf=idf,
        )

        results.append(
            SearchResult(filename=chunk.filename, content=chunk.content, score=score)
        )

    results.sort(key=lambda result: result.score, reverse=True)

    return results[:limit]


def _build_corpus(chunks: list[DocumentChunk]) -> dict[str, list[str]]:
    corpus = {}

    for chunk in chunks:
        corpus[chunk.filename] = tokenize(chunk.content)

    return corpus


def _compute_idf(corpus: dict[str, list[str]]) -> tuple[dict[str, float], float]:
    document_frequency = Counter()

    total_document_length = 0
    total_documents = len(corpus)

    for tokens in corpus.values():
        document_frequency.update(set(tokens))
        total_document_length += len(tokens)

    avg_document_length = (
        total_document_length / total_documents if total_documents > 0 else 0
    )

    idf = {}

    for term, df in document_frequency.items():
        idf[term] = log(((total_documents - df + 0.5) / (df + 0.5)) + 1)

    return idf, avg_document_length


def _score_document(
    query_tokens: list[str],
    term_frequencies: Counter[str],
    document_length: int,
    avg_document_length: float,
    idf: dict[str, float],
) -> float:
    if avg_document_length == 0:
        return 0.0

    score = 0.0

    for term in query_tokens:
        if term not in idf:
            continue

        tf = term_frequencies.get(term, 0)

        numerator = tf * (K1 + 1)

        denominator = tf + K1 * (1 - B + B * (document_length / avg_document_length))

        score += idf[term] * (numerator / denominator)

    return score
