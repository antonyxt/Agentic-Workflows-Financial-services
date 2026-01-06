## Objective
* To understand how you can pass the results of one LLM to another.
* Why we want to create prompt chains in enterprise applications.

## Enterprise Applications
* It is possible to give an agent a lot of power by asking it to do a lot.  The main issue that happens when doing this is that LLMS can get confused because of all the direction it is giving.  For this reason, many organizations use context engineering with LLMS only processing certain pieces of information.  Context engneering reduces hallucinations and increase accuracy.
* Another reason to distribute workload among different agents is cross departemental work.  There are pieces of the process that you are not privy to or do not have the ability to control.  Different departments handle different things.

## Udacity SWIFT
* Let's take a look at the code and understand the prompt chaining pattern and how it applies perfectly to SWIFT processing.
``` mermaid
flowchart LR
    A(["Start"]) --> n1["Receive Message"]
    B{"Initial Screener"} --> C["Reject"] & D["Keep Going"]
    n1 --> B
    D --> n2["Technical Analysis"]
    n2 --> n3["Reject"] & n4["Keep Going"]
    n4 --> n5["Final Review"]
    n5 --> n6["Process Transaction"] & n7["Hold"]
    n2@{ shape: diam}
    n5@{ shape: diam}
```
* We are asking the initial screener to return following:
  * "triage_decision": "GREEN|YELLOW|RED",
  * "immediate_concerns": ["list of immediate red flags"],
  * "requires_deep_analysis": true/false,
  * "escalation_priority": "LOW|MEDIUM|HIGH|CRITICAL",
  * "initial_reasoning": "Quick assessment reasoning",
  * "focus_areas": ["areas that need deeper analysis"],
  * "time_sensitivity": "How urgent is this review?"
* Based on the prompt we give the agent, we are allowing the agent free reign to decide if a SWIFT message should be returned to sender.   Since SWIFT processing includes multiple departments, the initial screening will probably not be in a department you are working in and you will get the result of the message.  You will now be tasked to either move this message forward.
* In our scenario, we will move the message to technical screening.  The task of the technical screener is to check reference data to see if the BIC format is correct, amounts are correct and dates are correct.  We pass in the message plus results from the initial screener.
* Finally, we pass the message and results to the final reviewer.  The job of this agent is to review previous agent decisions and determine if the message should continue to processing.
* One thing to note is that as the SWIFT message passes throught the system, we are adding hooks to the message to prompt LLMs later in the workflow.  As the message goes through the system, it is becoming smarter.

## Deliverables
* Add two classes to the project.
  * The first class is a risk assessor.  Risk can be associated with fraud but can be associated with financial risk.  Ask the LLM to check for large amounts or large credit amounts.  You can add anything you want to detect risk or you can ask the LLM to guide you on what risk topics to take.
  * The second class is compliance.  Remember, US banks cannot operate with banks on the 'do not trade' list.  Ask the LLM to check for regulated currencies or countries in the message.
* Add the results from both in the SWIFT message under agent_perspectives.  Have the final reviewer review you perspectives.  In the demo_prompt_chain class, there is output at the end to print out your agent perspectives.
* In a powerpoint, draw a class diagram detailing your new classes and provide what function each class accomplishes.

  
