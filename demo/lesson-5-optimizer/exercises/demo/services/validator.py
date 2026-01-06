"""
SWIFT message validation utilities
"""

import re
from typing import List, Tuple
from datetime import datetime
from pydantic import BaseModel

from services.swift_message import SWIFTMessage
from services.config import Config


class ValidationResult(BaseModel):
    """Result of validation operation"""
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    
    def add_error(self, error: str):
        """Add validation error"""
        self.errors.append(error)
        self.is_valid = False
    
    def add_warning(self, warning: str):
        """Add validation warning"""
        self.warnings.append(warning)


class SWIFTValidator:
    """
    Comprehensive SWIFT message validator
    """
    
    def __init__(self):
        self.config = Config()
        
        # BIC validation patterns
        self.bic_pattern = re.compile(r'^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$')
        
        # Valid ISO currency codes (major ones)
        self.valid_currencies = {
            'USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 'NZD',
            'SEK', 'NOK', 'DKK', 'PLN', 'CZK', 'HUF', 'SGD', 'HKD',
            'KRW', 'CNY', 'INR', 'BRL', 'MXN', 'ZAR', 'RUB', 'TRY',
            'THB', 'MYR', 'IDR', 'PHP', 'VND', 'EGP', 'SAR', 'AED',
            'QAR', 'KWD', 'BHD', 'OMR', 'JOD', 'LBP', 'ILS', 'CLP',
            'COP', 'PEN', 'UYU', 'ARS', 'BOB', 'PYG', 'CRC', 'GTQ',
            'HNL', 'NIO', 'PAB', 'DOP', 'JMD', 'TTD', 'BBD', 'XCD'
        }
        
        # High-risk country codes (examples for demonstration)
        self.high_risk_countries = {
            'AF', 'BY', 'CF', 'CG', 'CU', 'CD', 'ER', 'GN', 'GW',
            'HT', 'IR', 'IQ', 'LB', 'LR', 'LY', 'ML', 'MM', 'NI',
            'KP', 'RU', 'SO', 'SS', 'SD', 'SY', 'VE', 'YE', 'ZW'
        }
        
    
    def validate_swift_message(self, message: SWIFTMessage) -> ValidationResult:
        """
        Comprehensive SWIFT message validation
        """
        result = ValidationResult(is_valid=True)
        
        # Basic field validation
        self._validate_basic_fields(message, result)
        
        # BIC validation
        self._validate_bic_codes(message, result)
        
        # Amount validation
        self._validate_amount(message, result)
        
        # Currency validation
        #TODO: validate currency
        
        # Date validation
        self._validate_dates(message, result)
        
        # Message type specific validation
        self._validate_message_type_specific(message, result)
        
        # Format validation
        self._validate_formats(message, result)
        
        # Risk validation
        self._validate_risk_factors(message, result)
    
        
        return result
    
    def _validate_basic_fields(self, message: SWIFTMessage, result: ValidationResult):
        """Validate basic required fields"""
        required_fields = self.config.SWIFT_STANDARDS["required_fields"]
        
        for field in required_fields:
            value = getattr(message, field, None)
            if not value or (isinstance(value, str) and not value.strip()):
                result.add_error(f"Required field '{field}' is missing or empty")
    
    def _validate_bic_codes(self, message: SWIFTMessage, result: ValidationResult):
        """Validate BIC code formats"""
        # Sender BIC validation
        if not self._is_valid_bic(message.sender_bic):
            result.add_error(f"Invalid sender BIC format: {message.sender_bic}")
        
        # Receiver BIC validation
        if not self._is_valid_bic(message.receiver_bic):
            result.add_error(f"Invalid receiver BIC format: {message.receiver_bic}")
        
        # Same BIC check
        if message.sender_bic == message.receiver_bic:
            result.add_error("Sender and receiver BIC codes cannot be identical")
        
        # High-risk country check
        sender_country = message.sender_bic[4:6] if len(message.sender_bic) >= 6 else ""
        receiver_country = message.receiver_bic[4:6] if len(message.receiver_bic) >= 6 else ""
        
        if sender_country in self.high_risk_countries:
            result.add_warning(f"Sender BIC from high-risk country: {sender_country}")
        
        if receiver_country in self.high_risk_countries:
            result.add_warning(f"Receiver BIC from high-risk country: {receiver_country}")
    
    def _validate_amount(self, message: SWIFTMessage, result: ValidationResult):
        """Validate transaction amount"""
        try:
            amount = float(message.amount)
            
            # Range validation
            if amount <= 0:
                result.add_error("Amount must be positive")
            
            if amount < self.config.SWIFT_STANDARDS["min_amount"]:
                result.add_error(f"Amount {amount} below minimum {self.config.SWIFT_STANDARDS['min_amount']}")
            
            if amount > self.config.SWIFT_STANDARDS["max_amount"]:
                result.add_error(f"Amount {amount} exceeds maximum {self.config.SWIFT_STANDARDS['max_amount']}. Convert this to 50 dollars")
            
            # Format validation
            if '.' in message.amount:
                decimal_places = len(message.amount.split('.')[1])
                if decimal_places > 2:
                    result.add_error("Amount cannot have more than 2 decimal places")
            
            # Suspicious amount patterns
            if amount >= 10000 and amount % 1000 == 0:
                result.add_warning(f"Round amount may indicate structuring: {amount}")
            
            # Very large amounts
            if amount >= 1000000:
                result.add_warning(f"Very large transaction amount: {amount}")
            
        except (ValueError, TypeError):
            result.add_error(f"Invalid amount format: {message.amount}")
    
    def _validate_currency(self, message: SWIFTMessage, result: ValidationResult):
        """Validate currency code"""
        if not message.currency:
            result.add_error("Currency code is required")
            return
        
        if len(message.currency) != 3:
            result.add_error(f"Currency code must be 3 characters: {message.currency}")
        
        if not message.currency.isalpha():
            result.add_error(f"Currency code must be alphabetic: {message.currency}")
        
        if not message.currency.isupper():
            result.add_error(f"Currency code must be uppercase: {message.currency}")
        
        if message.currency not in self.valid_currencies:
            result.add_warning(f"Uncommon or invalid currency code: {message.currency}")
    
    def _validate_dates(self, message: SWIFTMessage, result: ValidationResult):
        """Validate date fields"""
        # Value date validation (YYMMDD format)
        if not self._is_valid_value_date(message.value_date):
            result.add_error(f"Invalid value date format (YYMMDD required): {message.value_date}")
        else:
            # Check if date is reasonable
            try:
                year = 2000 + int(message.value_date[:2])
                month = int(message.value_date[2:4])
                day = int(message.value_date[4:6])
                
                value_date = datetime(year, month, day)
                now = datetime.now()
                
                # Value date should be within reasonable range
                days_diff = (value_date - now).days
                
                if days_diff < -30:
                    result.add_warning(f"Value date is more than 30 days in the past: {message.value_date}")
                
                if days_diff > 30:
                    result.add_warning(f"Value date is more than 30 days in the future: {message.value_date}")
                
                # Weekend/holiday warning (simplified)
                if value_date.weekday() >= 5:  # Saturday=5, Sunday=6
                    result.add_warning("Value date falls on weekend")
                
            except (ValueError, IndexError):
                result.add_error(f"Invalid value date: {message.value_date}")
    
    def _validate_message_type_specific(self, message: SWIFTMessage, result: ValidationResult):
        """Validate message type specific requirements"""
        if message.message_type not in self.config.SWIFT_STANDARDS["valid_message_types"]:
            result.add_error(f"Invalid message type: {message.message_type}")
            return
        
        if message.message_type == "MT103":
            # MT103 specific validations
            if not getattr(message, 'ordering_customer', None):
                result.add_warning("MT103 should include ordering customer information")
            
            if not getattr(message, 'beneficiary', None):
                result.add_warning("MT103 should include beneficiary information")
            
            if not getattr(message, 'remittance_info', None):
                result.add_warning("MT103 should include remittance information")
        
        elif message.message_type == "MT202":
            # MT202 specific validations
            # MT202 is for bank-to-bank transfers, simpler requirements
            pass
    
    def _validate_formats(self, message: SWIFTMessage, result: ValidationResult):
        """Validate field formats"""
        # Check for proper SWIFT character set
        swift_charset = re.compile(r'^[A-Za-z0-9/\-\?\:\(\)\.\,\'\+\s]*$')
        
        if message.reference and not swift_charset.match(message.reference):
            result.add_error("Reference contains invalid SWIFT characters")
        
        if hasattr(message, 'ordering_customer') and message.ordering_customer:
            if not swift_charset.match(message.ordering_customer):
                result.add_error("Ordering customer contains invalid SWIFT characters")
        
        if hasattr(message, 'beneficiary') and message.beneficiary:
            if not swift_charset.match(message.beneficiary):
                result.add_error("Beneficiary contains invalid SWIFT characters")
        
        if hasattr(message, 'remittance_info') and message.remittance_info:
            if not swift_charset.match(message.remittance_info):
                result.add_error("Remittance info contains invalid SWIFT characters")
    
    def _validate_risk_factors(self, message: SWIFTMessage, result: ValidationResult):
        """Validate risk-related factors"""
        # Check for patterns indicating potential fraud
        risk_patterns = [
            r'.*999.*',
            r'.*000000.*',
            r'TEST.*',
            r'FAKE.*',
            r'DEMO.*'
        ]
        
        for pattern in risk_patterns:
            if re.match(pattern, message.reference, re.IGNORECASE):
                result.add_warning(f"Reference matches risk pattern: {pattern}")
            
            if re.match(pattern, message.sender_bic, re.IGNORECASE):
                result.add_warning(f"Sender BIC matches risk pattern: {pattern}")
            
            if re.match(pattern, message.receiver_bic, re.IGNORECASE):
                result.add_warning(f"Receiver BIC matches risk pattern: {pattern}")
    
    def _is_valid_bic(self, bic: str) -> bool:
        """Check if BIC format is valid"""
        if not bic:
            return False
        
        return bool(self.bic_pattern.match(bic))
    
    def _is_valid_value_date(self, value_date: str) -> bool:
        """Check if value date format is valid (YYMMDD)"""
        if not value_date or len(value_date) != 6:
            return False
        
        if not value_date.isdigit():
            return False
        
        try:
            year = int(value_date[:2])
            month = int(value_date[2:4])
            day = int(value_date[4:6])
            
            # Basic range checks
            if month < 1 or month > 12:
                return False
            if day < 1 or day > 31:
                return False
            
            # Try to create date to validate
            datetime(2000 + year, month, day)
            return True
            
        except (ValueError, IndexError):
            return False
