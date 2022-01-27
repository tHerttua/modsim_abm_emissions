from environment import Environment


"""
    agent daily limit per time step

    # could experiment with time step = 12, agent_daily_limit = 100
        -> per month, agent can do 100 transactions
"""

if __name__ == '__main__':
    for i in range(6):
        env = Environment(number_of_agents_per_group=10,
                          number_of_agents_group=66,
                          allowance_credits=160,#has to have divisor 32
                          agent_transaction_limit=20,
                          time_steps=365,
                          iterate=i)
        env.create_agents()
        env.do_magic(version=3)

