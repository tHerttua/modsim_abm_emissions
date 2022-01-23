import random
import math
from agent import Agent
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Environment:
    def __init__(self, number_of_agents, allowance_credits, time_steps):
        self.number_of_agents = number_of_agents
        self.time_steps = time_steps
        self.allowance_credits = allowance_credits
        self.average_price = 0
        self.agents = []
        self.results = []
        self.numtransection_series = []

    def create_agents(self):
        for _ in range(self.number_of_agents):
            original_price = 60
            emissions_amount = self.randomize_emission_amount()
            buying_price = self.randomize_prices(original_price - 10 )#the max price I would pay must be lower as the price
            selling_price = self.randomize_prices(original_price + 10)# I would sell a certificate, vice versa, the agent would be stupid
            allocated_credits = 0#later it is going to be added
            time_steps = self.time_steps
            new_agent = Agent(emissions_amount, allocated_credits, buying_price, selling_price, time_steps)
            self.agents.append(new_agent)

    def randomize_emission_amount(self):
        #testing purposes
        all_cr = self.allowance_credits/self.time_steps*12 #DIvided here by 30 because every day this gets added to the emissions
        min_emission = int(math.floor(all_cr -all_cr *0.15))
        max_emission = int(math.floor(all_cr + all_cr * 0.25))
        emission_amount = random.randint(min_emission, max_emission)

        return emission_amount

    def randomize_prices(self, original_price):
        #testing purposes
        min_price = int(math.floor(original_price - original_price * 0.8))
        max_price = int(math.floor(original_price + original_price * 0.8))
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
        buyers.sort(key=lambda x: x.max_buying_price, reverse=False)
        sellers.sort(key=lambda x: x.min_selling_price, reverse=True)

        return buyers, sellers

    def check_transaction_condition(self, buyer, seller):
        # simplify
        if buyer.number_transaction_left != 0 and seller.number_transaction_left != 0:
            if buyer.pre_allocated_credits < buyer.emissions_amount and seller.pre_allocated_credits > seller.emissions_amount:
                if buyer.max_buying_price > seller.min_selling_price: #changed here < to > !!!!!!!!!!!!!!!
                    return True
        return False

    def do_transactions(self, buyers, sellers, step):
        """
        WORK IN PROGRESS

        Iterates through the list of buyers in sequential activation order
        buyer picks the seller promising lowest price and does transactions
        until either transaction quota is depleted, or the emission allowance is satisfied
        """
        num_transection = 0

        for buyer in buyers:
            deals_buyer = []
            for seller in sellers:
                i = 0
                deals_seller = []

                while self.check_transaction_condition(buyer, seller):
                    i += 1
                    num_transection = num_transection + i
                    print("transaction #" + str(i))
                    buyer.do_transaction()
                    buyer.add_credits()
                    seller.do_transaction()
                    seller.decrease_credits()


                    deals_buyer.append(seller.min_selling_price)
                    deals_seller.append(seller.min_selling_price)
                seller.deals_sold[step] = seller.deals_sold[step] + deals_seller
            buyer.deals_bought[step] = buyer.deals_bought[step] + deals_buyer

        self.numtransection_series.append(num_transection)
        self.increase_incentives(step)

    def increase_incentives(self, step):

        """
        This Function decreases the minimu price which I want to have and decreases the max price which I am willing to pay IF
        I have not done any transaction in this period.

        If I have done an transaction, then my prices are set back to my inital prices
        :return:
        """
        for agent in self.agents:
            agent.update_buying_price(step)
            agent.update_selling_price(step)

    def add_emmission(self, step):
        for agent in self.agents:
            agent.emissions_series[step] = agent.emissions_amount
            agent.credit_series[step] = agent.pre_allocated_credits

            agent.emissions_amount = agent.emissions_amount + self.randomize_emission_amount()
            if (step % 31) == 0:
                agent.pre_allocated_credits = agent.pre_allocated_credits + self.allowance_credits
                pass





    def averageing(self):
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

        average_price_bought, average_price_sold, average_emission, average_credits, average_max_buying_price, average_min_selling_price = self.averageing()

        plt.plot(self.numtransection_series)
        plt.xlabel('days')
        plt.ylabel('Number Transections')
        plt.show()
        plt.plot(average_price_bought)
        plt.xlabel('days')
        plt.ylabel('average prices bought')
        plt.show()
        plt.plot(average_price_sold)
        plt.xlabel('days')
        plt.ylabel('average prices sold')
        plt.show()
        plt.plot(average_emission)
        plt.plot(average_credits)
        plt.xlabel('days')
        plt.ylabel('average emission and credits')
        plt.show()
        plt.plot(average_min_selling_price)
        plt.plot(average_max_buying_price)
        plt.xlabel('days')
        plt.ylabel('average max price I am willing to pay  & average min price I am willing to sell')
        plt.show()


    def do_magic(self):
        """
            • Buyers list sorted by max price
            • Sellers list sorted by min price
            • Market rules:
                1. Buyers with higher min prices matches first with lowest min price -> price = average
                2. Transaction and actualisation of Buyer/seller list
                3. Step 3 until all sellers or buyers reached their max sell/buy capazity.
        """

        for step in range(self.time_steps):
            buyers, sellers, satisfied = self.list_buyers_sellers_satisfied()
            sorted_b, sorted_s = self.sort_buyers_sellers(buyers, sellers)
            self.do_transactions(sorted_b, sorted_s, step)
            self.add_emmission(step)
            if (step % 30) == 0:
                pass
        self.statistics()





