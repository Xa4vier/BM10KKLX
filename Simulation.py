class Simulation:
    """ the environment where the magic happens """
    
    def __init__(self, households, heatPumps):
        self.households = households
        self.heatPumps = heatPumps
      
    def run(self):
        need = self.total_need()
        maxOutput = self.max_output()
        if need > maxOutput:
            message =   f""" heat pump crash!
            need: {need}
            max cap: {maxOutput}
                            """
        if need <= maxOutput:
            message = f"""all oke!
            need: {need}
            max cap: {maxOutput}"""
        return message
        
    
    def total_need(self):
        need = 0
        for household in self.households:
            need += household.energyNeed.energy
        return need

    def max_output(self):
        production = 0
        for heatpump in self.heatPumps:
            production += heatpump.maxOutput
        return production
    
    def total_production(self):
        production = 0
        for heatpump in self.heatPumps:
            production += heatpump.energyOutput
        return production