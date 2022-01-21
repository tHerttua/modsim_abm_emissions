
class Agent:
    def __init__(self, emissions_amount, pre_allocated_credits, max_buying_price=0, min_selling_price=0):
        self.emissions_amount = emissions_amount
        self.pre_allocated_credits = pre_allocated_credits
        self.max_buying_price = max_buying_price
        self.min_selling_price = min_selling_price
        self.daily_quota = 10
        self.number_transaction_left = self.daily_quota

    def do_transaction(self):
        self.number_transaction_left -= 1

    def reset_quota(self):
        self.number_transaction_left = self.daily_quota

    def add_credits(self):
        self.pre_allocated_credits += 1

    def decrease_credits(self):
        self.pre_allocated_credits -= 1

    def update_selling_price(self):
        pass

    def update_buying_price(self):
        pass