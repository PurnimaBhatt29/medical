import PyPDF2
from typing import List, Dict
import io


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from PDF file using PyPDF2.
    
    Args:
        pdf_file: File object, bytes, or Streamlit UploadedFile
        
    Returns:
        Extracted text
    """
    try:
        # Handle different input types
        if isinstance(pdf_file, bytes):
            pdf_file = io.BytesIO(pdf_file)
        elif hasattr(pdf_file, 'read'):
            # Handle file-like objects (including Streamlit UploadedFile)
            # Read the content and convert to BytesIO
            content = pdf_file.read()
            if isinstance(content, str):
                content = content.encode('utf-8')
            pdf_file = io.BytesIO(content)
        
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")


def extract_pdf_metadata(pdf_file) -> Dict:
    """
    Extract metadata from PDF.
    
    Args:
        pdf_file: File object, bytes, or Streamlit UploadedFile
        
    Returns:
        Dictionary of metadata
    """
    try:
        if isinstance(pdf_file, bytes):
            pdf_file = io.BytesIO(pdf_file)
        elif hasattr(pdf_file, 'read'):
            # Handle file-like objects (including Streamlit UploadedFile)
            content = pdf_file.read()
            if isinstance(content, str):
                content = content.encode('utf-8')
            pdf_file = io.BytesIO(content)
        
        reader = PyPDF2.PdfReader(pdf_file)
        metadata = {
            "num_pages": len(reader.pages),
            "title": reader.metadata.title if reader.metadata else None,
            "author": reader.metadata.author if reader.metadata else None,
            "creator": reader.metadata.creator if reader.metadata else None,
        }
        
        return metadata
    
    except Exception as e:
        return {"error": str(e)}


def split_pdf_by_pages(pdf_file) -> List[str]:
    """
    Extract text from each page separately.
    
    Args:
        pdf_file: File object, bytes, or Streamlit UploadedFile
        
    Returns:
        List of text per page
    """
    try:
        if isinstance(pdf_file, bytes):
            pdf_file = io.BytesIO(pdf_file)
        elif hasattr(pdf_file, 'read'):
            # Handle file-like objects (including Streamlit UploadedFile)
            content = pdf_file.read()
            if isinstance(content, str):
                content = content.encode('utf-8')
            pdf_file = io.BytesIO(content)
        
        reader = PyPDF2.PdfReader(pdf_file)
        pages = []
        
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            pages.append(f"[Page {i+1}]\n{page_text}")
        
        return pages
    
    except Exception as e:
        raise Exception(f"PDF page splitting failed: {str(e)}")
