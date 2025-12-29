"""Test the RAG system."""
import sys
from rag_system import RAGSystem

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 50)
print("Testing RAG System")
print("=" * 50)

try:
    print("\n[1] Initializing RAG system...")
    rag = RAGSystem()
    print("[OK] RAG system initialized")
    
    print("\n[2] Testing query: 'What is this club about?'")
    answer = rag.query("What is this club about?")
    print(f"\n[RESPONSE] {answer}")
    
    print("\n[3] Testing another query: 'What information is available?'")
    answer2 = rag.query("What information is available?")
    print(f"\n[RESPONSE] {answer2}")
    
    print("\n" + "=" * 50)
    print("[OK] RAG system is working!")
    print("=" * 50)
    
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()

