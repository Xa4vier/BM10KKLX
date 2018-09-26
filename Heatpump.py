class HeatPump:
    """ Headpump bass class """
    
    def __init__(self, amount, name, maxOutput):
        self.amount = amount
        self.name = name
        self.maxOutput = maxOutput
        self.energyOutput = 0