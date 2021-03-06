import random
import math
from agent import Agent
import matplotlib.pyplot as plt
import numpy as np
from itertools import permutations

#Control the amount of variance, could be made part of the environment for ease of use
EMISSION_VARIANCE = 0.9
PRICE_VARIANCE = 0.8
ORIGINAL_PRICE = 60
PRICE_CONTROL_VALUE = 20
CREDITS_ALLOCATION_INTERVAL = 30


class Environment:
    def __init__(self, modus_name, titlevalue,
                 number_of_agents_per_group,
                 number_of_agents_group,
                 allowance_credits,
                 agent_transaction_limit,
                 time_steps,
                 iterate,
                 certificate_reductionrate):
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
        self.num_buy = []
        self.num_sel = []
        self.agents_no_emission_added = [i for i in range(0, self.number_of_agents)]
        self.number_of_agents_per_group = number_of_agents_per_group
        self.period = 0
        self.iterate = iterate
        self.day_of_the_month = 0
        self.certificate_reductionrate = certificate_reductionrate
        self.modus_name = modus_name
        self.titlevalue = str(titlevalue)


    def create_agents(self):
        """
        Creates agents based on the initial values given.
        Iterates through number of groups and creates user decided amount of agents per each group.
        Allowance credits are taken from the user decided list, in which group number corresponds to the listed credits.
        Makes sure the initial maximum buying price is significantly lower than the initial minimum selling price.
        """
        for group_number in range(self.number_of_agents_group):
            agent_index = 0
            while agent_index != self.number_of_agents_per_group:
                agent_index += 1
                original_price = ORIGINAL_PRICE
                emissions_amount = 0
                buying_price = self.randomize_prices(original_price - PRICE_CONTROL_VALUE)
                selling_price = self.randomize_prices(original_price + PRICE_CONTROL_VALUE)
                allocated_credits = self.allowance_credits[group_number]
                new_agent = Agent(emissions_amount,
                                  allocated_credits,
                                  self.agent_transaction_limit,
                                  buying_price,
                                  selling_price,
                                  self.time_steps,
                                  original_price,
                                  group_number) # group number is also assigned
                self.agents.append(new_agent)

    def randomize_emission_amount(self, agent):
        """
        The total allowance credits are divided per month because they are increased daily
        emissions are stochastic distributed according to their allowances group
        (dirty company, not dirty company)
        """
        all_cr = agent.pre_allocated_credits_init/CREDITS_ALLOCATION_INTERVAL

        min_emission = int(math.floor(all_cr - all_cr * EMISSION_VARIANCE))
        max_emission = int(math.floor(all_cr + all_cr * EMISSION_VARIANCE))
        emission_amount = random.randint(min_emission, max_emission)

        return emission_amount

    def randomize_prices(self, original_price):
        #randomizes prices
        min_price = int(math.floor(original_price - original_price * PRICE_VARIANCE))
        max_price = int(math.floor(original_price + original_price * PRICE_VARIANCE))
        random_price = random.randint(min_price, max_price)

        return random_price

    def check_seller(self, agent):
        """
        check if an agent wants to sell
        it compares the total emission amount until now with the total number of credits minus the expected needed credits

        """
        k = agent.pre_allocated_credits_init * (CREDITS_ALLOCATION_INTERVAL-self.day_of_the_month+1)/ CREDITS_ALLOCATION_INTERVAL         #calculates the portion which will be expected to be needed in the future

        if agent.pre_allocated_credits - k > agent.emissions_amount: #or (abs(agent.pre_allocated_credits - agent.emissions_amount)  < willingness_gap and agent.willingness_to_reduce>=1):
            return True
        else:
            return False

    def check_buyer(self, agent):

        '''
        checks if an agent wants to buy
        inverted functionality as check_seller
        '''

        k = agent.pre_allocated_credits_init * (CREDITS_ALLOCATION_INTERVAL - self.day_of_the_month +1) / CREDITS_ALLOCATION_INTERVAL  # calculates the number of certificates which will be expected to be needed in the future

        if agent.pre_allocated_credits - k < agent.emissions_amount:  # or (abs(agent.pre_allocated_credits - agent.emissions_amount)  < willingness_gap and agent.willingness_to_reduce>=1):
            return True
        else:
            return False

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
            if self.check_seller(agent):
                #the assumption is that a agent just wants to sell if he has initially more credits
                # than emission until the end of the month
                sellers.append(agent)
                #at the transaction function he can make addionaly credits free by reducing emissions
            elif self.check_buyer(agent):
                buyers.append(agent)
            else:
                satisfied.append(agent)

        return buyers, sellers, satisfied

    def list_buyers_sellers_satisfied2(self):
        # Version 2: divides Buyers/sellers randomly.
        who_buyer = random.sample(range(len(self.agents)), int(math.floor(len(self.agents)/2 )))
        buyers = []
        sellers = []
        satisfied = []
        j = 0

        for agent in self.agents:
            if (j in who_buyer):
                buyers.append(agent)
            else:
                sellers.append(agent)
            j = j + 1
        return buyers, sellers, satisfied


    def sort_buyers_sellers(self, buyers, sellers):
        """
        Sorts buyers by their maximum buying price
        and sellers by their minimum selling price reversed.
        """
        buyers.sort(key=lambda x: x.max_buying_price, reverse=False)
        sellers.sort(key=lambda x: x.min_selling_price, reverse=True)

        return buyers, sellers

    def check_transaction_condition(self, buyer, seller):
        """
        DEPRECATED
        Basic skeleton
        not used anymore
        """
        if buyer.number_transaction_left > 0 and seller.number_transaction_left > 0:
            if self.check_buyer(buyer) and self.check_seller(seller):
                if buyer.max_buying_price > seller.min_selling_price:
                    return True
        return False

    def check_transaction_condition3(self, buyer, seller):
        """
        First check if both buyer and seller have transactions left for the time step
        Then buyer check if the emissions (still) exceed the allowed amount,
        and seller checks if their emissions are (still) lower than the allowed amount OR
        Seller will also agree if they are willing to drop emissions for this transaction and has done a transaction
        in the previous step (otherwise he would now have been selected as seller initally)
        Last, if the buying price is higher than selling price, the transaction can be made
        """
        if buyer.number_transaction_left > 0 and seller.number_transaction_left > 0:
            if self.check_buyer(buyer)  and \
                    (self.check_seller(seller) or seller.willingness_to_reduce >= 1):
                if buyer.max_buying_price > seller.min_selling_price:
                    return True
        return False

    def check_transaction_condition4(self, buyer, seller):
        """
        First check if both buyer and seller have transactions left for the time step
        Then buyer check if the emissions (still) exceed the allowed amount,
        and seller checks if their emissions are (still) lower than the allowed amount OR
        Last, if the buying price is higher than selling price, the transaction can be made
        """
        if buyer.number_transaction_left > 0 and seller.number_transaction_left > 0:
            if self.check_buyer(buyer)  and self.check_seller(seller):
                if buyer.max_buying_price > seller.min_selling_price:
                    return True
        return False



    def do_transactions3(self, buyers, sellers, step):
        """
        Iterates through the list of buyers in sequential activation order
        buyer picks the seller promising lowest price and does transactions
        until either transaction quota is depleted, or the emission allowance is satisfied.
        Updates buyers and sellers price, and tracks the transactions. (records data)
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

                    deals_buyer.append((seller.min_selling_price + buyer.max_buying_price)/2) #they agreed to the same price
                    deals_seller.append((seller.min_selling_price + buyer.max_buying_price)/2)
                    if self.check_seller(seller):
                        pass
                    elif seller.willingness_to_reduce >= 1:
                        seller.reduce_emission()
                        num_emission_reduced = num_emission_reduced + 1
                seller.deals_sold[step] = seller.deals_sold[step] + deals_seller #collecting data
            buyer.deals_bought[step] = buyer.deals_bought[step] + deals_buyer

        self.num_transaction_series.append(num_transaction)
        self.num_reduce_emission_series.append(num_emission_reduced)
      #  self.increase_incentives(step)
        for agent in self.agents:
            agent.record_price(step)

        for agent in buyers:
            agent.update_buying_price1(step)
            agent.reset_quota()
        for agent in sellers:
            agent.update_selling_price1(step)
            agent.reset_quota()


    def do_transactions4(self, buyers, sellers, step):
        """
        Iterates through the list of buyers in sequential activation order
        buyer picks the seller promising lowest price and does transactions
        until either transaction quota is depleted, or the emission allowance is satisfied.
        Updates buyers and sellers price, and tracks the transactions.
        """

        num_transaction = 0
        num_emission_reduced = 0
        for buyer in buyers:
            deals_buyer = []
            for seller in sellers:
                i = 0
                deals_seller = []

                while self.check_transaction_condition4(buyer, seller):
                    i += 1
                    num_transaction = num_transaction + 1
                    buyer.do_transaction()
                    buyer.add_credits()
                    seller.do_transaction()
                    seller.decrease_credits()

                    deals_buyer.append((seller.min_selling_price + buyer.max_buying_price)/2) #they agreed to the same price
                    deals_seller.append((seller.min_selling_price + buyer.max_buying_price)/2)
                    '''                    if self.check_seller(seller):
                        pass
                    elif seller.willingness_to_reduce >= 1:
                        seller.reduce_emission()
                        num_emission_reduced = num_emission_reduced + 1'''
                seller.deals_sold[step] = seller.deals_sold[step] + deals_seller #collecting data
            buyer.deals_bought[step] = buyer.deals_bought[step] + deals_buyer

        self.num_transaction_series.append(num_transaction)
        self.num_reduce_emission_series.append(num_emission_reduced)
     #   self.increase_incentives(step)
        for agent in self.agents:
            agent.record_price(step)

        for agent in buyers:
            agent.update_buying_price4(step)
            agent.reset_quota()
        for agent in sellers:
            agent.update_selling_price4(step)
            agent.reset_quota()


    def increase_incentives(self, step):
        """
        If no transaction is made in the time step,
        buyer increases the price it's willing to buy at,
        and the seller decreases the price it's willing to sell at.
        If a transaction is made, the prices adjusted in the favor of the repective buyer or seller
        """
        for agent in self.agents:
            agent.update_buying_price(step)
            agent.update_selling_price(step)

    def add_credits(self, step):
        """
        addes credits each month, each allocation intervall
        """
        if (step % CREDITS_ALLOCATION_INTERVAL) == 0:
            for agent in self.agents:
                agent.pre_allocated_credits = agent.pre_allocated_credits + agent.pre_allocated_credits_init * self.certificate_reductionrate

    def add_emission(self, step):
        """
        For every step and for every agent, the current emissions amount and allowance credits are recorded.
        whenever the "end of the month" is reached, the agents are given a fixed amount of credits.
        Amount of emissions are increased for every time step based on how many agents there are in a group.
        """
        for agent in self.agents:
            agent.emissions_series[step] = agent.emissions_amount
            agent.credit_series[step] = agent.pre_allocated_credits

            agent.emissions_add(self.randomize_emission_amount(agent))      #new Version: daily emissions



    def averaging(self):
        """
        Calculates averages between every step for:
        emissions, credits, max buying price and min selling price, ...
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

    def plot_agents(self):
        """
        in this method we plot the credit and emission path of 3 randomly selected agents
        """
        Nlines = 3

        rand_list = random.sample(range(len(self.agents)), Nlines)
        j = 0
        for i in rand_list:
            if j == 0:
                plt.plot(self.agents[i].emissions_series, '-', color=plt.cm.RdYlBu(np.linspace(0, 1, Nlines)[j]),
                         label="Emissions")
                plt.plot(self.agents[i].credit_series, '--', color=plt.cm.RdYlBu(np.linspace(0, 1, Nlines)[j]),
                         label="Credits")
                plt.legend()

            else:
                plt.plot(self.agents[i].emissions_series,  '-',color=plt.cm.RdYlBu(np.linspace(0,1, Nlines)[j]))
                plt.plot(self.agents[i].credit_series, '--', color=plt.cm.RdYlBu(np.linspace(0,1, Nlines)[j]))


            j = j + 1

        plt.xlabel('Steps')
        plt.ylabel('Emissions and Credits from 3 Agents')
        plt.title("Modus of Simulation: " + self.modus_name+ " " + self.titlevalue)
        plt.savefig("pics/"+self.modus_name+str(self.iterate)+"representative_agents.png")
        #plt.show()
        plt.clf()




    def statistics(self, plots):
        """
        calculate and plot key numbers of the model
        """

        average_price_bought, average_price_sold, average_emission, average_credits, average_max_buying_price, average_min_selling_price = self.averaging()

        if plots == True:

            self.plot_agents()

            plt.plot(self.num_buy, label ="Total Number of Buyers")
            plt.plot(self.num_sel, '--', label="Total Number of Sellers")
            plt.legend()
            plt.xlabel('Steps')
            plt.ylabel('Number of Agents')
            plt.title("Modus of Simulation: " + self.modus_name + " " + self.titlevalue)
            plt.savefig("pics/"+self.modus_name+str(self.iterate)+ "Number_Buy_sel.png")
            #plt.show()
            plt.clf()

            plt.plot(self.num_transaction_series, label ="Total Number of Transactions")
            plt.plot(self.num_reduce_emission_series, label ="Transactions because of Emissions Reduced")
            plt.legend()
            plt.xlabel('Steps')
            plt.ylabel('Number of Transactions')
            plt.title("Modus of Simulation: " + self.modus_name + " " + self.titlevalue)
            plt.savefig("pics/"+self.modus_name+str(self.iterate)+ "Number_of_Transactions.png")
            #plt.show()
            plt.clf()


            plt.clf()

            plt.plot(average_emission, label ="Average amount of Emissions per Agent")
            plt.plot(average_credits, label ="Average amount of Credits per Agent")
            plt.legend()
            plt.xlabel('days')
            plt.ylabel('Emissions and Credits')
            plt.title("Modus of Simulation: " + self.modus_name + " " + self.titlevalue)
            plt.savefig("pics/"+self.modus_name+str(self.iterate) +"average emissions and credits per agent.png")
            #plt.show()
            plt.clf()

            plt.plot(average_min_selling_price, label ="Average Minimal Selling Price per Agent")
            plt.plot(average_max_buying_price, label ="Average Maximal Buying Price per Agent")
            plt.legend()
            plt.xlabel('Step')
            plt.ylabel('Average Price')
            plt.title("Modus of Simulation: " + self.modus_name + " " + self.titlevalue)
            plt.savefig("pics/"+self.modus_name+str(self.iterate) +"average minimal selling buying price.png")
            #plt.show()
            plt.clf()

            plt.plot(average_price_bought)
            plt.xlabel('Steps')
            plt.ylabel('Average Prices Paid per Agent')
            plt.title("Modus of Simulation: " + self.modus_name + " " + self.titlevalue)
            plt.savefig("pics/" + self.modus_name + str(self.iterate) + "average_price.png")
            # plt.show()
            plt.clf()

        return average_price_bought, self.num_transaction_series

    def do_magic(self,
                 random_sel = False,
                    em_red = True,
                 plots = True):
        """
            ??? add emission and potentially credits each step
            ??? select  buyers and sellers
            ??? Buyers list sorted by max price
            ??? Sellers list sorted by min price
            ??? do transactions(rules, highest buyer price with lowest selling price first


        :version: different level of agent behaviour depending on the version
        """

        for step in range(self.time_steps):

            self.add_emission(step)
            self.add_credits(step)

            self.day_of_the_month = step % CREDITS_ALLOCATION_INTERVAL
            # computes the day of the month via modulo operator


            if random_sel == False:#depends on the setting if agents sellers are randomy selected
                buyers, sellers, satisfied = self.list_buyers_sellers_satisfied()
            else:
                buyers, sellers, satisfied = self.list_buyers_sellers_satisfied2()
            self.num_buy.append(len(buyers))
            self.num_sel.append(len(sellers))
            sorted_b, sorted_s = self.sort_buyers_sellers(buyers, sellers)


            try:#depends on the setting whether agents are allowed to reduce emissions for a deal
                if em_red ==True:
                    self.do_transactions3(sorted_b, sorted_s, step)
                else:
                    self.do_transactions4(sorted_b, sorted_s, step)

            except Exception as e:
                print(e)


        return_pr, average_em = self.statistics(plots)


        return [return_pr, average_em]





