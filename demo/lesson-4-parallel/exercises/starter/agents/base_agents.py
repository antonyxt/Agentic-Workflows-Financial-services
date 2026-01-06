
from services.llm_service import LLMService
from config import Config
from models.swift_message import SWIFTMessage
from typing import Dict, List, Tuple, Any
import json

    
class FraudAmountDetectionAgent:
    
    def __init__(self):
        self.config = Config()
        self.llm_service = LLMService()
        
    def create_prompt(self, message: SWIFTMessage)-> str:
        """
        Create prompt for LLM correction
        """
        prompt = f"""

Please grade the following SWIFT message for fraud using the rules below.

{message}

Rules 

Rule 1.  if the amount > 10000 this reflects a very high amount and has risk. Add .3 to total risk score
Rule 2.  if amount >= 5000 and amount % 1000 == 0.  This Round amount suggesting structuring: $<amount> and add .2 to total risk score
Rule 3.  if amount > 100000 and the decimal part of the amount is not 00 or 50.  This is unusual precision for large amount and add .1 to total risk score.

Please return your evaluation of the risk according to the rules plus the total risk score.

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
                    "content": "You are a SWIFT message fraud detection expert. "
                    "Your task is to investigate SWIFT messages for possibilities of fraud"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "text"},
            temperature=0
        )
        
        result = response.choices[0].message.content
        
        return result
    
class FraudPatternDetectionAgent:
    
    def __init__(self):
        self.config = Config()
        self.llm_service = LLMService()
        
    def create_prompt(self, message: SWIFTMessage)-> str:
        """
        Create prompt for LLM correction
        """
        prompt = f"""

Please grade the following SWIFT message for fraud using the rules below to detect risk risky fraud patterns.

{message}

Rules 

These are high risk patterns  'TEST.*', 'FAKE.*', 'DEMO.*', '.*999.*', '.*000000.*'
Rule 1.  if the sender bic or the receiver bic contain any of the high risk patterns, this suggests fraud and add .3 to total risk score.
Rule 2.  If the sender bic and the receiver bic are the same, this can be fraud and add a .2 to the total risk score.
Rule 3.  If any words are misspelled, that could be fraud and add a .1 to the total risk score.

Please return your evaluation of the risk according to the rules plus the total risk score.

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
                    "content": "You are a SWIFT message fraud detection expert. "
                    "Your task is to investigate SWIFT messages for possibilities of fraud"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "text"},
            temperature=0
        )
        
        result = response.choices[0].message.content
        
        return result
    
class FraudAggAgent:
    
    def __init__(self):
        self.config = Config()
        self.llm_service = LLMService()
        
    def create_prompt(self, message: SWIFTMessage) -> str:
        """
        Create prompt for LLM correction
        """
        prompt = f"""

Please review the following messages and tell me if a Swift transaction with these messages is fraudulent or not.

{message}

Please respond in json format with "thought" that contains the final review and "total_fraud_score" which contains your assessment from 1 to 100
on what you think the fraud score should be.  100 being highest. 

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
                    "content": "You are a SWIFT fraud supervisor"
                               "Your job is to make sure no fraudulent SWIFT transactions get processed."
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
    
   