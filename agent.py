
class Agent:
    def __init__(self, emissions_amount, allocated_credits, initial_max_price=0, intial_min_price=0):
        self.emissions_amount = emissions_amount
        self.allocated_credits = allocated_credits
        self.max_buying_price = initial_max_price
        self.min_selling_price = intial_min_price

    def do_transaction(self):
        pass
