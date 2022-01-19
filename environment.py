import random
import math
from agent import Agent

class Environment:
    def __init__(self, number_of_agents, allowance_credits, time_steps):
        self.number_of_agents = number_of_agents
        self.time_steps = time_steps
        self.allowance_credits = allowance_credits
        self.average_price = 0
        self.agents = []
        self.results = []

    def create_agents(self):
        for _ in range(self.number_of_agents):
            emissions_amount = self.randomize_emission_amount()
            buying_price = self.randomize_prices()
            selling_price = self.randomize_prices()
            allocated_credits = self.allowance_credits
            new_agent = Agent(emissions_amount, allocated_credits, buying_price, selling_price)
            self.agents.append(new_agent)

    def randomize_emission_amount(self):
        #testing purposes
        all_cr = self.allowance_credits
        min_emission = int(math.floor(all_cr - all_cr * 0.2))
        max_emission = int(math.floor(all_cr + all_cr * 0.2))
        emission_amount = random.randint(min_emission, max_emission)

        return emission_amount

    def randomize_prices(self):
        #testing purposes
        original_price = 60
        min_price = int(math.floor(original_price - original_price * 0.2))
        max_price = int(math.floor(original_price + original_price * 0.2))
        random_price = random.randint(min_price, max_price)

        return random_price

    def list_buyers_sellers_satisfied(self):
        """
        Based on the amount of allowances versus emissions,
        buyers and sellers are sorted in their respective lists.
        Those who have equal amount of allowances and emissions are satisfied.
        """
        buyers = []
        sellers = []
        satisfied = []
        for agent in self.agents:
            if agent.allocated_credits > agent.emissions_amount:
                sellers.append(agent)
            elif agent.allocated_credits < agent.emissions_amount:
                buyers.append(agent)
            else:
                satisfied.append(agent)

        return buyers, sellers, satisfied

    def sort_sellers_buyers(self, buyers, sellers):
        """
        Sorts buyers by their maximum buying price
        and sellers by their minimum selling price.
        """
        buyers.sort(key=lambda x: x.max_buying_price, reverse=True)
        sellers.sort(key=lambda x: x.min_selling_price, revers = False )


        return buyers, sellers

    def do_magic(self):
        """
            • Buyers list sorted by max price
            • Sellers list sorted by min price
            • Market rules:
                1. Buyers with higher min prices matches first with lowest min price -> price = average
                2. Transaction and actualisation of Buyer/seller list
                3. Step 3 until all sellers or buyers reached their max sell/buy capazity.
        """




