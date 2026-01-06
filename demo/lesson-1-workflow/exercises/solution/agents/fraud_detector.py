from typing import Dict, List, Tuple, Any
from models.swift_message import SWIFTMessage
from services.llm_service import LLMService
from config import Config
import json

class FraudDetector:
    def __init__(self):
        self.config = Config()
        self.llm_service = LLMService()
        
    def create_prompt(self, message: SWIFTMessage) -> str:
        prompt = f"""

You are a SWIFT Transaction processor.  Your job is to look for fraud in SWIFT messages.
Your primary definition of fraud is any currency not in USD. Please look at this message.

{message}

Now perform risk behavior analysis. Respond with JSON:
        {{
                "fraud": "YES"|"NO",
                "reasoning": "Why is this fraud"
        }}
"""
        return prompt
    
    def respond(self, prompt: str) -> Dict[str, Any]:
        """
        Get SWIFT message corrections from LLM
        """
        response = self.llm_service.client.chat.completions.create(
            model=self.llm_service.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        result = json.loads(response.choices[0].message.content or "{}")
         
        return result