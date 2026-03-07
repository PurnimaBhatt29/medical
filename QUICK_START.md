# ⚡ MedVision AI - Quick Start Guide

Get up and running in 5 minutes!

## 🚀 Installation (3 minutes)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration (1 minute)

### Option A: Groq (Recommended - Fast & Free)

1. Get API key: [console.groq.com](https://console.groq.com)
2. Create `.env` file:
```bash
cp .env.example .env
```
3. Add your key:
```env
GROQ_API_KEY=gsk_your_key_here
```

## 📊 Data Setup (1 minute)

```bash
python data_ingestion.py
```

Wait for: "INGESTION COMPLETE!"

## 🎮 Launch

```bash
streamlit run app.py
```

Browser opens at: `http://localhost:8501`

## ✅ Quick Test

1. Go to "Medicine Knowledge"
2. Ask: "Who should take Metformin?"
3. Click "Search Knowledge Base"
4. See AI response!

## 🎯 Features to Try

### 1. Report Analyzer
- Upload medical PDF
- Get risk assessment
- View findings

### 2. X-ray Vision
- Upload chest X-ray
- Get AI diagnosis
- See explanation

### 3. Prescription Analyzer
- Upload prescription PDF
- Get medication info
- Check interactions

### 4. Medical Chat
- Ask medical questions
- Contextual conversation
- Memory-based responses

### 5. Evaluation
- Test query quality
- View metrics
- Check confidence

## 🐛 Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Failed to initialize agents"
- Check `.env` file exists
- Verify GROQ_API_KEY is correct

### "ChromaDB not found"
```bash
python data_ingestion.py
```

### "Port already in use"
```bash
streamlit run app.py --server.port 8502
```

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup
- Check [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for architecture

## 🎉 That's It!

You're ready to use MedVision AI!

---

**Need Help?**
- Run system test: `python test_system.py`
- Check configuration: `cat .env`
- View logs in terminal

**Pro Tips:**
- Use Groq for fastest responses
- Generate sample data: `python generate_sample_data.py`
- Clear cache: Delete `chroma_db/` folder
