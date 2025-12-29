#!/usr/bin/env python3
"""
Test script to validate RAGdollBot components without running the full bot
"""
import sys
import os


def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import discord
        print(f"  ✅ discord.py {discord.__version__}")
    except ImportError as e:
        print(f"  ❌ discord.py: {e}")
        return False
    
    try:
        import langchain
        print("  ✅ langchain")
    except ImportError as e:
        print(f"  ❌ langchain: {e}")
        return False
    
    try:
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        print("  ✅ langchain_openai")
    except ImportError as e:
        print(f"  ❌ langchain_openai: {e}")
        return False
    
    try:
        from langchain_community.vectorstores import Chroma
        print("  ✅ langchain_community")
    except ImportError as e:
        print(f"  ❌ langchain_community: {e}")
        return False
    
    try:
        import chromadb
        print("  ✅ chromadb")
    except ImportError as e:
        print(f"  ❌ chromadb: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✅ python-dotenv")
    except ImportError as e:
        print(f"  ❌ python-dotenv: {e}")
        return False
    
    return True


def test_module_structure():
    """Test if bot modules can be imported"""
    print("\nTesting module structure...")
    
    try:
        import config
        print("  ✅ config.py")
    except Exception as e:
        print(f"  ❌ config.py: {e}")
        return False
    
    try:
        import rag_engine
        print("  ✅ rag_engine.py")
    except Exception as e:
        print(f"  ❌ rag_engine.py: {e}")
        return False
    
    try:
        import bot
        print("  ✅ bot.py")
    except Exception as e:
        print(f"  ❌ bot.py: {e}")
        return False
    
    return True


def test_configuration():
    """Test if configuration loads properly"""
    print("\nTesting configuration...")
    
    try:
        from config import Config
        
        # Check if attributes exist
        assert hasattr(Config, 'DISCORD_BOT_TOKEN')
        assert hasattr(Config, 'OPENAI_API_KEY')
        assert hasattr(Config, 'COMMAND_PREFIX')
        assert hasattr(Config, 'CHUNK_SIZE')
        
        print("  ✅ Configuration class structure is valid")
        
        # Check if paths are defined
        assert hasattr(Config, 'VECTOR_STORE_PATH')
        assert hasattr(Config, 'KNOWLEDGE_BASE_PATH')
        print("  ✅ Path configurations are defined")
        
        return True
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False


def test_knowledge_base():
    """Test knowledge base directory"""
    print("\nTesting knowledge base...")
    
    kb_path = "./knowledge_base"
    
    if not os.path.exists(kb_path):
        print(f"  ⚠️  Knowledge base directory not found")
        return True  # Not critical for tests
    
    files = [f for f in os.listdir(kb_path) if f.endswith(('.txt', '.pdf'))]
    if not files:
        print(f"  ⚠️  No documents in knowledge base")
        return True  # Not critical for tests
    
    print(f"  ✅ Found {len(files)} document(s)")
    for f in files[:3]:
        print(f"     - {f}")
    
    return True


def test_bot_structure():
    """Test bot class structure"""
    print("\nTesting bot structure...")
    
    try:
        from bot import RAGdollBot, setup_bot
        
        print("  ✅ RAGdollBot class defined")
        print("  ✅ setup_bot function defined")
        
        return True
    except Exception as e:
        print(f"  ❌ Bot structure error: {e}")
        return False


def test_rag_engine_structure():
    """Test RAG engine structure"""
    print("\nTesting RAG engine structure...")
    
    try:
        from rag_engine import RAGEngine
        
        # Check if critical methods exist
        assert hasattr(RAGEngine, 'initialize_vector_store')
        assert hasattr(RAGEngine, 'answer_question')
        assert hasattr(RAGEngine, 'load_documents')
        
        print("  ✅ RAGEngine class structure is valid")
        print("  ✅ Critical methods are defined")
        
        return True
    except Exception as e:
        print(f"  ❌ RAG engine error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("RAGdollBot Component Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Module Structure", test_module_structure),
        ("Configuration", test_configuration),
        ("Knowledge Base", test_knowledge_base),
        ("Bot Structure", test_bot_structure),
        ("RAG Engine Structure", test_rag_engine_structure),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
