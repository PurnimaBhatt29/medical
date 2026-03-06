import re
from typing import List, Tuple
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

def clean_medical_text(text: str) -> str:
    """
    Clean medical text by removing noise and normalizing.
    
    Args:
        text: Raw medical text
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep medical symbols
    text = re.sub(r'[^\w\s\.\,\-\:\;\(\)\%\/\+\°]', '', text)
    
    # Normalize medical abbreviations spacing
    text = re.sub(r'(\d+)\s*(mg|ml|mcg|g|kg|mmol|IU)', r'\1\2', text)
    
    # Remove page numbers and headers/footers
    text = re.sub(r'Page\s+\d+', '', text, flags=re.IGNORECASE)
    
    return text.strip()


def parent_child_chunking(text: str, parent_size: int = 1000, 
                         child_size: int = 200, overlap: int = 50) -> List[Tuple[str, List[str]]]:
    """
    Implement parent-child chunking strategy.
    
    Args:
        text: Input text to chunk
        parent_size: Size of parent chunks (tokens)
        child_size: Size of child chunks (tokens)
        overlap: Overlap between chunks
        
    Returns:
        List of tuples (parent_chunk, [child_chunks])
    """
    # Create parent chunks
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=parent_size * 4,  # Approximate tokens to chars
        chunk_overlap=overlap * 4,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    parent_chunks = parent_splitter.split_text(text)
    
    # Create child chunks for each parent
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=child_size * 4,
        chunk_overlap=overlap * 2,
        separators=["\n", ". ", " ", ""]
    )
    
    result = []
    for parent in parent_chunks:
        child_chunks = child_splitter.split_text(parent)
        result.append((parent, child_chunks))
    
    return result


def extract_medical_entities(text: str) -> dict:
    """
    Extract key medical entities from text.
    
    Args:
        text: Medical text
        
    Returns:
        Dictionary of extracted entities
    """
    entities = {
        "medications": [],
        "dosages": [],
        "conditions": [],
        "lab_values": []
    }
    
    # Extract dosages (e.g., 500mg, 10ml)
    dosage_pattern = r'\d+\.?\d*\s*(mg|ml|mcg|g|kg|mmol|IU|units?)'
    entities["dosages"] = re.findall(dosage_pattern, text, re.IGNORECASE)
    
    # Extract common medication patterns
    med_pattern = r'\b[A-Z][a-z]+(?:in|ol|ide|ate|cin|xin|pril|sartan)\b'
    entities["medications"] = re.findall(med_pattern, text)
    
    # Extract lab values (e.g., WBC: 12.5, Glucose: 110)
    lab_pattern = r'([A-Z]{2,}|[A-Z][a-z]+)\s*:?\s*(\d+\.?\d*)'
    entities["lab_values"] = re.findall(lab_pattern, text)
    
    return entities
