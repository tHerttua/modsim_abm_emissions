import random
from agent import Agent

class Environment:
    def __init__(self, number_of_agents, allowance_credits, time_steps):
        self.number_of_agents = number_of_agents
        self.time_steps = time_steps
        self.allowance_credits = allowance_credits
        self.price_equilibrium
        self.total_emissions
        self.agents = []
        self.results = []

    def create_agents(self):
        for _ in range(self.number_of_agents):
            emissions_amount = self.randomize_emission_amount
            allocated_credits = self.allowance_credits
            new_agent = Agent(emissions_amount, allocated_credits)
            self.agents.append(new_agent)

    def randomize_emission_amount(self):
        emission_amount = 1000
        return emission_amount
