# 🏥 MedVision AI - Multimodal RAG-based Medical Assistant

A production-ready, advanced medical AI assistant built with Streamlit, featuring multimodal analysis capabilities, agent-based architecture, and state-of-the-art RAG (Retrieval-Augmented Generation) techniques.

## ✨ Features

### 🎯 Core Capabilities
- **📄 Medical Report Analysis**: Analyze lab reports and discharge summaries with risk assessment
- **🔬 X-ray Vision**: AI-powered medical image analysis with explanations
- **💊 Prescription Analysis**: Extract medication details and check interactions
- **📚 Medicine Knowledge Base**: Query drug information, indications, and contraindications
- **💬 Medical Chat**: Contextual conversations with memory-based retrieval
- **📊 Evaluation Metrics**: Faithfulness, relevance, and hallucination detection

### 🏗️ Architecture Highlights
- **Agent-Based Design**: Specialized agents (BaseAgent → ReportAnalyzer, XRayVision, etc.)
- **Advanced RAG**: HyDE retrieval + parent-child chunking + cross-encoder reranking
- **Multimodal Processing**: Text (PDF), images (X-rays), and conversational queries
- **Vector Database**: ChromaDB with persistent storage
- **LLM Integration**: Groq cloud API for fast inference

### 🎨 Beautiful UI
- Medical-themed design with soft blue/teal/white gradients
- Glassmorphism-inspired cards
- Animated loading indicators
- Responsive layout
- Risk-level color coding
- Critical alerts for urgent conditions

## 📋 Prerequisites

- Python 3.9+
- Groq API key (free)
- 8GB+ RAM recommended
- Internet connection for initial model downloads

## 🚀 Installation

### 1. Get the Project
Download the project folder and navigate to it in your terminal.

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# Groq API (required)
GROQ_API_KEY=your_groq_api_key_here

# Optional: HuggingFace token for private models
HF_TOKEN=your_huggingface_token_here
```

## 📊 Data Ingestion (REQUIRED)

Before running the application, you MUST ingest medical datasets:

```bash
python data_ingestion.py
```

This script will:
- Download FDA drug label data
- Process medical conditions information
- Apply parent-child chunking
- Generate embeddings
- Store in ChromaDB vector database

**Expected output:**
```
STARTING MEDICAL KNOWLEDGE BASE INGESTION
==========================================
INGESTING FDA DRUG LABELS
✓ Successfully ingested 250 FDA drug label sections

INGESTING MEDICAL CONDITIONS DATA
✓ Successfully ingested 5 medical condition documents

INGESTION COMPLETE!
Vector database location: ./chroma_db
```

## 🎮 Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Report Analyzer
- Navigate to "Report Analyzer"
- Upload a medical PDF report
- Click "Analyze Report"
- View risk level, findings, and recommendations

### 2. X-ray Vision
- Navigate to "X-ray Vision"
- Upload an X-ray image (JPG/PNG)
- Click "Analyze X-ray"
- View detected conditions and explanations

### 3. Prescription Analyzer
- Navigate to "Prescription Analyzer"
- Upload prescription PDF
- Click "Analyze Prescription"
- View medication details and interactions

### 4. Medicine Knowledge
- Navigate to "Medicine Knowledge"
- Ask questions like:
  - "Who should take Metformin?"
  - "Why is Amoxicillin prescribed?"
  - "What are the side effects of Lisinopril?"

### 5. Medical Chat
- Navigate to "Medical Chat"
- Have contextual conversations
- System maintains conversation history
- Automatic urgency detection

### 6. Evaluation
- Navigate to "Evaluation"
- Enter a test query
- Optionally provide ground-truth relevant context snippets (one per line) to compute retrieval metrics
- View quality metrics:
  - Faithfulness score
  - Relevance score
  - Context precision
  - Hallucination risk
  - Overall confidence
  - **[when ground truth provided]** Retrieval Precision, Recall, and MRR

## 🏗️ Project Structure

```
medvision-ai/
├── agents/
│   ├── base_agent.py              # Base agent class
│   ├── report_analyzer_agent.py   # Report analysis
│   ├── xray_vision_agent.py       # X-ray analysis
│   ├── prescription_analyzer_agent.py
│   ├── medicine_knowledge_agent.py
│   ├── medical_chat_agent.py
│   └── evaluation_agent.py
├── utils/
│   ├── pdf_processor.py           # PDF extraction
│   ├── text_processing.py         # Chunking & cleaning
│   └── rag_pipeline.py            # HyDE + RAG
├── app.py                         # Streamlit UI
├── config.py                      # Configuration
├── data_ingestion.py              # Dataset ingestion
├── requirements.txt               # Dependencies
├── .env.example                   # Environment template
└── README.md                      # This file
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VISION_MODEL = "nickmuchi/vit-finetuned-chest-xray-pneumonia"
OLLAMA_MODEL = "llama3"
GROQ_MODEL = "llama3-70b-8192"

# Chunking Configuration
PARENT_CHUNK_SIZE = 1000
CHILD_CHUNK_SIZE = 200

# Retrieval Configuration
TOP_K_RETRIEVAL = 10
TOP_K_RERANK = 5
```

## 🧪 Advanced RAG Pipeline

### HyDE Retrieval Strategy
1. Generate hypothetical answer using LLM
2. Embed hypothetical answer
3. Perform similarity search in vector database
4. Apply cross-encoder reranking
5. Pass top-k chunks to LLM for final response

### Parent-Child Chunking
- **Parent chunks**: 1000 tokens (context)
- **Child chunks**: 200 tokens (retrieval)
- Maintains context while enabling precise retrieval

### Evaluation Metrics
- **Faithfulness**: Response grounded in retrieved context
- **Relevance**: Response relevance to query
- **Context Precision**: Quality of retrieved context
- **Hallucination Risk**: Risk of fabricated information
- **Confidence**: Overall quality score

## ⚠️ Medical Disclaimer

**IMPORTANT**: This AI assistant is for informational and educational purposes only. It does NOT replace professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical decisions.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational purposes. Consult legal requirements for medical AI applications in your jurisdiction.

## 🐛 Troubleshooting

### Issue: "Failed to initialize agents"
- **Solution**: Check `.env` file configuration
- Verify Groq API key is correct
- Ensure internet connection is working

### Issue: "No documents found in knowledge base"
- **Solution**: Run `python data_ingestion.py` first

### Issue: "Vision model not loading"
- **Solution**: Check internet connection for HuggingFace downloads
- Model will download on first use (~500MB)

### Issue: "ChromaDB errors"
- **Solution**: Delete `./chroma_db` folder and re-run ingestion

## 📞 Support

For issues and questions:
- Check documentation
- Review configuration settings
- Consult the troubleshooting section

## 🎯 Roadmap

- [ ] OCR support for prescription images
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Integration with EHR systems
- [ ] Mobile app version
- [ ] Real-time collaboration features

---

**Built with ❤️ using Streamlit, LangChain, and HuggingFace**
