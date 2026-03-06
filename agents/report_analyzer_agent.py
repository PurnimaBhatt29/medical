from typing import Dict, Any
from agents.base_agent import BaseAgent
from utils.pdf_processor import extract_text_from_pdf
from utils.text_processing import clean_medical_text, parent_child_chunking, extract_medical_entities
from utils.rag_pipeline import RAGPipeline
import config
import uuid


class ReportAnalyzerAgent(BaseAgent):
    """
    Specialized agent for analyzing medical PDF reports.
    Implements parent-child chunking, HyDE retrieval, and structured output.
    """
    
    def __init__(self, llm, rag_pipeline: RAGPipeline):
        super().__init__(llm=llm)
        self.rag_pipeline = rag_pipeline
        self.collection_name = "medical_reports"
    
    def process(self, pdf_file, **kwargs) -> Dict[str, Any]:
        """
        Process medical PDF report.
        
        Args:
            pdf_file: Uploaded PDF file
            **kwargs: Additional parameters
            
        Returns:
            Structured analysis results
        """
        self._log("Starting report analysis...")
        
        try:
            # Step 1: Extract text from PDF
            self._log("Extracting text from PDF...")
            raw_text = extract_text_from_pdf(pdf_file)
            
            # Step 2: Clean medical text
            self._log("Cleaning medical text...")
            cleaned_text = clean_medical_text(raw_text)
            
            # Step 3: Extract medical entities
            entities = extract_medical_entities(cleaned_text)
            
            # Step 4: Parent-child chunking
            self._log("Applying parent-child chunking...")
            chunks = parent_child_chunking(
                cleaned_text,
                parent_size=config.PARENT_CHUNK_SIZE,
                child_size=config.CHILD_CHUNK_SIZE,
                overlap=config.CHUNK_OVERLAP
            )
            
            # Step 5: Store in vector database
            self._log("Storing chunks in vector database...")
            doc_id = str(uuid.uuid4())
            
            all_child_chunks = []
            all_metadata = []
            all_ids = []
            
            for parent_idx, (parent, children) in enumerate(chunks):
                for child_idx, child in enumerate(children):
                    all_child_chunks.append(child)
                    all_metadata.append({
                        "doc_id": doc_id,
                        "parent_idx": parent_idx,
                        "child_idx": child_idx,
                        "parent_text": parent[:200],  # Store snippet of parent
                        "source": "uploaded_report"
                    })
                    all_ids.append(f"{doc_id}_p{parent_idx}_c{child_idx}")
            
            # Add to temporary collection for this session
            temp_collection = f"temp_report_{doc_id[:8]}"
            self.rag_pipeline.add_documents(
                collection_name=temp_collection,
                documents=all_child_chunks,
                metadatas=all_metadata,
                ids=all_ids
            )
            
            # Step 6: Generate analysis using RAG
            self._log("Generating comprehensive analysis...")
            
            analysis_query = f"""Analyze this medical report and provide:
1. Summary of the report
2. Key findings and abnormalities
3. Risk level assessment (Low/Moderate/High/Critical)
4. Recommendations

Report preview: {cleaned_text[:1000]}"""
            
            system_prompt = """You are a medical AI assistant analyzing patient reports. 
Provide accurate, structured analysis based on the retrieved medical knowledge and report content.
Be precise and highlight any concerning findings."""
            
            analysis_response = self.rag_pipeline.query_with_rag(
                query=analysis_query,
                collection_name=temp_collection,
                system_prompt=system_prompt,
                top_k=config.TOP_K_RERANK
            )
            
            # Step 7: Determine risk level
            risk_level = self._assess_risk_level(analysis_response, entities)
            
            # Step 8: Structure output
            result = {
                "status": "success",
                "summary": self._extract_summary(analysis_response),
                "key_findings": self._extract_findings(analysis_response, entities),
                "risk_level": risk_level,
                "risk_explanation": self._extract_risk_explanation(analysis_response),
                "recommendations": self._extract_recommendations(analysis_response),
                "entities": entities,
                "full_analysis": analysis_response,
                "temp_collection": temp_collection
            }
            
            self._log("Report analysis completed successfully")
            return result
            
        except Exception as e:
            self._log(f"Error during report analysis: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "summary": "Failed to analyze report",
                "risk_level": "Unknown"
            }
    
    def _assess_risk_level(self, analysis: str, entities: dict) -> str:
        """Assess risk level from analysis"""
        analysis_lower = analysis.lower()
        
        critical_keywords = ["critical", "emergency", "severe", "urgent", "immediate attention"]
        high_keywords = ["high risk", "abnormal", "elevated", "concerning", "significant"]
        moderate_keywords = ["moderate", "mild", "slightly elevated", "monitor"]
        
        if any(keyword in analysis_lower for keyword in critical_keywords):
            return "Critical"
        elif any(keyword in analysis_lower for keyword in high_keywords):
            return "High"
        elif any(keyword in analysis_lower for keyword in moderate_keywords):
            return "Moderate"
        else:
            return "Low"
    
    def _extract_summary(self, analysis: str) -> str:
        """Extract summary from analysis"""
        lines = analysis.split('\n')
        summary_lines = []
        capture = False
        
        for line in lines:
            if 'summary' in line.lower():
                capture = True
                continue
            if capture and line.strip():
                if any(keyword in line.lower() for keyword in ['finding', 'risk', 'recommendation']):
                    break
                summary_lines.append(line.strip())
        
        return ' '.join(summary_lines) if summary_lines else analysis[:300]
    
    def _extract_findings(self, analysis: str, entities: dict) -> list:
        """Extract key findings"""
        findings = []
        
        # Extract from analysis
        lines = analysis.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['finding', 'abnormal', 'detected', 'observed']):
                findings.append(line.strip())
        
        # Add entity-based findings
        if entities.get('medications'):
            findings.append(f"Medications mentioned: {', '.join(set(entities['medications'][:5]))}")
        
        return findings[:5] if findings else ["No specific findings extracted"]
    
    def _extract_risk_explanation(self, analysis: str) -> str:
        """Extract risk explanation"""
        lines = analysis.split('\n')
        for i, line in enumerate(lines):
            if 'risk' in line.lower():
                return ' '.join(lines[i:i+3])
        return "Risk assessment based on report analysis"
    
    def _extract_recommendations(self, analysis: str) -> list:
        """Extract recommendations"""
        lines = analysis.split('\n')
        recommendations = []
        capture = False
        
        for line in lines:
            if 'recommendation' in line.lower():
                capture = True
                continue
            if capture and line.strip():
                if line.strip().startswith(('-', '•', '*')):
                    recommendations.append(line.strip())
        
        return recommendations[:5] if recommendations else ["Consult with healthcare provider for detailed recommendations"]
