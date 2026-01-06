"""
LLM-Based Routing Agent Pattern for SWIFT message processing.

This agent implements an LLM-centric routing flow where a main LLM coordinates
routing to specialized LLMs and handles final processing.
"""

import json
from typing import Dict, Any
from openai import OpenAI

from services.swift_message import SWIFTMessage
from config import Config


class LLMRoutingAgent:
    """
    LLM-based routing agent that uses a main LLM to coordinate routing to specialized LLMs.
    
    Flow: Message → Main LLM → Specialized LLM → Main LLM → Complete
    """
    
    def __init__(self):
        self.config = Config()
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
        self.model = self.config.OPENAI_MODEL
    
    def route_message(self, message: SWIFTMessage) -> SWIFTMessage:
        """
        Main routing method: Main LLM → Specialized LLM → Main LLM → Complete
        """
        
        try:
            # Step 1: Main LLM analyzes and determines routing
            routing_decision = self._main_llm_initial_analysis(message)
            
            # Step 2: Route to specialized LLM based on decision
            specialized_result = self._route_to_specialized_llm(message, routing_decision)
            
            # Step 3: Main LLM does final processing
            final_result = self._main_llm_final_processing(message, routing_decision, specialized_result)
            
            # Step 4: Update message with final results
            self._update_message_with_results(message, final_result)
            
        except Exception as e:
            message.processing_status = "ERROR"
            message.validation_errors.append(f"LLM routing error: {str(e)}")
        
        return message
    
    def _main_llm_initial_analysis(self, message: SWIFTMessage) -> Dict[str, Any]:
        """
        Main LLM analyzes the message and determines which specialized LLM to route to
        """
        prompt = f"""
Analyze this SWIFT message and determine which specialized processing is needed.

SWIFT Message Details:
- Message ID: {message.message_id}
- Type: {message.message_type}
- Amount: {message.currency} {message.amount}
- From: {message.sender_bic}
- To: {message.receiver_bic}
- Reference: {message.reference}
- Value Date: {message.value_date}

Choose ONE of these specialized processors:
1. PROCESSING - For standard transaction processing
2. FRAUD_DETECTION - For suspicious patterns or high-risk transactions
3. BALANCE_CHECK - For verifying account balances and funds availability
4. MESSAGE_VALIDATION - For format issues or compliance violations

Respond with JSON:
{{
    "specialist_llm": "PROCESSING|FRAUD_DETECTION|BALANCE_CHECK|MESSAGE_VALIDATION",
    "routing_reason": "Brief explanation of why this specialist was chosen",
    "priority": "HIGH|MEDIUM|LOW",
    "key_concerns": ["list", "of", "main", "issues", "to", "address"],
    "analysis_summary": "Summary of initial message analysis"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are the Main LLM Coordinator for SWIFT transaction processing. "
                        "Your role is to analyze incoming messages and route them to the appropriate "
                        "specialist LLM for detailed processing. Be decisive and accurate in your routing."
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
            # Default to processing if analysis fails
            return {
                "specialist_llm": "PROCESSING",
                "routing_reason": "Default routing due to analysis failure",
                "priority": "MEDIUM",
                "key_concerns": ["analysis_failure"],
                "analysis_summary": f"Analysis failed: {str(e)}"
            }
    
    def _route_to_specialized_llm(self, message: SWIFTMessage, routing_decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route message to the appropriate specialized LLM based on routing decision
        """
        specialist = routing_decision.get("specialist_llm", "PROCESSING")
        
        if specialist == "PROCESSING":
            return self._processing_llm(message, routing_decision)
        elif specialist == "FRAUD_DETECTION":
            #TODO:  add fraud detector
            return message
           
        elif specialist == "BALANCE_CHECK":
            #TODO : add balance check
            return message
        elif specialist == "MESSAGE_VALIDATION":
            return self._message_validation_llm(message, routing_decision)
        else:
            # Default to processing
            return self._processing_llm(message, routing_decision)
    
    def _processing_llm(self, message: SWIFTMessage, routing_decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processing LLM - Handles standard transaction processing
        """
        prompt = f"""
Process this SWIFT transaction for completion.

Transaction Details:
- ID: {message.message_id}
- Type: {message.message_type}
- Amount: {message.currency} {message.amount}
- Route: {message.sender_bic} → {message.receiver_bic}
- Reference: {message.reference}

Key Concerns from Main LLM: {routing_decision.get('key_concerns', [])}
Priority: {routing_decision.get('priority', 'MEDIUM')}

Perform standard processing checks:
- Transaction limits and restrictions
- Business hours and processing windows
- Regulatory compliance requirements
- Standard processing fees and calculations

Respond with JSON:
{{
    "processing_decision": "APPROVE|HOLD|REJECT",
    "processing_notes": "Detailed processing analysis",
    "fees_calculated": "Processing fees if applicable",
    "compliance_status": "COMPLIANT|NON_COMPLIANT|REVIEW_REQUIRED",
    "estimated_processing_time": "Time estimate for completion",
    "recommendations": ["list", "of", "recommendations"]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are the Processing Specialist LLM. Your expertise is in standard "
                        "SWIFT transaction processing, compliance checks, fee calculations, and processing "
                        "workflows. Focus on efficient and compliant transaction processing."
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
            return {
                "processing_decision": "HOLD",
                "processing_notes": f"Processing LLM error: {str(e)}",
                "compliance_status": "REVIEW_REQUIRED",
                "recommendations": ["manual_review_required"]
            }
    

    def _message_validation_llm(self, message: SWIFTMessage, routing_decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Message Validation LLM - Checks message format and compliance
        """
        prompt = f"""
Validate this SWIFT message format and compliance requirements.

Message Details:
- ID: {message.message_id}
- Type: {message.message_type}
- Amount: {message.currency} {message.amount}
- Sender BIC: {message.sender_bic}
- Receiver BIC: {message.receiver_bic}
- Reference: {message.reference}
- Value Date: {message.value_date}

Key Concerns from Main LLM: {routing_decision.get('key_concerns', [])}

Perform comprehensive validation:
- SWIFT message format compliance
- BIC code format and validity
- Currency code validation
- Amount format and precision
- Value date format and business rules
- Reference format and uniqueness
- Regulatory compliance requirements

Respond with JSON:
{{
    "validation_status": "VALID|INVALID|WARNING|CORRECTABLE",
    "format_errors": ["list", "of", "format", "errors"],
    "compliance_issues": ["regulatory", "compliance", "issues"],
    "suggested_corrections": {{"field": "corrected_value"}},
    "severity": "LOW|MEDIUM|HIGH|CRITICAL",
    "can_auto_correct": true/false,
    "validation_notes": "Detailed validation analysis",
    "next_steps": ["required", "actions"]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are the Message Validation Specialist LLM. Your expertise is in "
                        "SWIFT message format validation, compliance checking, and ensuring messages "
                        "meet all technical and regulatory requirements. Be thorough and precise."
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
            return {
                "validation_status": "INVALID",
                "format_errors": [f"Validation LLM error: {str(e)}"],
                "severity": "HIGH",
                "can_auto_correct": False,
                "next_steps": ["manual_validation_required"]
            }
    
    def _main_llm_final_processing(self, message: SWIFTMessage, routing_decision: Dict[str, Any], 
                                  specialized_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main LLM performs final processing after receiving specialized LLM results
        """
        prompt = f"""
Complete final processing for this SWIFT transaction based on specialist analysis.

Original Message: {message.message_id}
Initial Routing: {routing_decision.get('specialist_llm', 'UNKNOWN')}
Routing Reason: {routing_decision.get('routing_reason', 'Unknown')}

Specialist LLM Results:
{json.dumps(specialized_result, indent=2)}

Make final decision considering:
- Specialist LLM recommendations
- Overall transaction risk
- Regulatory compliance
- Business impact
- Processing efficiency

Respond with JSON:
{{
    "final_decision": "APPROVE|REJECT|HOLD|ESCALATE",
    "decision_confidence": 0.0-1.0,
    "processing_status": "COMPLETED|PENDING|FAILED|REVIEW_REQUIRED",
    "fraud_status": "CLEAN|SUSPICIOUS|FRAUDULENT|HELD",
    "final_notes": "Comprehensive final analysis",
    "action_items": ["required", "follow", "up", "actions"],
    "escalation_needed": true/false,
    "processing_time_estimate": "Estimated completion time"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are the Main LLM Coordinator completing final processing. "
                        "Your role is to synthesize specialist recommendations and make final "
                        "decisions on SWIFT transactions. Be decisive and comprehensive."
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
            return {
                "final_decision": "HOLD",
                "processing_status": "REVIEW_REQUIRED",
                "fraud_status": "HELD",
                "final_notes": f"Final processing LLM error: {str(e)}",
                "escalation_needed": True
            }
    
    def _update_message_with_results(self, message: SWIFTMessage, final_result: Dict[str, Any]):
        """
        Update the SWIFT message with final processing results
        """
        # Set fraud status
        fraud_status = final_result.get('fraud_status', 'HELD')
        if fraud_status == "CLEAN":
            message.mark_as_clean(0.1)  # Low fraud score for clean transactions
        elif fraud_status == "SUSPICIOUS":
            message.mark_as_held(0.5, "LLM marked as suspicious")
        elif fraud_status == "FRAUDULENT":
            message.mark_as_fraudulent(0.9, "LLM detected fraud")
        else:  # HELD
            message.mark_as_held(0.4, "LLM requires review")
        
        # Set processing status
        processing_status = final_result.get('processing_status', 'REVIEW_REQUIRED')
        message.processing_status = processing_status
        
        # Add final notes to validation errors for tracking
        final_notes = final_result.get('final_notes', 'LLM processing completed')
        if final_notes:
            message.validation_errors.append(f"LLM Processing: {final_notes}")