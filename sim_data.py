import pygame

class SimData:
    def __init__(self):
        # Constructor. Define instance vars here.
        self.supplies = []
        self.products = []
        self.mouseXY = []
        self.lftClkSt = 0
        self.hoverFrame = 20 # 0-20
    class Supply:
        def __init__(self, ID, name):
            self.ID = ID
            self.name = name
            self.history = [] # [price,goalAmounts,orderedAmounts,usedAmounts]
    class Product:
        def __init__(self, ID, name):
            self.ID = ID
            self.name = name
            self.history = [] # [price,sales,supplyCost]
            # Revenue, cost, and profit can all be calculated with sales and supply cost.
    def addSupply(self, ID, name):
        self.supplies.append(self.Supply(ID, name))
    def addProduct(self, ID, name):
        self.products.append(self.Product(ID, name))
    def addSupplyHistory(self, ID, price, goal, ordered, used):
        for s in self.supplies:
            if(s.ID==ID):
                s.history.append([price,goal,ordered,used])
                break
    def addProductHistory(self, ID, price, sales, cost):
        for p in self.products:
            if(p.ID==ID):
                p.history.append([price,sales,cost])
                break
    def eraseHistory(self):
        for s in self.supplies:
            s.history = []
        for p in self.products:
            p.hsitory = []
    def storeInputs(self,MouseXY,lftClk): # Takes user input and converts them into a better format for the Sim to use
        self.mouseXY = MouseXY
        if(self.lftClkSt==0 and lftClk): # mouse was clicked
            self.lftClkSt = 1
            return
        if(self.lftClkSt==1 and lftClk): # mouse is held down
            self.lftClkSt = 2
            return
        if(self.lftClkSt>0 and not lftClk): # mouse was unclicked
            self.lftClkSt = 0
            return
    def drawSupplyGraph(self, supplyID):
        # TODO
        # Draw empty graph if -1
        pass
    def drawRevenueGraph(self, productID):
        # TODO
        # Draw total of all products if -1
        pass
    def drawSalesGraph(self, productID):
        # TODO
        # Draw empty graph if -1
        pass
    def drawEndOfDayGraph(self):
        # TODO
        pass
    