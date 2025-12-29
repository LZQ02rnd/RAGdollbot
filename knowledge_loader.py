"""Load and index knowledge base documents."""
import os
from pathlib import Path
from typing import List
from rag_system import RAGSystem


def load_text_file(file_path: str) -> str:
    """Load text from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Split text into chunks for better retrieval.
    
    Args:
        text: The text to split
        chunk_size: Maximum size of each chunk
        chunk_overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - chunk_overlap
    
    return chunks


def load_knowledge_base(rag_system: RAGSystem, knowledge_dir: str = "knowledge_base"):
    """
    Load all documents from the knowledge base directory.
    
    Args:
        rag_system: The RAG system instance to add documents to
        knowledge_dir: Directory containing knowledge base files
    """
    knowledge_path = Path(knowledge_dir)
    
    if not knowledge_path.exists():
        print(f"Knowledge base directory '{knowledge_dir}' not found. Creating it...")
        knowledge_path.mkdir(exist_ok=True)
        # Create a sample file
        sample_file = knowledge_path / "sample_info.txt"
        sample_file.write_text(
            "Welcome to the club knowledge base!\n\n"
            "Add your club information files to this directory. "
            "Supported formats: .txt files\n\n"
            "The bot will automatically index all text files in this directory."
        )
        print(f"Created sample file: {sample_file}")
        return
    
    all_texts = []
    all_metadatas = []
    
    # Load all .txt files
    for file_path in knowledge_path.glob("*.txt"):
        try:
            text = load_text_file(str(file_path))
            chunks = split_text(text)
            
            for i, chunk in enumerate(chunks):
                all_texts.append(chunk)
                all_metadatas.append({
                    "source": file_path.name,
                    "chunk_index": i
                })
            
            print(f"Loaded {len(chunks)} chunks from {file_path.name}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    if all_texts:
        # Clear existing knowledge base
        rag_system.clear_knowledge_base()
        
        # Add all documents
        rag_system.add_documents(all_texts, all_metadatas)
        print(f"[OK] Successfully indexed {len(all_texts)} document chunks!")
    else:
        print("[!] No documents found in knowledge base directory.")


if __name__ == "__main__":
    """Load knowledge base when run directly."""
    from rag_system import RAGSystem
    rag = RAGSystem()
    load_knowledge_base(rag)

