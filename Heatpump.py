class HeatPump:
    """ Headpump bass class """
    
    def __init__(self, name, maxOutput):
        self.name = name
        self.maxOutput = maxOutput
        self.energyOutput = 0