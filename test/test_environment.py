import environment

# Broken. Environment has changed
abm_env = environment.Environment(100, 1000, 10, 365)


def test_create_agents():
    abm_env.create_agents()
    agents = abm_env.agents
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
    agents = abm_env.agents
    ids = []
    for agent in agents:
        ids.append(id(agent))

    for buyer in buyers:
        assert id(buyer) in ids
    assert some_sellers_index is not None


def test_sort_agents():
    abm_env.create_agents()
    buyers, sellers, satisfied = abm_env.list_buyers_sellers_satisfied()
    sorted_buyers, sorted_sellers = abm_env.sort_buyers_sellers(buyers, sellers)

    assert len(sorted_buyers) != 0
    for i in range(len(sorted_buyers)-1):
        if i != len(sorted_buyers):
            #print(sorted_buyers[i].max_buying_price)
            #print(sorted_buyers[i+1].max_buying_price)
            assert sorted_buyers[i].max_buying_price <= sorted_buyers[i+1].max_buying_price


def test_do_transactions():
    abm_env.create_agents()
    buyers, sellers, satisfied = abm_env.list_buyers_sellers_satisfied()
    sorted_buyers, sorted_sellers = abm_env.sort_buyers_sellers(buyers, sellers)
    abm_env.do_transactions(sorted_buyers, sorted_sellers, step=1)
    assert sorted_buyers[0].number_transaction_left != 10


def test_reset_transactions_after_step():
    abm_env.create_agents()
    buyers, sellers, satisfied = abm_env.list_buyers_sellers_satisfied()
    sorted_buyers, sorted_sellers = abm_env.sort_buyers_sellers(buyers, sellers)
    abm_env.do_transactions(sorted_buyers, sorted_sellers, step=1)

    satisfied_ids = []
    agents_ids = []
    agents = abm_env.agents

    depleted = [agent for agent in agents if agent.number_transaction_left == 0]

    assert len(depleted) != 0

    for agnt in agents:
        agnt.reset_quota()

    depleted = [agent for agent in agents if agent.number_transaction_left == 0]

    assert len(depleted) == 0


def test_do_transactions2():
    pass


