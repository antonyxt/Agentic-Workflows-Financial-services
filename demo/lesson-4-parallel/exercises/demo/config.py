"""
Configuration settings for the SWIFT processing system
"""

import os
from typing import Dict, Any


class Config:
    """Configuration class for the SWIFT processing system"""
    
    # System settings
    MESSAGE_COUNT = 10
    BANK_COUNT = 5
    
    # Processing settings
    MAX_WORKERS = 8
    BATCH_SIZE = 50
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = "gpt-4o"  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
    BASE_URL = "https://openai.vocareum.com/v1"
    
    # SWIFT validation settings
    SWIFT_STANDARDS = {
        "max_reference_length": 16,
        "max_amount": 999999999.99,
        "min_amount": 0.01,
        "required_fields": ["message_type", "reference", "amount", "sender_bic", "receiver_bic"],
        "valid_message_types": ["MT103", "MT202"]
    }
    
    @classmethod
    def get_all_settings(cls) -> Dict[str, Any]:
        """Get all configuration settings as a dictionary"""
        return {
            attr: getattr(cls, attr)
            for attr in dir(cls)
            if not attr.startswith('_') and not callable(getattr(cls, attr))
        }

    # Fraud detection settings
    BENFORD_THRESHOLD = 0.05  # Chi-square test threshold
    FRAUD_REVIEW_THRESHOLD = 0.7  # LLM confidence threshold