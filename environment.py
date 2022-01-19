import random
from agent import Agent

class Environment:
    def __init__(self, number_of_agents, allowance_credits, time_steps):
        self.number_of_agents = number_of_agents
        self.time_steps = time_steps
        self.allowance_credits = allowance_credits
        self.average_price
        self.agents = []
        self.results = []

    def create_agents(self):
        for _ in range(self.number_of_agents):
            emissions_amount = self.randomize_emission_amount
            allocated_credits = self.allowance_credits
            new_agent = Agent(emissions_amount, allocated_credits)
            self.agents.append(new_agent)

    def randomize_emission_amount(self):
        emission_amount = 1000
        return emission_amount

    def list_buyers_and_sellers(self, list_of_agents):
        """
        Based on the total amount
        """

    def do_magic(self):
        """
            • Buyers list sorted by max price
            • Sellers list sorted by min price
            • Market rules:
                1. Buyers with higher min prices matches first with lowest min price -> price = average
                2. Transaction and actualisation of Buyer/seller list
                3. Step 3 until all sellers or buyers reached their max sell/buy capazity.
        """




