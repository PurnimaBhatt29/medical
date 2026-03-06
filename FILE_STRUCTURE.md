# 📁 MedVision AI - Complete File Structure

## Project Tree

```
medvision-ai/
│
├── 📂 agents/                              # Agent implementations
│   ├── __init__.py                         # Package initialization
│   ├── base_agent.py                       # Abstract BaseAgent class
│   ├── report_analyzer_agent.py            # Medical report analysis
│   ├── xray_vision_agent.py                # X-ray image analysis
│   ├── prescription_analyzer_agent.py      # Prescription analysis
│   ├── medicine_knowledge_agent.py         # Medicine Q&A
│   ├── medical_chat_agent.py               # Conversational AI
│   └── evaluation_agent.py                 # Response evaluation
│
├── 📂 utils/                               # Utility modules
│   ├── __init__.py                         # Package initialization
│   ├── pdf_processor.py                    # PDF text extraction
│   ├── text_processing.py                  # Chunking & cleaning
│   └── rag_pipeline.py                     # HyDE + RAG implementation
│
├── 📄 app.py                               # Main Streamlit application
├── 📄 config.py                            # Configuration settings
├── 📄 data_ingestion.py                    # Dataset preprocessing
├── 📄 run.py                               # Quick start script
├── 📄 test_system.py                       # System tests
├── 📄 generate_sample_data.py              # Sample PDF generator
│
├── 📄 requirements.txt                     # Python dependencies
├── 📄 .env.example                         # Environment template
├── 📄 .gitignore                           # Git ignore rules
│
├── 📚 README.md                            # Main documentation
├── 📚 QUICK_START.md                       # 5-minute setup guide
├── 📚 SETUP_GUIDE.md                       # Detailed setup
├── 📚 PROJECT_OVERVIEW.md                  # Architecture & design
└── 📚 FILE_STRUCTURE.md                    # This file
```

## File Descriptions

### 🎯 Core Application Files

#### `app.py` (Main Application)
- **Purpose**: Streamlit web application
- **Features**:
  - Beautiful medical-themed UI
  - Sidebar navigation
  - 6 main pages (Home, Report, X-ray, Prescription, Knowledge, Chat, Evaluation)
  - Agent initialization and caching
  - Custom CSS styling
  - Progress indicators
  - Risk level visualization
- **Lines**: ~400
- **Dependencies**: streamlit, agents, utils, config

#### `config.py` (Configuration)
- **Purpose**: Centralized configuration
- **Contains**:
  - API keys and endpoints
  - Model names
  - Chunking parameters
  - Retrieval settings
  - Vector store paths
  - Medical disclaimers
- **Lines**: ~50
- **Easy to modify**: Change models, parameters, etc.

#### `data_ingestion.py` (Data Pipeline)
- **Purpose**: Preprocess and index medical datasets
- **Features**:
  - FDA drug label fetching
  - Medical conditions data
  - Parent-child chunking
  - Embedding generation
  - ChromaDB storage
  - Progress tracking
- **Lines**: ~300
- **Must run before**: First application launch

### 🤖 Agent Files

#### `agents/base_agent.py` (Base Class)
- **Purpose**: Abstract base class for all agents
- **Defines**:
  - Common structure (llm, retriever)
  - Abstract process() method
  - Logging functionality
- **Lines**: ~30
- **Pattern**: Template method pattern

#### `agents/report_analyzer_agent.py`
- **Purpose**: Analyze medical PDF reports
- **Process**:
  1. Extract text from PDF
  2. Clean medical text
  3. Parent-child chunking
  4. Store in vector DB
  5. RAG-based analysis
  6. Risk assessment
  7. Structured output
- **Lines**: ~200
- **Output**: Summary, findings, risk level, recommendations

#### `agents/xray_vision_agent.py`
- **Purpose**: Analyze X-ray images
- **Process**:
  1. Load image
  2. Vision model inference
  3. Extract predictions
  4. RAG for explanation
  5. Severity assessment
  6. Recommendations
- **Lines**: ~150
- **Models**: HuggingFace chest X-ray classifier

#### `agents/prescription_analyzer_agent.py`
- **Purpose**: Analyze prescriptions
- **Process**:
  1. Extract text from PDF
  2. Parse medications
  3. RAG for each medication
  4. Check interactions
  5. Extract warnings
- **Lines**: ~180
- **Output**: Medication details, interactions, warnings

#### `agents/medicine_knowledge_agent.py`
- **Purpose**: Answer medicine queries
- **Process**:
  1. Classify query type
  2. Enhance query
  3. RAG retrieval
  4. Generate answer
  5. Confidence estimation
- **Lines**: ~120
- **Query types**: Indication, dosage, side effects, etc.

#### `agents/medical_chat_agent.py`
- **Purpose**: Conversational medical AI
- **Process**:
  1. Maintain conversation history
  2. Build context
  3. RAG with context
  4. Urgency detection
  5. Response generation
- **Lines**: ~100
- **Features**: Memory, context, urgency alerts

#### `agents/evaluation_agent.py`
- **Purpose**: Evaluate response quality (including optional retrieval performance)
- **Metrics**:
  - Faithfulness score
  - Relevance score
  - Context precision
  - Hallucination risk
  - Overall confidence
  - (*optional*) Retrieval precision, recall, MRR when ground‑truth is supplied
- **Lines**: ~170
- **Method**: Embedding similarity + LLM evaluation; simple string matching for retrieval metrics

### 🛠️ Utility Files

#### `utils/pdf_processor.py`
- **Purpose**: PDF text extraction
- **Functions**:
  - extract_text_from_pdf()
  - extract_pdf_metadata()
  - split_pdf_by_pages()
- **Lines**: ~80
- **Library**: PyPDF2

#### `utils/text_processing.py`
- **Purpose**: Text preprocessing
- **Functions**:
  - clean_medical_text()
  - parent_child_chunking()
  - extract_medical_entities()
- **Lines**: ~100
- **Features**: Regex cleaning, chunking, entity extraction

#### `utils/rag_pipeline.py`
- **Purpose**: Complete RAG implementation
- **Classes**:
  - HyDERetriever: HyDE retrieval strategy
  - RAGPipeline: Full pipeline orchestration
- **Lines**: ~200
- **Features**: HyDE, reranking, ChromaDB integration

### 🚀 Utility Scripts

#### `run.py` (Quick Start)
- **Purpose**: Check prerequisites and launch app
- **Checks**:
  - Python version
  - Dependencies
  - Environment file
  - Knowledge base
- **Lines**: ~100
- **Usage**: `python run.py`

#### `test_system.py` (System Tests)
- **Purpose**: Test all components
- **Tests**:
  - Package imports
  - Configuration
  - Utility modules
  - Agent modules
  - RAG pipeline
  - ChromaDB
  - LLM connection
- **Lines**: ~250
- **Usage**: `python test_system.py`

#### `generate_sample_data.py` (Sample Generator)
- **Purpose**: Create sample medical PDFs
- **Generates**:
  - sample_medical_report.pdf
  - sample_prescription.pdf
- **Lines**: ~200
- **Requires**: reportlab library

### 📚 Documentation Files

#### `README.md` (Main Documentation)
- **Sections**:
  - Features overview
  - Installation guide
  - Usage instructions
  - Project structure
  - Configuration
  - Troubleshooting
- **Length**: Comprehensive
- **Audience**: All users

#### `QUICK_START.md` (5-Minute Guide)
- **Purpose**: Get running fast
- **Sections**:
  - Installation (3 min)
  - Configuration (1 min)
  - Data setup (1 min)
  - Launch
  - Quick test
- **Length**: Concise
- **Audience**: Impatient users

#### `SETUP_GUIDE.md` (Detailed Setup)
- **Purpose**: Step-by-step setup
- **Sections**:
  - System requirements
  - Installation steps
  - Configuration options
  - Data ingestion
  - Testing
  - Troubleshooting
- **Length**: Detailed
- **Audience**: First-time users

#### `PROJECT_OVERVIEW.md` (Architecture)
- **Purpose**: Technical deep dive
- **Sections**:
  - Architecture diagram
  - Implementation details
  - Performance characteristics
  - Security considerations
  - Future enhancements
- **Length**: Comprehensive
- **Audience**: Developers

#### `FILE_STRUCTURE.md` (This File)
- **Purpose**: File organization reference
- **Sections**:
  - Project tree
  - File descriptions
  - Line counts
  - Dependencies
- **Audience**: Contributors

### ⚙️ Configuration Files

#### `requirements.txt`
- **Purpose**: Python dependencies
- **Packages**: 15+ packages
- **Key dependencies**:
  - streamlit==1.32.0
  - langchain==0.1.16
  - chromadb==0.4.24
  - sentence-transformers==2.6.1
  - transformers==4.39.3

#### `.env.example`
- **Purpose**: Environment template
- **Variables**:
  - GROQ_API_KEY
  - OLLAMA_BASE_URL
  - HF_TOKEN
- **Usage**: Copy to `.env` and fill in

#### `.gitignore`
- **Purpose**: Git ignore rules
- **Ignores**:
  - Python cache
  - Virtual environments
  - ChromaDB data
  - Environment files
  - IDE files
  - OS files

## File Statistics

### Total Files: 25

#### By Category:
- **Agent files**: 8 (base + 6 specialized + 1 evaluation)
- **Utility files**: 4 (3 modules + 1 init)
- **Core application**: 3 (app, config, ingestion)
- **Scripts**: 3 (run, test, generate)
- **Documentation**: 5 (README, guides, overview)
- **Configuration**: 3 (requirements, env, gitignore)

#### By Type:
- **Python files**: 16
- **Markdown files**: 5
- **Config files**: 3
- **Init files**: 2

### Total Lines of Code: ~2,500

#### Breakdown:
- **Agents**: ~900 lines
- **Utils**: ~400 lines
- **App**: ~400 lines
- **Scripts**: ~550 lines
- **Config**: ~100 lines
- **Documentation**: ~2,000 lines

## Dependencies Between Files

```
app.py
├── config.py
├── agents/
│   ├── base_agent.py
│   ├── report_analyzer_agent.py
│   │   ├── utils/pdf_processor.py
│   │   ├── utils/text_processing.py
│   │   └── utils/rag_pipeline.py
│   ├── xray_vision_agent.py
│   │   └── utils/rag_pipeline.py
│   ├── prescription_analyzer_agent.py
│   │   ├── utils/pdf_processor.py
│   │   └── utils/rag_pipeline.py
│   ├── medicine_knowledge_agent.py
│   │   └── utils/rag_pipeline.py
│   ├── medical_chat_agent.py
│   │   └── utils/rag_pipeline.py
│   └── evaluation_agent.py
└── utils/
    ├── pdf_processor.py
    ├── text_processing.py
    └── rag_pipeline.py

data_ingestion.py
├── config.py
├── utils/text_processing.py
└── utils/rag_pipeline.py

run.py
└── (standalone)

test_system.py
├── config.py
├── agents/*
└── utils/*

generate_sample_data.py
└── (standalone, requires reportlab)
```

## How to Navigate This Project

### For Users:
1. Start with `QUICK_START.md`
2. Read `README.md` for full features
3. Use `SETUP_GUIDE.md` if issues arise

### For Developers:
1. Read `PROJECT_OVERVIEW.md` for architecture
2. Check `FILE_STRUCTURE.md` (this file)
3. Review `config.py` for settings
4. Explore `agents/` for agent implementations
5. Study `utils/rag_pipeline.py` for RAG details

### For Contributors:
1. Read all documentation
2. Run `test_system.py` to verify setup
3. Check `.gitignore` before committing
4. Follow existing code patterns
5. Update documentation for changes

## File Modification Guide

### To Add a New Agent:
1. Create `agents/new_agent.py`
2. Extend `BaseAgent`
3. Implement `process()` method
4. Import in `app.py`
5. Add UI page in `app.py`

### To Add a New Dataset:
1. Add ingestion logic to `data_ingestion.py`
2. Update `config.py` if needed
3. Run ingestion script
4. Test with agents

### To Modify UI:
1. Edit `app.py`
2. Update CSS in `load_custom_css()`
3. Modify page functions
4. Test responsiveness

### To Change Models:
1. Update `config.py`
2. Modify agent initialization
3. Test compatibility
4. Update documentation

## Maintenance Checklist

### Regular Tasks:
- [ ] Update dependencies in `requirements.txt`
- [ ] Re-run `data_ingestion.py` for fresh data
- [ ] Clear `chroma_db/` if corrupted
- [ ] Update API keys in `.env`
- [ ] Run `test_system.py` after changes

### Before Deployment:
- [ ] Test all features
- [ ] Check error handling
- [ ] Verify documentation
- [ ] Update version numbers
- [ ] Review security settings

---

**This file structure supports a production-ready, maintainable, and scalable medical AI application.**
