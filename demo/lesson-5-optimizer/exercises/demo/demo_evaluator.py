"""
Demo class showcasing the Evaluator-Optimizer Pattern for SWIFT message processing.

This demonstration shows how the evaluator-optimizer pattern iteratively validates
and corrects SWIFT messages using multiple evaluation cycles with automatic optimization.
"""

from typing import Dict, List
from services.swift_message import SWIFTMessage
from services.evaluator_optimizer import EvaluatorOptimizer
from services.validator import SWIFTValidator

class EvaluatorOptimizerDemo:
    """
    Demonstration class for the Evaluator-Optimizer pattern.
    Shows iterative validation and correction of SWIFT messages.
    """
    
    def __init__(self):
        self.evaluator_optimizer = EvaluatorOptimizer()
    
    def run_demo(self):
        """
        Run a complete demonstration of the evaluator-optimizer pattern
        """
        print("=" * 80)
        print("EVALUATOR-OPTIMIZER PATTERN DEMONSTRATION")
        print("=" * 80)
        print()
        
        # Create test messages with various error types
        test_messages = self._create_test_messages()
        
        for i, (message, description) in enumerate(test_messages, 1):
            print(f"TEST CASE {i}: {description}")
            print("-" * 60)
            
            self._display_original_message(message)
            self._demonstrate_pattern(message)
            
            print("\n" + "=" * 80 + "\n")
    
    def _create_test_messages(self) -> List[tuple]:
        """
        Create test SWIFT messages with intentional errors for demonstration.
        These pass Pydantic validation but trigger business rule errors.
        """
        return [
            (
                SWIFTMessage(
                    message_id="DEMO001",
                    message_type="MT103",
                    reference="TOOLONGREF12345",  # Too long but will be truncated
                    amount="999999999.99",  # Amount too high for business rules
                    currency="USD",  # Valid currency
                    sender_bic="ABCDUS33",  # Valid pattern but will trigger business validation
                    receiver_bic="CHASUS33",  # Valid BIC
                    value_date="240915"  # Valid date format
                ),
                "High Amount and Invalid BIC Errors"
            ),
            (
                SWIFTMessage(
                    message_id="DEMO002",
                    message_type="MT202",
                    reference="REF12345",
                    amount="50000.00",
                    currency="EUR",
                    sender_bic="DEUTDEFF",  # Valid BIC
                    receiver_bic="DEUTDEFF",  # Same as sender (business rule error)
                    value_date="240915"  # Valid date format
                ),
                "Same Sender/Receiver Business Rule Error"
            ),
            (
                SWIFTMessage(
                    message_id="DEMO003",
                    message_type="MT103",
                    reference="VALIDREF",
                    amount="5.00",  # Below minimum amount (business rule error)
                    currency="GBP",
                    sender_bic="BARCGB22",
                    receiver_bic="CHASUS33",
                    value_date="240915"
                ),
                "Low Amount Business Rule Error"
            ),
            (
                SWIFTMessage(
                    message_id="DEMO004",
                    message_type="MT103",
                    reference="PERFECT",
                    amount="10000.00",
                    currency="USD",
                    sender_bic="CHASUS33",
                    receiver_bic="DEUTDEFF",
                    value_date="240915"
                ),
                "Perfect Message (No Errors Expected)"
            )
        ]
    
    def _display_original_message(self, message: SWIFTMessage):
        """
        Display the original message details
        """
        print("ORIGINAL MESSAGE:")
        print(f"  Message ID: {message.message_id}")
        print(f"  Type: {message.message_type}")
        print(f"  Reference: {message.reference}")
        print(f"  Amount: {message.amount}")
        print(f"  Currency: {message.currency}")
        print(f"  Sender BIC: {message.sender_bic}")
        print(f"  Receiver BIC: {message.receiver_bic}")
        print(f"  Value Date: {message.value_date}")
        print()
    
    def _demonstrate_pattern(self, message: SWIFTMessage):
        """
        Demonstrate the evaluator-optimizer pattern step by step
        """
        print("EVALUATOR-OPTIMIZER PROCESS:")
        print()
        
        # Create a custom evaluator for detailed demonstration
        demo_evaluator = DetailedEvaluatorOptimizer()
        processed_message = demo_evaluator.process_message_with_details(message)
        
        print("FINAL RESULT:")
        print(f"  Status: {processed_message.validation_status}")
        print(f"  Final Reference: {processed_message.reference}")
        print(f"  Final Amount: {processed_message.amount}")
        print(f"  Final Currency: {processed_message.currency}")
        print(f"  Final Sender BIC: {processed_message.sender_bic}")
        print(f"  Final Receiver BIC: {processed_message.receiver_bic}")
        print(f"  Final Value Date: {processed_message.value_date}")
        
        if hasattr(processed_message, 'validation_errors') and processed_message.validation_errors:
            print(f"  Remaining Errors: {len(processed_message.validation_errors)}")
            for error in processed_message.validation_errors:
                print(f"    - {error}")
        else:
            print("  No remaining errors!")


class DetailedEvaluatorOptimizer(EvaluatorOptimizer):
    """
    Extended evaluator-optimizer that provides detailed step-by-step output
    """
    #TODO:  Pass the amount piece.  Right now it fails for three times.  You have to teach the LLM how to handle this.
    
    def process_message_with_details(self, message: SWIFTMessage) -> SWIFTMessage:
        """
        Process message with detailed console output for demonstration
        """
        print(f"Starting evaluation-optimization cycle for message {message.message_id}")
        print()
        
        iteration = 0
        current_message = message.copy(deep=True)
        
        while iteration < self.max_iterations:
            print(f"ITERATION {iteration + 1}:")
            print("  Phase 1: EVALUATION")
            
            # Evaluation phase with details
            is_valid, errors = self._evaluate_message_with_details(current_message)
            
            if is_valid:
                print("  ✓ Message is VALID!")
                current_message.validation_status = "VALID"
                print(f"  Success! Message validated in {iteration + 1} iteration(s)")
                break
            
            print(f"  ✗ Found {len(errors)} validation errors:")
            for error in errors:
                print(f"    - {error}")
            print()
            
            # Optimization phase
            if iteration < self.max_iterations - 1:
                print("  Phase 2: OPTIMIZATION")
                print("  Attempting automatic correction using AI assistance...")
                
                original_values = {
                    'reference': current_message.reference,
                    'amount': current_message.amount,
                    'currency': current_message.currency,
                    'sender_bic': current_message.sender_bic,
                    'receiver_bic': current_message.receiver_bic,
                    'value_date': current_message.value_date
                }
                
                current_message = self._optimize_message(current_message, errors)
                
                # Show what changed
                self._show_optimization_changes(original_values, current_message)
                print()
            else:
                print("  Phase 2: OPTIMIZATION")
                print(f"  ✗ Maximum iterations ({self.max_iterations}) reached")
                print("  Unable to automatically correct all errors")
                current_message.validation_status = "INVALID"
                current_message.validation_errors.extend(errors)
            
            iteration += 1
        
        return current_message
    
    def _evaluate_message_with_details(self, message: SWIFTMessage) -> tuple:
        """
        Evaluate message with detailed output
        """
        errors = []
        
        print("    Checking SWIFT standards compliance...")
        
        # Basic field validation
        
        validator = SWIFTValidator()
        
        validation_result = validator.validate_swift_message(message)
        if not validation_result.is_valid:
            errors.extend(validation_result.errors)
        
        # Business rule validation
        business_errors = self._validate_business_rules(message)
        errors.extend(business_errors)
        
        # TODO : Validate Format
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def _show_optimization_changes(self, original_values: Dict, corrected_message: SWIFTMessage):
        """
        Show what changes were made during optimization
        """
        changes_made = []
        
        if original_values['reference'] != corrected_message.reference:
            changes_made.append(f"Reference: '{original_values['reference']}' → '{corrected_message.reference}'")
        
        if original_values['amount'] != corrected_message.amount:
            changes_made.append(f"Amount: '{original_values['amount']}' → '{corrected_message.amount}'")
        
        if original_values['currency'] != corrected_message.currency:
            changes_made.append(f"Currency: '{original_values['currency']}' → '{corrected_message.currency}'")
        
        if original_values['sender_bic'] != corrected_message.sender_bic:
            changes_made.append(f"Sender BIC: '{original_values['sender_bic']}' → '{corrected_message.sender_bic}'")
        
        if original_values['receiver_bic'] != corrected_message.receiver_bic:
            changes_made.append(f"Receiver BIC: '{original_values['receiver_bic']}' → '{corrected_message.receiver_bic}'")
        
        if original_values['value_date'] != corrected_message.value_date:
            changes_made.append(f"Value Date: '{original_values['value_date']}' → '{corrected_message.value_date}'")
        
        if changes_made:
            print("  Changes applied:")
            for change in changes_made:
                print(f"    - {change}")
        else:
            print("  No automatic corrections could be applied")


def main():
    """
    Run the evaluator-optimizer demonstration
    """
    
    # Run demonstration
    demo = EvaluatorOptimizerDemo()
    demo.run_demo()
    
    print("EVALUATOR-OPTIMIZER PATTERN DEMONSTRATION COMPLETE")
    print()
    print("KEY FEATURES DEMONSTRATED:")
    print("• Iterative validation with up to 3 correction attempts")
    print("• Automatic error detection for business rules and formats")
    print("• AI-powered optimization suggestions")
    print("• Step-by-step evaluation and correction process")
    print("• Graceful handling of uncorrectable errors")


if __name__ == "__main__":
    main()