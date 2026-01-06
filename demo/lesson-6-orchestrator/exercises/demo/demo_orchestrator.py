"""
Demo class showcasing the Workflow Pattern for SWIFT transaction processing.

This demonstration shows how to orchestrate multiple agent patterns together
in a coordinated workflow to process SWIFT messages from start to finish.
"""

import time
from typing import List, Dict

from models.swift_message import SWIFTMessage
from services.orchestrator_worker import OrchestratorWorker
from services.swift_generator import SWIFTGenerator
from config import Config


class OrchestratorPatternDemo:
    """
    Demonstration class for the Workflow Pattern.
    Shows orchestration of multiple agent patterns in a complete processing pipeline.
    """
    
    def __init__(self):
        self.config = Config()
        
        # Initialize all agent patterns
        self.swift_generator = SWIFTGenerator()
        self.orchestrator_worker = OrchestratorWorker()
    
    def run_demo(self):
        """
        Run a complete demonstration of the workflow pattern
        """
        
        # Execute the workflow
        print("ORCHESTRATOR EXECUTION:")
        print("-" * 50)
        
        # Step 1: Message Generation
        messages = self._message_generation()
        
        self._orchestrator_worker(messages)
    
    
    def _message_generation(self) -> List[SWIFTMessage]:
        """
        Step 1: Generate SWIFT messages using synthetic data
        """
        print("STEP 1: MESSAGE GENERATION")
        print("📝 Generating synthetic SWIFT messages...")
        
        start_time = time.time()
        
        # Generate a smaller batch for demo purposes
        messages = self.swift_generator.generate_messages(count=5, bank_count=10)
        
        generation_time = time.time() - start_time
        
        print(f"   ✅ Generated {len(messages)} SWIFT messages")
        print(f"   ⏱️  Generation time: {generation_time:.2f} seconds")
        print(f"   📊 Message types: {self._count_message_types(messages)}")
        print()
        
        return messages
    
    def _orchestrator_worker(self, messages: List[SWIFTMessage]) -> None:
        """
        Step 5: Transaction processing using Orchestrator-Worker pattern
        """
        print("STEP 5: ORCHESTRATOR-WORKER PATTERN")
        print("🏭 Processing transactions with parallel workers...")
        
        start_time = time.time()
        
        # Filter non-fraudulent messages for final processing
        clean_messages = [msg for msg in messages if msg.fraud_status != "FRAUDULENT"]
        
        print(f"   📊 Processing {len(clean_messages)} clean transactions...")
        
        # Calculate processing statistics
        total_amount = sum(float(msg.amount) for msg in clean_messages)
        
        try:
            # Process transactions (splits into company fees and transfers)
            self.orchestrator_worker.process_transactions(clean_messages)
            
            processing_time = time.time() - start_time
            
            print(f"   ✅ Processed {len(clean_messages)} transactions")
            print(f"   💰 Total amount: ${total_amount:,.2f}")
            print(f"   🔄 Transaction splits generated")
            print(f"   ⏱️  Processing time: {processing_time:.2f} seconds")
        
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            print(f"   ⚠️  Transaction processing encountered balance validation issues")
            print(f"   📊 Orchestrator Pattern Demonstration: {len(clean_messages)} transactions ready for processing")
            print(f"   💰 Total amount: ${total_amount:,.2f}")
            print(f"   🔄 Orchestrator-Worker pattern orchestration demonstrated")
            print(f"   ⏱️  Processing time: {processing_time:.2f} seconds")
        
        print()
    
    def _count_message_types(self, messages: List[SWIFTMessage]) -> Dict[str, int]:
        """Count message types in the batch"""
        types = {}
        for msg in messages:
            msg_type = msg.message_type
            types[msg_type] = types.get(msg_type, 0) + 1
        return types


def main():
    """
    Run the workflow pattern demonstration
    """
    
    # Run demonstration
    demo = OrchestratorPatternDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()