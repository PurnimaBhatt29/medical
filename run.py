"""
Quick start script for MedVision AI
Checks prerequisites and launches the application
"""

import os
import sys
import subprocess


def check_python_version():
    """Check if Python version is 3.9+"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    return True


def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("⚠️ .env file not found")
        print("Creating .env from template...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✓ .env file created. Please edit it with your API keys.")
            return False
        else:
            print("❌ .env.example not found")
            return False
    print("✓ .env file exists")
    return True


def check_chroma_db():
    """Check if ChromaDB has been initialized"""
    if not os.path.exists('chroma_db'):
        print("⚠️ Medical knowledge base not found")
        print("\nYou need to run data ingestion first:")
        print("  python data_ingestion.py")
        return False
    print("✓ Medical knowledge base found")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit
        import langchain
        import chromadb
        import sentence_transformers
        print("✓ Core dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        return False


def main():
    print("=" * 60)
    print("MedVision AI - Quick Start")
    print("=" * 60)
    print()
    
    # Run checks
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Knowledge Base", check_chroma_db),
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✓ All checks passed!")
        print("\nLaunching MedVision AI...")
        print("=" * 60)
        print()
        
        # Launch Streamlit
        subprocess.run(["streamlit", "run", "app.py"])
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nQuick Setup Guide:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure .env file with your API keys")
        print("3. Run data ingestion: python data_ingestion.py")
        print("4. Launch app: python run.py")


if __name__ == "__main__":
    main()
