from environment import Environment
import matplotlib.pyplot as plt
import numpy as np

#Methods for ploting and calculating the results

def plot_result(label, result_pr, result_em, modus_name, change, runs):
#plots results for modus = 1 and modus = 2

    for i in range(len(result_pr)):

        plt.plot(result_pr[i], '-', color=plt.cm.RdYlBu(np.linspace(0, 1, runs)[i]),
                         label=label + str(i*change +1))
        plt.legend()

    plt.xlabel('Steps')
    plt.ylabel('Price paid different runs')
    plt.title("Modus of Simulation: " + modus_name)
    plt.savefig("pics/"+modus_name+"Price.png")
    #plt.show()s
    plt.clf()

    for i in range(len(result_em)):

        plt.plot(result_em[i], '-', color=plt.cm.RdYlBu(np.linspace(0, 1, runs)[i]),
                         label=label + str(i*change +1))
        plt.legend()

    plt.xlabel('Steps')
    plt.ylabel('Transactions average per run')
    plt.title("Modus of Simulation: " + modus_name)
    plt.savefig("pics/"+modus_name+"transaction.png")
    #plt.show()s
    plt.clf()

def plot_result_aver(label, result_pr, result_em, modus_name):
    #polot results for modus = 3, meaning ploting average line
    # as well as light grey path lines of each run
    price_av, transaction_av = avering(result_pr, result_em)

    plt.plot(price_av, color = "red", label="Average Price")
    plt.legend()

    for i in range(len(result_pr)):
        plt.plot(result_pr[i], color = "grey", alpha=0.1)

    plt.xlabel('Steps')
    plt.ylabel('Price paid different runs')
    plt.savefig("pics/"+"Average_price.png")
    #plt.show()s
    plt.clf()

    plt.plot(transaction_av, color = "blue", label="Average Transaction Number")
    plt.legend()

    for i in range(len(result_pr)):
        plt.plot(result_em[i], color = "grey", alpha=0.1)

    plt.xlabel('Steps')
    plt.ylabel('Transactions done different runs')
    plt.savefig("pics/"+"Average_Transaction.png")
    #plt.show()s
    plt.clf()


def avering(result_pr, result_em):
    #averages over all runds of modus = 3
    price = []
    transaction = []

    for step in range(len(result_pr[1])):
        price_tmp = 0
        transaction_tmp = 0
        for j in range(len(result_pr)):
            price_tmp = price_tmp + result_pr[j][step]
            transaction_tmp = transaction_tmp + result_em[j][step]

        price_tmp = price_tmp/len(result_pr)
        transaction_tmp = transaction_tmp / len(result_pr)
        price.append(price_tmp)
        transaction.append(transaction_tmp)

    return price, transaction


def chan_cred_red(allowances, random_sel, em_red, limit_transaction,  change, limit):
    #modus = 1, makes agent based modeling in the manner that it
    #runs multiple times the model with changing credit-reducing-rate
    modus_name = "Changing Reduction Rate of Credits"
    label = "Reduction Rate: "
    runs = limit
    result_pr =[]
    result_em = []

    for i in range(runs):

        env = Environment(modus_name,
                          titlevalue = (1 - i * change),
                          number_of_agents_per_group=20,
                          number_of_agents_group=10,
                          allowance_credits=allowances,
                          agent_transaction_limit=limit_transaction,
                          time_steps=365,
                          iterate=i,
                          certificate_reductionrate = (1 - i * change))
        env.create_agents()
        result = env.do_magic(
                          random_sel,
                          em_red,
        plots= True)

        result_pr.append(result[0])
        result_em.append(result[1])
        print(str(i) + " run, finished")

    plot_result(label, result_pr, result_em, modus_name, -change, runs)



def chan_tran_limit(allowances, random_sel, em_red, cred_red_rate, change, limit):
    #modus = 2, makes agent based modeling in the manner that it
    #runs multiple times the model with changing transactional limit
    modus_name = "Changing Number of Transaction Limit"
    label = "Transactionlimit: "
    runs = limit
    result_pr =[]
    result_em = []

    for i in range(runs):

        env = Environment(modus_name,
                          titlevalue = (1 + i * change),
                          number_of_agents_per_group=20,
                          number_of_agents_group=10,
                          allowance_credits=allowances,
                          agent_transaction_limit=(1 + i * change),
                          time_steps=365,
                          iterate=i,
                          certificate_reductionrate = cred_red_rate)
        env.create_agents()
        result = env.do_magic(
                          random_sel,
                          em_red,
        plots = True)

        result_pr.append(result[0])
        result_em.append(result[1])
        print(str(i) + " run, finished")

    plot_result(label, result_pr, result_em, modus_name, change, runs)

def many_runs(allowances, random_sel, em_red, limit_transaction, cred_red_rate , limit, plots):
    #modus = 3, makes agent based modeling in the manner that it
    #runs multiple times the model with the same parameters and averages over the results
    # and plots them
    modus_name = "Average"
    label = "Avererging: "
    runs = limit
    result_pr =[]
    result_em = []

    for i in range(runs):

        env = Environment(modus_name,
                          titlevalue = "",
                          number_of_agents_per_group=20,
                          number_of_agents_group=10,
                          allowance_credits=allowances,
                          agent_transaction_limit=limit_transaction,
                          time_steps=365,
                          iterate=i,
                          certificate_reductionrate = cred_red_rate)
        env.create_agents()
        result = env.do_magic(
                          random_sel,
                          em_red, plots = plots)

        result_pr.append(result[0])
        result_em.append(result[1])
        print(str(i) + " run, finished")


    plot_result_aver(label, result_pr, result_em, modus_name)

#initializing the model
"""
200 companies split between 10 groups (every 10th percentile)
Groups have the following emissions averages,
and they're used as a proxy for the initial credits.
(Subject to having divisor of 30 (days per month))
monthly allowances = (avg_emission / 12) - (avg_emission / 12) % 30
Groups  Average Emissions   Allowance credits assigned monthly
1	    883.39              60
2	    2886.11             180
3   	5229.72             420
4	    8372.33             690
5	    14848.94            1230
6	    22214.83            1830
7	    32504.00            2700
8	    49125.83            4080
9	    89848.94            7470
10	    366534.00           30540

"""

if __name__ == '__main__':

    allowances = [
        60,
        180,
        420,
        690,
        1230,
        1830,
        2700,
        4080,
        7470,
        30540
    ]

    #note, for us credits, allocations and allowances are the same thing

    #Settings

    #here can be put two extensions on of

    #first
    # Are buyers and Sellers Randomly Selected or after a Logic
    #True =  they are randomly selected
    random_sel = False
    #second
    # Can Sellers Reduce Emissions after a successful Deal in the same step
    # for addionally selling credits
    #True =  it is possible to reduce emission for a deal
    em_red = False

    #Modus

    #Three Modes can be selected for calculating results and investigate different aspects of the model

    #changing parameters of time
    #modus = 1 for investigating an unexpected reduction per step of free allowances per month
    #modus = 2 for investigating for changing transaction limits

    #averaging over multiple runs
    #modus = 3 is for averaging over the price and transaction numbers development
    # over multiple runs by keeping initial parameters concant several months

    modus = 2

    #limit transaction is the max number of transactions per agent per step
    #each transaction can just include 1 credit or eventually 1 emission
    #200 works very good but takes a lot of comuptation so we take 40


    #change ist the changing parameter per run
        #mode = 1 decreases the reduction factor by 1 - change * number_of_run
        #mode = 2 increases limit transaction by 1 + change * number_of_run
        #(Number_of_Run is initialized with 0)

    #limit is the number of runs

    # cred_red_rate is the rate with which new free allowances are unexptedely reduced for agents per month

    # plot is just an option for the last function, which says
    # whether each run plots from each run should be saved

    if modus == 1:
        chan_cred_red(allowances, random_sel, em_red, limit_transaction = 40, change = 0.02, limit = 3)
        pass
    elif modus == 2:
        chan_tran_limit(allowances, random_sel, em_red, cred_red_rate = 1, change = 20, limit = 5)

    elif modus == 3:
        many_runs(allowances, random_sel, em_red, limit_transaction = 40, cred_red_rate = 0.96, limit = 20, plots = False)

