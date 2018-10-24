from Household import Household
from Energy import EnergyNeed
from Simulation import Simulation
  
# adding households
households = []
# gezin met kinderen huishouden
households.append(Household(100, 'gezin met kinderen', 'standaart', 60 ))
households[len(households) - 1].energyNeed.append(EnergyNeed(30, 7, 9))
households[len(households) - 1].energyNeed.append(EnergyNeed(25, 16, 21))
households[len(households) - 1].energyNeed.append(EnergyNeed(15, 21, 23))

# eens gezins huishouden
households.append(Household(100, 'eens gezins', 'standaart', 60))
households[len(households) - 1].energyNeed.append(EnergyNeed(13, 8, 9))
households[len(households) - 1].energyNeed.append(EnergyNeed(10, 17, 24))

# set simulation
Simulation = Simulation(households)

# run simulation
#data = Simulation.run()

## print the return data 
#i = 1
#for d in data:
#    print(f"{i} overload: {d.get('overload')}, need: {d.get('need')}, max: {d.get('max_output')}")
#    i += 1