import environment

abm_env = environment.Environment(100, 1000, 365)


def test_create_agents():
    abm_env.create_agents()
    agents = abm_env.agents

    assert type(agents[0].allocated_credits) == int
    assert type(agents[0].max_buying_price) == int


def test_split_agents():
    abm_env.create_agents()
    buyers, sellers, satisfied = abm_env.list_buyers_sellers_satisfied()

    assert len(buyers) != 0
    assert len(sellers) != 0
    assert buyers[0].emissions_amount > buyers[0].allocated_credits
    assert sellers[0].emissions_amount < sellers[0].allocated_credits


def test_sort_agents():
    abm_env.create_agents()
    buyers, sellers, satisfied = abm_env.list_buyers_sellers_satisfied()
    sorted_buyers, sorted_sellers = abm_env.sort_buyers_sellers(buyers, sellers)

    assert len(sorted_buyers) != 0
    for i in range(len(sorted_buyers)-1):
        if i != len(sorted_buyers):
            print(sorted_buyers[i].max_buying_price)
            print(sorted_buyers[i+1].max_buying_price)
            assert sorted_buyers[i].max_buying_price <= sorted_buyers[i+1].max_buying_price


def test_do_transactions():
    abm_env.create_agents()
    buyers, sellers, satisfied = abm_env.list_buyers_sellers_satisfied()
    sorted_buyers, sorted_sellers = abm_env.sort_buyers_sellers(buyers, sellers)
    x = abm_env.do_transaction(sorted_buyers, sorted_sellers)


test_create_agents()
test_split_agents()
test_sort_agents()
test_do_transactions()

