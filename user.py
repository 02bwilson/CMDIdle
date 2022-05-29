class user():
    def __init__(self):
        self.mps = 1
        self.bal = 0
        self.mult = 1
        self.prestiges = 0
        
    def setMps(self, val):
        self.mps = val
    def getMps(self):
        return self.mps
    def setBal(self, val):
        self.bal = val
    def getBal(self):
        return self.bal
    def setMult(self, val):
        self.mult = val
    def getMult(self):
        return self.mult
    def setPrestiges(self, val):
        self.prestiges = val
    def getPrestiges(self):
        return self.prestiges