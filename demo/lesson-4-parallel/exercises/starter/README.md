## Objective
* To understand how parallelization can work with SWIFT and processing transactions.

## Udacity SWIFT
* One thing to remember is that SWIFT transactions need to processed quickly.  There are processes that occur during the process of a SWIFT transaction and processes that happen after the SWIFT transaction. One process that would be nice to have before a transaction is processed is Fraud detection.  Agents and LLMS take time so this type of work may be left for transactions that are allowed to take minutes to process but to speed up processing, we can add parallelization.
* Parallelization also helps in the enterprise architecture concept.  There may be some rules that are new or temporary, like the Russian sanctions that happened some years ago.  Instead of changing your code base, you can create a class that will be automatically pulled into the loop that processes the message.  This class will update the message and finally be consumed by the last agent.
* The flow:

``` mermaid
flowchart TD
    Start(["SWIFT Transaction Initiated"])
    Fork{{"Parallel Agent Workflows"}}
    subgraph ComplianceAgent["Your Agent"]
        CompCheck(["Your Check"])
        CompCheck --> CompResult{"Fraud Detected?"}
    end
    subgraph RiskAgent["Amount Agent"]
        RiskCheck(["Amount Checked"])
        RiskCheck --> RiskResult{"Fraud Detected?"}
    end
    subgraph AMLAgent["Pattern Agent"]
        AMLCheck(["Fraud Pattern"])
        AMLCheck --> AMLResult{"Fraud Detected?"}
    end
    Join{{"Aggregate Results"}}
    AllGood(["Transaction Executed"])
    Flagged(["Fraud Detected - Investigation Initiated"])

    Start --> Fork
    Fork --> CompCheck
    Fork --> RiskCheck
    Fork --> AMLCheck
    CompResult -->|Yes| Join
    RiskResult -->|Yes| Join
    AMLResult -->|Yes| Join
    CompResult -->|No| Join
    RiskResult -->|No| Join
    AMLResult -->|No| Join
    Join -->|Any Agent Detected Fraud| Flagged
    Join -->|All Agents Clear| AllGood
```
## Fraud
*  There is no way to 100% say a transaction is fraud or not before it is proccessed.  Most fraud detection happens after the fact, when the person who is losing the money complains.  What happens then is the account is locked and prevented from further transactions.
*  In order to stop a payment before processing, we need to detect a probablilty for fraud or create a fraud score.  Based on this score, we can infer fraud.  This is where deterministic and non-deterministic flow starts to show a grey area.
*  In a deterministic flow, we can increase a fraud score based on certain key conditions (i.e high amounts, out of time transactions).  Based on this score, (i.e.  amount > 99999), we can infer the transaction is fraud.  The issue here is that we cannot easily create exceptions to the rule without changing the code base.
*  In an agent workflow, we can let the LLM make the decision on what is fraud or not.  This is problematic.  I can tell an agent tell me what is fraud in a one liner or I can write a page.  Depending on your prompt will determine the decision.  Adding memory will also cause issues.
*  In SWIFT transactions and detecting fraud, you need to mix both types of flows.  In one scenario, I will tell an agent this is specifically what fraud means and you score this message.  In another llm, I will give a different idea of fraud.  Both agents will update the message and a final aggregrator will make the determinations.

## Udacity SWIFT 
* We have two classses that represent two different agents.
  * FraudAmountDetectionAgent
    * In the prompt, we state these are the rules for fraud.
      * Rule 1.  if the amount > 10000 this reflects a very high amount and has risk. Add .3 to total risk score
      * Rule 2.  if amount >= 5000 and amount % 1000 == 0.  This Round amount suggesting structuring: $<amount> and add .2 to total risk score
      * Rule 3.  if amount > 100000 and the decimal part of the amount is not 00 or 50.  This is unusual precision for large amount and add .1 to total risk score.
  * FraudPatternDetectionAgent
     * In the prompt, we state these are the rules for fraud.
       * These are high risk patterns  'TEST.*', 'FAKE.*', 'DEMO.*', '.*999.*', '.*000000.*'
       * Rule 1.  if the sender bic or the receiver bic contain any of the high risk patterns, this suggests fraud and add .3 to total risk score.
       * Rule 2.  If the sender bic and the receiver bic are the same, this can be fraud and add a .2 to the total risk score.
       * Rule 3.  If any words are misspelled, that could be fraud and add a .1 to the total risk score.
* What happens is that each class makes an evaluation for fraud and lets the agregrator decide.  The prompt for the aggregrator is the following:
  
"Please review the following messages and tell me if a Swift transaction with these messages is fraudulent or not.

{message}

Please respond in json format with "thought" that contains the final review and "total_fraud_score" which contains your assessment from 1 to 100
on what you think the fraud score should be.  100 being highest. "

## Deliverables
* Create your own class like FraudAmountDetectionAgent and FraudPatternDetectionAgent.  Add this class to the loop that is reading the class.  This loop will process the messages in parallel.
* Change your prompt to to make all messages fail and are held for fraud.
* Change your prompt to make all messages pass.
* You can only change your current prompt in your new class.  The point here is to see when the agent goes off on its own on determining what is fraud and not.  For example, in your prompt, you can say that " return this message is fraud" and see what happens.

