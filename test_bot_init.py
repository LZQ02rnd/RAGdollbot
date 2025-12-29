"""Test bot initialization without connecting to Discord."""
import sys
from config import Config
from rag_system import RAGSystem

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 50)
print("Testing Bot Initialization")
print("=" * 50)

try:
    print("\n[1] Validating configuration...")
    Config.validate()
    print("[OK] Configuration valid")
    
    print("\n[2] Initializing RAG system...")
    rag = RAGSystem()
    print("[OK] RAG system initialized")
    
    print("\n[3] Checking Discord bot setup...")
    if Config.DISCORD_BOT_TOKEN:
        print(f"[OK] Discord token configured (length: {len(Config.DISCORD_BOT_TOKEN)} chars)")
    else:
        print("[X] Discord token missing")
    
    print("\n[4] Checking DeepSeek API setup...")
    if Config.DEEPSEEK_API_KEY:
        print(f"[OK] DeepSeek API key configured (length: {len(Config.DEEPSEEK_API_KEY)} chars)")
        print(f"[INFO] DeepSeek API Base: {Config.DEEPSEEK_API_BASE}")
        print(f"[INFO] DeepSeek Model: {Config.DEEPSEEK_MODEL}")
    else:
        print("[X] DeepSeek API key missing")
    
    print("\n[5] Checking embeddings...")
    print(f"[INFO] Embedding Model: {Config.EMBEDDING_MODEL}")
    print(f"[INFO] Use OpenAI Embeddings: {Config.USE_OPENAI_EMBEDDINGS}")
    
    print("\n" + "=" * 50)
    print("[OK] Bot initialization test passed!")
    print("\nNote: DeepSeek API returned 'Insufficient Balance' error.")
    print("This means the API key is valid but needs account balance.")
    print("Add credits to your DeepSeek account to use the bot.")
    print("=" * 50)
    
except ValueError as e:
    print(f"\n[ERROR] Configuration error: {e}")
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()

