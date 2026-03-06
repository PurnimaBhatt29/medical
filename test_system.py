"""
System test script for MedVision AI
Tests all components and agents
"""

import sys
import os


def test_imports():
    """Test if all required packages can be imported"""
    print("\n" + "="*60)
    print("Testing Package Imports")
    print("="*60)
    
    packages = [
        ('streamlit', 'Streamlit'),
        ('langchain', 'LangChain'),
        ('chromadb', 'ChromaDB'),
        ('sentence_transformers', 'Sentence Transformers'),
        ('transformers', 'Transformers'),
        ('PyPDF2', 'PyPDF2'),
        ('PIL', 'Pillow'),
        ('numpy', 'NumPy'),
    ]
    
    all_passed = True
    for package, name in packages:
        try:
            __import__(package)
            print(f"✓ {name}")
        except ImportError as e:
            print(f"✗ {name}: {e}")
            all_passed = False
    
    return all_passed


def test_config():
    """Test configuration file"""
    print("\n" + "="*60)
    print("Testing Configuration")
    print("="*60)
    
    try:
        import config
        print(f"✓ Config loaded")
        print(f"  - Embedding Model: {config.EMBEDDING_MODEL}")
        print(f"  - Vision Model: {config.VISION_MODEL}")
        print(f"  - Chroma Dir: {config.CHROMA_PERSIST_DIR}")
        return True
    except Exception as e:
        print(f"✗ Config error: {e}")
        return False


def test_utils():
    """Test utility modules"""
    print("\n" + "="*60)
    print("Testing Utility Modules")
    print("="*60)
    
    try:
        from utils.text_processing import clean_medical_text, parent_child_chunking
        from utils.pdf_processor import extract_text_from_pdf
        
        # Test text cleaning
        test_text = "Test   text  with   spaces"
        cleaned = clean_medical_text(test_text)
        print(f"✓ Text processing works")
        
        # Test chunking
        chunks = parent_child_chunking("This is a test text for chunking.", 50, 20)
        print(f"✓ Parent-child chunking works ({len(chunks)} chunks)")
        
        return True
    except Exception as e:
        print(f"✗ Utils error: {e}")
        return False


def test_agents():
    """Test agent imports"""
    print("\n" + "="*60)
    print("Testing Agent Modules")
    print("="*60)
    
    agents = [
        'base_agent',
        'report_analyzer_agent',
        'xray_vision_agent',
        'prescription_analyzer_agent',
        'medicine_knowledge_agent',
        'medical_chat_agent',
        'evaluation_agent'
    ]
    
    all_passed = True
    for agent in agents:
        try:
            __import__(f'agents.{agent}')
            print(f"✓ {agent}")
        except Exception as e:
            print(f"✗ {agent}: {e}")
            all_passed = False
    
    return all_passed


def test_evaluation_metrics():
    """Validate that retrieval metrics compute without crashing"""
    print("\n" + "="*60)
    print("Testing Retrieval Metrics")
    print("="*60)
    try:
        from agents.evaluation_agent import EvaluationAgent
        from sentence_transformers import SentenceTransformer
        import config
        
        dummy_llm = type("Dummy", (), {"invoke": lambda self, x: "ok"})()
        emb = SentenceTransformer(config.EMBEDDING_MODEL)
        agent = EvaluationAgent(dummy_llm, emb)
        retrieved = ["This is relevant doc", "Another irrelevant text"]
        relevant = ["relevant doc"]
        metrics = agent._compute_retrieval_metrics(retrieved, relevant)
        print(f"✓ Computed metrics: {metrics}")
        return True
    except Exception as e:
        print(f"✗ Evaluation metrics error: {e}")
        return False


def test_rag_pipeline():
    """Test RAG pipeline initialization"""
    print("\n" + "="*60)
    print("Testing RAG Pipeline")
    print("="*60)
    
    try:
        from utils.rag_pipeline import RAGPipeline
        from sentence_transformers import SentenceTransformer
        import config
        
        print("✓ RAG pipeline imports successful")
        
        # Test embedding model
        print("  Loading embedding model...")
        embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        print(f"✓ Embedding model loaded: {config.EMBEDDING_MODEL}")
        
        # Test embedding
        test_text = "This is a test sentence."
        embedding = embedding_model.encode(test_text)
        print(f"✓ Embedding generated: shape {embedding.shape}")
        
        return True
    except Exception as e:
        print(f"✗ RAG pipeline error: {e}")
        return False


def test_chroma_db():
    """Test ChromaDB"""
    print("\n" + "="*60)
    print("Testing ChromaDB")
    print("="*60)
    
    try:
        import chromadb
        from chromadb.config import Settings
        import config
        
        # Check if database exists
        if os.path.exists(config.CHROMA_PERSIST_DIR):
            print(f"✓ ChromaDB directory exists: {config.CHROMA_PERSIST_DIR}")
            
            # Try to connect
            client = chromadb.PersistentClient(
                path=config.CHROMA_PERSIST_DIR,
                settings=Settings(anonymized_telemetry=False)
            )
            
            collections = client.list_collections()
            print(f"✓ ChromaDB accessible")
            print(f"  - Collections: {len(collections)}")
            for col in collections:
                print(f"    • {col.name}")
            
            return True
        else:
            print(f"⚠ ChromaDB not initialized yet")
            print(f"  Run: python data_ingestion.py")
            return False
            
    except Exception as e:
        print(f"✗ ChromaDB error: {e}")
        return False


def test_llm_connection():
    """Test LLM connection"""
    print("\n" + "="*60)
    print("Testing LLM Connection")
    print("="*60)
    
    import config
    
    # Test Groq
    if config.GROQ_API_KEY:
        try:
            from langchain_groq import ChatGroq
            llm = ChatGroq(
                api_key=config.GROQ_API_KEY,
                model_name=config.GROQ_MODEL,
                temperature=0.3
            )
            response = llm.invoke("Say 'test successful'")
            print(f"✓ Groq connection successful")
            print(f"  - Model: {config.GROQ_MODEL}")
            return True
        except Exception as e:
            print(f"✗ Groq error: {e}")
    
    # Test Ollama
    try:
        from langchain_community.llms import Ollama
        llm = Ollama(
            model=config.OLLAMA_MODEL,
            base_url=config.OLLAMA_BASE_URL
        )
        response = llm.invoke("Say 'test successful'")
        print(f"✓ Ollama connection successful")
        print(f"  - Model: {config.OLLAMA_MODEL}")
        return True
    except Exception as e:
        print(f"✗ Ollama error: {e}")
        print(f"  Make sure Ollama is running: ollama serve")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("MedVision AI - System Test")
    print("="*60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Configuration", test_config),
        ("Utility Modules", test_utils),
        ("Agent Modules", test_agents),
        ("Retrieval Metrics", test_evaluation_metrics),
        ("RAG Pipeline", test_rag_pipeline),
        ("ChromaDB", test_chroma_db),
        ("LLM Connection", test_llm_connection),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Run data ingestion: python data_ingestion.py")
        print("2. Launch application: streamlit run app.py")
        return 0
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
