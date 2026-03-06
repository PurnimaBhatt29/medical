from typing import Dict, Any
from agents.base_agent import BaseAgent
import config


class MedicineKnowledgeAgent(BaseAgent):
    """
    Specialized agent for answering medicine-related queries.
    Handles questions about indications, contraindications, dosage, etc.
    """
    
    def __init__(self, llm, rag_pipeline):
        super().__init__(llm=llm)
        self.rag_pipeline = rag_pipeline
    
    def process(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Process medicine knowledge query.
        
        Args:
            query: User question about medicine
            **kwargs: Additional parameters
            
        Returns:
            Structured answer with sources
        """
        self._log(f"Processing medicine query: {query[:100]}...")
        
        try:
            # Step 1: Classify query type
            query_type = self._classify_query(query)
            
            # Step 2: Build enhanced query based on type
            enhanced_query = self._enhance_query(query, query_type)
            
            # Step 3: Retrieve and generate answer using RAG
            self._log("Retrieving information from medical knowledge base...")
            
            system_prompt = self._get_system_prompt(query_type)
            
            answer = self.rag_pipeline.query_with_rag(
                query=enhanced_query,
                collection_name="medical_knowledge",
                system_prompt=system_prompt,
                top_k=config.TOP_K_RERANK
            )
            
            # Step 4: Structure output
            result = {
                "status": "success",
                "query": query,
                "query_type": query_type,
                "answer": answer,
                "confidence": self._estimate_confidence(answer),
                "sources": "Medical knowledge database",
                "disclaimer": "This information is for educational purposes. Consult healthcare providers for medical advice."
            }
            
            self._log("Medicine query processed successfully")
            return result
            
        except Exception as e:
            self._log(f"Error processing medicine query: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "query": query,
                "answer": "Unable to process query"
            }
    
    def _classify_query(self, query: str) -> str:
        """Classify the type of medicine query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["who should take", "who can take", "suitable for"]):
            return "target_population"
        elif any(word in query_lower for word in ["why", "used for", "prescribed for", "indication"]):
            return "indication"
        elif any(word in query_lower for word in ["dosage", "dose", "how much", "how many"]):
            return "dosage"
        elif any(word in query_lower for word in ["side effect", "adverse", "reaction"]):
            return "side_effects"
        elif any(word in query_lower for word in ["contraindication", "should not", "avoid", "warning"]):
            return "contraindication"
        elif any(word in query_lower for word in ["interaction", "combine", "together with"]):
            return "interaction"
        else:
            return "general"
    
    def _enhance_query(self, query: str, query_type: str) -> str:
        """Enhance query based on type for better retrieval"""
        enhancements = {
            "target_population": f"{query}\nInclude information about: patient demographics, conditions, age groups, and special populations.",
            "indication": f"{query}\nInclude: primary uses, approved indications, off-label uses, and mechanism of action.",
            "dosage": f"{query}\nInclude: standard dosing, dosing adjustments, administration route, and timing.",
            "side_effects": f"{query}\nInclude: common side effects, serious adverse reactions, and frequency.",
            "contraindication": f"{query}\nInclude: absolute contraindications, relative contraindications, and warnings.",
            "interaction": f"{query}\nInclude: drug-drug interactions, drug-food interactions, and severity.",
            "general": query
        }
        
        return enhancements.get(query_type, query)
    
    def _get_system_prompt(self, query_type: str) -> str:
        """Get appropriate system prompt based on query type"""
        base_prompt = "You are a medical AI assistant providing evidence-based medication information."
        
        type_specific = {
            "target_population": " Focus on patient demographics and suitability criteria.",
            "indication": " Focus on therapeutic uses and clinical applications.",
            "dosage": " Focus on dosing guidelines and administration.",
            "side_effects": " Focus on adverse reactions and safety profile.",
            "contraindication": " Focus on warnings and contraindications.",
            "interaction": " Focus on drug interactions and precautions.",
            "general": " Provide comprehensive medication information."
        }
        
        return base_prompt + type_specific.get(query_type, type_specific["general"]) + \
               "\nBase your response on the retrieved medical knowledge. Always emphasize consulting healthcare providers."
    
    def _estimate_confidence(self, answer: str) -> str:
        """Estimate confidence level of the answer"""
        answer_lower = answer.lower()
        
        # High confidence indicators
        if any(phrase in answer_lower for phrase in ["approved for", "indicated for", "fda approved"]):
            return "High"
        
        # Low confidence indicators
        if any(phrase in answer_lower for phrase in ["may", "possibly", "unclear", "limited information"]):
            return "Moderate"
        
        # Check answer length and detail
        if len(answer) > 500 and answer.count('.') > 5:
            return "High"
        elif len(answer) > 200:
            return "Moderate"
        else:
            return "Low"
