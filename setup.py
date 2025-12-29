"""Setup script to help initialize the bot."""
import os
from pathlib import Path


def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        print("✅ .env file already exists")
        return
    
    # Create .env.example if it doesn't exist
    if not env_example_path.exists():
        env_example_content = """# Discord Bot Configuration
DISCORD_BOT_TOKEN=your_discord_bot_token_here

# LLM Provider Selection (groq, ollama, deepseek, openai)
# groq = FREE API (recommended, no credit card needed)
# ollama = FREE local (requires Ollama installation)
# deepseek = Paid API
# openai = Paid API
LLM_PROVIDER=groq

# Groq Configuration (FREE - Recommended)
# Get API key at: https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant

# Ollama Configuration (FREE - Local)
# Install Ollama from: https://ollama.ai
# Then run: ollama pull llama3.2
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# DeepSeek Configuration (Optional - Paid)
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

# OpenAI Configuration (Optional - Paid)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Embedding Configuration
# Using sentence-transformers (free, local) by default
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Optional: Use OpenAI embeddings instead (set USE_OPENAI_EMBEDDINGS=true)
USE_OPENAI_EMBEDDINGS=false

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Bot Configuration
BOT_PREFIX=!
MAX_MESSAGE_LENGTH=2000
"""
        env_example_path.write_text(env_example_content)
        print("✅ Created .env.example file")
    
    # Create .env from example
    if env_example_path.exists():
        env_path.write_text(env_example_path.read_text())
        print("✅ Created .env file from .env.example")
        print("⚠️  Please edit .env and add your DISCORD_BOT_TOKEN and LLM API key")
        print("   For FREE option, use LLM_PROVIDER=groq and get key at: https://console.groq.com/keys")


def create_knowledge_base():
    """Ensure knowledge_base directory exists."""
    kb_path = Path("knowledge_base")
    kb_path.mkdir(exist_ok=True)
    
    sample_file = kb_path / "sample_info.txt"
    if not sample_file.exists():
        sample_file.write_text(
            "Welcome to the club knowledge base!\n\n"
            "Add your club information files to this directory. "
            "Supported formats: .txt files\n\n"
            "The bot will automatically index all text files in this directory."
        )
        print("✅ Created knowledge_base directory with sample file")
    else:
        print("✅ knowledge_base directory exists")


def main():
    """Run setup."""
    print("Setting up RAGdollbot...\n")
    create_env_file()
    create_knowledge_base()
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file and add your DISCORD_BOT_TOKEN")
    print("2. For FREE LLM: Set LLM_PROVIDER=groq and get API key at https://console.groq.com/keys")
    print("   OR use Ollama (local): Install from https://ollama.ai and set LLM_PROVIDER=ollama")
    print("3. Add your club information to knowledge_base/*.txt files")
    print("4. Run: python knowledge_loader.py")
    print("5. Run: python bot.py")


if __name__ == "__main__":
    main()

