# 🚀 MedVision AI - Complete Setup Guide

This guide will walk you through setting up MedVision AI from scratch.

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Data Ingestion](#data-ingestion)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **Python**: 3.9 or higher
- **RAM**: 8GB (16GB recommended)
- **Storage**: 5GB free space
- **Internet**: Required for initial setup

### Recommended Setup
- **RAM**: 16GB+
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster inference)
- **Storage**: 10GB+ free space

## 🔧 Installation Steps

### Step 1: Install Python

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer and check "Add Python to PATH"
3. Verify: `python --version`

**macOS:**
```bash
brew install python@3.11
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### Step 2: Clone or Download Project

```bash
# Navigate to the project directory
cd medvision-ai
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- Streamlit (UI framework)
- LangChain (RAG orchestration)
- ChromaDB (vector database)
- Sentence Transformers (embeddings)
- Transformers (vision models)
- PyPDF2 (PDF processing)
- And more...

**Installation time**: 5-10 minutes depending on internet speed.

## ⚙️ Configuration

### Option 1: Using Groq (Recommended - Fast & Cloud-based)

1. Get Groq API key:
   - Visit [console.groq.com](https://console.groq.com)
   - Sign up for free account
   - Create API key

2. Configure `.env`:
```bash
cp .env.example .env
```

3. Edit `.env`:
```env
GROQ_API_KEY=gsk_your_actual_api_key_here
HF_TOKEN=
```

## 📊 Data Ingestion

**CRITICAL**: You MUST run data ingestion before using the application.

### Run Ingestion Script

```bash
python data_ingestion.py
```

### What Happens During Ingestion:

1. **Downloads FDA Drug Labels** (50 drugs)
   - Indications, contraindications, dosages, warnings
   - ~2-3 minutes

2. **Processes Medical Conditions** (5 conditions)
   - Diabetes, Hypertension, Pneumonia, GERD, Infections
   - ~30 seconds

3. **Applies Parent-Child Chunking**
   - Parent: 1000 tokens
   - Child: 200 tokens

4. **Generates Embeddings**
   - Uses sentence-transformers/all-MiniLM-L6-v2
   - ~2-3 minutes

5. **Stores in ChromaDB**
   - Creates `./chroma_db` directory
   - Persistent vector database

### Expected Output:

```
STARTING MEDICAL KNOWLEDGE BASE INGESTION
==========================================

INGESTING FDA DRUG LABELS
Fetching FDA drug labels (limit: 50)...
Retrieved 50 drug labels
Processing drug labels: 100%|████████| 50/50
Adding 250 documents to vector database...
✓ Successfully ingested 250 FDA drug label sections

INGESTING MEDICAL CONDITIONS DATA
✓ Successfully ingested 5 medical condition documents

==========================================
INGESTION COMPLETE!
==========================================

Medical knowledge base is ready.
Vector database location: ./chroma_db

You can now run the Streamlit application:
  streamlit run app.py
```

### Troubleshooting Ingestion:

**Issue**: FDA API timeout
- **Solution**: Script will automatically use sample data

**Issue**: Out of memory
- **Solution**: Reduce batch size in `data_ingestion.py`

**Issue**: ChromaDB errors
- **Solution**: Delete `./chroma_db` and re-run

## 🎮 Running the Application

### Method 1: Quick Start Script (Recommended)

```bash
python run.py
```

This script will:
- Check Python version
- Verify dependencies
- Check .env configuration
- Verify knowledge base exists
- Launch Streamlit app

### Method 2: Direct Launch

```bash
streamlit run app.py
```

### First Launch:

1. **Model Downloads** (first time only):
   - Embedding model: ~90MB
   - Cross-encoder: ~80MB
   - Vision model: ~500MB
   - Total: ~670MB
   - Time: 5-10 minutes

2. **Application Loads**:
   - Initializes agents
   - Loads vector database
   - Ready in ~30 seconds

3. **Browser Opens**:
   - Default: `http://localhost:8501`
   - If port busy, Streamlit will use next available port

## 🧪 Testing the Application

### Test 1: Medicine Knowledge

1. Navigate to "Medicine Knowledge"
2. Enter: "Who should take Metformin?"
3. Click "Search Knowledge Base"
4. Verify response about diabetes patients

### Test 2: Medical Chat

1. Navigate to "Medical Chat"
2. Type: "What is hypertension?"
3. Send message
4. Verify contextual response

### Test 3: Evaluation

1. Navigate to "Evaluation"
2. Enter: "What are the side effects of Lisinopril?"
3. Click "Generate & Evaluate Response"
4. Verify metrics display:
   - Faithfulness score
   - Relevance score
   - Confidence percentage

### Test 4: Report Analyzer (with sample PDF)

1. Create a sample medical report PDF
2. Navigate to "Report Analyzer"
3. Upload PDF
4. Click "Analyze Report"
5. Verify structured output

## 🐛 Troubleshooting

### Issue: "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: "Failed to initialize agents"
```bash
# Check .env file
cat .env  # Linux/Mac
type .env  # Windows

# Test Groq API key
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

### Issue: "ChromaDB not found"
```bash
# Re-run ingestion
python data_ingestion.py
```

### Issue: "Port already in use"
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Issue: "Out of memory"
```bash
# Reduce batch size in config.py
TOP_K_RETRIEVAL = 5  # Instead of 10
TOP_K_RERANK = 3     # Instead of 5
```

### Issue: "Vision model not loading"
```bash
# Pre-download model
python -c "from transformers import AutoModel; AutoModel.from_pretrained('nickmuchi/vit-finetuned-chest-xray-pneumonia')"
```

## 🔒 Security Considerations

1. **API Keys**: Never commit `.env` to version control
2. **Data Privacy**: Medical data stays local (except LLM API calls)
3. **HIPAA Compliance**: This is a demo - not HIPAA compliant
4. **Production Use**: Requires additional security measures

## 📈 Performance Optimization

### For Faster Inference:

1. **Check Internet**: Ensure stable connection to Groq
2. **GPU Acceleration**: Install CUDA for PyTorch
3. **Reduce Retrieval**: Lower `TOP_K_RETRIEVAL` in config
4. **Cache Results**: Streamlit caching is enabled

### For Lower Memory:

1. **Smaller Models**: Use smaller embedding models
2. **Reduce Batch Size**: Process fewer documents at once
3. **Clear Cache**: Delete `./chroma_db` periodically

## 🎯 Next Steps

1. ✅ Complete setup
2. ✅ Run data ingestion
3. ✅ Test all features
4. 📚 Read main README.md
5. 🔧 Customize configuration
6. 🚀 Deploy to production (if needed)

## 📞 Getting Help

- **Documentation**: See README.md
- **Configuration**: Review config.py
- **Logs**: Check terminal output
- **Troubleshooting**: See GETTING_STARTED.md

---

**Setup complete! Enjoy using MedVision AI! 🎉**
