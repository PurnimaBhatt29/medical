# 🚀 Getting Started with MedVision AI

## Welcome to MedVision AI!

This guide will walk you through everything you need to know to get MedVision AI up and running.

## 📋 What You'll Need

Before starting, make sure you have:
- ✅ Computer with Windows, Mac, or Linux
- ✅ Python 3.9 or higher installed
- ✅ 8GB+ RAM (16GB recommended)
- ✅ 5GB free disk space
- ✅ Internet connection
- ✅ Either Groq API key (free) OR Ollama installed

## 🎯 Choose Your Path

### Path A: Quick Start (5 minutes) ⚡
For users who want to get running fast.
→ See [QUICK_START.md](QUICK_START.md)

### Path B: Detailed Setup (15 minutes) 📚
For users who want to understand each step.
→ See [SETUP_GUIDE.md](SETUP_GUIDE.md)

### Path C: This Guide (10 minutes) 🎓
Balanced approach with explanations.
→ Continue reading below

## 📦 Step 1: Get the Code

### Option 1: Download ZIP
1. Download the project ZIP file
2. Extract to a folder (e.g., `C:\medvision-ai` or `~/medvision-ai`)
3. Open terminal/command prompt in that folder

### Option 2: Git Clone
```bash
git clone <repository-url>
cd medvision-ai
```

## 🐍 Step 2: Set Up Python Environment

### Check Python Version
```bash
python --version
```
Should show 3.9 or higher. If not, install from [python.org](https://python.org).

### Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will take 5-10 minutes. It installs:
- Streamlit (web framework)
- LangChain (RAG orchestration)
- ChromaDB (vector database)
- Sentence Transformers (embeddings)
- Transformers (vision models)
- And more...

## 🔑 Step 3: Configure API Keys

You need either Groq (recommended) OR Ollama (local).

### Option A: Groq (Recommended - Fast & Free)

**Why Groq?**
- ✅ Very fast inference (~1-2 seconds)
- ✅ Free tier available
- ✅ No local installation needed
- ✅ Cloud-based

**Setup:**
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for free account
3. Create API key
4. Copy the key (starts with `gsk_`)

**Configure:**
```bash
# Copy template
cp .env.example .env

# Edit .env file
# Add your Groq API key:
GROQ_API_KEY=gsk_your_actual_key_here
```

### Option B: Ollama (Local & Private)

**Why Ollama?**
- ✅ Runs locally (private)
- ✅ No API costs
- ✅ Works offline
- ✅ Full control

**Setup:**
1. Install Ollama:
   - **Windows/Mac**: Download from [ollama.ai](https://ollama.ai)
   - **Linux**: `curl -fsSL https://ollama.ai/install.sh | sh`

2. Pull model:
```bash
ollama pull llama3
```

3. Verify:
```bash
ollama list
```

**Configure:**
```bash
# Copy template
cp .env.example .env

# Edit .env file
# Leave GROQ_API_KEY empty
# Ensure OLLAMA_BASE_URL is set:
OLLAMA_BASE_URL=http://localhost:11434
```

### Option C: Both (Best of Both Worlds)

Configure both Groq and Ollama. The system will use Groq by default if API key is present, but fall back to Ollama if needed.

## 📊 Step 4: Load Medical Knowledge

**CRITICAL**: You MUST run this before using the app!

```bash
python data_ingestion.py
```

**What happens:**
1. Downloads FDA drug labels (50 drugs)
2. Processes medical conditions (5 conditions)
3. Cleans and chunks text
4. Generates embeddings
5. Stores in ChromaDB

**Expected output:**
```
STARTING MEDICAL KNOWLEDGE BASE INGESTION
==========================================

INGESTING FDA DRUG LABELS
Fetching FDA drug labels (limit: 50)...
Retrieved 50 drug labels
Processing drug labels: 100%|████████| 50/50
✓ Successfully ingested 250 FDA drug label sections

INGESTING MEDICAL CONDITIONS DATA
✓ Successfully ingested 5 medical condition documents

==========================================
INGESTION COMPLETE!
==========================================
```

**Time**: 3-5 minutes

**Note**: If FDA API fails, the script automatically uses sample data.

## 🎮 Step 5: Launch the Application

```bash
streamlit run app.py
```

**What happens:**
1. Streamlit starts web server
2. Models download (first time only, ~670MB)
3. Agents initialize
4. Browser opens automatically

**URL**: `http://localhost:8501`

**First launch**: Takes ~1 minute for model downloads

## 🧪 Step 6: Test the System

### Test 1: Medicine Knowledge (Easiest)

1. Click "Medicine Knowledge" in sidebar
2. Type: `Who should take Metformin?`
3. Click "Search Knowledge Base"
4. Wait 2-5 seconds
5. ✅ You should see detailed answer about diabetes patients

**If this works, your system is configured correctly!**

### Test 2: Medical Chat

1. Click "Medical Chat" in sidebar
2. Type: `What is hypertension?`
3. Click "Send"
4. ✅ You should see explanation about high blood pressure

### Test 3: Evaluation

1. Click "Evaluation" in sidebar
2. Type: `What are the side effects of Lisinopril?`
3. Click "Generate & Evaluate Response"
4. ✅ You should see:
   - Generated response
   - Faithfulness score
   - Relevance score
   - Confidence percentage

### Test 4: Report Analyzer (Requires PDF)

**Option A: Use Sample Data**
```bash
# Generate sample PDFs
pip install reportlab
python generate_sample_data.py
```

Then:
1. Click "Report Analyzer"
2. Upload `sample_medical_report.pdf`
3. Click "Analyze Report"
4. ✅ See analysis with risk level

**Option B: Use Your Own PDF**
- Upload any medical report PDF
- System will extract and analyze text

## 🎨 Step 7: Explore Features

### Home Page
- Overview of features
- Medical disclaimer
- Navigation guide

### Report Analyzer
- Upload medical reports
- Get risk assessment
- View findings and recommendations
- See structured analysis

### X-ray Vision
- Upload chest X-ray images
- Get AI classification
- View medical explanation
- See severity assessment

### Prescription Analyzer
- Upload prescription PDFs
- Extract medication details
- Check drug interactions
- View warnings

### Medicine Knowledge
- Ask about medications
- Query indications, dosages, side effects
- Get evidence-based answers
- See confidence scores

### Medical Chat
- Have conversations
- Ask follow-up questions
- Context-aware responses
- Urgency detection

### Evaluation
- Test response quality
- View detailed metrics
- Understand confidence scores
- Check for hallucinations

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: "Failed to initialize agents"
**Cause**: API key or Ollama not configured

**Solution:**
1. Check `.env` file exists
2. Verify API key is correct
3. If using Ollama, ensure it's running: `ollama list`

### Issue: "ChromaDB not found"
**Cause**: Data ingestion not run

**Solution:**
```bash
python data_ingestion.py
```

### Issue: "Port already in use"
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Issue: "Out of memory"
**Solution:**
1. Close other applications
2. Reduce batch size in `config.py`:
```python
TOP_K_RETRIEVAL = 5  # Instead of 10
```

### Issue: "Vision model not loading"
**Solution:**
```bash
# Pre-download model
python -c "from transformers import AutoModel; AutoModel.from_pretrained('nickmuchi/vit-finetuned-chest-xray-pneumonia')"
```

### Issue: "Slow responses"
**Solution:**
1. Use Groq instead of Ollama (much faster)
2. Reduce `TOP_K_RETRIEVAL` in `config.py`
3. Close other applications

## 🔍 Understanding the System

### How RAG Works

1. **Your Query**: "What are side effects of Metformin?"
2. **HyDE**: System generates hypothetical answer
3. **Embedding**: Converts to vector
4. **Search**: Finds similar documents in database
5. **Rerank**: Sorts by relevance
6. **Generate**: Creates final answer using top documents

### How Agents Work

Each agent is specialized:
- **Report Analyzer**: Extracts and analyzes medical reports
- **X-ray Vision**: Classifies medical images
- **Prescription Analyzer**: Parses medication information
- **Medicine Knowledge**: Answers drug-related questions
- **Medical Chat**: Maintains conversation context
- **Evaluation**: Assesses response quality

### How Knowledge Base Works

1. **Ingestion**: Medical data preprocessed
2. **Chunking**: Split into parent (1000) and child (200) tokens
3. **Embedding**: Converted to vectors
4. **Storage**: Saved in ChromaDB
5. **Retrieval**: Searched during queries

## 📚 Next Steps

### Learn More
- Read [README.md](README.md) for full documentation
- Check [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for architecture
- Review [FILE_STRUCTURE.md](FILE_STRUCTURE.md) for code organization

### Customize
- Edit `config.py` to change models
- Modify `app.py` to adjust UI
- Add new agents in `agents/` folder
- Extend knowledge base in `data_ingestion.py`

### Deploy
- Use Streamlit Cloud for easy deployment
- Deploy to AWS/GCP/Azure for production
- Configure HTTPS and authentication
- Set up monitoring and logging

## 🎯 Quick Reference

### Start Application
```bash
streamlit run app.py
```

### Run Tests
```bash
python test_system.py
```

### Generate Samples
```bash
python generate_sample_data.py
```

### Re-ingest Data
```bash
python data_ingestion.py
```

### Quick Start
```bash
python run.py
```

## ⚠️ Important Reminders

1. **Medical Disclaimer**: This is NOT a replacement for professional medical advice
2. **Data Privacy**: Medical data is processed locally (except LLM API calls)
3. **Not HIPAA Compliant**: This is a demo system
4. **Educational Use**: For learning and demonstration purposes
5. **Verify Information**: Always consult healthcare professionals

## 🎉 You're Ready!

Congratulations! You now have a fully functional medical AI assistant.

### What You Can Do:
- ✅ Analyze medical reports
- ✅ Classify X-ray images
- ✅ Parse prescriptions
- ✅ Query medicine information
- ✅ Chat about medical topics
- ✅ Evaluate response quality

### Get Help:
- Check documentation files
- Run `python test_system.py`
- Review error messages
- Check terminal logs

### Have Fun:
- Explore all features
- Test with different inputs
- Customize the system
- Learn about medical AI

---

**Welcome to the future of medical AI assistance!** 🏥🤖

*Questions? Check the documentation or run system tests.*
