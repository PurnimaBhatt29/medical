from typing import Dict, Any
from agents.base_agent import BaseAgent
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import config


class XRayVisionAgent(BaseAgent):
    """
    Specialized agent for analyzing X-ray images.
    Uses HuggingFace vision model for classification and RAG for explanation.
    """
    
    def __init__(self, llm, rag_pipeline):
        super().__init__(llm=llm)
        self.rag_pipeline = rag_pipeline
        self._load_vision_model()
    
    def _load_vision_model(self):
        """Load HuggingFace vision model for X-ray analysis"""
        self._log(f"Loading vision model: {config.VISION_MODEL}")
        try:
            self.processor = AutoImageProcessor.from_pretrained(config.VISION_MODEL)
            self.model = AutoModelForImageClassification.from_pretrained(config.VISION_MODEL)
            self.model.eval()
            self._log("Vision model loaded successfully")
        except Exception as e:
            self._log(f"Warning: Could not load vision model: {e}")
            self.processor = None
            self.model = None
    
    def process(self, image_file, **kwargs) -> Dict[str, Any]:
        """
        Process X-ray image.
        
        Args:
            image_file: Uploaded image file
            **kwargs: Additional parameters
            
        Returns:
            Structured analysis results
        """
        self._log("Starting X-ray analysis...")
        
        try:
            # Step 1: Load and preprocess image
            self._log("Loading image...")
            image = Image.open(image_file).convert('RGB')
            
            # Step 2: Run vision model inference
            self._log("Running vision model inference...")
            predictions = self._classify_xray(image)
            
            # Step 3: Extract findings
            primary_finding = predictions[0] if predictions else {"label": "Unknown", "score": 0.0}
            
            # Step 4: Query RAG for detailed explanation
            self._log("Retrieving medical explanation from knowledge base...")
            
            explanation_query = f"""Explain the medical condition: {primary_finding['label']}
Include:
- What this condition means
- Common causes
- Typical symptoms
- When to seek medical attention
- Treatment approaches"""
            
            system_prompt = """You are a medical AI assistant explaining X-ray findings.
Provide clear, accurate explanations based on medical knowledge.
Always emphasize the importance of professional medical evaluation."""
            
            explanation = self.rag_pipeline.query_with_rag(
                query=explanation_query,
                collection_name="medical_knowledge",
                system_prompt=system_prompt,
                top_k=config.TOP_K_RERANK
            )
            
            # Step 5: Assess severity
            severity = self._assess_severity(primary_finding)
            
            # Step 6: Structure output
            result = {
                "status": "success",
                "primary_finding": primary_finding['label'],
                "confidence": f"{primary_finding['score']*100:.1f}%",
                "all_predictions": predictions[:3],
                "severity": severity,
                "explanation": explanation,
                "recommendations": self._generate_recommendations(primary_finding, severity),
                "disclaimer": "X-ray interpretation requires professional radiologist review"
            }
            
            self._log("X-ray analysis completed successfully")
            return result
            
        except Exception as e:
            self._log(f"Error during X-ray analysis: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "primary_finding": "Analysis failed",
                "severity": "Unknown"
            }
    
    def _classify_xray(self, image: Image) -> list:
        """Classify X-ray image using vision model"""
        if self.processor is None or self.model is None:
            return [{"label": "Model not available", "score": 0.0}]
        
        try:
            inputs = self.processor(images=image, return_tensors="pt")
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
            
            # Get predictions
            probs = torch.nn.functional.softmax(logits, dim=-1)
            top_probs, top_indices = torch.topk(probs, k=min(3, probs.shape[-1]))
            
            predictions = []
            for prob, idx in zip(top_probs[0], top_indices[0]):
                label = self.model.config.id2label[idx.item()]
                predictions.append({
                    "label": label,
                    "score": prob.item()
                })
            
            return predictions
            
        except Exception as e:
            self._log(f"Classification error: {e}")
            return [{"label": "Classification failed", "score": 0.0}]
    
    def _assess_severity(self, finding: dict) -> str:
        """Assess severity based on finding"""
        label_lower = finding['label'].lower()
        confidence = finding['score']
        
        if confidence < 0.5:
            return "Uncertain"
        
        critical_keywords = ["pneumonia", "effusion", "pneumothorax", "mass", "tumor"]
        moderate_keywords = ["infiltrate", "opacity", "consolidation"]
        
        if any(keyword in label_lower for keyword in critical_keywords):
            return "High" if confidence > 0.7 else "Moderate"
        elif any(keyword in label_lower for keyword in moderate_keywords):
            return "Moderate"
        elif "normal" in label_lower:
            return "Low"
        else:
            return "Moderate"
    
    def _generate_recommendations(self, finding: dict, severity: str) -> list:
        """Generate recommendations based on findings"""
        recommendations = []
        
        if severity in ["High", "Critical"]:
            recommendations.append("⚠️ Seek immediate medical evaluation")
            recommendations.append("Consult with a pulmonologist or radiologist")
        elif severity == "Moderate":
            recommendations.append("Schedule appointment with healthcare provider")
            recommendations.append("Discuss findings with your doctor")
        else:
            recommendations.append("Routine follow-up as recommended by physician")
        
        recommendations.append("This AI analysis does not replace professional radiologist interpretation")
        
        return recommendations
