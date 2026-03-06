from typing import Dict, Any, List
from agents.base_agent import BaseAgent
import config


class MedicalChatAgent(BaseAgent):
    """
    Specialized agent for contextual medical conversations.
    Maintains conversation history and provides memory-based retrieval.
    """
    
    def __init__(self, llm, rag_pipeline):
        super().__init__(llm=llm)
        self.rag_pipeline = rag_pipeline
        self.conversation_history = []
    
    def process(self, message: str, **kwargs) -> Dict[str, Any]:
        """
        Process chat message with context.
        
        Args:
            message: User message
            **kwargs: Additional parameters
            
        Returns:
            Chat response with context
        """
        self._log(f"Processing chat message: {message[:50]}...")
        
        try:
            # Step 1: Add message to history
            self.conversation_history.append({
                "role": "user",
                "content": message
            })
            
            # Step 2: Build context from history
            context = self._build_conversation_context()
            
            # Step 3: Enhance query with context
            enhanced_query = f"""Conversation context:
{context}

Current question: {message}

Provide a helpful medical response considering the conversation history."""
            
            # Step 4: Retrieve relevant information using RAG
            self._log("Retrieving relevant medical information...")
            
            system_prompt = """You are a helpful medical AI assistant engaged in conversation.
Provide accurate, empathetic responses based on medical knowledge.
Maintain conversation context and refer to previous messages when relevant.
Always remind users to consult healthcare professionals for medical decisions."""
            
            response = self.rag_pipeline.query_with_rag(
                query=enhanced_query,
                collection_name="medical_knowledge",
                system_prompt=system_prompt,
                top_k=config.TOP_K_RERANK
            )
            
            # Step 5: Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Step 6: Detect if medical attention needed
            urgency = self._detect_urgency(message, response)
            
            # Step 7: Structure output
            result = {
                "status": "success",
                "response": response,
                "urgency": urgency,
                "conversation_length": len(self.conversation_history),
                "context_used": True
            }
            
            self._log("Chat message processed successfully")
            return result
            
        except Exception as e:
            self._log(f"Error processing chat message: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "response": "I apologize, but I encountered an error processing your message."
            }
    
    def _build_conversation_context(self, max_messages: int = 5) -> str:
        """Build context from recent conversation history"""
        recent_history = self.conversation_history[-(max_messages*2):]
        
        context_parts = []
        for msg in recent_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"][:200]  # Limit length
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)
    
    def _detect_urgency(self, message: str, response: str) -> str:
        """Detect if message indicates medical urgency"""
        message_lower = message.lower()
        response_lower = response.lower()
        
        emergency_keywords = [
            "chest pain", "difficulty breathing", "severe pain", "bleeding heavily",
            "unconscious", "seizure", "stroke", "heart attack", "emergency"
        ]
        
        urgent_keywords = [
            "severe", "worsening", "sudden", "intense", "unbearable"
        ]
        
        if any(keyword in message_lower for keyword in emergency_keywords):
            return "emergency"
        elif any(keyword in message_lower for keyword in urgent_keywords):
            return "urgent"
        elif any(keyword in response_lower for keyword in ["seek immediate", "emergency", "call 911"]):
            return "urgent"
        else:
            return "normal"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self._log("Conversation history cleared")
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
