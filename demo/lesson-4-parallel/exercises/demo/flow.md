


## Routing Flow Diagram

```mermaid
flowchart TD
    Start([SWIFT Transaction]) --> Detect[Fraud Detection Analysis]
    
    Detect --> Multi[Multi-Layer Analysis]
    
    Multi --> Amount[Amount Pattern Analysis<br/>• Round numbers<br/>• Unusual precision<br/>• Size anomalies]
    Multi --> BIC[BIC Pattern Analysis<br/>• High-risk countries<br/>• Same sender/receiver<br/>• Test patterns]
    Multi --> Time[Timing Analysis<br/>• Old value dates<br/>• Suspicious timing<br/>• Holiday patterns]
    Multi --> Individual[Individual Analysis<br/>• Transaction history<br/>• Behavioral patterns]
    
    Amount --> Combine[Combine Fraud Scores<br/>Weighted Average]
    BIC --> Combine
    Time --> Combine
    Individual --> Combine
    
    Combine --> Score{Fraud Score?}
    
    Score -->|> 0.8<br/>High Risk| Reject[❌ ROUTE: AUTOMATIC REJECT<br/>Block Transaction<br/>Flag as Fraudulent]
    Score -->|0.3 - 0.8<br/>Medium Risk| LLM[🔍 ROUTE: LLM REVIEW<br/>AI Analysis Required]
    Score -->|< 0.3<br/>Low Risk| Process[✅ ROUTE: NORMAL PROCESSING<br/>Approve Transaction]
    
    LLM --> AIReview
    AIReview --> AIDecision{AI Decision?}
    
    AIDecision -->|Approve| Clean[Mark as CLEAN<br/>Process Transaction]
    AIDecision -->|Suspicious| Hold[Mark as HELD<br/>Manual Review Queue]
    
    Reject --> End([Final Status])
    Process --> End
    Clean --> End
    Hold --> End
    
    style Start fill:#e3f2fd
    style Reject fill:#f8d7da
    style LLM fill:#fff3cd
    style Process fill:#d4edda
    style Clean fill:#d4edda
    style Hold fill:#fff3cd
    style End fill:#e3f2fd
```

## Sequence Diagram - Routing Process

```mermaid
sequenceDiagram
    participant T as Transaction
    participant RA as RoutingAgent
    participant FS as FraudService
    participant AP as AmountAnalyzer
    participant BP as BICAnalyzer
    participant TP as TimingAnalyzer
    participant LLM as LLMService
    
    T->>RA: route_message(transaction)
    
    RA->>RA: _detect_fraud(message)
    
    par Multi-Layer Analysis
        RA->>FS: analyze_transaction()
        FS-->>RA: Individual Score + Indicators
        
        RA->>AP: _analyze_amount_patterns()
        AP-->>RA: Amount Score + Indicators
        
        RA->>BP: _analyze_bic_patterns()
        BP-->>RA: BIC Score + Indicators
        
        RA->>TP: _analyze_timing_patterns()
        TP-->>RA: Timing Score + Indicators
    end
    
    RA->>RA: Calculate Weighted Score
    Note over RA: Weights: Individual(40%)<br/>Amount(30%)<br/>BIC(20%)<br/>Timing(10%)
    
    alt Fraud Score > 0.8 (High Risk)
        RA->>RA: _route_to_reject()
        RA->>T: Mark as FRAUDULENT
        RA-->>T: REJECTED
    
    else Fraud Score 0.3-0.8 (Medium Risk)
        RA->>LLM: review_suspicious_transaction()
        LLM->>LLM: AI Analysis
        LLM-->>RA: Decision + Reasoning
        
        alt LLM Approves
            RA->>T: Mark as CLEAN
            RA-->>T: APPROVED
        else LLM Suspicious
            RA->>T: Mark as HELD
            RA-->>T: HELD FOR REVIEW
        end
    
    else Fraud Score < 0.3 (Low Risk)
        RA->>RA: _route_to_processing()
        RA->>T: Mark as CLEAN
        RA-->>T: APPROVED
    end
```

## Fraud Indicators by Category

```mermaid
mindmap
  root((Fraud<br/>Indicators))
    Amount Based
      Round Numbers
        Exact thousands
        Structuring pattern
      Unusual Precision
        Too many decimals
        Large amounts
      Size Anomalies
        Very small $
        Very large $
        Under reporting limits
    BIC Based
      Geographic Risk
        High-risk countries
        Sanctions lists
      Pattern Issues
        Same sender/receiver
        Test patterns
        Invalid BICs
      Network Issues
        Non-SWIFT networks
        Routing anomalies
    Timing Based
      Date Issues
        Old value dates
        Future dates
        Weekend transactions
      Velocity
        Rapid succession
        Burst patterns
      Holidays
        Suspicious timing
    Behavioral
      History
        First transaction
        Out of pattern
      Frequency
        Unusual volume
        Sudden changes
      Relationships
        Unknown parties
        Shell companies
```

## Fraud Detection Analysis Methods

### 1. Amount Pattern Analysis

**Checks:**
- ✓ Round number detection (structuring)
- ✓ Unusual precision for large amounts
- ✓ Suspiciously small amounts
- ✓ Very large transaction amounts

**Scoring:**
- Round amounts (≥$10k): +0.2
- Excessive decimals: +0.1
- Small amounts (<$100): +0.15
- Large amounts (>$1M): +0.25

### 2. BIC Pattern Analysis

**Checks:**
- ✓ High-risk country codes
- ✓ Identical sender/receiver BICs
- ✓ Test pattern detection (TEST, FAKE, DEMO)
- ✓ Invalid BIC formats

**Scoring:**
- High-risk country: +0.3 per BIC
- Same sender/receiver: +0.5
- Test patterns: +0.4 per occurrence

### 3. Timing Pattern Analysis

**Checks:**
- ✓ Value date validation
- ✓ Old transaction dates
- ✓ Weekend/holiday patterns
- ✓ Rapid transaction velocity

**Scoring:**
- Old dates (>30 days): +0.2
- Invalid date format: +0.1

### 4. Individual Transaction Analysis

**Checks:**
- ✓ Transaction history patterns
- ✓ Behavioral anomalies
- ✓ Known fraud patterns
- ✓ Statistical outliers

**Scoring:**
- Provided by FraudDetectionService
- Weighted at 40% in final score

## Routing Thresholds

| Fraud Score | Range | Decision | Action |
|-------------|-------|----------|--------|
| **Low Risk** | 0.0 - 0.3 | ✅ APPROVE | Route to normal processing |
| **Medium Risk** | 0.3 - 0.8 | 🔍 REVIEW | Route to LLM for AI analysis |
| **High Risk** | 0.8 - 1.0 | ❌ REJECT | Automatic rejection, block transaction |





