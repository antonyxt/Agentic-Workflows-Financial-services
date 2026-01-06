"""
Demo class showcasing the Workflow Pattern for SWIFT transaction processing.

This demonstration shows how to orchestrate multiple agent patterns together
in a coordinated workflow to process SWIFT messages from start to finish.
"""

import time
from typing import List, Dict, Any

from models.swift_message import SWIFTMessage
from agents.evaluator_optimizer import EvaluatorOptimizer
from agents.prompt_chaining import PromptChainingAgent
from agents.orchestrator_worker import OrchestratorWorker
from services.swift_generator import SWIFTGenerator
from agents.fraud_detector import FraudDetector
from config import Config


class WorkflowPatternDemo:
    """
    Demonstration class for the Workflow Pattern.
    Shows orchestration of multiple agent patterns in a complete processing pipeline.
    """
    
    def __init__(self):
        self.config = Config()
        
        # Initialize all agent patterns
        self.swift_generator = SWIFTGenerator()
        self.evaluator_optimizer = EvaluatorOptimizer()
        self.prompt_chaining_agent = PromptChainingAgent()
        self.orchestrator_worker = OrchestratorWorker()
        self.fraud_detector = FraudDetector()

        #TODO:  Create fraud class to instantiate
        
        # Workflow statistics
        self.workflow_stats = {}
    
    def run_demo(self):
        """
        Run a complete demonstration of the workflow pattern
        """
        print("=" * 90)
        print("WORKFLOW PATTERN DEMONSTRATION")
        print("Orchestrating Multiple Agent Patterns for SWIFT Processing")
        print("=" * 90)
        print()
        
        # Show workflow overview
        self._show_workflow_overview()
        
        # Execute the workflow
        print("WORKFLOW EXECUTION:")
        print("-" * 50)
        
        workflow_start = time.time()
        
        # Step 1: Message Generation
        messages = self._step_1_message_generation()
        
        # Step 2: Validation & Correction
        validated_messages = self._step_2_evaluator_optimizer(messages)

        #TODO:  What can I add here to change the validated messages to do a fraud check.
        validated_messages = self._step_2a_fraud(validated_messages)
        
        # Step 3: Chaining
        analyzed_messages = self._step_3_prompt_chaining(validated_messages)
        
        # Step 5: Transaction Processing
        # self._step_4_orchestrator_worker(analyzed_messages)
        
        workflow_time = time.time() - workflow_start
        
        # Show final results
        self._show_workflow_results(analyzed_messages, workflow_time)
    
    def _show_workflow_overview(self):
        """
        Display the workflow architecture and agent patterns involved
        """
        print("WORKFLOW ARCHITECTURE:")
        print()
        print("┌─────────────────────────────────────────────────────────────┐")
        print("│                    SWIFT WORKFLOW PIPELINE                  │")
        print("├─────────────────────────────────────────────────────────────┤")
        print("│  1. 📝 Message Generation    │ Create synthetic SWIFT data  │")
        print("│  2. ✅ Evaluator-Optimizer   │ Validate & correct messages  │") 
        print("│  3. 🤖 Prompt Chaining       │ AI-powered fraud analysis    │")
        print("│  5. 🏭 Orchestrator-Worker   │ Transaction splitting        │")
        print("└─────────────────────────────────────────────────────────────┘")
        print()
    
    def _step_1_message_generation(self) -> List[SWIFTMessage]:
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
        
        self.workflow_stats['generation'] = {
            'count': len(messages),
            'time': generation_time,
            'types': self._count_message_types(messages)
        }
        
        return messages
    
    def _step_2_evaluator_optimizer(self, messages: List[SWIFTMessage]) -> List[SWIFTMessage]:
        """
        Step 2: Validate and correct messages using Evaluator-Optimizer pattern
        """
        print("STEP 2: EVALUATOR-OPTIMIZER PATTERN")
        print("✅ Validating and correcting SWIFT messages...")
        
        start_time = time.time()
        validated_messages = []
        corrections_made = 0
        
        for message in messages:
            original_status = message.validation_status
            validated_message = self.evaluator_optimizer.process_message(message)
            validated_messages.append(validated_message)
            
            # Count corrections
            if original_status != validated_message.validation_status:
                corrections_made += 1
        
        validation_time = time.time() - start_time
        
        valid_count = sum(1 for msg in validated_messages if msg.validation_status == "VALID")
        invalid_count = len(validated_messages) - valid_count
        
        print(f"   ✅ Validated {len(validated_messages)} messages")
        print(f"   🔧 Corrections applied: {corrections_made}")
        print(f"   ✔️  Valid messages: {valid_count}")
        print(f"   ❌ Invalid messages: {invalid_count}")
        print(f"   ⏱️  Processing time: {validation_time:.2f} seconds")
        print()
        
        self.workflow_stats['validation'] = {
            'total': len(validated_messages),
            'valid': valid_count,
            'invalid': invalid_count,
            'corrections': corrections_made,
            'time': validation_time
        }
        
        return validated_messages
    
    def _step_2a_fraud(self, messages: List[SWIFTMessage]) -> List[SWIFTMessage]:
        checked_messages = []
        for message in messages:
            fraud_prompt = self.fraud_detector.create_prompt(message)
            fraud_message = self.fraud_detector.respond(fraud_prompt)
            if fraud_message["fraud"] == "YES":
                message.mark_as_fraudulent(.9, fraud_message["reasoning"])
            checked_messages.append(message)
        return checked_messages

    
    def _step_3_prompt_chaining(self, messages: List[SWIFTMessage]) -> List[SWIFTMessage]:
        """
        Step 3: Enhanced fraud analysis using Prompt Chaining pattern
        """
        print("STEP 4: PROMPT CHAINING PATTERN")
        print("🤖 Enhanced AI analysis for high-risk transactions...")
        
        start_time = time.time()
        
        # Select high-risk messages for prompt chaining
        high_risk_messages = [
            msg for msg in messages 
            if hasattr(msg, 'fraud_score') and float(getattr(msg, 'fraud_score', 0)) >= 0.3
        ]
        
        chain_analyses = 0
        
        if high_risk_messages:
            print(f"   🎯 Analyzing {len(high_risk_messages)} high-risk transactions...")
            
            # Run prompt chain analysis
            chain_results = []
            for msg in high_risk_messages:
                chain_results.append( self.prompt_chaining_agent.analyze_transaction_chain(
                    msg
                ))
            
            # Update messages with chain analysis results
            decisions = {'APPROVE': 0, 'HOLD': 0, 'REJECT': 0}
            
            for i, result in enumerate(chain_results):
                if i < len(high_risk_messages):
                    msg = high_risk_messages[i]
                    chain_analyses += 1
                    
                    # Update fraud status based on chain decision
                    final_decision = result.get_chain_analysis().get("final_decision")
                    decisions[final_decision] += 1
                    
                    #TODO: Append the agent perspectives to the message.
                    msg.set_agent_perspectives(result.agent_perspectives)

                    if final_decision == "REJECT":
                        msg.fraud_status = "FRAUDULENT"
                    elif final_decision == "HOLD":
                        msg.fraud_status = "HELD"
                    elif final_decision == "APPROVE":
                        msg.fraud_status = "CLEAN"
            
            print(f"   🤖 AI analysis decisions:")
            print(f"      ✅ Approved: {decisions['APPROVE']}")
            print(f"      🟡 Held: {decisions['HOLD']}")
            print(f"      ❌ Rejected: {decisions['REJECT']}")
        else:
            print("   ✅ No high-risk transactions requiring enhanced analysis")
        
        chaining_time = time.time() - start_time
        
        print(f"   ⏱️  Analysis time: {chaining_time:.2f} seconds")
        print()
        
        self.workflow_stats['prompt_chaining'] = {
            'high_risk_count': len(high_risk_messages),
            'analyses_performed': chain_analyses,
            'time': chaining_time
        }
        
        return messages
    
    def _step_4_orchestrator_worker(self, messages: List[SWIFTMessage]) -> None:
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
            
            self.workflow_stats['transaction_processing'] = {
                'transactions_processed': len(clean_messages),
                'total_amount': total_amount,
                'time': processing_time,
                'status': 'completed'
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            print(f"   ⚠️  Transaction processing encountered balance validation issues")
            print(f"   📊 Workflow Pattern Demonstration: {len(clean_messages)} transactions ready for processing")
            print(f"   💰 Total amount: ${total_amount:,.2f}")
            print(f"   🔄 Orchestrator-Worker pattern orchestration demonstrated")
            print(f"   ⏱️  Processing time: {processing_time:.2f} seconds")
            
            self.workflow_stats['transaction_processing'] = {
                'transactions_processed': len(clean_messages),
                'total_amount': total_amount,
                'time': processing_time,
                'status': 'pattern_demonstrated'
            }
        
        print()
    
    def _show_workflow_results(self, messages: List[SWIFTMessage], total_time: float):
        """
        Display comprehensive workflow results and statistics
        """
        print("=" * 90)
        print("WORKFLOW RESULTS SUMMARY")
        print("=" * 90)
        
        # Overall statistics
        total_messages = len(messages)
        fraudulent = sum(1 for msg in messages if msg.fraud_status == "FRAUDULENT")
        held = sum(1 for msg in messages if msg.fraud_status == "HELD") 
        clean = sum(1 for msg in messages if msg.fraud_status == "CLEAN")
        
        print()
        print("📊 PROCESSING SUMMARY:")
        print(f"   Total Messages Processed: {total_messages}")
        print(f"   Clean Transactions: {clean} ({clean/total_messages*100:.1f}%)")
        print(f"   Held for Review: {held} ({held/total_messages*100:.1f}%)")
        print(f"   Fraudulent Transactions: {fraudulent} ({fraudulent/total_messages*100:.1f}%)")
        print()
        
        print("⏱️ PERFORMANCE METRICS:")
        print(f"   Total Workflow Time: {total_time:.2f} seconds")
        print(f"   Average Processing per Message: {total_time/total_messages:.3f} seconds")
        print(f"   Throughput: {total_messages/total_time:.1f} messages/second")
        print()
        
        print("🔍 STEP-BY-STEP BREAKDOWN:")
        for step, stats in self.workflow_stats.items():
            print(f"   {step.title().replace('_', ' ')}: {stats.get('time', 0):.2f}s")
        print()
        
        print("🏆 WORKFLOW EFFICIENCY:")
        if self.workflow_stats.get('routing', {}).get('fraud_stats'):
            fraud_detection_rate = (fraudulent + held) / total_messages * 100
            print(f"   Fraud Detection Rate: {fraud_detection_rate:.1f}%")
        
        validation_success = self.workflow_stats.get('validation', {}).get('valid', 0)
        if validation_success:
            print(f"   Validation Success Rate: {validation_success/total_messages*100:.1f}%")
        
        print(f"   End-to-End Success Rate: {clean/total_messages*100:.1f}%")
        print()
        
        print("✅ WORKFLOW PATTERN DEMONSTRATION COMPLETE")
        print()
        self._show_pattern_summary()
    
    def _show_pattern_summary(self):
        """
        Show summary of all patterns demonstrated
        """
        print("🔧 AGENT PATTERNS DEMONSTRATED:")
        print("• Evaluator-Optimizer: Iterative validation and correction")
        print("• Prompt Chaining: Multi-agent AI conversations for complex analysis")
        print("• Orchestrator-Worker: Coordinated transaction splitting")
        print("• Workflow Orchestration: End-to-end pipeline coordination")
    
    def _count_message_types(self, messages: List[SWIFTMessage]) -> Dict[str, int]:
        """Count message types in the batch"""
        types = {}
        for msg in messages:
            msg_type = msg.message_type
            types[msg_type] = types.get(msg_type, 0) + 1
        return types
    
    def _analyze_fraud_results(self, messages: List[SWIFTMessage]) -> Dict[str, Any]:
        """Analyze fraud detection results"""
        clean = sum(1 for msg in messages if msg.fraud_status == "CLEAN")
        held = sum(1 for msg in messages if msg.fraud_status == "HELD")
        fraudulent = sum(1 for msg in messages if msg.fraud_status == "FRAUDULENT")
        
        # Calculate average fraud score
        fraud_scores = []
        for msg in messages:
            if hasattr(msg, 'fraud_score') and msg.fraud_score is not None:
                fraud_scores.append(float(msg.fraud_score))
        
        avg_score = sum(fraud_scores) / len(fraud_scores) if fraud_scores else 0
        
        return {
            'clean': clean,
            'held': held,
            'fraudulent': fraudulent,
            'avg_score': avg_score
        }


def main():
    """
    Run the workflow pattern demonstration
    """
    
    # Run demonstration
    demo = WorkflowPatternDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()