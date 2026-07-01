"""
Retrieves relevant content from the resume based on a JD or query.
"""
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from src.config import CHROMA_DIR

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Load once and reuse
_embeddings = None
_vectorstore = None


def _get_store():
    global _embeddings, _vectorstore
    if _vectorstore is None:
        _embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        _vectorstore = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=_embeddings,
            collection_name="resume",
        )
    return _vectorstore


def retrieve_relevant(query: str, k: int = 4) -> list[str]:
    """
    Returns the top-k resume chunks most similar to the query.
    The query can be a JD summary or a list of skills.
    """
    store = _get_store()
    results = store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]
