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
            allocated_credits = self.allowance_credits
            new_agent = Agent(emissions_amount, allocated_credits)
            self.agents.append(new_agent)

    def randomize_emission_amount(self):
        #testing purposes
        all_cr = self.allowance_credits
        min_emission = int(math.floor(all_cr - all_cr * 0.2))
        max_emission = int(math.floor(all_cr + all_cr * 0.2))
        emission_amount = random.randint(min_emission, max_emission)

        return emission_amount

    def list_buyers_sellers_satisfied(self):
        """
        Based on the amount of allowances versus emissions,
        buyers and sellers are sorted in their respective lists
        """
        buyers = []
        sellers = []
        satisfied = []
        for agent in self.agents:
            if agent.allocated_credits > agent.emissions_amount:
                sellers.append(agent)
            elif agent.allocated_credits > agent.emissions_amount:
                buyers.append(agent)
            else:
                satisfied.append(agent)

        return buyers, sellers, satisfied

    def sort_sellers_buyers(self, buyers, sellers):
        """
        Sorts buyers by their maximum buying price
        and sellers by their minimum selling price.
        """
        for buyer1 in buyers:
            for buyer2 in buyers[1:]:
                if buyer1.max_buying_price < buyer2.max_buying_price:
                    buyer1_index, buyer2_index = buyers.index(buyer1), buyers.index(buyer2)
                    buyers[buyer2_index], buyers[buyer1_index] = buyers[buyer1_index], buyers[buyer2_index]

        for seller1 in sellers:
            for seller2 in sellers[1:]:
                if seller1.min_selling_price < seller2.min_selling_price:
                    seller1_index, seller2_index = sellers.index(seller1), sellers.index(seller2)
                    sellers[seller2_index], sellers[seller1_index] = sellers[seller1_index], sellers[seller2_index]

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




