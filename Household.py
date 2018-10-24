from Heatpump import Heatpump

class Household:
    """ Household bass class """
    
    def __init__(self, amount, name, *args):
        self.amount = amount
        self.name = name
        self.energyNeed = []
        self.heatpump = Heatpump(*args)