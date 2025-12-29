"""Quick setup checker for RAGdollbot."""
import sys
from pathlib import Path
from config import Config

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 50)
print("RAGdollbot Setup Check")
print("=" * 50)

# Check .env file
env_exists = Path(".env").exists()
print(f"\n[FILE] .env file: {'[OK] Found' if env_exists else '[X] Not found'}")

# Check configuration
print("\n[CONFIG] Configuration:")
print(f"  Discord Bot Token: {'[OK] Set' if Config.DISCORD_BOT_TOKEN else '[X] Missing'}")
print(f"  DeepSeek API Key: {'[OK] Set' if Config.DEEPSEEK_API_KEY else '[X] Missing'}")
print(f"  DeepSeek Model: {Config.DEEPSEEK_MODEL}")
print(f"  Embedding Model: {Config.EMBEDDING_MODEL}")
print(f"  Use OpenAI Embeddings: {Config.USE_OPENAI_EMBEDDINGS}")

# Check knowledge base
kb_path = Path("knowledge_base")
print(f"\n[KB] Knowledge Base:")
if kb_path.exists():
    txt_files = list(kb_path.glob("*.txt"))
    print(f"  Directory: [OK] Found")
    print(f"  .txt files: {len(txt_files)} file(s)")
    for txt_file in txt_files:
        size = txt_file.stat().st_size
        print(f"    - {txt_file.name} ({size} bytes)")
else:
    print(f"  Directory: [X] Not found")
    txt_files = []

# Check ChromaDB
chroma_path = Path(Config.CHROMA_PERSIST_DIRECTORY)
print(f"\n[DB] Vector Database:")
print(f"  ChromaDB: {'[OK] Indexed' if chroma_path.exists() else '[!] Not indexed yet'}")
if chroma_path.exists():
    print(f"  Location: {chroma_path.absolute()}")

# Summary
print("\n" + "=" * 50)
print("Next Steps:")
if not Config.DISCORD_BOT_TOKEN or not Config.DEEPSEEK_API_KEY:
    print("  1. [!] Add your API keys to .env file")
if len(txt_files) == 0 or (len(txt_files) == 1 and txt_files[0].name == "sample_info.txt"):
    print("  2. [!] Add your club information to knowledge_base/*.txt files")
if not chroma_path.exists():
    print("  3. [!] Run: python knowledge_loader.py (to index knowledge base)")
else:
    print("  [OK] Ready to run: python bot.py")
print("=" * 50)

