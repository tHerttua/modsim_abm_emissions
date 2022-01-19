
class Agent:
    def __init__(self, emissions_amount, allocated_credits, initial_max_price, intial_min_price):
        self.emissions_amount = emissions_amount
        self.allocated_credits = allocated_credits
        self.max_buying_price = initial_max_price
        self.min_selling_price = intial_min_price

    def do_transaction(self):
        pass
