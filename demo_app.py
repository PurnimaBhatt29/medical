"""
MedVision AI - Simplified Demo Version
This demo shows the UI and basic functionality without requiring complex dependencies
"""

import streamlit as st
import time
from PIL import Image
import config

# Page configuration
st.set_page_config(
    page_title="MedVision AI - Medical Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #e3f2fd 0%, #f0f4f8 100%);
}

.glass-card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
    margin: 15px 0;
}

.main-header {
    background: linear-gradient(135deg, #4A90E2 0%, #50C9CE 100%);
    padding: 30px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
}

.disclaimer {
    background: #fff3cd;
    border-left: 5px solid #ffc107;
    padding: 15px;
    border-radius: 10px;
    margin: 20px 0;
}

.alert-critical {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
    color: white;
    padding: 20px;
    border-radius: 15px;
    margin: 20px 0;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def show_disclaimer():
    st.markdown(f"""
    <div class="disclaimer">
        {config.MEDICAL_DISCLAIMER}
    </div>
    """, unsafe_allow_html=True)

def home_page():
    st.markdown("""
    <div class="main-header">
        <h1>🏥 MedVision AI</h1>
        <p style="font-size: 1.2em; margin-top: 10px;">
            Advanced Multimodal RAG-based Medical Assistant (Demo Version)
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
            <h3>💊 Medical Knowledge</h3>
            <p>Query drug information and medical knowledge base</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 Demo Features
    
    This is a simplified demo version showing the UI and basic functionality.
    
    **To run the full version with AI capabilities:**
    1. Install all dependencies (see README.md)
    2. Configure API keys (.env file)
    3. Run data ingestion: `python data_ingestion.py`
    4. Launch full app: `streamlit run app.py`
    
    ### 📚 Documentation
    - **QUICK_START.md** - Get running in 5 minutes
    - **GETTING_STARTED.md** - Complete walkthrough
    - **README.md** - Full documentation
    """)

def demo_report_analyzer():
    st.markdown("""
    <div class="main-header">
        <h2>📄 Medical Report Analyzer (Demo)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    show_disclaimer()
    
    uploaded_file = st.file_uploader("Upload Medical Report (PDF)", type=['pdf'])
    
    if uploaded_file:
        if st.button("🔍 Analyze Report (Demo)", use_container_width=True):
            with st.spinner("🔄 Analyzing..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                st.success("✅ Demo Analysis Complete!")
                
                st.markdown("""
                <div class="glass-card">
                    <h3>Risk Level: <span style="color: #ffc107;">Moderate</span></h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📋 Demo Summary")
                st.info("This is a demo. The full version would analyze the PDF and provide detailed medical insights using AI.")
                
                st.markdown("### 🔍 Demo Key Findings")
                st.markdown("- Sample finding 1: Blood glucose slightly elevated")
                st.markdown("- Sample finding 2: Cholesterol within normal range")
                st.markdown("- Sample finding 3: Recommend follow-up in 3 months")

def demo_medicine_knowledge():
    st.markdown("""
    <div class="main-header">
        <h2>💊 Medicine Knowledge Base (Demo)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    show_disclaimer()
    
    st.markdown("""
    ### Ask questions about medications:
    - "Who should take Metformin?"
    - "Why is Amoxicillin prescribed?"
    - "What are the side effects of Lisinopril?"
    """)
    
    query = st.text_input("Enter your medicine-related question:", placeholder="e.g., Who should take Metformin?")
    
    if query:
        if st.button("🔍 Search (Demo)", use_container_width=True):
            with st.spinner("🔄 Searching..."):
                time.sleep(1)
                
                st.success("✅ Demo Response!")
                
                st.markdown("### 📖 Demo Answer")
                st.info("""
                This is a demo response. The full version would use Advanced RAG to retrieve 
                accurate medical information from the knowledge base.
                
                For example, if you asked about Metformin:
                - Used for Type 2 Diabetes
                - Helps control blood sugar levels
                - Common side effects: nausea, diarrhea
                - Contraindicated in severe kidney disease
                """)

def demo_chat():
    st.markdown("""
    <div class="main-header">
        <h2>💬 Medical Chat Assistant (Demo)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    show_disclaimer()
    
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
    
    user_message = st.text_input("Type your message:", key="chat_input")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        if st.button("📤 Send (Demo)", use_container_width=True):
            if user_message:
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_message
                })
                
                demo_response = "This is a demo response. The full version would provide contextual medical information using Advanced RAG and maintain conversation history."
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': demo_response
                })
                
                st.rerun()
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

def main():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1>🏥</h1>
            <h3>MedVision AI</h3>
            <p style="color: #ff6b6b;">DEMO VERSION</p>
        </div>
        """, unsafe_allow_html=True)
        
        selected = st.selectbox(
            "Navigation",
            ["Home", "Report Analyzer (Demo)", "Medicine Knowledge (Demo)", "Medical Chat (Demo)"],
            key="navigation"
        )
        
        st.markdown("---")
        
        st.markdown("""
        ### ⚠️ Demo Mode
        
        This is a simplified demo showing the UI.
        
        **For full AI capabilities:**
        1. See QUICK_START.md
        2. Install dependencies
        3. Configure API keys
        4. Run full app.py
        
        ### 📚 Documentation
        - QUICK_START.md
        - GETTING_STARTED.md
        - README.md
        """)
        
        st.markdown("---")
        st.caption("Demo Version 1.0.0")
    
    if selected == "Home":
        home_page()
    elif selected == "Report Analyzer (Demo)":
        demo_report_analyzer()
    elif selected == "Medicine Knowledge (Demo)":
        demo_medicine_knowledge()
    elif selected == "Medical Chat (Demo)":
        demo_chat()

if __name__ == "__main__":
    main()
