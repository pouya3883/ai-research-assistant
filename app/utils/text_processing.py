import re
import string

PUNCTUATION_TABLE = str.maketrans("", "", string.punctuation)
MULTIPLE_WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """
    Normalize text for retrieval tasks.

    Operations:
    - Convert to lowercase
    - Remove punctuation
    - Collapse multiple whitespaces
    - Strip leading/trailing spaces
    """
    text = text.lower()

    text = text.translate(PUNCTUATION_TABLE)

    text = MULTIPLE_WHITESPACE_PATTERN.sub(" ", text)

    return text.strip()


def tokenize(text: str) -> list[str]:
    """
    Tokenize normalized text into whitespace-separated tokens.
    """
    normalized_text = normalize_text(text)

    return normalized_text.split()
