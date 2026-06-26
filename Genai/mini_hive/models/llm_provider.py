"""LLM provider configuration and clients."""
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# load_dotenv()

# groq_llm = ChatGroq(model="llama3-70b-8192")
from langchain_ollama import ChatOllama

def get_olllama_client(model: str) -> ChatOllama:
    """Get an instance of the Ollama client."""
    return ChatOllama(model=model, temperature=0.3)