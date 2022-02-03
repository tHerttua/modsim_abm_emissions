from environment import Environment


"""
200 companies split between 10 groups
Groups have the following emissions averages,
and they're used as a proxy for the initial credits.
(Subject to having divisor of 32)

monthly allowances =  = (avg_emission / 12) - (avg_emission / 12) % 32 
NOT FINAL -> change to any other function you want

Groups  Average Emissions   Allowance credits assigned monthly
1	    883.39              64
2	    2886.11             160
3   	5229.72             448
4	    8372.33             672
5	    14848.94            1216
6	    22214.83            1824
7	    32504.00            2688
8	    49125.83            4064
9	    89848.94            7456
10	    366534.00           30528



"""

if __name__ == '__main__':

    allowances = [
        64,
        160,
        448,
        672,
        1216,
        1824,
        2688,
        4064,
        7456,
        30528
    ]

    i = 1

    env = Environment(number_of_agents_per_group=20,
                      number_of_agents_group=10,
                      allowance_credits=allowances,#has to have divisor 32
                      agent_transaction_limit=20,
                      time_steps=365,
                      iterate=i) #??
    env.create_agents()
    env.do_magic(version=3)

