#!/usr/bin/env python3
"""
Setup script for RAGdollBot
Helps users verify their environment and configuration
"""
import os
import sys


def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        print("   Please copy .env.example to .env and fill in your credentials")
        return False
    print("✅ .env file found")
    return True


def check_env_variables():
    """Check if required environment variables are set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ["DISCORD_BOT_TOKEN", "OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith("your_"):
            missing_vars.append(var)
            print(f"❌ {var} is not set or still has default value")
        else:
            # Show partial value for security
            masked_value = value[:8] + "..." if len(value) > 8 else "***"
            print(f"✅ {var} is set ({masked_value})")
    
    return len(missing_vars) == 0


def check_knowledge_base():
    """Check if knowledge base directory exists and has documents"""
    kb_path = "./knowledge_base"
    
    if not os.path.exists(kb_path):
        print(f"⚠️  Knowledge base directory not found: {kb_path}")
        print("   Creating directory...")
        os.makedirs(kb_path, exist_ok=True)
        return True
    
    files = [f for f in os.listdir(kb_path) if f.endswith(('.txt', '.pdf'))]
    if not files:
        print(f"⚠️  No documents found in {kb_path}")
        print("   Add .txt or .pdf files to the knowledge_base directory")
    else:
        print(f"✅ Found {len(files)} document(s) in knowledge base:")
        for f in files[:5]:  # Show first 5 files
            print(f"   - {f}")
        if len(files) > 5:
            print(f"   ... and {len(files) - 5} more")
    
    return True


def check_dependencies():
    """Check if required packages are installed"""
    try:
        import discord
        print(f"✅ discord.py version {discord.__version__}")
    except ImportError:
        print("❌ discord.py is not installed")
        return False
    
    try:
        import langchain
        print(f"✅ langchain version {langchain.__version__}")
    except ImportError:
        print("❌ langchain is not installed")
        return False
    
    try:
        import chromadb
        print(f"✅ chromadb installed")
    except ImportError:
        print("❌ chromadb is not installed")
        return False
    
    try:
        import openai
        print(f"✅ openai installed")
    except ImportError:
        print("❌ openai is not installed")
        return False
    
    return True


def main():
    """Run all checks"""
    print("=" * 50)
    print("RAGdollBot Setup Verification")
    print("=" * 50)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Environment Variables", check_env_variables),
        ("Knowledge Base", check_knowledge_base),
    ]
    
    all_passed = True
    
    for name, check_func in checks:
        print(f"\nChecking {name}:")
        print("-" * 40)
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"❌ Error during {name} check: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All checks passed! You're ready to run the bot.")
        print("\nTo start the bot, run:")
        print("   python bot.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nTo install dependencies, run:")
        print("   pip install -r requirements.txt")
    print("=" * 50)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
