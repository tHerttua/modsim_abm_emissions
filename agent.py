#Control the price update
UPDATE_RATE = 0.2#0.5 makes the model unstable (too much changes, always different outcomes)
REDUCE_RATE = 0.3

from math import floor
from math import exp
from math import log
import numpy as np


class Agent:
    def __init__(self, emissions_amount,
                 pre_allocated_credits,
                 daily_quota=1,
                 max_buying_price=0,
                 min_selling_price=0,
                 time_steps = 360,
                 original_price=0,
                 group=0):

        self.emissions_amount = emissions_amount
        self.pre_allocated_credits = 0
        self.pre_allocated_credits_init = pre_allocated_credits
        self.max_buying_price = max_buying_price
        self.max_buying_price_init = max_buying_price
        self.min_selling_price = min_selling_price
        self.min_selling_price_init = min_selling_price
        self.original_price = original_price
        self.daily_quota = daily_quota # the transaction limit per time step
        self.group_number = group # agents know which group they belong to
        self.number_transaction_left = self.daily_quota
        self.willingness_to_reduce = emissions_amount * REDUCE_RATE
        self.emission_ever_had = emissions_amount # Total amount of emissions since the start
        self.emission_have_reduced = 0 # Number of times emissions have reduced


        # Progress tracking
        self.deals_bought = [[]] * time_steps
        self.deals_sold = [[]] * time_steps
        self.emissions_series = [[]] * time_steps
        self.credit_series = [[]] * time_steps
        self.max_buying_price_series = [[]] * time_steps
        self.min_selling_price_series = [[]] * time_steps

    def do_transaction(self):
        self.number_transaction_left -= 1

    def reset_quota(self):
        self.number_transaction_left = self.daily_quota

    def add_credits(self):
        self.pre_allocated_credits += 1

    def decrease_credits(self):
        self.pre_allocated_credits -= 1

    def record_price(self, step):
        self.min_selling_price_series[step] = self.min_selling_price
        self.max_buying_price_series[step] = self.max_buying_price

    def update_selling_price2(self, step):
        """
        The selling price is updated if the current step doesn't have record of a transaction.
        New price is calculated per update rate
        """
        if len(self.deals_sold[step]) != 0:
            self.min_selling_price = self.min_selling_price * (1 + UPDATE_RATE)
        else:
            self.min_selling_price = self.min_selling_price * (1 - UPDATE_RATE)

    def update_buying_price2(self, step):
        """
        The buying price is updated if the current step doesn't have record of a transaction.
        New price is calculated per update rate
        """

        if len(self.deals_bought[step]) != 0:
            self.max_buying_price = self.max_buying_price * (1 - UPDATE_RATE)
        else:
            self.max_buying_price = self.max_buying_price * (1 + UPDATE_RATE)

    def update_selling_price3(self, step):
        """
        The selling price is updated if the current step doesn't have record of a transaction.
        New price is calculated per update rate (concave)
        """
        if len(self.deals_sold[step]) != 0:

            self.min_selling_price = log(exp(self.min_selling_price) * (1 + UPDATE_RATE))

        else:
            self.min_selling_price = log(exp(self.min_selling_price) * (1 - UPDATE_RATE))

    def update_buying_price3(self, step):
        """
        The buying price is updated if the current step doesn't have record of a transaction.
        New price is calculated per update rate (concave)
        """

        if len(self.deals_bought[step]) != 0:
            self.max_buying_price = log(exp(self.max_buying_price) * (1 - UPDATE_RATE))
        else:
            self.max_buying_price = log(exp(self.max_buying_price) * (1 + UPDATE_RATE))


    def update_selling_price1(self, step):
        """
        The selling price is updated if the current step doesn't have record of a transaction.
        New price is calculated per update rate
        """
        if len(self.deals_sold[step]) != 0:
            self.min_selling_price = max(self.max_buying_price, self.min_selling_price + abs(self.original_price - self.min_selling_price) * UPDATE_RATE)
        else:
            self.min_selling_price = max(self.min_selling_price_init * 0.7, self.min_selling_price - abs(self.original_price - self.min_selling_price) * UPDATE_RATE)

    def update_buying_price1(self, step):
        """
        The buying price is updated if the current step doesn't have record of a transaction.
        New price is calculated per update rate
        """
        if len(self.deals_bought[step]) != 0:
            self.max_buying_price = min(self.min_selling_price, self.max_buying_price - abs(self.max_buying_price - self.original_price) * UPDATE_RATE)
        else:
            self.max_buying_price = min(self. max_buying_price_init * 1.3, self.max_buying_price + abs(self.max_buying_price - self.original_price) * UPDATE_RATE)


    def emissions_add(self, add):
        self.emissions_amount = self.emissions_amount + add
        self.update_emission_ever_had(add)

    def update_emission_ever_had(self, add):
        self.emission_ever_had = self.emission_ever_had + add
        self.updata_potential_reduce()

    def updata_potential_reduce(self):
        self.willingness_to_reduce = floor(self.emission_ever_had * REDUCE_RATE) - self.emission_have_reduced

    def reduce_emission(self):
        self.emissions_amount = self.emissions_amount - 1
        self.emission_have_reduced = self.emission_have_reduced + 1
        self.updata_potential_reduce()


