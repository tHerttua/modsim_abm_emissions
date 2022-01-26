# Group 4: Modeling the price dynamics of CO2 emission allowances 

## Agents

### 1 Properties

Upon initialization takes the following parameters:
- Initial amount of emissions
- Number of allowance credits to work with
- Limit of transactions per time step
- Max price for buying credits
- Min price for selling credits
- Original price (as the other prices may be updated)

- Other variables to store the transactions history: prices, deals, emisisons

### 2 Methods overview

Upon agreeing on a transaction, agents track their state:
- Number of transactions available for the time step is decreased
- Current credits are either increased, depending on whether agent bought or sold
- The buying or selling price may be updated, if no transaction happened during a step
- Total amount of emissions is accumulated
- Additionally, there is a chance that an agent can reduce their emission

## Environment

### 1 Properties

Upon initialization, environment takes the arguments:
- Number of agents per group
- Number of different groups
- Number of allowance credits to be distributed to each agent
- The time steps (Hard coded for 365)

Global variables can be modified to control their respective targets:
- Variance in emissions range
- Variance in price range
- Original price per one credit

### 2 Methods overview

- First agents and listed are created using randomized prices, credits, transaction limit and time steps
- Prices are generated using randomization method which uses price variance and the original price point
- Emission amount per agent is based on the allocated credits, further randomized to create situation with some agents 
falling under the allowed amount, and some above.
- Buyers and sellers are separated in different lists, and later sorted in anoter method
- Method to iterate through the lists and do transactions (details in next section)
- Methods to visualize progress over the steps
- Emissions accumulate for each agent every time step, and each "month" or 31 steps agents are allocate more credits

### 3 Transactions logic

do_transaction abstracts the agent behaviour and matches agents to do transaction with each other.
- Iterates through the list of buyers, which is sorted by the highest price, in sequential activation order.
- The buyer with the highest price has the priority to choose the seller, which will be the one who has the lowest price
- The matched buyer and seller will do transactions between each other until transaction limit is met by either
or they have reached their limit of how many credits they want to sell or buy
- Additionally seller may drop the emissions to sell credits over the limit between emissions versus current credits
- Buyer moves to the next seller, if transaction conditions are not met
- If buyer and seller did not do any transactions, because they didn't match by their prices, buyer increases the price
to buy at and seller lowers the price to sell at
- After each agent has been iterated through, their transaction limit is reseted for the next time step

## The setting

- There are 300 companies, 3 groups, 100 companies per group
- Each of the companies are allocated x credits (source)
- One credit is worth X € (source)
- The companies do transactions between each other over span a year (365 time steps)
- Companies accumulate emissions in daily basis towards the total emissions count
- Every month (30 time steps) the companies are allocated more credits
- Because of the randomization, there can be companies which: 
have less credits than they have emisions (credit buyers),
have more credits than they have emissions (credit sellers)
and those who have equal amount of credits and emissions (satisfied)

## Results

- Different hyper parameters yield ...
- About prices convergence
- Emissions reduced
- What else?





