
class Agent:
    def __init__(self, emissions_amount, allocated_credits, initial_max_price=0, initial_min_price=0):
        self.emissions_amount = emissions_amount
        self.allocated_credits = allocated_credits
        self.max_buying_price = initial_max_price
        self.min_selling_price = initial_min_price
        self.number_transaction = 0

    def do_transaction(self):
        pass

    def update_selling_price(self):
        pass

    def update_buying_price(self):
        pass