"""
LLM service for fraud analysis and SWIFT message correction using OpenAI
"""


from openai import OpenAI
from services.config import Config


class LLMService:
    """
    Service for LLM-based fraud analysis and SWIFT message correction
    """
    
    def __init__(self):
        self.config = Config()
        
        # Initialize OpenAI client
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
        self.model = self.config.OPENAI_MODEL
        
    
    