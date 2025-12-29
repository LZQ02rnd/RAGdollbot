"""Configuration management for the Discord RAG bot."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Bot configuration settings."""
    
    # Discord Bot Token
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
    
    # LLM Provider Selection (groq, ollama, deepseek, openai)
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()
    
    # Groq Configuration (FREE - Recommended)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    # Ollama Configuration (FREE - Local)
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    # DeepSeek Configuration (Optional)
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    # OpenAI Configuration (Optional)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Embedding Configuration (using sentence-transformers for free local embeddings)
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    USE_OPENAI_EMBEDDINGS = os.getenv("USE_OPENAI_EMBEDDINGS", "false").lower() == "true"
    
    # Vector Database
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    
    # Bot Settings
    BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
    MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "2000"))
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.DISCORD_BOT_TOKEN:
            raise ValueError("DISCORD_BOT_TOKEN is required in .env file")
        
        # Validate LLM provider configuration
        if cls.LLM_PROVIDER == "groq":
            if not cls.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is required when LLM_PROVIDER=groq")
        elif cls.LLM_PROVIDER == "ollama":
            # Ollama doesn't need API key, just needs to be running locally
            pass
        elif cls.LLM_PROVIDER == "deepseek":
            if not cls.DEEPSEEK_API_KEY:
                raise ValueError("DEEPSEEK_API_KEY is required when LLM_PROVIDER=deepseek")
        elif cls.LLM_PROVIDER == "openai":
            if not cls.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        else:
            raise ValueError(f"Invalid LLM_PROVIDER: {cls.LLM_PROVIDER}. Must be one of: groq, ollama, deepseek, openai")
        
        if cls.USE_OPENAI_EMBEDDINGS and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when USE_OPENAI_EMBEDDINGS=true")

