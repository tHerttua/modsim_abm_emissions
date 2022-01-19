
class Agent:
    def __init__(self, emissions_amount, allocated_credits):
        self.emissions_amount = emissions_amount
        self.allocated_credits = allocated_credits
        self.max_buying_price = 0
        self.max_selling_price = 0

    def do_transaction(self):
        pass
