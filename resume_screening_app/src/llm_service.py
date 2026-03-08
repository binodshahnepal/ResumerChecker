import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from src.config import GOOGLE_API_KEY, LLM_MODEL, TEMPERATURE

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


def get_llm():
    return ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=TEMPERATURE
    )


def get_embedding_model():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )