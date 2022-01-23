import agent
from environment import Environment


if __name__ == '__main__':
    env = Environment(1000, 100000, 365)
    env.create_agents()
    env.do_magic()




