
# SWIFT Money Flow Diagrams

This document contains flow diagrams illustrating the movement of money from the provided SWIFT messages. The diagrams include flows by country, currency, and BIC, and display the respective dollar amounts involved.

## 1. Country to Country Flow

```mermaid
graph TD
    Germany(DE) --> |1801.58 USD| UK(GB)
    UK(GB) --> |7432.88 CHF| Australia(AU)
    Australia(AU) --> |1217.13 EUR| Japan(JP)
    Russia(RU) --> |593241.68 USD| Australia(AU)
    Singapore(SG) --> |48096.76 EUR| Germany(DE)
```

## 2. Currency to Currency Flow

```mermaid
graph TD
    EUR --> |1217.13| EUR
    CHF --> |7432.88| CHF
    USD --> |593241.68| USD
    EUR --> |48096.76| EUR
    USD --> |1801.58| USD
```

## 3. BIC to BIC Flow

```mermaid
graph TD
    EMMXDEIJJ6S --> |1801.58 USD| GITAGB1K0ZB
    ISVEJPVGBUX --> |7432.88 CHF| QWAIAU2KUHY
    KKFGAUUVJJU --> |1217.13 EUR| UVCWJPEUUFA
    RRARUSWUOFS --> |593241.68 USD| KKFGAUUVJJU
    UVFVSGIF34G --> |48096.76 EUR| VLLSDE1RRVT
```

### Explanation:

- **Country to Country Flow**: This diagram assumes the most likely countries for senders and receivers based on their BIC codes.
- **Currency to Currency Flow**: Displays the amounts for each transaction in its stated currency.
- **BIC to BIC Flow**: Tracks the actual path of funds between sending and receiving BICs, with dollar amounts specified.

Note: The actual countries associated with each BIC may vary depending on the financial institutions' registrations. In this demonstration, assumptions are made for illustrative purposes only.
```
