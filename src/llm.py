from langchain_groq import ChatGroq
from src.config import GROQ_API_KEY, LLM_MODEL

def get_llm(temperature: float = 0.3):
    """Groq LLM client — fast aur free."""
    return ChatGroq(
        model=LLM_MODEL,
        groq_api_key=GROQ_API_KEY,
        temperature=temperature,
    )
