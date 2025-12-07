class SimData:
    def __init__(self):
        # Constructor. Define instance vars here.
        self.supplyHistories = []
        self.productHistories = []
        self.mouseXY = []
        self.hoverFrame = 20 # 0-20
    
    class SupplyHIstory:
        def __init__(self, ID, name, goalAmounts, orderedAmounts, usedAmounts):
            self.ID = ID
            self.name = name
            self.goalAmounts = goalAmounts
            self.orderedAmounts = orderedAmounts
            self.usedAmounts = usedAmounts
    
    class ProductHistory:
        def __init__(self, ID, name, price, sales, supplyCost):
            self.ID = ID
            self.name = name
            self.price = price
            self.sales = sales
            self.supplyCost = supplyCost
            # Revenue, cost, and profit can all be calculated with sales and supply cost.
    
    def addSupply(self, ID, name):
        # TODO
    def addProduct(self, ID, name, price, cost):
        # TODO
    def addSupplyHistory(self, ID, goal, ordered, used):
        # TODO
    def addProductHistory(self, ID, sales):
        # TODO
    def eraseHistory(self):
        # TODO
    def storeInput(self):
        # TODO
    
    def drawSupplyGraph(self, supplyID):
        # TODO
        # Draw empty graph if -1
    def drawRevenueGraph(self, productID):
        # TODO
        # Draw total of all products if -1
    def drawSalesGraph(self, productID):
        # TODO
        # Draw empty graph if -1
    def drawEndOfDayGraph(self):
        # TODO