# Group 4: Modeling the price dynamics of CO2 emission allowances 


## Moduls overview

To investigate the model, three modules with ploting and calulating results are offered
  -modul 1: decreases in different runs of the model the credit_reducing facor
  -modul 2: increases in different runs of the model the limit transaction number per agets
  -modul 3: runs the model multiple times with the same parameter and calculates the average outcomes and plots it
  
Results are saved in the \pics direcory

Also, two extension can be set on and off:
Firstly, do agents decide after a logic to be seller or buyer or randomly
Secondly, are agents allowed to reduce emissions for additional credits after a successful transaction in the same step
  
Initial values
  -array of allowances per group
  -unexpected credit reducing factor
  -limit transactions
  -agents per group
  
## Agents

### Properties

Upon initialization takes the following parameters:
- Initial amount of emissions
- Number of allowance credits to work with
- Limit of transactions per time step
- Max price for buying credits
- Min price for selling credits
- Original price (as the other prices may be updated)

- Other variables to store the transactions history: prices, deals, emisisons

## Environment

### Properties

Upon initialization, environment takes the arguments:
- Number of agents per group
- Number of different groups
- The time steps (Hard coded for 360)

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

### Transactions logic

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


- agents calculates whether number of credits is enough to reach the end of the month
- by introducing the credit reduction rate, agents become the rate less credits as expected each month, so we can
- play in the model with the expectations of the agents

## The setting

- Each of the companies are allocated x credits (source), initial depends on allowances array
- One credit is worth X € (source)
- The companies do transactions between each other over span a year (360 time steps)
- Companies accumulate emissions in daily basis towards the total emissions count
- decide their action also based on the fact how many emissions are left for reaching the end of the month
- Every month (30 time steps) the companies are allocated more credits
- Because of the randomization, there can be companies which: 
have less credits than they have emisions (credit buyers),
have more credits than they have emissions (credit sellers)
and those who have equal amount of credits and emissions (satisfied)

## Results
- average paid price
- average number of transaction
- price expectation development
- ratio from buyer to seller
- individuall emission and credit path of agents (just for illustration)

- Different hyper parameters yield ...
- About prices convergence
- number of transactions
- dynamic of the model
- ratio buy sellers
- price expectation convergence

-results are saved in the \pic direcory




