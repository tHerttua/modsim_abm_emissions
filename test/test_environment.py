import environment

abm_env = environment.Environment(100, 1000, 365)


def test_create_agents():
    abm_env.create_agents()
    agents = abm_env.agents
    print("x")
    assert len(agents) != 0


test_create_agents()