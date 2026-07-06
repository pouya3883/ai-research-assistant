import re

from app.core.config import CHUNK_SIZE

PARAGRAPH_PATTERN = re.compile(r"\n\s*\n")
SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+")


def _split_paragraphs(text: str) -> list[str]:
    """
    Split text into paragraphs.
    """
    return [
        paragraph.strip()
        for paragraph in PARAGRAPH_PATTERN.split(text.strip())
        if paragraph.strip()
    ]


def _split_sentences(paragraph: str) -> list[str]:
    """
    Split a paragraph into sentences.
    """
    return [
        sentence.strip()
        for sentence in SENTENCE_PATTERN.split(paragraph)
        if sentence.strip()
    ]


def _merge_sentences(sentences: list[str], chunk_size: int) -> list[str]:
    """
    Merge sentences into chunks without exceeding chunk_size.
    """
    chunks: list[str] = []
    current_chunk: list[str] = []

    current_size = 0

    for sentence in sentences:
        sentence_length = len(sentence)

        if current_chunk and current_size + sentence_length + 1 > chunk_size:
            chunks.append(" ".join(current_chunk))

            current_chunk = [sentence]
            current_size = sentence_length
        else:
            current_chunk.append(sentence)
            current_size += sentence_length + 1

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def _chunk_large_paragraph(paragraph: str, chunk_size: int) -> list[str]:
    """
    Split an oversized paragraph using sentence-aware chunking.
    """
    sentences = _split_sentences(paragraph)

    return _merge_sentences(sentences, chunk_size)


def _merge_paragraphs(paragraphs: list[str], chunk_size: int) -> list[str]:
    """
    Merge paragraphs while respecting chunk_size.
    """
    chunks: list[str] = []

    current_chunk: list[str] = []
    current_size = 0

    for paragraph in paragraphs:
        paragraph_length = len(paragraph)

        if paragraph_length > chunk_size:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_size = 0

            chunks.extend(_chunk_large_paragraph(paragraph, chunk_size))
            continue

        if current_chunk and current_size + paragraph_length + 2 > chunk_size:
            chunks.append("\n\n".join(current_chunk))

            current_chunk = [paragraph]
            current_size = paragraph_length
        else:
            current_chunk.append(paragraph)
            current_size += paragraph_length + 2

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    """
    Split text into paragraph-aware chunks.

    Oversized paragraphs are further split using sentence-aware chunking.
    """

    paragraphs = _split_paragraphs(text)

    return _merge_paragraphs(paragraphs, chunk_size)
