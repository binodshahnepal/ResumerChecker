import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE, CHUNK_OVERLAP


HEADER_FOOTER_PATTERNS = [
    r"Page\s+\d+\s+of\s+\d+",
    r"Curriculum Vitae",
]


def clean_text(text: str) -> str:
    if not text:
        return ""

    for pattern in HEADER_FOOTER_PATTERNS:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return splitter.split_text(text)
