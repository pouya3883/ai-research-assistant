import re

from app.core.config import CHUNK_SIZE, CHUNK_OVERLAP

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


def _apply_overlap(
    chunks: list[str],
    overlap_size: int,
) -> list[str]:
    """
    Apply sentence-aware overlap between consecutive chunks.
    """
    if len(chunks) <= 1:
        return chunks

    overlapped_chunks = [chunks[0]]

    for index in range(1, len(chunks)):
        previous_chunk = chunks[index - 1]

        chunk = chunks[index]

        previous_sentences = _split_sentences(previous_chunk)

        overlap_sentences: list[str] = []

        overlap_length = 0

        for sentence in reversed(previous_sentences):
            sentence_length = len(sentence) + 1

            if overlap_sentences and overlap_length + sentence_length > overlap_size:
                break

            overlap_sentences.insert(0, sentence)
            overlap_length += sentence_length

        merged_chunk = " ".join(overlap_sentences)

        if merged_chunk:
            merged_chunk += " "

        merged_chunk += chunk

        overlapped_chunks.append(merged_chunk)

    return overlapped_chunks


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    """
    Split text into paragraph-aware chunks.

    Oversized paragraphs are further split using sentence-aware chunking.
    """

    paragraphs = _split_paragraphs(text)

    chunks = _merge_paragraphs(paragraphs, chunk_size)

    return _apply_overlap(chunks, CHUNK_OVERLAP)
