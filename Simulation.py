class Simulation:
    """ the environment where the magic happens """
    
    def __init__(self, households, heatPumps):
        self.households = households
        self.heatPumps = heatPumps
      
    def run(self):
        max_output = self.max_output()
        data = []
        for hour in range(1, 25): 
            need = self.total_need_per_hour(hour)
            overload = True
            if need > max_output: 
                overload = False
                
            data.append({'overload' : overload, 'need' : need, 'max_output' : max_output,})
        return data
        
    
    def total_need_per_hour(self, hour):
        need = 0
        for household in self.households:
            for energyNeed in household.energyNeed:
                if energyNeed.startTime <= hour and energyNeed.stopTime > hour:
                    need += energyNeed.energy * household.amount
        return need

    def max_output(self):
        production = 0
        for heatpump in self.heatPumps:
            production += heatpump.maxOutput * heatpump.amount
        return production
    
    def total_production(self):
        production = 0
        for heatpump in self.heatPumps:
            production += heatpump.energyOutput
        return production