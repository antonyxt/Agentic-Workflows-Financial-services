

## Evaluator-Optimizer Flow

```mermaid
flowchart TD
    Start([SWIFT Message]) --> Init[Initialize<br/>Iteration = 0]
    
    Init --> Evaluate[EVALUATE Phase<br/>Validate Message]
    
    Evaluate --> Check{Is Valid?}
    
    Check -->|Yes| Valid[✅ Mark as VALID<br/>Success!]
    Valid --> End([Return Validated Message])
    
    Check -->|No| HasErrors[Errors Found]
    
    HasErrors --> MaxIter{Max Iterations<br/>Reached?}
    
    MaxIter -->|Yes| Invalid[❌ Mark as INVALID<br/>Cannot Fix]
    Invalid --> LogErrors[Log All Errors]
    LogErrors --> End
    
    MaxIter -->|No| Optimize[OPTIMIZE Phase<br/>Attempt Correction]
    
    Optimize --> LLM[Request LLM Correction<br/>Based on Errors]
    
    LLM --> Apply[Apply Corrections<br/>to Message]
    
    Apply --> Increment[Increment Iteration]
    
    Increment --> Evaluate
    
    style Start fill:#e3f2fd
    style Valid fill:#d4edda
    style Invalid fill:#f8d7da
    style Evaluate fill:#fff3cd
    style Optimize fill:#d1ecf1
    style End fill:#e3f2fd
```



## Validation Layers

```mermaid
flowchart LR
    subgraph Input
        MSG[SWIFT Message]
    end
    
    subgraph Layer1[Layer 1: Field Validation]
        F1[BIC Format Check]
        F2[Amount Format]
        F3[Currency Code]
        F4[Date Format]
        F5[Reference Length]
    end
    
    subgraph Layer2[Layer 2: Business Rules]
        B1[Amount Limits]
        B2[Same Sender/Receiver]
        B3[BIC Validity]
        B4[Country Restrictions]
    end
    
    subgraph Layer3[Layer 3: Format Standards]
        S1[Message Type]
        S2[Field Structure]
        S3[Character Encoding]
        S4[SWIFT MT Format]
    end
    
    subgraph Output
        E1[Validation Errors]
        E2[Error Categories]
        E3[Correction Hints]
    end
    
    MSG --> F1
    MSG --> F2
    MSG --> F3
    MSG --> F4
    MSG --> F5
    
    F1 --> B1
    F2 --> B1
    F3 --> B2
    F4 --> B3
    F5 --> B4
    
    B1 --> S1
    B2 --> S2
    B3 --> S3
    B4 --> S4
    
    S1 --> E1
    S2 --> E1
    S3 --> E2
    S4 --> E3
    
    style Input fill:#e3f2fd
    style Layer1 fill:#fff3cd
    style Layer2 fill:#d1ecf1
    style Layer3 fill:#f8d7da
    style Output fill:#d4edda
```

## State Machine - Message Status

```mermaid
stateDiagram-v2
    [*] --> Pending: New Message
    
    Pending --> Evaluating: Start Validation
    
    Evaluating --> Valid: No Errors Found
    Evaluating --> HasErrors: Errors Detected
    
    HasErrors --> Optimizing: Attempt Correction<br/>(Iterations < Max)
    HasErrors --> Invalid: Max Iterations Reached
    
    Optimizing --> Evaluating: Apply Corrections<br/>Re-validate
    
    Valid --> [*]: Message Ready
    Invalid --> [*]: Cannot Fix
    
    note right of Evaluating
        Multi-layer validation:
        • Field validation
        • Business rules
        • Format standards
    end note
    
    note right of Optimizing
        LLM-powered correction:
        • Analyze errors
        • Suggest fixes
        • Apply changes
    end note
    
    note right of Valid
        Validation Status: VALID
        Ready for processing
    end note
    
    note right of Invalid
        Validation Status: INVALID
        Manual review required
    end note
```

## Validation Categories

### 1. Field Validation

**BIC Code Format:**
- Length: 8 or 11 characters
- Bank Code: 4 letters (positions 1-4)
- Country Code: 2 letters (positions 5-6)
- Location Code: 2 alphanumeric (positions 7-8)
- Branch Code: 3 alphanumeric (positions 9-11, optional)

**Amount Validation:**
- Valid decimal format
- Positive values only
- Within configured limits (min/max)

**Currency Code:**
- Exactly 3 letters
- ISO 4217 standard
- Alphabetic only

**Value Date:**
- YYMMDD format
- Exactly 6 digits
- Valid calendar date

**Reference:**
- Maximum 16 characters
- Alphanumeric only
- Unique identifier

### 2. Business Rules

**Amount Limits:**
```python
min_amount: 0.01       # Minimum transaction
max_amount: 10,000,000 # Maximum transaction
```

**BIC Restrictions:**
- Sender ≠ Receiver BIC
- Both BICs must be valid institutions
- Active SWIFT network members

**Message Type Support:**
- MT103 (Customer Transfer)
- MT202 (Bank Transfer)

### 3. Format Standards

**Message Type Validation:**
- Valid SWIFT MT format
- Supported message types only

**Structure Compliance:**
- Required fields present
- Correct field ordering
- Valid delimiters

**Character Encoding:**
- SWIFT character set
- No special characters
- Proper encoding

## Correction Strategy

### Error Type → Correction Action

| Error Type | Detection | Correction Strategy |
|-----------|-----------|---------------------|
| **Invalid BIC** | Format check fails | LLM suggests valid BIC from bank name/country |
| **Invalid Currency** | Length ≠ 3 or non-alpha | LLM infers from context (USD, EUR, GBP, etc.) |
| **Invalid Date** | Non-YYMMDD format | LLM converts to proper format |
| **Amount Out of Range** | < min or > max | LLM adjusts to boundary or suggests review |
| **Invalid Reference** | Special chars or too long | LLM sanitizes and truncates to 16 chars |
| **Same Sender/Receiver** | BIC codes match | LLM identifies correct receiver institution |


