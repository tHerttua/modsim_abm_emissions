import environment

abm_env = environment.Environment(100, 1000, 365)


def test_create_agents():
    abm_env.create_agents()# I am not so familiar with python so I ask out of curisoty
    agents = abm_env.agents#why do we need two lines here?

    assert type(agents[0].pre_allocated_credits) == int
    assert type(agents[0].max_buying_price) == int


def test_split_agents():
    abm_env.create_agents()
    buyers, sellers, satisfied = abm_env.list_buyers_sellers_satisfied()

    assert len(buyers) != 0
    assert len(sellers) != 0
    assert buyers[0].emissions_amount > buyers[0].pre_allocated_credits
    assert sellers[0].emissions_amount < sellers[0].pre_allocated_credits


def test_identify_agents():
    abm_env.create_agents()
    buyers, sellers, satisfied = abm_env.list_buyers_sellers_satisfied()

    some_seller = sellers[2]
    some_sellers_index = abm_env.agents.index(some_seller)

    for buyer in buyers:
        assert buyer in abm_env.agents
    assert some_sellers_index is not None


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
    x = abm_env.do_transactions(sorted_buyers, sorted_sellers)


