

## 🧠 End-to-End Routing Flow
```mermaid
flowchart TD
  Swift --> D[_create_test_scenarios]
  D --> E{Loop through SWIFTMessage scenarios}
  E --> F[_demonstrate_llm_routing]
  F --> G[llm_routing_agent.route_message]

  subgraph LLMRoutingAgent Flow
    G --> H[_main_llm_initial_analysis]
    H --> I{specialist_llm?}
    I -->|PROCESSING| J1[_processing_llm]
    I -->|FRAUD_DETECTION| J2[_fraud_detection_llm]
    I -->|BALANCE_CHECK| J3[_balance_check_llm]
    I -->|MESSAGE_VALIDATION| J4[_message_validation_llm]
    J1 & J2 & J3 & J4 --> K[_main_llm_final_processing]
    K --> L[_update_message_with_results]
  end

  L --> M[[Return updated SWIFTMessage]]
  M --> N[Print results & decision]
  N --> E
  E -->|All done| Z[🏁 Demonstration Complete]
