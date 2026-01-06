"""
SWIFT Transaction Processing System with Agent Patterns
Main application entry point
"""

from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import Config
from models.swift_message import SWIFTMessage
from services.swift_generator import SWIFTGenerator
from agents.parallelization import ParallelizationAgent


class SWIFTProcessingSystem:
    """Main system orchestrating all agent patterns for SWIFT processing"""
    
    def __init__(self):
        self.config = Config()
        self.swift_generator = SWIFTGenerator()
        
        # Initialize agent patterns
        self.parallelization_agent = ParallelizationAgent()
    
    def generate_swift_messages(self) -> List[SWIFTMessage]:
        """Generate 1000 SWIFT messages across 30 banks"""

        messages = self.swift_generator.generate_messages(
            count=self.config.MESSAGE_COUNT,
            bank_count=self.config.BANK_COUNT
        )
        
        return messages
    
    def process_with_parallelization(self, messages: List[SWIFTMessage]) -> List[SWIFTMessage]:
        """Step 2: Process messages in parallel with fraud detection routing"""
        
        fraud_messages = self.parallelization_agent.process_messages_parallel(
            messages 
        )
        
        processed_messages = self.parallelization_agent.aggregrate_fraud(
            fraud_messages 
        )
        
        return processed_messages
    
    
    def run(self):
        """Main execution method"""
        try:
            
            # Step 1: Generate SWIFT messages
            messages = self.generate_swift_messages()
            
            # Step 2: Parallelization 
            processed_messages = self.process_with_parallelization(messages)
            print(processed_messages)
            
            
        except Exception as e:
            raise


if __name__ == "__main__":
    system = SWIFTProcessingSystem()
    system.run()
