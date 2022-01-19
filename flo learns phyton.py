from agent import Agent

x = Agent(1,300, 7, 5)
y = Agent(2,400, 8, 4)
z = Agent(3, 300, 4, 9)

sheeps = [x,y,z]

newlist =sorted(sheeps, key=lambda x: x.max_buying_price, reverse=True)

print(sheeps[0].emissions_amount,sheeps[1].emissions_amount, sheeps[2].emissions_amount)
print(newlist[0].emissions_amount,newlist[1].emissions_amount,newlist[2].emissions_amount)

sheeps.sort(key=lambda x: x.max_buying_price, reverse=False)

print(sheeps[0].emissions_amount,sheeps[1].emissions_amount, sheeps[2].emissions_amount)
