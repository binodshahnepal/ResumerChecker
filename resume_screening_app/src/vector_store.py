from langchain_chroma import Chroma
from langchain_core.documents import Document
from src.llm_service import get_embedding_model
from src.config import CHROMA_DIR


def get_vectorstore():
    embedding_model = get_embedding_model()
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_model,
    )


def store_resume_chunks(chunks: list[str], metadata: dict) -> None:
    vectorstore = get_vectorstore()
    documents = [Document(page_content=chunk, metadata=metadata) for chunk in chunks]
    vectorstore.add_documents(documents)
