from typing import Dict, Any
from agents.base_agent import BaseAgent
from utils.pdf_processor import extract_text_from_pdf
from utils.text_processing import clean_medical_text
import re
import config


class PrescriptionAnalyzerAgent(BaseAgent):
    """
    Specialized agent for analyzing prescriptions.
    Extracts medication details and queries RAG for comprehensive information.
    """
    
    def __init__(self, llm, rag_pipeline):
        super().__init__(llm=llm)
        self.rag_pipeline = rag_pipeline
    
    def process(self, prescription_file, **kwargs) -> Dict[str, Any]:
        """
        Process prescription document.
        
        Args:
            prescription_file: Uploaded prescription file (PDF or image)
            **kwargs: Additional parameters
            
        Returns:
            Structured prescription analysis
        """
        self._log("Starting prescription analysis...")
        
        try:
            # Step 1: Extract text
            self._log("Extracting text from prescription...")
            text = self._extract_prescription_text(prescription_file)
            
            # Step 2: Parse prescription details
            self._log("Parsing prescription details...")
            medications = self._parse_medications(text)
            
            if not medications:
                return {
                    "status": "error",
                    "error": "No medications detected in prescription",
                    "medications": []
                }
            
            # Step 3: Analyze each medication using RAG
            self._log("Analyzing medications using knowledge base...")
            analyzed_medications = []
            
            for med in medications:
                med_analysis = self._analyze_medication(med)
                analyzed_medications.append(med_analysis)
            
            # Step 4: Generate overall assessment
            overall_assessment = self._generate_overall_assessment(analyzed_medications)
            
            # Step 5: Structure output
            result = {
                "status": "success",
                "medications": analyzed_medications,
                "total_medications": len(analyzed_medications),
                "overall_assessment": overall_assessment,
                "warnings": self._extract_warnings(analyzed_medications),
                "interactions": self._check_interactions(analyzed_medications)
            }
            
            self._log("Prescription analysis completed successfully")
            return result
            
        except Exception as e:
            self._log(f"Error during prescription analysis: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "medications": []
            }
    
    def _extract_prescription_text(self, file) -> str:
        """Extract text from prescription file"""
        try:
            # Try PDF extraction first
            text = extract_text_from_pdf(file)
            return clean_medical_text(text)
        except:
            # If PDF fails, could implement OCR here
            # For now, return empty string
            return ""
    
    def _parse_medications(self, text: str) -> list:
        """Parse medication details from text"""
        medications = []
        
        # Common medication name patterns
        med_pattern = r'\b([A-Z][a-z]+(?:in|ol|ide|ate|cin|xin|pril|sartan|mine|zole|mycin))\b'
        med_names = re.findall(med_pattern, text)
        
        # Dosage patterns
        dosage_pattern = r'(\d+\.?\d*\s*(?:mg|ml|mcg|g|units?))'
        dosages = re.findall(dosage_pattern, text)
        
        # Frequency patterns
        frequency_pattern = r'(once|twice|thrice|\d+\s*times?)\s*(?:daily|per day|a day)'
        frequencies = re.findall(frequency_pattern, text, re.IGNORECASE)
        
        # Combine extracted information
        for i, med_name in enumerate(set(med_names)):
            medication = {
                "name": med_name,
                "dosage": dosages[i] if i < len(dosages) else "Not specified",
                "frequency": frequencies[i] if i < len(frequencies) else "Not specified",
                "raw_text": text[max(0, text.find(med_name)-50):text.find(med_name)+100]
            }
            medications.append(medication)
        
        return medications
    
    def _analyze_medication(self, medication: dict) -> dict:
        """Analyze single medication using RAG"""
        med_name = medication['name']
        
        query = f"""Provide comprehensive information about the medication {med_name}:
1. What is {med_name} used for? (Indications)
2. Who should take {med_name}? (Target population)
3. Who should NOT take {med_name}? (Contraindications)
4. Common side effects
5. Special warnings for elderly, pregnant women, or children
6. Typical dosage ranges"""
        
        system_prompt = """You are a pharmaceutical AI assistant providing medication information.
Base your response on verified medical knowledge from the database.
Always emphasize consulting healthcare providers."""
        
        analysis = self.rag_pipeline.query_with_rag(
            query=query,
            collection_name="medical_knowledge",
            system_prompt=system_prompt,
            top_k=config.TOP_K_RERANK
        )
        
        return {
            **medication,
            "indications": self._extract_section(analysis, "used for", "indication"),
            "contraindications": self._extract_section(analysis, "should not", "contraindication"),
            "side_effects": self._extract_section(analysis, "side effect"),
            "warnings": self._extract_section(analysis, "warning", "caution"),
            "full_analysis": analysis
        }
    
    def _extract_section(self, text: str, *keywords) -> str:
        """Extract specific section from analysis"""
        lines = text.split('\n')
        section_lines = []
        capture = False
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in keywords):
                capture = True
                section_lines.append(line.strip())
                continue
            if capture:
                if line.strip() and not line.strip().startswith(('#', '-', '•')):
                    if any(stop in line_lower for stop in ['dosage', 'interaction', 'storage']):
                        break
                section_lines.append(line.strip())
        
        return ' '.join(section_lines[:3]) if section_lines else "Information not available"
    
    def _generate_overall_assessment(self, medications: list) -> str:
        """Generate overall prescription assessment"""
        if not medications:
            return "No medications to assess"
        
        assessment = f"Prescription contains {len(medications)} medication(s). "
        
        has_warnings = any("warning" in med.get("warnings", "").lower() for med in medications)
        if has_warnings:
            assessment += "⚠️ Some medications have important warnings. "
        
        assessment += "Consult your healthcare provider about proper usage, timing, and potential interactions."
        
        return assessment
    
    def _extract_warnings(self, medications: list) -> list:
        """Extract all warnings from medications"""
        warnings = []
        for med in medications:
            med_warnings = med.get("warnings", "")
            if med_warnings and "not available" not in med_warnings.lower():
                warnings.append(f"{med['name']}: {med_warnings[:200]}")
        return warnings[:5]
    
    def _check_interactions(self, medications: list) -> str:
        """Check for potential drug interactions"""
        if len(medications) < 2:
            return "Single medication - no interaction check needed"
        
        med_names = [med['name'] for med in medications]
        
        query = f"""Are there any known drug interactions between these medications: {', '.join(med_names)}?
Provide specific interaction warnings if any exist."""
        
        try:
            interaction_info = self.rag_pipeline.query_with_rag(
                query=query,
                collection_name="medical_knowledge",
                system_prompt="You are a pharmaceutical AI checking drug interactions.",
                top_k=3
            )
            return interaction_info
        except:
            return "Interaction check unavailable - consult pharmacist"
