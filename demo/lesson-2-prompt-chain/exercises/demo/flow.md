
## Agent Chain Flow

```mermaid
flowchart TD
    Start([SWIFT Transaction<br/>+ Fraud Score<br/>+ Risk Indicators]) --> Screener
    
    Screener[🔍 Agent 1: Initial Screener<br/>Fast Triage Assessment] --> S1{Triage<br/>Decision?}
    S1 -->|GREEN| ScreenerOut[Low Priority]
    S1 -->|YELLOW| ScreenerOut[Medium Priority]
    S1 -->|RED| ScreenerOut[High Priority]
    
    ScreenerOut --> Technical[🔧 Agent 2: Technical Analyst<br/>Format & Data Validation]
    
    Technical --> T1{Technical<br/>Validation?}
    T1 -->|VALID| TechOut[Format Compliant]
    T1 -->|ISSUES| TechOut[Technical Concerns]
    
    TechOut --> Risk[📊 Agent 3: Risk Assessor<br/>Pattern & Behavior Analysis]
    
    Risk --> R1{Risk<br/>Assessment?}
    R1 -->|APPROVE| RiskOut[Low Risk Pattern]
    R1 -->|INVESTIGATE| RiskOut[Medium Risk]
    R1 -->|BLOCK| RiskOut[High Risk Pattern]
    
    RiskOut --> Compliance[⚖️ Agent 4: Compliance Officer<br/>Regulatory Review]
    
    Compliance --> C1{Compliance<br/>Status?}
    C1 -->|COMPLIANT| CompOut[Meets Regulations]
    C1 -->|QUESTIONABLE| CompOut[Requires Investigation]
    C1 -->|NON_COMPLIANT| CompOut[Violations Detected]
    
    CompOut --> Final[👔 Agent 5: Final Reviewer<br/>Synthesis & Decision]
    
    Final --> FD{Final<br/>Decision?}
    FD -->|APPROVE| Approve[✅ APPROVE<br/>Process Transaction]
    FD -->|HOLD| Hold[⏸️ HOLD<br/>Manual Review Required]
    FD -->|REJECT| Reject[❌ REJECT<br/>Block Transaction]
    
    Approve --> End([Transaction Decision])
    Hold --> End
    Reject --> End
    
    style Start fill:#e3f2fd
    style Screener fill:#fff3cd
    style Technical fill:#d1ecf1
    style Risk fill:#f8d7da
    style Compliance fill:#d4edda
    style Final fill:#e2e3e5
    style Approve fill:#d4edda
    style Hold fill:#fff3cd
    style Reject fill:#f8d7da
    style End fill:#e3f2fd
```

## Detailed Agent Architecture

```mermaid
classDiagram
    class PromptChainingAgent {
        -Logger logger
        -Config config
        -OpenAI client
        -str model
        +analyze_transaction_chain(message, score, indicators) Dict
        +batch_process_with_chaining(messages, scores, indicators) List
        -_run_initial_screener() Dict
        -_run_technical_analyst() Dict
        -_run_risk_assessor() Dict
        -_run_compliance_officer() Dict
        -_run_final_reviewer() Dict
        -_create_error_response() Dict
    }
    
    class InitialScreener {
        <<AI Agent>>
        +triage_decision: GREEN|YELLOW|RED
        +immediate_concerns: List[str]
        +requires_deep_analysis: bool
        +escalation_priority: str
        +focus_areas: List[str]
        +perform_triage() Dict
    }
    
    class TechnicalAnalyst {
        <<AI Agent>>
        +format_compliance: str
        +bic_validation: str
        +amount_analysis: str
        +technical_concerns: List[str]
        +agrees_with_screener: bool
        +validate_format() Dict
    }
    
    class RiskAssessor {
        <<AI Agent>>
        +behavioral_score: float
        +pattern_analysis: str
        +contextual_factors: List[str]
        +risk_recommendation: str
        +confidence_level: float
        +assess_risk() Dict
    }
    
    class ComplianceOfficer {
        <<AI Agent>>
        +compliance_status: str
        +regulatory_concerns: List[str]
        +aml_assessment: str
        +legal_risk: str
        +required_documentation: List[str]
        +review_compliance() Dict
    }
    
    class FinalReviewer {
        <<AI Agent>>
        +final_decision: APPROVE|HOLD|REJECT
        +confidence_score: float
        +risk_level: str
        +consensus_reasoning: str
        +recommended_actions: List[str]
        +synthesize_decision() Dict
    }
    
    PromptChainingAgent --> InitialScreener
    PromptChainingAgent --> TechnicalAnalyst
    PromptChainingAgent --> RiskAssessor
    PromptChainingAgent --> ComplianceOfficer
    PromptChainingAgent --> FinalReviewer
    
    InitialScreener --|> TechnicalAnalyst : passes context
    TechnicalAnalyst --|> RiskAssessor : passes context
    RiskAssessor --|> ComplianceOfficer : passes context
    ComplianceOfficer --|> FinalReviewer : passes context
```

## Sequence Diagram - Agent Conversation

```mermaid
sequenceDiagram
    participant T as Transaction
    participant PC as PromptChainingAgent
    participant S as Screener Agent
    participant TA as Technical Analyst
    participant RA as Risk Assessor
    participant CO as Compliance Officer
    participant FR as Final Reviewer
    
    T->>PC: Transaction + Fraud Score + Indicators
    
    PC->>S: Step 1: Initial Triage
    Note over S: Fast assessment<br/>Flag red flags<br/>Set priority
    S-->>PC: Triage Decision (GREEN/YELLOW/RED)
    
    PC->>TA: Step 2: Technical Analysis + Screener Result
    Note over TA: Format validation<br/>BIC analysis<br/>Data integrity check
    TA-->>PC: Technical Validation + Concerns
    
    PC->>RA: Step 3: Risk Analysis + Previous Results
    Note over RA: Behavioral patterns<br/>Contextual factors<br/>Risk scoring
    RA-->>PC: Risk Assessment + Recommendation
    
    PC->>CO: Step 4: Compliance Review + All Previous Results
    Note over CO: Regulatory check<br/>AML assessment<br/>Policy validation
    CO-->>PC: Compliance Status + Legal Risk
    
    PC->>FR: Step 5: Final Synthesis + All Agent Opinions
    Note over FR: Weigh all opinions<br/>Resolve conflicts<br/>Make decision
    FR-->>PC: Final Decision (APPROVE/HOLD/REJECT)
    
    PC-->>T: Complete Chain Analysis Result
```

## Agent Roles & Responsibilities

### 🔍 Agent 1: Initial Screener
**Role:** Fast triage and priority assessment

**Outputs:**
- `triage_decision`: GREEN | YELLOW | RED
- `escalation_priority`: LOW | MEDIUM | HIGH | CRITICAL
- `immediate_concerns`: List of red flags
- `requires_deep_analysis`: Boolean flag
- `focus_areas`: Areas needing attention

**Expertise:**
- Quick pattern recognition
- Immediate risk flagging
- Priority setting

---

### 🔧 Agent 2: Technical Analyst
**Role:** Deep technical validation and format analysis

**Outputs:**
- `format_compliance`: VALID | MINOR_ISSUES | MAJOR_ISSUES | INVALID
- `bic_validation`: BIC code analysis
- `amount_analysis`: Amount pattern analysis
- `technical_concerns`: Technical red flags
- `agrees_with_screener`: Consensus check

**Expertise:**
- SWIFT message format validation
- BIC code verification
- Data integrity assessment
- Technical compliance

---

### 📊 Agent 3: Risk Assessor
**Role:** Behavioral pattern and risk analysis

**Outputs:**
- `behavioral_score`: 0.0 - 1.0
- `pattern_analysis`: Suspicious patterns
- `contextual_factors`: Risk factors
- `risk_recommendation`: APPROVE | INVESTIGATE | BLOCK
- `confidence_level`: 0.0 - 1.0

**Expertise:**
- Behavioral pattern recognition
- Historical comparison
- Contextual risk evaluation
- Statistical analysis

---

### ⚖️ Agent 4: Compliance Officer
**Role:** Regulatory compliance and legal assessment

**Outputs:**
- `compliance_status`: COMPLIANT | QUESTIONABLE | NON_COMPLIANT
- `regulatory_concerns`: Regulatory issues
- `aml_assessment`: AML evaluation
- `legal_risk`: LOW | MEDIUM | HIGH | CRITICAL
- `required_documentation`: Additional docs needed

**Expertise:**
- Anti-money laundering (AML) regulations
- Financial compliance
- Legal risk assessment
- Policy enforcement

---

### 👔 Agent 5: Final Reviewer
**Role:** Synthesis and final decision making

**Outputs:**
- `final_decision`: APPROVE | HOLD | REJECT
- `confidence_score`: 0.0 - 1.0
- `risk_level`: LOW | MEDIUM | HIGH | CRITICAL
- `consensus_reasoning`: Decision rationale
- `recommended_actions`: Next steps
- `conflict_resolution`: How conflicts were resolved

**Expertise:**
- Multi-perspective synthesis
- Conflict resolution
- Final decision authority
- Strategic reasoning

