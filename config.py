import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")

# Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VISION_MODEL = "nickmuchi/vit-finetuned-chest-xray-pneumonia"
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
GROQ_MODEL = "llama-3.3-70b-versatile"

# Chunking Configuration
PARENT_CHUNK_SIZE = 1000
CHILD_CHUNK_SIZE = 200
CHUNK_OVERLAP = 50

# Retrieval Configuration
TOP_K_RETRIEVAL = 10
TOP_K_RERANK = 5
SIMILARITY_THRESHOLD = 0.5

# Vector Store Configuration
CHROMA_PERSIST_DIR = "./chroma_db"
TEMP_CHROMA_DIR = "./temp_chroma_db"

# Dataset URLs
FDA_DRUG_LABELS_URL = "https://api.fda.gov/drug/label.json"
MEDLINEPLUS_BASE_URL = "https://medlineplus.gov/xml.html"

# Medical Disclaimer
MEDICAL_DISCLAIMER = """
⚠️ **MEDICAL DISCLAIMER**: This AI assistant is for informational purposes only and does NOT replace professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical decisions.
"""

CRITICAL_ALERT = """
🚨 **CRITICAL ALERT**: Potential serious medical condition detected. 
**SEEK IMMEDIATE MEDICAL ATTENTION** from qualified healthcare professionals.
"""
