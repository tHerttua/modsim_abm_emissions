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
            if agent.pre_allocated_credits > agent.emissions_amount:
                sellers.append(agent)
            elif agent.pre_allocated_credits < agent.emissions_amount:
                buyers.append(agent)
            else:
                satisfied.append(agent)

        return buyers, sellers, satisfied

    def sort_buyers_sellers(self, buyers, sellers):
        """
        Sorts buyers by their maximum buying price
        and sellers by their minimum selling price.
        """
        buyers.sort(key=lambda x: x.max_buying_price, reverse= False)
        sellers.sort(key=lambda x: x.min_selling_price, reverse = True )

        return buyers, sellers

    def check_transaction_condition(self, buyer, seller):
        # simplify
        if buyer.number_transaction_left != 0 and seller.number_transaction_left != 0:
            if buyer.pre_allocated_credits < buyer.emissions_amount and seller.pre_allocated_credits > seller.emissions_amount:
                if buyer.max_buying_price < seller.min_selling_price:
                    return True
        return False

    def do_transactions(self, buyers, sellers):
        """
        WORK IN PROGRESS

        Iterates through the list of buyers in sequential activation order
        buyer picks the seller promising lowest price and does transactions
        until either transaction quota is depleted, or the emission allowance is satisfied
        """

        for buyer in buyers:
            for seller in sellers:
                i = 0
                while self.check_transaction_condition(buyer, seller):
                    i += 1
                    print("transaction #" + str(i))
                    buyer.do_transaction()
                    buyer.add_credits()
                    seller.do_transaction()
                    seller.decrease_credits()


    def do_magic(self):
        """
            • Buyers list sorted by max price
            • Sellers list sorted by min price
            • Market rules:
                1. Buyers with higher min prices matches first with lowest min price -> price = average
                2. Transaction and actualisation of Buyer/seller list
                3. Step 3 until all sellers or buyers reached their max sell/buy capazity.
        """
        buyers, sellers, satisfied = self.list_buyers_sellers_satisfied(buyers, sellers)
        sorted_b, sorted_s = self.sort_buyers_sellers(buyers, seller)
        #for step in range(self.time_steps):
        self.do_transaction(sorted_b, sorted_s)
        #reset number of transactions


