from environment import Environment


"""
    agent daily limit per time step

    # could experiment with time step = 12, agent_daily_limit = 100
        -> per month, agent can do 100 transactions
"""

if __name__ == '__main__':
    env = Environment(number_of_agents_per_group=3,
                      number_of_agents_group=100,
                      allowance_credits=320,
                      agent_transaction_limit=3,
                      time_steps=365)
    env.create_agents()
    env.do_magic(version=3)

