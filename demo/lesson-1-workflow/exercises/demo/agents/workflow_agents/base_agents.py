
from services.llm_service import LLMService
from config import Config
from models.swift_message import SWIFTMessage
from typing import Dict, List, Tuple, Any
import json


class Orchestrator:
    
    def __init__(self):
        self.config = Config()
        self.llm_service = LLMService()
        
    def create_prompt(self, messages: List[SWIFTMessage]) -> str:
        """
        Create prompt for Orchestration
        """
        prompt = f"""

You are a SWIFT Transaction processor.  You have this list of messages.

{messages}

Your job is to analyze these messages and process them. Only concern your self with amounts, countries, debits and credits.

Do not concern yourself with fraud or compliance.

One of the tasks should be a report for amounts by country and currency.

Please break down the plan into sub plans and tasks.

Return your response in the following format, with an <analysis> section and a <tasks> section.

<analysis>
Provide a high-level summary.
</analysis>

<tasks>
Provide four tasks to process these transactions. Each task must have a <type> and a <description>.
Example task format:
<task>
  <type>compliance report</type>
  <description>Generate a report on the compliance metrics of these messages.</description>
</task>
</tasks>

Respond in JSON Format. 
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
    
class GenericAgent():
    def __init__(self):
        self.config = Config()
        self.llm_service = LLMService()

    def respond(self, task: str, analysis: str, messages:List[SWIFTMessage] ) -> Dict[str, Any]:
        prompt = f"""
You are a SWIFT payment processor.  Please process the subtasks according to the subtask type and description.

Main Task: {analysis}
Subtask Type: {task['type']}
Subtask Description: {task['description']}

The Swift Messages are here
{messages}

Return 
1.  How the task was processed and a summary of findings for review.

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
            response_format={"type": "text"},
            temperature=0
        )
        
        result = response.choices[0].message.content 
         
        return result