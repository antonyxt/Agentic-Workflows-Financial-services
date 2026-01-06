## Objective
* The purpose of this exercise is to show how to have an agent do the routing.
* Mixing old architecture with LLMs.

## A Typical Swift flow
*  One thing to understand is that SWIFT messages are usually freeform text.  Anything can go in a SWIFT message.  The hope is that there is enough information in the message to complete a transaction.  One argument I would like to make is what if rules change or you are trying to meet new compliance audits.  Sometimes you would want to add items to the SWIFT message or change fields in the message to allow the transaction to go through.  One way to do this is to mix agentic workflows with current technology streams.  For example, what if you need to verify the country of incorporation before the transaction is processed.  That information is not necesarrily in a SWIFT transaction but it is in the BIC and to find other information, you will have to check data in your proprietary databases.
*  I would like you to think about this while processing the router logic.  The main python script is in the demo_routing.py file.
  
  ``` mermaid
flowchart TD
    A(["Start"]) --> B["Receive Message"]
    B --> C["main_llm_initial_analysis"]
    C --> n1["route_to_specialized_llm"]
    n1 --> n2["Processing"] & n3["Fraud Detection"] & n4["Balance Check"] & n5["Message Validation"]
    n3 --> n6["Final Processing"]
    n2 --> n6
    n4 --> n6
    n5 --> n6
    B@{ shape: rounded}
    n1@{ shape: diam}
``` 
*  In our application, we receive a message and send the message to agent that will detect where the message needs to go next.  Usually, there would be a loop to keep processing messages until everything is complete, but we are leaving that idea open until after we discuss the other patterns.
*  The router will direct the next step to Processing, Fraud Detection, Balance Check or Message Validation.

## Deliverables
* Change the prompt in the intial analysis to make sure that Fraud Detection and Balance Check can be returned.
* Create the Balance Check and Fraud Detecton class that can be consumed by the rest of the program.  At the current time we are returning the message which is causing issues.
