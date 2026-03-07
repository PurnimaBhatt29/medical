"""
MedVision AI - Multimodal RAG-based Medical Assistant
Production-ready Streamlit application with beautiful medical-themed UI
"""

import streamlit as st
from streamlit_option_menu import option_menu
import time
from PIL import Image
import config
from utils.rag_pipeline import RAGPipeline
from agents.report_analyzer_agent import ReportAnalyzerAgent
from agents.xray_vision_agent import XRayVisionAgent
from agents.prescription_analyzer_agent import PrescriptionAnalyzerAgent
from agents.medicine_knowledge_agent import MedicineKnowledgeAgent
from agents.medical_chat_agent import MedicalChatAgent
from agents.evaluation_agent import EvaluationAgent
from sentence_transformers import SentenceTransformer
import os


# Page configuration
st.set_page_config(
    page_title="MedVision AI - Medical Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful medical-themed UI
def load_custom_css():
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-blue: #4A90E2;
        --secondary-teal: #50C9CE;
        --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-bg: rgba(255, 255, 255, 0.95);
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #e3f2fd 0%, #f0f4f8 100%);
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin: 15px 0;
        color: black;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #4A90E2 0%, #50C9CE 100%);
        padding: 30px;
        border-radius: 15px;
        color: black;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
    }
    
    /* Alert boxes */
    .alert-critical {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: black;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Risk level badges */
    .risk-low { color: #28a745; font-weight: bold; }
    .risk-moderate { color: #ffc107; font-weight: bold; }
    .risk-high { color: #fd7e14; font-weight: bold; }
    .risk-critical { color: #dc3545; font-weight: bold; }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4A90E2 0%, #50C9CE 100%);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4A90E2 0%, #50C9CE 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(74, 144, 226, 0.4);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Disclaimer box */
    .disclaimer {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        color: black !important;
        font-weight: 500;
    }
    
    /* Typing animation */
    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }
    
    .typing-text {
        overflow: hidden;
        white-space: nowrap;
        animation: typing 2s steps(40);
    }
    
    /* Info box text color */
    .stAlert > div > p {
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

load_custom_css()


# Initialize session state
def init_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.chat_history = []
        st.session_state.agents_loaded = False
        st.session_state.current_page = "Home"

init_session_state()


# Initialize agents (cached)
@st.cache_resource
def initialize_agents():
    """Initialize all agents with LLM and RAG pipeline"""
    try:
        # Initialize LLM - Try Groq first, then Ollama
        llm = None
        
        if config.GROQ_API_KEY:
            try:
                from langchain_groq import ChatGroq
                llm = ChatGroq(
                    api_key=config.GROQ_API_KEY,
                    model_name=config.GROQ_MODEL,
                    temperature=0.3
                )
                st.success("✅ Using Groq API for LLM")
            except Exception as e:
                st.warning(f"⚠️ Groq initialization failed: {str(e)}")
        
        if llm is None and config.OLLAMA_BASE_URL:
            try:
                from langchain_ollama import OllamaLLM
                llm = OllamaLLM(
                    model=config.OLLAMA_MODEL,
                    base_url=config.OLLAMA_BASE_URL
                )
                st.success("✅ Using Ollama (local) for LLM")
            except Exception as e:
                st.warning(f"⚠️ Ollama initialization failed: {str(e)}")
        
        if llm is None:
            st.error("❌ No LLM configured!")
            st.info("Please configure either:\n- GROQ_API_KEY (recommended, cloud-based)\n- OLLAMA_BASE_URL (local, private)")
            st.stop()
        
        # Initialize RAG pipeline
        rag_pipeline = RAGPipeline(
            llm=llm,
            embedding_model_name=config.EMBEDDING_MODEL,
            cross_encoder_name=config.CROSS_ENCODER_MODEL,
            chroma_persist_dir=config.CHROMA_PERSIST_DIR
        )
        
        # Check if ChromaDB has data
        try:
            collection = rag_pipeline.get_or_create_collection("medical_knowledge")
            count = collection.count()
            if count == 0:
                st.warning("⚠️ Medical knowledge base is empty. Some features may not work properly.")
                st.info("To populate the database, run: `python data_ingestion.py` locally and upload the chroma_db folder.")
        except Exception as e:
            st.warning(f"⚠️ ChromaDB warning: {str(e)}")
        
        # Initialize embedding model for evaluation
        embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        
        # Initialize all agents
        agents = {
            'report_analyzer': ReportAnalyzerAgent(llm, rag_pipeline),
            'xray_vision': XRayVisionAgent(llm, rag_pipeline),
            'prescription_analyzer': PrescriptionAnalyzerAgent(llm, rag_pipeline),
            'medicine_knowledge': MedicineKnowledgeAgent(llm, rag_pipeline),
            'medical_chat': MedicalChatAgent(llm, rag_pipeline),
            'evaluation': EvaluationAgent(llm, embedding_model)
        }
        
        return agents, rag_pipeline
    
    except Exception as e:
        st.error(f"❌ Error initializing agents: {str(e)}")
        st.info("Please check your configuration and try again.")
        return None, None


# Display medical disclaimer
# def show_disclaimer():
#     st.markdown(f"""
#     <div class="disclaimer">
#         {config.MEDICAL_DISCLAIMER}
#     </div>
#     """, unsafe_allow_html=True)
def show_disclaimer():
    st.markdown(
        f'<div class="disclaimer">{config.MEDICAL_DISCLAIMER}</div>',
        unsafe_allow_html=True
    )


# Display critical alert
def show_critical_alert():
    st.markdown(
        f'<div class="alert-critical">{config.CRITICAL_ALERT}</div>', 
        unsafe_allow_html=True
        )


# Home page
def home_page():
    st.markdown("""
    <div class="main-header">
        <h1>🏥 MedVision AI</h1>
        <p style="font-size: 1.2em; margin-top: 10px;">
            Advanced Multimodal RAG-based Medical Assistant
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    show_disclaimer()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>📄 Report Analysis</h3>
            <p>Upload medical reports for comprehensive AI analysis with risk assessment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>🔬 X-ray Vision</h3>
            <p>AI-powered X-ray image analysis with medical explanations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card">
            <h3>💊 Prescription Analysis</h3>
            <p>Detailed medication information and interaction checking</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 Key Features
    
    - **Advanced RAG Architecture**: HyDE retrieval with parent-child chunking
    - **Multi-Agent System**: Specialized agents for different medical tasks
    - **Multimodal Analysis**: Text, PDF, and image processing
    - **Evaluation Metrics**: Faithfulness, relevance, and hallucination detection
    - **Medical Knowledge Base**: FDA drug labels and disease information
    
    ### 🚀 Get Started
    
    Use the sidebar to navigate to different features and start analyzing medical data!
    """)


# Report Analyzer page
def report_analyzer_page(agents):
    st.markdown("""
    <div class="main-header">
        <h2>📄 Medical Report Analyzer</h2>
    </div>
    """, unsafe_allow_html=True)
    
    show_disclaimer()
    
    uploaded_file = st.file_uploader(
        "Upload Medical Report (PDF)",
        type=['pdf'],
        help="Upload lab reports, discharge summaries, or medical documents"
    )
    
    if uploaded_file:
        if st.button("🔍 Analyze Report", use_container_width=True):
            with st.spinner("🔄 Analyzing medical report..."):
                # Progress bar
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Process report
                result = agents['report_analyzer'].process(uploaded_file)
                
                if result['status'] == 'success':
                    # Display results
                    st.success("✅ Analysis Complete!")
                    
                    # Risk level with color coding
                    risk_level = result['risk_level']
                    risk_class = f"risk-{risk_level.lower()}"
                    
                    st.markdown(f"""
                    <div class="glass-card">
                        <h3>Risk Level: <span class="{risk_class}">{risk_level}</span></h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show critical alert if needed
                    if risk_level == "Critical":
                        show_critical_alert()
                    
                    # Summary
                    st.markdown("### 📋 Summary")
                    st.info(result['summary'])
                    
                    # Key Findings
                    st.markdown("### 🔍 Key Findings")
                    for finding in result['key_findings']:
                        st.markdown(f"- {finding}")
                    
                    # Risk Explanation
                    st.markdown("### ⚠️ Risk Explanation")
                    st.warning(result['risk_explanation'])
                    
                    # Recommendations
                    st.markdown("### 💡 Recommendations")
                    for rec in result['recommendations']:
                        st.markdown(f"- {rec}")
                    
                    # Full Analysis (expandable)
                    with st.expander("📊 Full Analysis"):
                        st.write(result['full_analysis'])
                
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")


# X-ray Vision page
def xray_vision_page(agents):
    st.markdown("""
    <div class="main-header">
        <h2>🔬 X-ray Vision Analyzer</h2>
    </div>
    """, unsafe_allow_html=True)
    
    show_disclaimer()
    
    uploaded_image = st.file_uploader(
        "Upload X-ray Image",
        type=['jpg', 'jpeg', 'png'],
        help="Upload chest X-ray or other medical images"
    )
    
    if uploaded_image:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_image, caption="Uploaded X-ray", use_column_width=True)
        
        with col2:
            if st.button("🔍 Analyze X-ray", use_container_width=True):
                with st.spinner("🔄 Analyzing X-ray image..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    result = agents['xray_vision'].process(uploaded_image)
                    
                    if result['status'] == 'success':
                        st.success("✅ Analysis Complete!")
                        
                        # Primary Finding
                        st.markdown(f"""
                        <div class="glass-card">
                            <h3>Primary Finding: {result['primary_finding']}</h3>
                            <p>Confidence: {result['confidence']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Severity
                        severity = result['severity']
                        severity_class = f"risk-{severity.lower()}"
                        st.markdown(f"""
                        <div class="glass-card">
                            <h3>Severity: <span class="{severity_class}">{severity}</span></h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if severity in ["High", "Critical"]:
                            show_critical_alert()
                        
                        # Explanation
                        st.markdown("### 📖 Medical Explanation")
                        st.info(result['explanation'])
                        
                        # Recommendations
                        st.markdown("### 💡 Recommendations")
                        for rec in result['recommendations']:
                            st.markdown(f"- {rec}")
                        
                        # All Predictions
                        with st.expander("📊 All Predictions"):
                            for pred in result['all_predictions']:
                                st.write(f"- {pred['label']}: {pred['score']*100:.1f}%")
                    
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")


# Prescription Analyzer page
def prescription_analyzer_page(agents):
    st.markdown("""
    <div class="main-header">
        <h2>💊 Prescription Analyzer</h2>
    </div>
    """, unsafe_allow_html=True)
    
    show_disclaimer()
    
    uploaded_file = st.file_uploader(
        "Upload Prescription (PDF)",
        type=['pdf'],
        help="Upload prescription document"
    )
    
    if uploaded_file:
        if st.button("🔍 Analyze Prescription", use_container_width=True):
            with st.spinner("🔄 Analyzing prescription..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                result = agents['prescription_analyzer'].process(uploaded_file)
                
                if result['status'] == 'success':
                    st.success("✅ Analysis Complete!")
                    
                    # Overall Assessment
                    st.markdown("### 📋 Overall Assessment")
                    st.info(result['overall_assessment'])
                    
                    # Medications
                    st.markdown(f"### 💊 Medications ({result['total_medications']})")
                    
                    for med in result['medications']:
                        with st.expander(f"📌 {med['name']} - {med['dosage']}"):
                            st.markdown(f"**Frequency:** {med['frequency']}")
                            st.markdown(f"**Indications:** {med['indications']}")
                            st.markdown(f"**Contraindications:** {med['contraindications']}")
                            st.markdown(f"**Side Effects:** {med['side_effects']}")
                            
                            if med['warnings']:
                                st.warning(f"⚠️ {med['warnings']}")
                    
                    # Warnings
                    if result['warnings']:
                        st.markdown("### ⚠️ Important Warnings")
                        for warning in result['warnings']:
                            st.warning(warning)
                    
                    # Interactions
                    st.markdown("### 🔄 Drug Interactions")
                    st.info(result['interactions'])
                
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")


# Medicine Knowledge page
def medicine_knowledge_page(agents):
    st.markdown("""
    <div class="main-header">
        <h2>💊 Medicine Knowledge Base</h2>
    </div>
    """, unsafe_allow_html=True)
    
    show_disclaimer()
    
    st.markdown("""
    ### Ask questions about medications:
    - "Who should take Metformin?"
    - "Why is Amoxicillin prescribed?"
    - "What are the side effects of Lisinopril?"
    - "What is the dosage for Atorvastatin?"
    """)
    
    query = st.text_input("Enter your medicine-related question:", placeholder="e.g., Who should take Metformin?")
    
    if query:
        if st.button("🔍 Search Knowledge Base", use_container_width=True):
            with st.spinner("🔄 Searching medical knowledge base..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                result = agents['medicine_knowledge'].process(query)
                
                if result['status'] == 'success':
                    st.success("✅ Information Retrieved!")
                    
                    # Query Type
                    st.markdown(f"""
                    <div class="glass-card">
                        <p><strong>Query Type:</strong> {result['query_type'].replace('_', ' ').title()}</p>
                        <p><strong>Confidence:</strong> {result['confidence']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Answer
                    st.markdown("### 📖 Answer")
                    st.info(result['answer'])
                    
                    # Disclaimer
                    st.warning(result['disclaimer'])
                
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")


# Medical Chat page
def medical_chat_page(agents):
    st.markdown("""
    <div class="main-header">
        <h2>💬 Medical Chat Assistant</h2>
    </div>
    """, unsafe_allow_html=True)
    
    show_disclaimer()
    
    # Chat history display
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="glass-card" style="background: #e3f2fd;">
                    <strong>You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="glass-card" style="background: #f1f8e9;">
                    <strong>MedVision AI:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    user_message = st.text_input("Type your message:", key="chat_input", placeholder="Ask me anything about medical topics...")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        if st.button("📤 Send", use_container_width=True):
            if user_message:
                # Add user message to history
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_message
                })
                
                with st.spinner("🤔 Thinking..."):
                    # Simulate typing animation
                    time.sleep(0.5)
                    
                    result = agents['medical_chat'].process(user_message)
                    
                    if result['status'] == 'success':
                        # Add assistant response to history
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'content': result['response']
                        })
                        
                        # Show alert if urgent
                        if result['urgency'] == 'emergency':
                            show_critical_alert()
                        
                        st.rerun()
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_history = []
            agents['medical_chat'].clear_history()
            st.rerun()


# Evaluation page
def evaluation_page(agents, rag_pipeline):
    st.markdown("""
    <div class="main-header">
        <h2>📊 Response Evaluation</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Evaluate RAG Response Quality
    Test the system's response quality with various metrics including faithfulness, relevance, and hallucination detection.
    """)
    
    query = st.text_area("Enter test query:", placeholder="e.g., What are the side effects of Metformin?")
    # allow user to optionally specify ground‑truth contexts for retrieval metrics
    relevant_input = st.text_area(
        "Ground-truth relevant contexts (one per line, optional)",
        placeholder="Copy/paste short text snippets from the retrieved contexts (not doc IDs) that should be considered relevant"
    )
    relevant_list = [line.strip() for line in relevant_input.splitlines() if line.strip()]
    
    if query:
        if st.button("🔍 Generate & Evaluate Response", use_container_width=True):
            with st.spinner("🔄 Generating and evaluating response..."):
                progress_bar = st.progress(0)
                
                # Generate response
                progress_bar.progress(30)
                response = rag_pipeline.query_with_rag(
                    query=query,
                    collection_name="medical_knowledge",
                    system_prompt="You are a medical AI assistant.",
                    top_k=config.TOP_K_RERANK
                )
                
                # Get retrieved contexts (simplified)
                progress_bar.progress(60)
                retriever = rag_pipeline.create_hyde_retriever("medical_knowledge")
                docs = retriever.retrieve(query, top_k=5, rerank_top_k=5)
                contexts = [doc.page_content for doc in docs]
                
                # Debug: Check if contexts were retrieved
                if not contexts:
                    st.warning("⚠️ No contexts retrieved from knowledge base. Metrics may be inaccurate.")
                else:
                    st.success(f"✅ Retrieved {len(contexts)} context chunks for evaluation")
                
                # Evaluate
                progress_bar.progress(90)
                # pass ground truth contexts if any
                kwargs = {}
                if relevant_list:
                    kwargs['relevant_contexts'] = relevant_list
                result = agents['evaluation'].process(query, response, contexts, **kwargs)
                progress_bar.progress(100)
                
                if result['status'] == 'success':
                    st.success("✅ Evaluation Complete!")
                    
                    # Display response
                    st.markdown("### 💬 Generated Response")
                    st.info(response)
                    
                    # Debug info
                    with st.expander("🔍 Debug Info"):
                        st.write(f"Query length: {len(query)} chars")
                        st.write(f"Response length: {len(response)} chars")
                        st.write(f"Contexts retrieved: {len(contexts)}")
                        st.write(f"First context preview: {contexts[0][:200] if contexts else 'EMPTY'}...")
                    
                    # Metrics
                    st.markdown("### 📊 Evaluation Metrics")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Faithfulness Score")
                        st.progress(result['faithfulness_score'])
                        st.write(f"{result['faithfulness_score']*100:.1f}%")
                        
                        st.markdown("#### Context Precision")
                        st.progress(result['context_precision'])
                        st.write(f"{result['context_precision']*100:.1f}%")
                        
                        # show retrieval metrics (these are computed only with ground truth snippets)
                        st.markdown("#### Retrieval Metrics")
                        st.caption("ℹ️ These metrics require ground-truth contexts (see input above)")

                        st.markdown("**Precision**")
                        st.progress(result.get('precision', 0.0))
                        st.write(f"{result.get('precision', 0.0)*100:.1f}%")

                        st.markdown("**Recall**")
                        st.progress(result.get('recall', 0.0))
                        st.write(f"{result.get('recall', 0.0)*100:.1f}%")

                        st.markdown("**MRR**")
                        st.write(f"{result.get('mrr', 0.0):.3f}")

                        if not result.get('retrieval_metrics_computed', False):
                            st.info(
                                "💡 To compute Precision, Recall, and MRR: Copy relevant text snippets from the retrieved contexts and paste them in the 'Ground-truth relevant contexts' field above, then re-run the evaluation."
                            )
                    
                    with col2:
                        st.markdown("#### Relevance Score")
                        st.progress(result['relevance_score'])
                        st.write(f"{result['relevance_score']*100:.1f}%")
                        
                        st.markdown("#### Hallucination Risk")
                        st.progress(result['hallucination_risk'])
                        st.write(f"{result['hallucination_risk']*100:.1f}%")
                    
                    # Overall Confidence
                    st.markdown("### 🎯 Overall Confidence")
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <h1 style="color: #4A90E2;">{result['confidence_percentage']:.1f}%</h1>
                        <h3>Quality Grade: {result['quality_grade']}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Summary
                    st.markdown("### 📝 Evaluation Summary")
                    st.info(result['summary'])
                    
                    # Metrics Explanation
                    with st.expander("ℹ️ Understanding the Metrics"):
                        for metric, explanation in result['metrics_explanation'].items():
                            st.markdown(f"**{metric.title()}:** {explanation}")
                    
                    # Show retrieved contexts
                    with st.expander("📚 Retrieved Contexts Used for Evaluation"):
                        if contexts:
                            for i, ctx in enumerate(contexts, 1):
                                st.markdown(f"**Context {i}:**")
                                st.text(ctx[:500] + "..." if len(ctx) > 500 else ctx)
                                st.divider()
                        else:
                            st.warning("No contexts were retrieved.")
                
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")


# Main application
def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1>🏥</h1>
            <h3>MedVision AI</h3>
        </div>
        """, unsafe_allow_html=True)
        
        selected = st.selectbox(
            "Navigation",
            ["Home", "Report Analyzer", "X-ray Vision", "Prescription Analyzer", 
             "Medicine Knowledge", "Medical Chat", "Evaluation"],
            key="navigation"
        )
        
        st.markdown("---")
        
        st.markdown("""
        ### About
        MedVision AI is an advanced multimodal RAG-based medical assistant powered by:
        - 🤖 Agent-based architecture
        - 🔍 HyDE retrieval strategy
        - 📚 Parent-child chunking
        - 🎯 Cross-encoder reranking
        - 📊 Comprehensive evaluation
        """)
        
        st.markdown("---")
        st.caption("Version 1.0.0 | © 2024 MedVision AI")
    
    # Initialize agents
    if not st.session_state.agents_loaded:
        with st.spinner("🔄 Loading AI models and agents..."):
            agents, rag_pipeline = initialize_agents()
            if agents:
                st.session_state.agents = agents
                st.session_state.rag_pipeline = rag_pipeline
                st.session_state.agents_loaded = True
            else:
                st.error("Failed to initialize agents. Please check configuration.")
                return
    
    agents = st.session_state.agents
    rag_pipeline = st.session_state.rag_pipeline
    
    # Route to selected page
    if selected == "Home":
        home_page()
    elif selected == "Report Analyzer":
        report_analyzer_page(agents)
    elif selected == "X-ray Vision":
        xray_vision_page(agents)
    elif selected == "Prescription Analyzer":
        prescription_analyzer_page(agents)
    elif selected == "Medicine Knowledge":
        medicine_knowledge_page(agents)
    elif selected == "Medical Chat":
        medical_chat_page(agents)
    elif selected == "Evaluation":
        evaluation_page(agents, rag_pipeline)


if __name__ == "__main__":
    main()
