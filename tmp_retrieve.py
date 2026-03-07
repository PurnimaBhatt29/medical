import traceback
from utils.rag_pipeline import RAGPipeline
import config

try:
    # Try Groq first, then Ollama
    llm = None
    
    if config.GROQ_API_KEY:
        from langchain_groq import ChatGroq
        llm = ChatGroq(
            api_key=config.GROQ_API_KEY,
            model_name=config.GROQ_MODEL,
            temperature=0.3
        )
        print("Using Groq API")
    elif config.OLLAMA_BASE_URL:
        from langchain_ollama import OllamaLLM
        llm = OllamaLLM(
            model=config.OLLAMA_MODEL,
            base_url=config.OLLAMA_BASE_URL
        )
        print("Using Ollama")
    else:
        raise ValueError("No LLM configured. Set GROQ_API_KEY or OLLAMA_BASE_URL")

    pipeline = RAGPipeline(
        llm=llm,
        embedding_model_name=config.EMBEDDING_MODEL,
        cross_encoder_name=config.CROSS_ENCODER_MODEL,
        chroma_persist_dir=config.CHROMA_PERSIST_DIR,
    )
    retriever = pipeline.create_hyde_retriever('medical_knowledge')
    query = 'What are the side effects of Metformin?'
    docs = retriever.retrieve(query, top_k=5, rerank_top_k=5)
    print('Retrieved', len(docs), 'docs')
    for i, doc in enumerate(docs, start=1):
        print('--- Doc', i, '---')
        print(doc.page_content[:800].replace('\n',' '))
        print('---')
except Exception as e:
    print('ERROR:', e)
    traceback.print_exc()
