# Instructions

## Purpose
* The purpose of this lesson is to show how you can create a workflow with LLM's to create an agentic system.
* This workflow is the start of how SWIFT transactions can be verified in a financial context.

## SWIFT Flow
* Remember, that a SWIFT message is similar to a JSON file and transmits payment data from one instituion to the next.
* In our Udacity SWIFT architecture, we will evaluate SWIFT messages and then add fields to the SWIFT message to be processed in later stages of the pipeline.
* SWIFT messages work well with LLM's since we can ask LLMS to evaluate each stage of the process.
* A typical SWIFT flow is the following:

  ``` mermaid
  flowchart LR
    A(["Start"]) --> n1["Receive Message"]
    B{"Check for Error Messages"} --> C["Yes"] & D["No"]
    n1 --> n2["Convert to Database"]
    n2 --> B
    D --> n3["Check for Fraud"]
    n3 --> n4["Yes"] & n5["No"]
    C --> n6["Back to Sender"]
    n4 --> n7["Stop Message"]
    n5 --> n8["Check for AML"]
    n8 --> n9["Yes"] & n10["No"]
    n9 --> n11["Hold"]
    n10 --> n12["Check for Debit/Credit Avaiability"]
    n12 --> n13["Pass"] & n14["Fail"]
    n13 --> n15["Process Transaction"]
    n1@{ shape: event}
    n2@{ shape: event}
    n3@{ shape: diam}
    n4@{ shape: rect}
    n5@{ shape: rect}
    n8@{ shape: diam}
    n12@{ shape: diam}
  ```
  * A SWIFT transaction usually has .001 seconds to process in a bank.  Because of this need to be quick, most banks will process the SWIFT transactions in two parallel streams. One stream to process the transaction and another to record the transaction for further evaluation.
  * There are some key issues to understand when processing SWIFT transactions that will allow us to update a message real time and when to process something after the fact.
      * Errors
          * SWIFT messages can be created by a human or a machine and can have mistakes.  For example, a BIC value could be truncated and this will prevent the message from being processed.  The second a bank receives a message, there are some protocols that can be checked and the message returned immediately for issues.
      * AML issue
          *  There is a list of countries that US banks cannot do business with.  For this reason, certain currencies are prohibited.  Currency is an easy catch for pre-processing SWIFT messages.
      *  Fraud
          *  Fraud is difficult to discover at time of the messsage.  If a beneficiary account is compromised, pre-processing can be established to reject beneficiary issues up front.  More than likely, fraud will happen after the transaction is processed but there is a time frame to recoup that transaction so the sooner fraud is detected the better.
      *  Funds are available
          *  The SWIFT transaction allows the bank to move money from one bank to another.  There is a need to do some processing to check if funds are available and to check if amounts seem correct.

## Udacity SWIFT
  *  What we are building here is a fictious system to show how agentic workflows can help expedite the process of SWIFT transactions.  This will not be a perfect system but it will help you think on what else can be done to improve this type of work to use in a real world setting.
  *  The code is in python.  The runnable class is demo_workflow.py.
  *  demo_workflow.py calls the WorkflowPatternDemo class.  The instantiation of this class creates three agentic patterns that will evaluate the message.  In this section, there are two agents we care about.  The first is the evaluator and the second is the prompt chainer.  Right now, we do not care what they are doing but we need you to understand how the system is working.
  *  The goal of Udacity SWIFT is to process messages in real time in one flow with parallel processing.  While SWIFT transactions today involve many systems, Udacity SWIFT will only need one system because the SWIFT messages will become self correcting and self routing.  Each processing stage is added to the message and then re-routed by LLMS for processing.

## Deterministic and non-Deterministic Flows
*  LLMS and agentic workflows cater to non-deterministic flows.  When we use LLMs, we offer new ambiguity to the results.  Because of this, many try to avoid workflows that have any level of certainty to avoid inaccuracy.  In the Udacity SWIFT system, we are showing how deterministic flows can be mixed in with the non-determinism flows to process transactions.  We do this by mixing deteriminstic code with the LLM prompts.  This will be part of your first exercise.

## Deliverables
* Create a power point with three pages.
    * The first page should be who you are and why we should believe what you have to say.
    * The second page will introduce us to why we should be using agents and LLMS to process SWIFT transactions.
    * The third page should explain the flow of the current system to include the following:
        * Generating fake swift messages.
        * Evaluator optimizer
        * prompt chaining
* Review the SWIFTMessage.py and in any document, tell us:
    * Why is this class needed?
    * What is the variable validation_status and is it used in the program.
    * A print out of agent perspectives after the process has run.
* Looking at the code, you will see that prompt chaining does not do anything because there are no high risk messages.  Please create an agent that can change the fraud score to create high risk messages.
    1.  Create a new class that will call a prompt.  Try to mimic the PromptChainingAgent.
        *  Instantiate this class in WorkflowPatternDemo.
        *  Call the classs to return either a processed message or json that will update the message.
    2. You are going to create a prompt that will act like a fraud processor that will initially screen a SWIFT message for abnormalities.  You can leave the definition of fraud up to the LLM.  As you can see, once you increase the fraud score, you will have another workflow that will merge deterministic analysis with LLM prompts.
       *  An example prompt could be "You are a SWIFT analyst looking for fraud.  Please return a fraud_score in json format"
    3. In the PromptChainingAgent, add the agent perspectives from the prompt chain back to the message and print out the results from the SWIFTMessage class.
