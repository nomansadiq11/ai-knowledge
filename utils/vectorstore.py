from langchain_community.vectorstores import Chroma
from chromadb.config import Settings
from typing import Tuple, List
from .ingestion import split_text
import os


def create_vector_store(texts: str, embeddings) -> Tuple[Chroma, List[str]]:
    """Create or update vector store with new documents and return chunks."""
    chunks = split_text(texts, chunk_size=1000, chunk_overlap=200)
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db",
        client_settings=Settings(anonymized_telemetry=False),
    )
    return vectorstore, chunks


def load_vector_store(embeddings, persist_directory: str = "./chroma_db") -> Chroma:
    """Load an existing persisted Chroma vector store for querying.

    Returns a Chroma instance if the directory exists; raises if not.
    """
    if not os.path.isdir(persist_directory):
        raise FileNotFoundError(f"Vector store directory not found: {persist_directory}")
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        client_settings=Settings(anonymized_telemetry=False),
    )
