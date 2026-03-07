"""Test evaluation metrics to debug why they show 0"""
import config
from utils.rag_pipeline import RAGPipeline
from agents.evaluation_agent import EvaluationAgent
from sentence_transformers import SentenceTransformer

# Initialize LLM
try:
    from langchain_groq import ChatGroq
    llm = ChatGroq(
        api_key=config.GROQ_API_KEY,
        model_name=config.GROQ_MODEL,
        temperature=0.3
    )
    print("✅ Using Groq API")
except Exception as e:
    print(f"❌ Groq failed: {e}")
    from langchain_ollama import OllamaLLM
    llm = OllamaLLM(
        model=config.OLLAMA_MODEL,
        base_url=config.OLLAMA_BASE_URL
    )
    print("✅ Using Ollama")

# Initialize RAG pipeline
print("\n📦 Initializing RAG pipeline...")
rag_pipeline = RAGPipeline(
    llm=llm,
    embedding_model_name=config.EMBEDDING_MODEL,
    cross_encoder_name=config.CROSS_ENCODER_MODEL,
    chroma_persist_dir=config.CHROMA_PERSIST_DIR
)

# Initialize evaluation agent
print("📦 Initializing evaluation agent...")
embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
eval_agent = EvaluationAgent(llm, embedding_model)

# Test query
query = "What are the side effects of aspirin?"
print(f"\n🔍 Query: {query}")

# Generate response
print("\n💬 Generating response...")
response = rag_pipeline.query_with_rag(
    query=query,
    collection_name="medical_knowledge",
    system_prompt="You are a medical AI assistant.",
    top_k=config.TOP_K_RERANK
)
print(f"Response: {response[:200]}...")

# Get contexts
print("\n📚 Retrieving contexts...")
retriever = rag_pipeline.create_hyde_retriever("medical_knowledge")
docs = retriever.retrieve(query, top_k=5, rerank_top_k=5)
contexts = [doc.page_content for doc in docs]
print(f"Retrieved {len(contexts)} contexts")
print(f"First context preview: {contexts[0][:200] if contexts else 'EMPTY'}...")

# Evaluate
print("\n📊 Evaluating...")
result = eval_agent.process(query, response, contexts)

print("\n✅ RESULTS:")
print(f"Status: {result['status']}")
print(f"Faithfulness: {result.get('faithfulness_score', 0)}")
print(f"Relevance: {result.get('relevance_score', 0)}")
print(f"Context Precision: {result.get('context_precision', 0)}")
print(f"Hallucination Risk: {result.get('hallucination_risk', 0)}")
print(f"Confidence: {result.get('confidence_percentage', 0)}%")
print(f"Grade: {result.get('quality_grade', 'N/A')}")
print(f"\nSummary: {result.get('summary', 'N/A')}")

if result['status'] == 'error':
    print(f"\n❌ Error: {result.get('error')}")
