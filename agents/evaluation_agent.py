from typing import Dict, Any
from agents.base_agent import BaseAgent
from sentence_transformers import SentenceTransformer
import numpy as np
import config


class EvaluationAgent(BaseAgent):
    """
    Specialized agent for evaluating RAG responses.
    Computes faithfulness, relevance, context precision, and hallucination risk.
    """
    
    def __init__(self, llm, embedding_model: SentenceTransformer):
        super().__init__(llm=llm)
        self.embedding_model = embedding_model
    
    def process(self, query: str, response: str, retrieved_contexts: list, **kwargs) -> Dict[str, Any]:
        """
        Evaluate RAG response quality.
        
        Args:
            query: Original user query
            response: Generated response
            retrieved_contexts: List of retrieved context chunks
            **kwargs: Additional parameters
                - relevant_contexts (optional): list of strings considered relevant to the query; used to compute
                  precision/recall/MRR for retrieval.
        
        Returns:
            Evaluation metrics
        """
        self._log("Starting response evaluation...")
        
        try:
            # Step 1: Compute faithfulness score
            self._log("Computing faithfulness score...")
            faithfulness = self._compute_faithfulness(response, retrieved_contexts)
            
            # Step 2: Compute relevance score
            self._log("Computing relevance score...")
            relevance = self._compute_relevance(query, response)
            
            # Step 3: Compute context precision
            self._log("Computing context precision...")
            context_precision = self._compute_context_precision(query, retrieved_contexts)
            
            # Step 4: Estimate hallucination risk
            self._log("Estimating hallucination risk...")
            hallucination_risk = self._estimate_hallucination_risk(response, retrieved_contexts)
            
            # Step 5: Compute overall confidence
            confidence = self._compute_confidence(faithfulness, relevance, context_precision, hallucination_risk)
            
            # Step 6: Generate evaluation summary
            summary = self._generate_evaluation_summary(
                faithfulness, relevance, context_precision, hallucination_risk, confidence
            )
            
            # Step 7: Structure output
            # Always include retrieval metric keys (defaults to 0 if no ground-truth supplied)
            retrieval_metrics = {"precision": 0.0, "recall": 0.0, "mrr": 0.0}
            retrieval_metrics_computed = False

            if kwargs.get("relevant_contexts"):
                self._log("Computing retrieval precision/recall/MRR...")
                retrieval_metrics = self._compute_retrieval_metrics(
                    retrieved_contexts, kwargs.get("relevant_contexts")
                )
                retrieval_metrics_computed = True

            result = {
                "status": "success",
                "faithfulness_score": round(faithfulness, 2),
                "relevance_score": round(relevance, 2),
                "context_precision": round(context_precision, 2),
                "hallucination_risk": round(hallucination_risk, 2),
                "confidence_percentage": round(confidence, 1),
                "quality_grade": self._assign_grade(confidence),
                "summary": summary,
                **retrieval_metrics,
                "retrieval_metrics_computed": retrieval_metrics_computed,
                "metrics_explanation": {
                    "faithfulness": "How well the response is grounded in retrieved context",
                    "relevance": "How relevant the response is to the query",
                    "context_precision": "Quality of retrieved context",
                    "hallucination_risk": "Risk of fabricated information",
                    "confidence": "Overall confidence in response quality",
                }
            }
            # add explanations for retrieval metrics if computed
            if retrieval_metrics:
                result["metrics_explanation"].update({
                    "precision": "Proportion of retrieved contexts that are relevant",
                    "recall": "Proportion of relevant contexts that were retrieved",
                    "mrr": "Mean reciprocal rank (higher = first relevant appears earlier)"
                })
            
            self._log("Evaluation completed successfully")
            return result
            
        except Exception as e:
            self._log(f"Error during evaluation: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "confidence_percentage": 0.0
            }
    
    def _compute_faithfulness(self, response: str, contexts: list) -> float:
        """
        Compute faithfulness score using embedding similarity.
        Measures how grounded the response is in retrieved contexts.
        """
        if not contexts:
            return 0.0
        
        try:
            # Embed response
            response_embedding = self.embedding_model.encode(response)
            
            # Embed contexts
            context_embeddings = self.embedding_model.encode(contexts)
            
            # Compute cosine similarities
            similarities = []
            for ctx_emb in context_embeddings:
                similarity = np.dot(response_embedding, ctx_emb) / (
                    np.linalg.norm(response_embedding) * np.linalg.norm(ctx_emb)
                )
                similarities.append(similarity)
            
            # Return max similarity as faithfulness score
            return float(max(similarities))
            
        except Exception as e:
            self._log(f"Faithfulness computation error: {e}")
            return 0.5
    
    def _compute_relevance(self, query: str, response: str) -> float:
        """
        Compute relevance score between query and response.
        """
        try:
            query_embedding = self.embedding_model.encode(query)
            response_embedding = self.embedding_model.encode(response)
            
            similarity = np.dot(query_embedding, response_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(response_embedding)
            )
            
            return float(similarity)
            
        except Exception as e:
            self._log(f"Relevance computation error: {e}")
            return 0.5
    
    def _compute_context_precision(self, query: str, contexts: list) -> float:
        """
        Compute context precision - how relevant retrieved contexts are to query.
        """
        if not contexts:
            return 0.0
        
        try:
            query_embedding = self.embedding_model.encode(query)
            context_embeddings = self.embedding_model.encode(contexts)
            
            similarities = []
            for ctx_emb in context_embeddings:
                similarity = np.dot(query_embedding, ctx_emb) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(ctx_emb)
                )
                similarities.append(similarity)
            
            # Average similarity of top contexts
            return float(np.mean(similarities))
            
        except Exception as e:
            self._log(f"Context precision computation error: {e}")
            return 0.5
    
    def _estimate_hallucination_risk(self, response: str, contexts: list) -> float:
        """
        Estimate hallucination risk (inverse of faithfulness).
        """
        faithfulness = self._compute_faithfulness(response, contexts)
        
        # Hallucination risk is inverse of faithfulness
        hallucination_risk = 1.0 - faithfulness
        
        # Check for uncertainty markers
        uncertainty_markers = ["may", "might", "possibly", "unclear", "uncertain"]
        if any(marker in response.lower() for marker in uncertainty_markers):
            hallucination_risk *= 0.8  # Reduce risk if model shows uncertainty
        
        return hallucination_risk

    def _compute_retrieval_metrics(self, retrieved: list, relevant: list) -> Dict[str, float]:
        """
        Compute retrieval metrics.

        - precision = (# retrieved that are relevant) / len(retrieved)
        - recall = (# retrieved that are relevant) / len(relevant)
        - mrr = 1 / rank of first relevant document (0 if none found)

        Both "retrieved" and "relevant" should be lists of strings.
        Matching is done via:
        1) substring containment (case-insensitive)
        2) fuzzy similarity (difflib) for partial / paraphrased matches
        """
        from difflib import SequenceMatcher

        def _is_relevant(doc_text: str, rel_text: str) -> bool:
            # Exact substring match
            if rel_text.lower() in doc_text.lower() or doc_text.lower() in rel_text.lower():
                return True

            # Fuzzy similarity threshold (helps with paraphrases/partial matches)
            ratio = SequenceMatcher(None, doc_text.lower(), rel_text.lower()).ratio()
            return ratio >= 0.6

        metrics: Dict[str, float] = {"precision": 0.0, "recall": 0.0, "mrr": 0.0}
        if not retrieved or not relevant:
            return metrics

        hits = []
        for idx, doc in enumerate(retrieved):
            # consider relevant if any relevant string matches (substring or fuzzy)
            is_rel = any(_is_relevant(doc, rel) for rel in relevant)
            if is_rel:
                hits.append(idx)

        num_hits = len(hits)
        metrics["precision"] = num_hits / len(retrieved)
        metrics["recall"] = num_hits / len(relevant)
        metrics["mrr"] = 1.0 / (hits[0] + 1) if hits else 0.0

        return metrics
    
    def _compute_confidence(self, faithfulness: float, relevance: float, 
                           context_precision: float, hallucination_risk: float) -> float:
        """
        Compute overall confidence percentage.
        """
        # Weighted average
        confidence = (
            faithfulness * 0.35 +
            relevance * 0.25 +
            context_precision * 0.25 +
            (1.0 - hallucination_risk) * 0.15
        ) * 100
        
        return min(100.0, max(0.0, confidence))
    
    def _assign_grade(self, confidence: float) -> str:
        """Assign quality grade based on confidence"""
        if confidence >= 85:
            return "Excellent"
        elif confidence >= 70:
            return "Good"
        elif confidence >= 55:
            return "Fair"
        else:
            return "Poor"
    
    def _generate_evaluation_summary(self, faithfulness: float, relevance: float,
                                    context_precision: float, hallucination_risk: float,
                                    confidence: float) -> str:
        """Generate human-readable evaluation summary"""
        grade = self._assign_grade(confidence)
        
        summary = f"Response quality: {grade} ({confidence:.1f}% confidence). "
        
        if faithfulness > 0.7:
            summary += "Response is well-grounded in retrieved knowledge. "
        elif faithfulness < 0.5:
            summary += "⚠️ Response may not be fully supported by retrieved context. "
        
        if hallucination_risk > 0.5:
            summary += "⚠️ Higher risk of hallucinated information - verify with healthcare provider. "
        
        if relevance > 0.7:
            summary += "Response directly addresses the query."
        
        return summary
