import random
import math
from agent import Agent
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Control the amount of variance, could be made part of the environment for ease of use
EMISSION_VARIANCE = 0.2
PRICE_VARIANCE = 0.8
ORIGINAL_PRICE = 60

class Environment:
    def __init__(self, number_of_agents_per_group,
                 number_of_agents_group,
                 allowance_credits,
                 agent_transaction_limit,
                 time_steps):
        self.number_of_agents = number_of_agents_per_group * number_of_agents_group
        self.number_of_agents_group = number_of_agents_group
        self.time_steps = time_steps
        self.allowance_credits = allowance_credits
        self.agent_transaction_limit = agent_transaction_limit
        self.average_price = 0
        self.agents = []
        self.results = []
        self.num_transaction_series = []
        self.num_reduce_emission_series = []
        self.agents_no_emission_added = [i for i in range(0, self.number_of_agents)]
        self.period = 0

    def create_agents(self):
        """
        Creates agents based on the initial values.
        Makes sure the inital maximum buying price is significantly lower than the initial minimum selling price
        """
        for _ in range(self.number_of_agents):
            original_price = ORIGINAL_PRICE
            emissions_amount = 0
            buying_price = self.randomize_prices(original_price-20)
            selling_price = self.randomize_prices(original_price+20)
            allocated_credits = self.allowance_credits
            time_steps = self.time_steps
            new_agent = Agent(emissions_amount,
                              allocated_credits,
                              self.agent_transaction_limit,
                              buying_price,
                              selling_price,
                              time_steps,
                              original_price)

            self.agents.append(new_agent)

    def randomize_emission_amount(self):
        """
        The total allowance credits are divided per month because they are increased daily
        """
        all_cr = self.allowance_credits /31*self.number_of_agents_group

        min_emission = int(math.floor(all_cr -all_cr * EMISSION_VARIANCE))
        max_emission = int(math.floor(all_cr + all_cr * EMISSION_VARIANCE))
        emission_amount = random.randint(min_emission, max_emission)

        return emission_amount

    def randomize_prices(self, original_price):
        min_price = int(math.floor(original_price - original_price * PRICE_VARIANCE))
        max_price = int(math.floor(original_price + original_price * PRICE_VARIANCE))
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
            if agent.pre_allocated_credits> agent.emissions_amount:
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
        buyers.sort(key=lambda x: x.max_buying_price, reverse=False)
        sellers.sort(key=lambda x: x.min_selling_price, reverse=True)

        return buyers, sellers

    def check_transaction_condition(self, buyer, seller):
        """
        Basic skeleton
        """
        if buyer.number_transaction_left > 0 and seller.number_transaction_left > 0:
            if buyer.pre_allocated_credits < buyer.emissions_amount and \
                    seller.pre_allocated_credits > seller.emissions_amount:
                if buyer.max_buying_price > seller.min_selling_price:
                    return True
        return False

    def check_transaction_condition3(self, buyer, seller):
        """
        First check if both buyer and seller have transactions left for the time step
        Then buyer check if the emissions (still) exceed the allowed amount,
        and seller checks if their emissions are (still) lower than the allowed amount OR
        Seller will also agree if they are willing to drop emissions for this transaction
        Last, if the buying price is higher than selling price, the transaction can be made
        """
        if buyer.number_transaction_left > 0 and seller.number_transaction_left > 0:
            if buyer.pre_allocated_credits < buyer.emissions_amount and \
                    (seller.pre_allocated_credits > seller.emissions_amount or seller.willingness_to_reduce >= 1):
                if buyer.max_buying_price > seller.min_selling_price:
                    return True
        return False

    def do_transactions(self, buyers, sellers, step):
        """
        Basic functionality:
        Iterates through the list of buyers in sequential activation order
        buyer picks the seller promising lowest price and does transactions
        until either transaction quota is depleted, or the emission allowance is satisfied
        """
        for buyer in buyers:
            for seller in sellers:
                i = 0
                while self.check_transaction_condition(buyer, seller):
                    i += 1
                    #print("transaction #" + str(i))
                    buyer.do_transaction()
                    buyer.add_credits()
                    seller.do_transaction()
                    seller.decrease_credits()

    def do_transactions2(self, buyers, sellers, step):
        """
        Iterates through the list of buyers in sequential activation order
        buyer picks the seller promising lowest price and does transactions
        until either transaction quota is depleted, or the emission allowance is satisfied.
        Updates buyers and sellers price and tracks the transactions.
        """
        num_transaction = 0

        for buyer in buyers:
            deals_buyer = []
            for seller in sellers:
                i = 0
                deals_seller = []

                while self.check_transaction_condition(buyer, seller):
                    i += 1
                    num_transaction = num_transaction + 1
                    buyer.do_transaction()
                    buyer.add_credits()
                    seller.do_transaction()
                    seller.decrease_credits()

                    deals_buyer.append(seller.min_selling_price)
                    deals_seller.append(seller.min_selling_price)
                seller.deals_sold[step] = seller.deals_sold[step] + deals_seller
            buyer.deals_bought[step] = buyer.deals_bought[step] + deals_buyer

        self.num_transaction_series.append(num_transaction)
        self.increase_incentives(step)

        for agent in buyers:
            agent.reset_quota()
        for agent in sellers:
            agent.reset_quota()

    def do_transactions3(self, buyers, sellers, step):
        """
        Iterates through the list of buyers in sequential activation order
        buyer picks the seller promising lowest price and does transactions
        until either transaction quota is depleted, or the emission allowance is satisfied.
        Updates buyers and sellers price, and tracks the transactions.
        Added functionality: checks if an Agent has possibility to drop their emission amount.
        """
        num_transaction = 0
        num_emission_reduced = 0
        for buyer in buyers:
            deals_buyer = []
            for seller in sellers:
                i = 0
                deals_seller = []

                while self.check_transaction_condition3(buyer, seller):
                    i += 1
                    num_transaction = num_transaction + 1
                    buyer.do_transaction()
                    buyer.add_credits()
                    seller.do_transaction()
                    seller.decrease_credits()

                    deals_buyer.append(seller.min_selling_price)
                    deals_seller.append(seller.min_selling_price)
                    if seller.pre_allocated_credits > seller.emissions_amount:
                        pass
                    elif seller.willingness_to_reduce >= 1:
                        seller.reduce_emission()
                        num_emission_reduced = num_emission_reduced + 1
                seller.deals_sold[step] = seller.deals_sold[step] + deals_seller
            buyer.deals_bought[step] = buyer.deals_bought[step] + deals_buyer

        self.num_transaction_series.append(num_transaction)
        self.num_reduce_emission_series.append(num_emission_reduced)
        self.increase_incentives(step)

        for agent in buyers:
            agent.reset_quota()
        for agent in sellers:
            agent.reset_quota()


    def increase_incentives(self, step):
        """
        If no transaction is made in the time step,
        buyer increases the price it's willing to buy at,
        and the seller decreases the price it's willing to sell at.
        If a transaction is made, the prices are set back to my initial prices
        """
        for agent in self.agents:
            agent.update_buying_price(step)
            agent.update_selling_price(step)

    def add_emission(self, step):
        """
        For every step and for every agent, the current emissions amount and allowance credits are recorded.
        whenever the "end of the month" is reached, the agents are given a fixed amount of credits.
        Amount of emissions are increased for every time step based on how many agents there are in a group.
        """
        for agent in self.agents:
            agent.emissions_series[step] = agent.emissions_amount
            agent.credit_series[step] = agent.pre_allocated_credits

            if (step % 31) == 0 and step > 1:
                agent.pre_allocated_credits = agent.pre_allocated_credits + self.allowance_credits

        agent.emissions_add(self.randomize_emission_amount()/5)

        agents_add_emissoin = random.sample(self.agents_no_emission_added, math.floor(self.number_of_agents/self.number_of_agents_group))
        self.period = self.period + 1

        for num in agents_add_emissoin:
            self.agents[num].emissions_add(self.randomize_emission_amount())
            self.agents_no_emission_added.remove(num)

        if self.period == self.number_of_agents_group:
            self.period = 0
            self.agents_no_emission_added = [i for i in range(0, len(self.agents))]

    def averaging(self):
        """
        Calculates averages between every step for:
        emissions, credits, max buying price and min selling price
        """
        bought_average = []
        sold_average = []
        emission_average = []
        credit_average = []
        max_price_average = []
        min_price_average = []

        for step in range(self.time_steps):
            sum_bought = 0
            sum_sold = 0
            sum_emission = 0
            sum_credit = 0
            sum_max_price = 0
            sum_min_price = 0
            num_transaction = 0

            for agent in self.agents:
                if len(agent.deals_bought[step]) != 0:
                    sum_bought = sum_bought + sum(agent.deals_bought[step])/len(agent.deals_bought[step])
                    num_transaction = num_transaction + 1
                if len(agent.deals_sold[step]) != 0:
                    sum_sold = sum_sold + sum(agent.deals_sold[step]) /len(agent.deals_sold[step])

                sum_emission = sum_emission + agent.emissions_series[step]
                sum_credit = sum_credit + agent.credit_series[step]
                sum_max_price = sum_max_price + agent.max_buying_price_series[step]
                sum_min_price = sum_min_price + agent.min_selling_price_series[step]

            if num_transaction !=0:
                bought_average.append(sum_bought/num_transaction)
                sold_average.append(sum_bought/num_transaction)
            else:
                bought_average.append(0)
                sold_average.append(0)

            emission_average.append(sum_emission/len(self.agents))
            credit_average.append(sum_credit/len(self.agents))
            max_price_average.append(sum_max_price/len(self.agents))
            min_price_average.append(sum_min_price/len(self.agents))

        return bought_average, sold_average, emission_average, credit_average, max_price_average, min_price_average

    def statistics(self):
        """
        Draws the statistics
        """
        average_price_bought, average_price_sold, average_emission, average_credits, average_max_buying_price, average_min_selling_price = self.averaging()

        plt.plot(self.num_transaction_series)
        plt.plot(self.num_reduce_emission_series)
        plt.xlabel('steps')
        plt.ylabel('Total umber Transactions and Number of Times Emission Reduced')
        plt.show()
        plt.plot(average_price_bought)
        plt.xlabel('steps')
        plt.ylabel('Average prices bought')
        plt.show()
        plt.plot(average_price_sold)
        plt.xlabel('steps')
        plt.ylabel('Average prices sold')
        plt.show()
        plt.plot(average_emission)
        plt.plot(average_credits)
        plt.xlabel('days')
        plt.ylabel('Average emission and credits')
        plt.show()
        plt.plot(average_min_selling_price)
        plt.plot(average_max_buying_price)
        plt.xlabel('days')
        plt.ylabel('Average max price for buying & average min price for selling')
        plt.show()

    def do_magic(self, version=1):
        """
            • Buyers list sorted by max price
            • Sellers list sorted by min price
            • Market rules:
                1. Buyers with higher min prices matches first with the lowest min price -> price = average
                2. Transaction and actualisation of Buyer/seller list
                3. Step 3 until all sellers or buyers reached their max sell/buy capacity.

        :version: different level of agent behaviour depending on the version
        """

        for step in range(self.time_steps):
            buyers, sellers, satisfied = self.list_buyers_sellers_satisfied()
            sorted_b, sorted_s = self.sort_buyers_sellers(buyers, sellers)

            try:
                if version == 1:
                    self.do_transactions(sorted_b, sorted_s, step)
                elif version == 2:
                    self.do_transactions2(sorted_b, sorted_s, step)
                elif version == 3:
                    self.do_transactions3(sorted_b, sorted_s, step)
            except Exception as e:
                print(e)

            self.add_emission(step)

        self.statistics()





