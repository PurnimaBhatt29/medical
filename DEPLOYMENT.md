# 🚀 Deployment Guide for Streamlit Cloud

## Quick Deploy

1. **Fork/Clone this repository** to your GitHub account

2. **Go to Streamlit Cloud**: https://share.streamlit.io/

3. **Click "New app"**

4. **Configure:**
   - Repository: `PurnimaBhatt29/medical`
   - Branch: `main`
   - Main file path: `app.py`

5. **Add Secrets** (Click "Advanced settings" → "Secrets"):
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   HF_TOKEN = "your_huggingface_token_here"
   ```

6. **Deploy!**

## Important Notes

### ⚠️ ChromaDB Database

The vector database (`chroma_db/`) is NOT included in the repository (too large). 

**Options:**

**Option 1: Limited Functionality (Quick Deploy)**
- Deploy without the database
- X-ray Vision and Report Analyzer will work
- Medicine Knowledge and Chat features will have limited functionality

**Option 2: Full Functionality (Recommended)**
1. Run `python data_ingestion.py` locally
2. Upload the generated `chroma_db/` folder to a cloud storage (Google Drive, S3, etc.)
3. Modify the app to download the database on startup
4. Or use Streamlit's file upload feature

### 📦 Large Model Files

The app downloads these models on first run (~500MB total):
- Sentence Transformers embedding model
- Cross-encoder model  
- Vision model for X-ray analysis

**First deployment will take 5-10 minutes** to download and cache these models.

### 🔑 Required Secrets

Add these in Streamlit Cloud secrets:

```toml
# Required
GROQ_API_KEY = "gsk_your_actual_groq_api_key"

# Optional (for private HuggingFace models)
HF_TOKEN = "hf_your_huggingface_token"
```

### 💾 Memory Requirements

This app requires:
- **Minimum**: 2GB RAM (basic features)
- **Recommended**: 4GB RAM (all features)

Streamlit Cloud free tier provides 1GB RAM, which may cause issues with all models loaded simultaneously.

**Solutions:**
- Use Streamlit Cloud paid tier
- Deploy on other platforms (Heroku, Railway, Render)
- Optimize by lazy-loading models

## Alternative Deployment Platforms

### Railway
```bash
railway login
railway init
railway up
```

### Render
1. Connect your GitHub repo
2. Select "Web Service"
3. Build command: `pip install -r requirements.txt`
4. Start command: `streamlit run app.py --server.port $PORT`

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

## Troubleshooting

### "Module not found" errors
- Check `requirements.txt` has all dependencies
- Streamlit Cloud may need to rebuild

### "Out of memory" errors
- Reduce model sizes in `config.py`
- Use lighter models
- Upgrade to paid tier

### "API key not found" errors
- Verify secrets are added correctly in Streamlit Cloud
- Check secret names match exactly (case-sensitive)

### Models downloading slowly
- First deployment is slow (5-10 min)
- Subsequent runs use cached models

## Performance Tips

1. **Use st.cache_resource** for model loading (already implemented)
2. **Lazy load** heavy models only when needed
3. **Reduce batch sizes** for inference
4. **Use lighter models** for embedding/vision if needed

## Support

For deployment issues:
- Check Streamlit Cloud logs
- Review error messages in the app
- Ensure all secrets are configured
- Verify internet connectivity for model downloads
