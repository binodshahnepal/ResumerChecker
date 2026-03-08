from pathlib import Path
from pypdf import PdfReader
from docx import Document


def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text).strip()


def load_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([
        para.text.strip() for para in doc.paragraphs if para.text and para.text.strip()
    ]).strip()


def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()


def load_resume(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        return load_pdf(file_path)
    if ext == ".docx":
        return load_docx(file_path)
    if ext == ".txt":
        return load_txt(file_path)

    raise ValueError(f"Unsupported file format: {ext}")
