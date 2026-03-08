from src.vector_store import get_vectorstore


def search_resumes(query: str, k: int = 5):
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})
    return retriever.invoke(query)
