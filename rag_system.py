"""RAG (Retrieval-Augmented Generation) system for the Discord bot."""
import os
from typing import List, Optional
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from config import Config

# Try to import HuggingFaceEmbeddings, fallback if not available
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
except ImportError:
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError:
        HuggingFaceEmbeddings = None

# Try to import Groq and Ollama
try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

try:
    from langchain_community.chat_models import ChatOllama
except ImportError:
    try:
        from langchain_ollama import ChatOllama
    except ImportError:
        ChatOllama = None


class RAGSystem:
    """Handles RAG operations: embedding, retrieval, and generation."""
    
    def __init__(self):
        """Initialize the RAG system with vector store and LLM."""
        # Initialize embeddings
        if Config.USE_OPENAI_EMBEDDINGS:
            # Use OpenAI embeddings
            self.embeddings = OpenAIEmbeddings(
                model=Config.EMBEDDING_MODEL,
                openai_api_key=Config.OPENAI_API_KEY
            )
        else:
            # Use sentence-transformers (free, local)
            if HuggingFaceEmbeddings is None:
                raise ImportError(
                    "HuggingFaceEmbeddings not available. "
                    "Install with: pip install langchain-community sentence-transformers"
                )
            self.embeddings = HuggingFaceEmbeddings(
                model_name=Config.EMBEDDING_MODEL
            )
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_PERSIST_DIRECTORY
        )
        
        # Initialize vector store
        self.vectorstore = Chroma(
            client=self.client,
            collection_name="club_knowledge",
            embedding_function=self.embeddings
        )
        
        # Initialize LLM based on provider
        if Config.LLM_PROVIDER == "groq":
            if ChatGroq is None:
                raise ImportError(
                    "ChatGroq not available. Install with: pip install langchain-groq"
                )
            self.llm = ChatGroq(
                model=Config.GROQ_MODEL,
                temperature=0.7,
                groq_api_key=Config.GROQ_API_KEY
            )
        elif Config.LLM_PROVIDER == "ollama":
            if ChatOllama is None:
                raise ImportError(
                    "ChatOllama not available. Install with: pip install langchain-community"
                )
            self.llm = ChatOllama(
                model=Config.OLLAMA_MODEL,
                base_url=Config.OLLAMA_BASE_URL,
                temperature=0.7
            )
        elif Config.LLM_PROVIDER == "deepseek":
            self.llm = ChatOpenAI(
                model_name=Config.DEEPSEEK_MODEL,
                temperature=0.7,
                openai_api_key=Config.DEEPSEEK_API_KEY,
                openai_api_base=Config.DEEPSEEK_API_BASE
            )
        elif Config.LLM_PROVIDER == "openai":
            self.llm = ChatOpenAI(
                model_name=Config.OPENAI_MODEL,
                temperature=0.7,
                openai_api_key=Config.OPENAI_API_KEY
            )
        else:
            raise ValueError(f"Invalid LLM_PROVIDER: {Config.LLM_PROVIDER}")
        
        # Create custom prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant for a university club. Answer the user's question based on the following context from the club's knowledge base.

Context:
{context}

Provide a helpful, accurate answer based on the context. If the context doesn't contain enough information to answer the question, say so politely and suggest what information might be helpful."""),
            ("human", "{question}")
        ])
        
        # Create retrieval chain using LCEL
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 4}  # Retrieve top 4 most relevant chunks
        )
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        self.qa_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )
    
    def add_documents(self, texts: List[str], metadatas: Optional[List[dict]] = None):
        """
        Add documents to the knowledge base.
        
        Args:
            texts: List of text documents to add
            metadatas: Optional list of metadata dictionaries for each document
        """
        if metadatas is None:
            metadatas = [{}] * len(texts)
        
        self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
    
    def query(self, question: str) -> str:
        """
        Query the RAG system with a question.
        
        Args:
            question: The user's question
            
        Returns:
            The generated answer
        """
        try:
            answer = self.qa_chain.invoke(question)
            
            # Truncate if too long for Discord
            if len(answer) > Config.MAX_MESSAGE_LENGTH:
                answer = answer[:Config.MAX_MESSAGE_LENGTH - 3] + "..."
            
            return answer
        except Exception as e:
            return f"I encountered an error while processing your question: {str(e)}"
    
    def clear_knowledge_base(self):
        """Clear all documents from the knowledge base."""
        self.client.delete_collection(name="club_knowledge")
        self.vectorstore = Chroma(
            client=self.client,
            collection_name="club_knowledge",
            embedding_function=self.embeddings
        )

