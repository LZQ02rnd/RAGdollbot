"""
RAG (Retrieval-Augmented Generation) engine for document retrieval and question answering
"""
import os
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from config import Config


class RAGEngine:
    """Handles document ingestion, retrieval, and question answering"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.vector_store = None
        self.qa_chain = None
        self.llm = ChatOpenAI(
            model_name=Config.MODEL_NAME,
            temperature=Config.TEMPERATURE,
            openai_api_key=Config.OPENAI_API_KEY
        )
        
    def load_documents(self, path: str) -> List:
        """Load documents from a directory"""
        if not os.path.exists(path):
            print(f"Creating knowledge base directory: {path}")
            os.makedirs(path, exist_ok=True)
            return []
        
        documents = []
        
        # Load text files
        try:
            text_loader = DirectoryLoader(
                path,
                glob="**/*.txt",
                loader_cls=TextLoader,
                show_progress=True
            )
            documents.extend(text_loader.load())
        except Exception as e:
            print(f"Error loading text files: {e}")
        
        # Load PDF files
        try:
            pdf_loader = DirectoryLoader(
                path,
                glob="**/*.pdf",
                loader_cls=PyPDFLoader,
                show_progress=True
            )
            documents.extend(pdf_loader.load())
        except Exception as e:
            print(f"Error loading PDF files: {e}")
        
        return documents
    
    def split_documents(self, documents: List) -> List:
        """Split documents into chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
        )
        return text_splitter.split_documents(documents)
    
    def initialize_vector_store(self, force_reload: bool = False):
        """Initialize or load the vector store"""
        if os.path.exists(Config.VECTOR_STORE_PATH) and not force_reload:
            print("Loading existing vector store...")
            self.vector_store = Chroma(
                persist_directory=Config.VECTOR_STORE_PATH,
                embedding_function=self.embeddings
            )
        else:
            print("Creating new vector store...")
            documents = self.load_documents(Config.KNOWLEDGE_BASE_PATH)
            
            if not documents:
                print("Warning: No documents found in knowledge base!")
                # Create empty vector store
                self.vector_store = Chroma(
                    persist_directory=Config.VECTOR_STORE_PATH,
                    embedding_function=self.embeddings
                )
            else:
                print(f"Loaded {len(documents)} documents")
                chunks = self.split_documents(documents)
                print(f"Split into {len(chunks)} chunks")
                
                self.vector_store = Chroma.from_documents(
                    documents=chunks,
                    embedding=self.embeddings,
                    persist_directory=Config.VECTOR_STORE_PATH
                )
                self.vector_store.persist()
        
        self._setup_qa_chain()
    
    def _setup_qa_chain(self):
        """Set up the question-answering chain"""
        prompt_template = """You are a helpful assistant for a university club. Use the following pieces of context to answer the question at the end. 
If you don't know the answer based on the context provided, just say that you don't know, don't try to make up an answer.
Be friendly, concise, and helpful in your responses.

Context:
{context}

Question: {question}

Helpful Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": Config.TOP_K_RESULTS}
            ),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
    
    def answer_question(self, question: str) -> dict:
        """Answer a question using RAG"""
        if not self.qa_chain:
            return {
                "answer": "The knowledge base is not initialized yet. Please contact an administrator.",
                "sources": []
            }
        
        try:
            result = self.qa_chain.invoke({"query": question})
            
            # Extract source information
            sources = []
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    source = doc.metadata.get("source", "Unknown")
                    sources.append(os.path.basename(source))
            
            return {
                "answer": result["result"],
                "sources": list(set(sources))  # Remove duplicates
            }
        except Exception as e:
            print(f"Error answering question: {e}")
            return {
                "answer": f"Sorry, I encountered an error while processing your question: {str(e)}",
                "sources": []
            }
    
    def reload_knowledge_base(self):
        """Reload the knowledge base from scratch"""
        print("Reloading knowledge base...")
        self.initialize_vector_store(force_reload=True)
        print("Knowledge base reloaded successfully!")
