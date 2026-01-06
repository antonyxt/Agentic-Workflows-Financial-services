## Objective
*  This exercise will help you understand the use of orchestration and workers to help process a message.

## SWIFT Audits
*  Almost every day, each bank will have to detail to the federal government different types of audit reports about money transactions that happen at the bank.  For this reason, there are large sets of infrastructure that create these reports.
*  One negative input of audit reports is that there is no consensus on what is to be reported as requirements change annually.  One great thing about agents and LLMS is that they can't mimic reasoning on what compliance reports are needed.
*  In our SWIFT system, we will ask the LLM to process the whole thing.  We are going to process a group of messages and ask the LLM to process four tasks that it thinks it needs to process.

## Return Prompt
*  Let's look at our return prompt from the task creator agent.
```
{'analysis': 'The provided SWIFT messages consist of both MT202 and MT103 message types, indicating interbank fund transfers and customer credit transfers, respectively. The messages involve transactions in various currencies, including EUR, USD, SGD, and GBP. The transactions are pending processing, and the focus is on analyzing the amounts by country and currency without considering fraud or compliance aspects.', 
'tasks': [{'type': 'data extraction', 'description': 'Extract the relevant data from each SWIFT message, focusing on the amount, currency, sender BIC, and receiver BIC.'}, 
          {'type': 'country identification', 'description': 'Identify the countries involved in each transaction based on the sender and receiver BIC codes.'}, 
          {'type': 'amount aggregation', 'description': 'Aggregate the transaction amounts by country and currency to prepare for reporting.'}, 
          {'type': 'report generation', 'description': 'Generate a report that summarizes the total transaction amounts by country and currency.'}]}
```
* The tasks are associated with the prompt we originally gave the agent (kind of).  We told the agent
     ```
     Your job is to analyze these messages and process them. Only concern your self with amounts, countries, debits and credits.
     ```

## Deliverables
*  This will be an easy exercise but meaningful.  In the OrchestratorWorker class, create another class to handle a fifth task.  Instead of using GenericAgent, create another class.
*  You will have to change the prompt to guide the agent to create a new task.
*  Take a look at what the LLM returns now to see that it is doing a good job of analyzing and creating reports.  For example, the data extraction llm returns the below with minimal guidance:

```
- **Currencies Involved:**
  - EUR: 1 transaction
  - USD: 2 transactions
  - SGD: 1 transaction
  - GBP: 1 transaction

- **Total Amounts by Currency:**
  - EUR: 6816.45
  - USD: 9406490.54 (15318.68 + 9391171.86)
  - SGD: 803.18
  - GBP: 2449939.53

- **BIC Codes:**
  - Sender BICs: VCNLCAL120M, IWRMCARI05Q, IKRPGBBR2T6, KEKDAU8YAKK, JBJGJPCMUJV
  - Receiver BICs: GFPRAU58ZW7, VEILAUS0F31, WPEBHK35MXJ, NQFPCHWVAAP

This data provides a clear overview of the transactions, focusing on the amounts and currencies involved, as well as the sender and receiver BICs. This information can be used for further analysis or reporting as needed.
```
