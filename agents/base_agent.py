from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
# from langchain.schema import BaseRetriever
from langchain_core.retrievers import BaseRetriever
# from langchain.llms.base import BaseLLM
from langchain_core.language_models import BaseLLM


class BaseAgent(ABC):
    """
    Base Agent class defining common structure for all specialized medical agents.
    """
    
    def __init__(self, llm: Optional[BaseLLM] = None, retriever: Optional[BaseRetriever] = None):
        """
        Initialize base agent with LLM and retriever.
        
        Args:
            llm: Language model for reasoning
            retriever: Vector store retriever for RAG
        """
        self.llm = llm
        self.retriever = retriever
        self.agent_name = self.__class__.__name__
    
    @abstractmethod
    def process(self, input_data: Any, **kwargs) -> Dict[str, Any]:
        """
        Process input and return structured output.
        Must be implemented by all child agents.
        
        Args:
            input_data: Input to process (text, image, file, etc.)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing processed results
        """
        pass
    
    def _log(self, message: str):
        """Log agent activity"""
        print(f"[{self.agent_name}] {message}")
