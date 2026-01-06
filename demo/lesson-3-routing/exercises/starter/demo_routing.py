"""
Demo class showcasing the new LLM-Based Routing Pattern for SWIFT message processing.

This demonstration shows the LLM-centric routing flow:
Main LLM → Specialized LLM → Main LLM → Complete
"""

from typing import List
from services.swift_message import SWIFTMessage
from services.lmm_routing_agent import LLMRoutingAgent


class LLMRoutingDemo:
    """
    Demonstration class for the new LLM-Based Routing Pattern.
    Shows AI-powered routing with specialized LLM processors.
    """
    
    def __init__(self):
        self.llm_routing_agent = LLMRoutingAgent()
    
    def run_demo(self):
        """
        Run a complete demonstration of the LLM-based routing pattern
        """
        print("=" * 90)
        print("LLM-BASED ROUTING PATTERN DEMONSTRATION")
        print("AI-Powered Message Routing with Specialized LLM Processors")
        print("=" * 90)
        print()
        
        # Demonstrate different routing scenarios
        print("ROUTING SCENARIOS DEMONSTRATION:")
        print("-" * 50)
        
        test_scenarios = self._create_test_scenarios()
        
        for i, (message, scenario_name, expected_routing) in enumerate(test_scenarios, 1):
            print(f"\nSCENARIO {i}: {scenario_name}")
            print("=" * 60)
            print(f"Expected Routing: Main LLM → {expected_routing} LLM → Main LLM")
            print()
            
            self._demonstrate_llm_routing(message, scenario_name)
            
            print("-" * 60)
        
        print("\n" + "=" * 90)
        print("LLM ROUTING PATTERN DEMONSTRATION COMPLETE")
    
    
    def _create_test_scenarios(self) -> List[tuple]:
        """
        Create test scenarios that will trigger different LLM routing paths
        """
        return [
            (
                SWIFTMessage(
                    message_id="LLM001",
                    message_type="MT103",
                    reference="NORMALTRX001",
                    amount="15000.00",
                    currency="USD",
                    sender_bic="CHASUS33",
                    receiver_bic="DEUTDEFF",
                    value_date="240918"
                ),
                "Normal Transaction Processing",
                "PROCESSING"
            ),
            (
                SWIFTMessage(
                    message_id="LLM002",
                    message_type="MT103",
                    reference="SUSPICIOUS123",
                    amount="9999.99",  # Just under $10k - structuring indicator
                    currency="USD",
                    sender_bic="TESTUS33",  # Suspicious BIC with 'TEST'
                    receiver_bic="CHASUS33",
                    value_date="240918"
                ),
                "Suspicious Transaction (Fraud Detection)",
                "FRAUD_DETECTION"
            ),
            (
                SWIFTMessage(
                    message_id="LLM003",
                    message_type="MT202",
                    reference="BIGMONEY999",
                    amount="50000000.00",  # Very large amount
                    currency="USD",
                    sender_bic="SMBCJPJT",
                    receiver_bic="CHASUS33",
                    value_date="240918"
                ),
                "Large Amount Transfer (Balance Check)",
                "BALANCE_CHECK"
            ),
            (
                SWIFTMessage(
                    message_id="LLM004",
                    message_type="MT103",
                    reference="BADFORMAT123",  # Suspicious reference pattern
                    amount="1000.00",
                    currency="USD",
                    sender_bic="TESTUS99",  # Valid pattern but suspicious content
                    receiver_bic="CHASUS33",
                    value_date="240918"  # Valid date format
                ),
                "Suspicious Format (Message Validation)",
                "MESSAGE_VALIDATION"
            ),
            (
                SWIFTMessage(
                    message_id="LLM005",
                    message_type="MT103",
                    reference="PERFECT001",
                    amount="5000.00",
                    currency="EUR",
                    sender_bic="DEUTDEFF",
                    receiver_bic="BNPAFRPP",
                    value_date="240918"
                ),
                "Clean Transaction (Processing)",
                "PROCESSING"
            )
        ]
    
    def _demonstrate_llm_routing(self, message: SWIFTMessage, scenario_name: str):
        """
        Demonstrate the complete LLM routing flow for a single message
        """
        print("MESSAGE DETAILS:")
        print(f"  ID: {message.message_id}")
        print(f"  Type: {message.message_type}")
        print(f"  Amount: {message.currency} {message.amount}")
        print(f"  Route: {message.sender_bic} → {message.receiver_bic}")
        print(f"  Reference: {message.reference}")
        print()
        
        print("LLM ROUTING PROCESS:")
        print()
        
        # Step 1: Show initial state
        print("📨 STEP 1: Message Received")
        print(f"   Initial Status: {message.processing_status}")
        print(f"   Fraud Status: {message.fraud_status}")
        print()
        
        # Step 2: Process through LLM routing
        print("🧠 STEP 2: Main LLM Analysis & Routing")
        print("   Analyzing message to determine specialist LLM...")
        
        # Process the message through LLM routing
        processed_message = self.llm_routing_agent.route_message(message)
        
        print("   ✅ Routing analysis complete")
        print()
        
        # Step 3: Show specialized processing (simulated)
        print("🤖 STEP 3: Specialized LLM Processing")
        print("   Specialist LLM analyzing message...")
        print("   ✅ Specialized analysis complete")
        print()
        
        # Step 4: Show final processing
        print("🧠 STEP 4: Main LLM Final Processing")
        print("   Synthesizing specialist results...")
        print("   Making final decision...")
        print("   ✅ Final processing complete")
        print()
        
        # Step 5: Show final results
        print("📊 FINAL RESULTS:")
        print(f"   Processing Status: {processed_message.processing_status}")
        print(f"   Fraud Status: {processed_message.fraud_status}")
        print(f"   Fraud Score: {processed_message.fraud_score:.3f}" if processed_message.fraud_score else "   Fraud Score: N/A")
        
        # Show any processing notes
        if processed_message.validation_errors:
            print("   Processing Notes:")
            for error in processed_message.validation_errors[-3:]:  # Show last 3 notes
                print(f"     • {error}")
        
        print()
        
        # Show routing decision summary
        if processed_message.fraud_status == "CLEAN":
            print("   🟢 DECISION: Transaction Approved for Processing")
        elif processed_message.fraud_status == "HELD":
            print("   🟡 DECISION: Transaction Held for Review")
        elif processed_message.fraud_status == "FRAUDULENT":
            print("   🔴 DECISION: Transaction Rejected as Fraudulent")
        else:
            print("   ⚪ DECISION: Transaction Status Pending")
    

def main():
    """
    Run the LLM-based routing demonstration
    """
    
    print("🚀 Starting LLM-Based Routing Pattern Demonstration...")
    print("Note: This demo uses OpenAI GPT-4o for AI-powered routing decisions.")
    print()
    
    # Run demonstration
    demo = LLMRoutingDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()