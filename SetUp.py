from Household import Household
from Energy import EnergyNeed
from Heatpump import HeatPump
from Simulation import Simulation

def add_heatpumps(amount, name, maxOutput):
    heatpumps = []
    for i in range(amount):
        heatpumps.append(HeatPump(name, maxOutput))
    return heatpumps

def add_households(amount, name, energy, startTime, stopTime):
    households = []
    for i in range(amount):
        households.append(Household(name, EnergyNeed(energy, startTime, stopTime)))
    return households

def make_list_one_dim(list_):
    returnList = []
    for i in list_:
        for j in i:
            returnList.append(j)
    return returnList

# adding heat pumps
heatPumps = [] 
heatPumps.append(add_heatpumps(2, 'standaart', 300))
heatPumps.append(add_heatpumps(4, 'extra Turbo', 500))

heatPumps = make_list_one_dim(heatPumps)

# adding households
households = []
households.append(add_households(100, 'gezin met kinderen', 30, 1200, 1200))
households.append(add_households(50, 'een persoon', 13, 1200, 1200))

households = make_list_one_dim(households)

# set simulation
Simulation = Simulation(households, heatPumps)

print(Simulation.run())