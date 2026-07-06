import re

from app.core.config import CHUNK_SIZE


SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+")


def _split_sentences(text: str) -> list[str]:
    return SENTENCE_PATTERN.split(text.strip())


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    """
    Split text into sentence-aware chunks.

    Sentences are kept intact whenever possible while respecting the
    configured maximum chunk size.
    """

    sentences = _split_sentences(text)

    chunks: list[str] = []
    current_chunk: list[str] = []

    current_size = 0

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        sentence_length = len(sentence)

        if (current_size + sentence_length) > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))

            current_chunk = [sentence]
            current_size = sentence_length
        else:
            current_chunk.append(sentence)
            current_size += sentence_length + 1

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
