#Control the price update
UPDATE_RATE = 0.01
REDUCE_RATE = 0.3

from math import floor


class Agent:
    def __init__(self, emissions_amount,
                 pre_allocated_credits,
                 daily_quota=1,
                 max_buying_price=0,
                 min_selling_price=0,
                 time_steps=0,
                 original_price=0,
                 group=0):

        self.emissions_amount = emissions_amount
        self.pre_allocated_credits = pre_allocated_credits
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

    def update_selling_price(self, step):
        """
        The selling price is updated if the current step doesn't have record of a transaction.
        New price is calculated per update rate
        """
        self.min_selling_price_series[step] = self.min_selling_price
        if len(self.deals_sold[step]) != 0:
            self.min_selling_price = self.min_selling_price_init
        else:
            self.min_selling_price = max(self.max_buying_price, self.min_selling_price - abs(self.original_price - self.min_selling_price) * UPDATE_RATE)

    def update_buying_price(self, step):
        """
        The buying price is updated if the current step doesn't have record of a transaction.
        New price is calculated per update rate
        """
        self.max_buying_price_series[step] = self.max_buying_price
        if len(self.deals_bought[step]) != 0:
            self.max_buying_price = self.max_buying_price_init
        else:
            self.max_buying_price = min(self.min_selling_price, self.max_buying_price + abs(self.max_buying_price - self.original_price) * UPDATE_RATE)

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


