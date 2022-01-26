import random
import math
from agent import Agent
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Control the amount of variance, could be made part of the environment for ease of use
EMISSION_VARIANCE = 0.2
PRICE_VARIANCE = 0.8

class Environment:
    def __init__(self, number_of_agents_per_group, number_of_agents_group, allowance_credits, agent_transaction_limit, time_steps):
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
        self.number_of_agents_per_group = number_of_agents_per_group
        self.period = 0

    def create_agents(self):
        for _ in range(self.number_of_agents):
            original_price = 60
            emissions_amount = 0
            buying_price = self.randomize_prices(original_price-20)#the max price I would pay must be lower as the price <- already picked from random pool
            selling_price = self.randomize_prices(original_price+20)# I would sell a certificate, vice versa, the agent would be stupid
            allocated_credits = self.allowance_credits #later it is going to be added <- introduced a bug, need to be allocated
            time_steps = self.time_steps
            new_agent = Agent(emissions_amount, allocated_credits/2, self.agent_transaction_limit, buying_price, selling_price, time_steps, original_price)
            self.agents.append(new_agent)

    def randomize_emission_amount(self):
        #testing purposes
        all_cr = self.allowance_credits /31*self.number_of_agents_group #DIvided here by 30 because every day this gets added to the emissions
        # if such division is made, it must be present in list_buyers_sellers_satisfied() and check_transaction_condition() methods

        min_emission = int(math.floor(all_cr -all_cr * EMISSION_VARIANCE))
        max_emission = int(math.floor(all_cr + all_cr * EMISSION_VARIANCE))
        emission_amount = random.randint(min_emission, max_emission)

        return emission_amount

    def randomize_prices(self, original_price):
        #testing purposes
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
        # simplify
        if buyer.number_transaction_left > 0 and seller.number_transaction_left > 0:
            if buyer.pre_allocated_credits < buyer.emissions_amount and seller.pre_allocated_credits > seller.emissions_amount:
                if buyer.max_buying_price > seller.min_selling_price: #changed here < to > !!!!!!!!!!!!!!! <- good catch!
                    return True
        return False

    def check_transaction_condition3(self, buyer, seller):
        # simplify
        if buyer.number_transaction_left > 0 and seller.number_transaction_left > 0:
            if buyer.pre_allocated_credits < buyer.emissions_amount and (seller.pre_allocated_credits > seller.emissions_amount or seller.willingness_to_reduce >= 1):
                if buyer.max_buying_price > seller.min_selling_price: #changed here < to > !!!!!!!!!!!!!!! <- good catch!
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
        WORK IN PROGRESS

        Iterates through the list of buyers in sequential activation order
        buyer picks the seller promising lowest price and does transactions
        until either transaction quota is depleted, or the emission allowance is satisfied
        """
        num_transaction = 0

        for buyer in buyers:
            deals_buyer = []
            for seller in sellers:
                i = 0
                deals_seller = []

                while self.check_transaction_condition(buyer, seller):
                    i += 1
                    num_transaction = num_transaction + 1#there was a mistake !!!
                    #print("transaction #" + str(i))
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
                    #print("transaction #" + str(i))
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
        This Function decreases the minimum price which I want to have and decreases the max price which I am willing to pay IF
        I have not done any transaction in this period.

        If I have done a transaction, then my prices are set back to my initial prices
        """
        for agent in self.agents:
            agent.update_buying_price(step)
            agent.update_selling_price(step)

    def add_emission(self, step):
        for agent in self.agents:
            agent.emissions_series[step] = agent.emissions_amount
            agent.credit_series[step] = agent.pre_allocated_credits

            if (step % 31) == 0 and step > 1:
                agent.pre_allocated_credits = agent.pre_allocated_credits + self.allowance_credits


        for num in range(self.period * self.number_of_agents_per_group, (self.period + 1)* self.number_of_agents_per_group -1):
            self.agents[num].emissions_add(self.randomize_emission_amount())
        self.period = self.period + 1
        if self.period == self.number_of_agents_group:
            self.period = 0

    def averaging(self):
        """
        method logic

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





