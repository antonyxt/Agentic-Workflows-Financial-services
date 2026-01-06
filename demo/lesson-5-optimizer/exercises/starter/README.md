## Objective
* Understand how optimization works and how important this pattern is.
* Understand the enterprise architecture when using this technique.

## Optimization
*  Remember that a SWIFT statement is a freeform text file that is interpreted by financial systems to direct payments.  Because of this, SWIFT statements can be incorrect and turned around to be sent back to the originating bank.
*  What the Udacity SWIFT application can try to do is to self correct a SWIFT message if errors are found.
*  In this exercise, you will tend to use more deterministic processing to correct SWIFT payments.  In the final project,  you will see allow the agent to try to self correct a message without using external classes.
*  Again, this architecture brings up the idea of enterprise architecture.  The rules that are created are not necesssarily in your control but the application will consume them and present them to the final agent.

## Flow
* There is a new class called SWIFTValidator.py.  This class contains the deterministic rules on how a SWIFT message should be formatted.  What we are doing is creating a deterministic prompt to be used to optimize a payment.
* Example:
    * In the validator we call validate_swift_message.
      * The first validation is validating SWIFT fields.  In this method, we check a config for SWIFT standards which contain the fields that are required.
      * One thing to note is that we are creating SWIFT messsage classes to test and are not using the SWIFT message directly.  The SWIFTMessage class can be changed to use the SWIFT dictionary.
      * In the basic field validation check, we look to see if a field exists and if so, verify the type.  For example, a non-numeric amount is an issue.
      * When an error is determined, we add an error response to a result list that will eventually get passed up to the final stage agent.
      * This error can just the error or it can be a correction.  For example, the error message can be "the amount is 9999 and should be 9000.  Please correct the amount to 9000".  This is allowing you to help prompt the final agent on how to fix the message otherwise you will leave it up the llm to decide how to fix.
  *   The next key method is optimize swift message.
       * In this method, we create a correction prompt with this signature:
         
You are a SWIFT message validation expert. Please help correct the following SWIFT message:

Message Type: {message.message_type}
Reference: {message.reference}
Currency: {message.currency}
Sender BIC: {message.sender_bic}
Receiver BIC: {message.receiver_bic}
Value Date: {message.value_date}

Validation Errors Found:
{chr(10).join(f"- {error}" for error in errors)
   * As you can see, we are printing the error in the prompt.  In our last example, the prompt will include, "the amount is 9999 and should be 9000.  Please correct the amount to 9000". 
   * There is no correct way to do this type of processing without using tools and that will be handled in aonther lesson.  But in this scenario, we are asking the agent, to send a json back with the corrections.  What we can also try to do is to ask the agent to correct the message directly.
## Deliverables
* Create a powerpoint with a flow of the architecture, stating what rules are governed through the agents and what rules are determined in a class.
* In the validator class, create a currency check.  For example, you can add that AFN violates the compliance rules and to label this message as fraud.
* In the DetailedEvaluatorOptimizer class, make the amount checks work.  Right now, the code will go through three iterations of amount checks and not pass the transaction.  You have to change the prompt to handle the amounts.  I gave a hint earlier on on add a correction in the error handling.
