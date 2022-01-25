#Control the price update
UPDATE_RATE = 0.05

class Agent:
    def __init__(self, emissions_amount,
                 pre_allocated_credits,
                 daily_quota=10,
                 max_buying_price=0,
                 min_selling_price=0,
                 time_steps=0):

        self.emissions_amount = emissions_amount
        self.pre_allocated_credits = pre_allocated_credits
        self.max_buying_price = max_buying_price
        self.max_buying_price_init = max_buying_price
        self.min_selling_price = min_selling_price
        self.min_selling_price_init = min_selling_price
        self.daily_quota = daily_quota
        self.number_transaction_left = self.daily_quota

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
        self.min_selling_price_series[step] = self.min_selling_price
        if len(self.deals_sold[step]) != 0:
            self.min_selling_price = self.min_selling_price_init
        else:
            self.min_selling_price = self.min_selling_price * (1 - UPDATE_RATE)

    def update_buying_price(self, step):
        self.max_buying_price_series[step] = self.max_buying_price
        if len(self.deals_bought[step]) != 0:
            self.max_buying_price = self.max_buying_price_init
        else:
            self.max_buying_price = self.max_buying_price * (1 + UPDATE_RATE)