from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import numpy as np
from sentence_transformers import CrossEncoder
import chromadb
from chromadb.config import Settings
# from langchain.schema import Document
from langchain_core.documents import Document
import faiss
import pickle
import os


class HyDERetriever:
    """
    Hypothetical Document Embeddings (HyDE) retriever.
    Generates hypothetical answer, embeds it, and retrieves similar documents.
    """
    
    def __init__(self, llm, embedding_model: SentenceTransformer, 
                 vector_store, cross_encoder: CrossEncoder):
        self.llm = llm
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.cross_encoder = cross_encoder
    
    def generate_hypothetical_answer(self, query: str) -> str:
        """Generate hypothetical answer using LLM"""
        prompt = f"""Given the medical query below, generate a detailed hypothetical answer that a medical expert would provide:

Query: {query}

Hypothetical Answer:"""
        
        try:
            response = self.llm.invoke(prompt)
            return response if isinstance(response, str) else response.content
        except Exception as e:
            print(f"HyDE generation failed: {e}")
            return query
    
    def retrieve(self, query: str, top_k: int = 10, rerank_top_k: int = 5) -> List[Document]:
        """
        Retrieve documents using HyDE strategy with reranking.
        
        Args:
            query: User query
            top_k: Number of documents to retrieve initially
            rerank_top_k: Number of documents after reranking
            
        Returns:
            List of reranked documents
        """
        # Step 1: Generate hypothetical answer
        hypothetical_answer = self.generate_hypothetical_answer(query)
        
        # Step 2: Embed hypothetical answer
        hyde_embedding = self.embedding_model.encode(hypothetical_answer)
        
        # Step 3: Similarity search in vector store
        try:
            results = self.vector_store.query(
                query_embeddings=[hyde_embedding.tolist()],
                n_results=top_k
            )
            
            if not results['documents'] or not results['documents'][0]:
                return []
            
            # Convert to documents
            documents = []
            for i, doc_text in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                documents.append(Document(page_content=doc_text, metadata=metadata))
            
            # Step 4: Cross-encoder reranking
            if len(documents) > 0:
                doc_texts = [doc.page_content for doc in documents]
                pairs = [[query, doc_text] for doc_text in doc_texts]
                scores = self.cross_encoder.predict(pairs)
                
                # Sort by scores
                ranked_indices = np.argsort(scores)[::-1][:rerank_top_k]
                reranked_docs = [documents[i] for i in ranked_indices]
                
                return reranked_docs
            
            return documents[:rerank_top_k]
            
        except Exception as e:
            print(f"Retrieval error: {e}")
            return []


class RAGPipeline:
    """
    Complete RAG pipeline with HyDE and reranking.
    """
    
    def __init__(self, llm, embedding_model_name: str, cross_encoder_name: str,
                 chroma_persist_dir: str):
        self.llm = llm
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.cross_encoder = CrossEncoder(cross_encoder_name)
        
        # Initialize Chroma client
        self.chroma_client = chromadb.PersistentClient(
            path=chroma_persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )
    
    def get_or_create_collection(self, collection_name: str):
        """Get or create a Chroma collection"""
        try:
            collection = self.chroma_client.get_collection(collection_name)
        except:
            collection = self.chroma_client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        return collection
    
    def add_documents(self, collection_name: str, documents: List[str], 
                     metadatas: List[Dict] = None, ids: List[str] = None):
        """Add documents to collection"""
        collection = self.get_or_create_collection(collection_name)
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(documents).tolist()
        
        # Generate IDs if not provided
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Add to collection
        collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas if metadatas else [{}] * len(documents),
            ids=ids
        )
    
    def create_hyde_retriever(self, collection_name: str) -> HyDERetriever:
        """Create HyDE retriever for a collection"""
        collection = self.get_or_create_collection(collection_name)
        return HyDERetriever(self.llm, self.embedding_model, collection, self.cross_encoder)
    
    def query_with_rag(self, query: str, collection_name: str, 
                       system_prompt: str = "", top_k: int = 5) -> str:
        """
        Complete RAG query with HyDE retrieval.
        
        Args:
            query: User query
            collection_name: Chroma collection name
            system_prompt: System prompt for LLM
            top_k: Number of documents to use for context
            
        Returns:
            Generated response
        """
        # Retrieve relevant documents
        retriever = self.create_hyde_retriever(collection_name)
        relevant_docs = retriever.retrieve(query, top_k=top_k*2, rerank_top_k=top_k)
        
        if not relevant_docs:
            return "I couldn't find relevant information in the knowledge base to answer this query."
        
        # Build context
        context = "\n\n".join([f"[Source {i+1}]\n{doc.page_content}" 
                               for i, doc in enumerate(relevant_docs)])
        
        # Build prompt
        full_prompt = f"""{system_prompt}

Context from medical knowledge base:
{context}

User Query: {query}

Based on the context provided above, generate a comprehensive medical response:"""
        
        # Generate response
        try:
            response = self.llm.invoke(full_prompt)
            return response if isinstance(response, str) else response.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
