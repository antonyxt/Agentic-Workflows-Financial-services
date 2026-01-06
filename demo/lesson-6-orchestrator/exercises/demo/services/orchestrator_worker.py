"""
Orchestrator-Worker Agent Pattern for transaction splitting and processing
"""

from typing import List
from models.swift_message import SWIFTMessage
from config import Config
from services.base_agents import Orchestrator, GenericAgent


class OrchestratorWorker:
    """
    Orchestrator-Worker pattern implementation for SWIFT transaction processing
    """
    
    def __init__(self):
        self.config = Config()
        self.orchestrator = Orchestrator()
    
    def process_transactions(self, messages: List[SWIFTMessage]):
        """
        Main orchestrator method - coordinates workers to process transactions
        """

        prompt = self.orchestrator.create_prompt(messages)

        tasks = self.orchestrator.respond(prompt)

        for task in tasks['tasks']:
            #TODO: Intercept an agent with your own class.
            print("*" * 50)
            print("* The task we are going to do is ")
            print(f"{task["type"]}")
            print(f" * Description is {task["description"]}")
            print(GenericAgent().respond(task, tasks['analysis'], messages))
            print("*" * 50)

