import traceback
from utils.rag_pipeline import RAGPipeline
import config

try:
    if not config.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is required. Please set it in your .env file.")
    
    from langchain_groq import ChatGroq
    llm = ChatGroq(
        api_key=config.GROQ_API_KEY,
        model_name=config.GROQ_MODEL,
        temperature=0.3
    )

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
