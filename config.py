"""
Configuration management for RAGdollBot
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Bot configuration from environment variables"""
    
    # Discord Settings
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")
    BOT_NAME = os.getenv("BOT_NAME", "RAGdollBot")
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # RAG Settings
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))
    
    # Paths
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./vector_store")
    KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH", "./knowledge_base")
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.DISCORD_BOT_TOKEN:
            raise ValueError("DISCORD_BOT_TOKEN is required")
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        return True
