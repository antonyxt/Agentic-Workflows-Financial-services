"""
LLM service for fraud analysis and SWIFT message correction using OpenAI
"""

import json
from typing import Dict, Any

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

    
    def get_swift_correction(self, prompt: str) -> Dict[str, Any]:
        """
        Get SWIFT message corrections from LLM
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a SWIFT message validation expert. "
                        "Your task is to correct SWIFT message format errors while "
                        "maintaining the business intent of the transaction. "
                        "Respond with JSON containing the corrected fields."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content or "{}")
            
            return result
            
        except Exception as e:
            return {}
    
    