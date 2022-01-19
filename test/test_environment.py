import environment

abm_env = environment.Environment(100, 1000, 365)


def test_create_agents():
    abm_env.create_agents()
    agents = abm_env.agents
    print("x")
    assert len(agents) != 0


def test_sort_agents():
    abm_env.create_agents()
    buyers, sellers, satisfied = abm_env.list_buyers_sellers_satisfied()
    sorted_buyers, sorted_sellers = abm_env.sort_sellers_buyers(buyers, sellers)
    for buyer in sorted_buyers:
        if buyer.