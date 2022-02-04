from environment import Environment
import matplotlib.pyplot as plt
import numpy as np
"""
200 companies split between 10 groups (every 10th percentile)
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

    i = 0
    runs = 5
    result_pr =[]
    result_em = []
    for i in range(runs):

        env = Environment(number_of_agents_per_group=20,
                          number_of_agents_group=10,
                          allowance_credits=allowances,
                          agent_transaction_limit=(1 + i * 10 ),
                          time_steps=365,
                          iterate=i)
        env.create_agents()
        result = env.do_magic(version=3)
        result_pr.append(result[0])
        result_em.append(result[1])
        i = i + 1

    for i in range(len(result_pr)):

        plt.plot(result_pr[i], '-', color=plt.cm.RdYlBu(np.linspace(0, 1, runs)[i]),
                         label="limit" + str(i*10 +1) + "Price")
        plt.legend()

    plt.xlabel('Steps')
    plt.ylabel('Price paid different runs')
    plt.savefig("pics/"+"limitPrice.png")
    #plt.show()s
    plt.clf()

    for i in range(len(result_em)):

        plt.plot(result_em[i], '-', color=plt.cm.RdYlBu(np.linspace(0, 1, runs)[i]),
                         label="limit" + str(i*10 +1) + "Emission")
        plt.legend()

    plt.xlabel('Steps')
    plt.ylabel('Emissions average different runs')
    plt.savefig("pics/"+"limitEmission.png")
    #plt.show()s
    plt.clf()





