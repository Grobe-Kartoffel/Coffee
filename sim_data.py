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
            self.history = [] # [price,goalAmounts,orderedAmounts,usedAmounts,remaining]
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
    def addSupplyHistory(self, ID, price, goal, ordered, used, remaining):
        for s in self.supplies:
            if(s.ID==ID):
                s.history.append([price,goal,ordered,used,remaining])
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
    def storeInputs(self,MouseXY): # Takes user input and converts them into a better format for the Sim to use
        self.mouseXY = MouseXY
    def drawSupplyGraph(self, supplyID, surface, SCALE):
        # when a supply item is clicked
            # display ordered (green), used (blue), and remaining (red) for the last 7 days
        # when -1, no supply item is clicked
            # display text "No Data"
        xWindowMin = 162*SCALE
        xWindowMax = 316*SCALE
        yWindowMin = 71*SCALE
        yWindowMax = 137*SCALE
        font = pygame.font.SysFont(None,40)
        text = font.render("Supply History",True,(0,0,0))
        surface.blit(text,[163*SCALE,62*SCALE])
        if(supplyID==-1):
            text = font.render("No Data",True,(0,0,0))
            surface.blit(text,[(xWindowMin+xWindowMax)/2-font.size("No Data")[0]/2, (yWindowMin+yWindowMax)/2-font.size("No Data")[1]/2])
            return
        xGraphMin = -0.3
        xGraphMax = 6.3
        yGraphMin = 0
        yGraphMax = 0
        orderedPoints = []
        usedPoints = []
        remainingPoints = []
        # draw specific graph here
        for s in self.supplies:
            if(s.ID==supplyID):
                # get all the data points
                day = 0
                if(len(s.history)<=7):
                    for i in range(len(s.history)):
                        orderedPoints.append([day,s.history[i][2]])
                        usedPoints.append([day,s.history[i][3]])
                        remainingPoints.append([day,s.history[i][4]])
                        day += 1
                else:
                    for i in range(len(s.history)-7,len(s.history)):
                        orderedPoints.append([day,s.history[i][2]])
                        usedPoints.append([day,s.history[i][3]])
                        remainingPoints.append([day,s.history[i][4]])
                        day += 1 
                # find y maxes and mins
                yGraphMin = orderedPoints[0][1]
                yGraphMax = orderedPoints[0][1]
                for p in orderedPoints:
                    if(p[1]>yGraphMax):
                        yGraphMax = p[1]
                    if(p[1]<yGraphMin):
                        yGraphMin = p[1]
                for p in usedPoints:
                    if(p[1]>yGraphMax):
                        yGraphMax = p[1]
                    if(p[1]<yGraphMin):
                        yGraphMin = p[1]
                for p in remainingPoints:
                    if(p[1]>yGraphMax):
                        yGraphMax = p[1]
                    if(p[1]<yGraphMin):
                        yGraphMin = p[1]
                yGraphMax += 0.05*(yGraphMax-yGraphMin)
                yGraphMin -= 0.05*(yGraphMax*0.95-yGraphMin)
                # graph points
                # draw 0 lines
                x0 = float(0-xGraphMin)/float(xGraphMax-xGraphMin) # find the "scale" of a point by comparing it's value minus the min to the max minus the min
                if(x0>=0 and x0<=1):
                    # to draw a point, reverse the process, multiply by the max minus the min, then add the min
                    pygame.draw.line(surface, (0,0,0), (x0*(xWindowMax-xWindowMin)+xWindowMin,yWindowMin), (x0*(xWindowMax-xWindowMin)+xWindowMin,yWindowMax), width=2)
                y0 = 1.0 - float(0-yGraphMin)/float(yGraphMax)
                if(y0>=0 and y0<=1):
                    pygame.draw.line(surface, (0,0,0), (xWindowMin,y0*(yWindowMax-yWindowMin)+yWindowMin), (xWindowMax,y0*(yWindowMax-yWindowMin)+yWindowMin), width=2)
                # draw points
                BLUE = (18,83,175)
                GREEN = (66,170,59)
                RED = (255,0,0)
                font = pygame.font.SysFont(None,18)
                captions = []
                for i in range(len(orderedPoints)):
                    p = orderedPoints[i]
                    x = float(p[0]-xGraphMin)/float(xGraphMax-xGraphMin)
                    y = 1 - float(p[1]-yGraphMin)/float(yGraphMax-yGraphMin)
                    pygame.draw.circle(surface, GREEN, (x*(xWindowMax-xWindowMin)+xWindowMin,y*(yWindowMax-yWindowMin)+yWindowMin), 6)
                    # draw line to previous point
                    if(i>0):
                        p_ = orderedPoints[i-1]
                        x_ = float(p_[0]-xGraphMin)/float(xGraphMax-xGraphMin)
                        y_ = 1 - float(p_[1]-yGraphMin)/float(yGraphMax-yGraphMin)                            
                        pygame.draw.line(surface, GREEN, (x*(xWindowMax-xWindowMin)+xWindowMin,y*(yWindowMax-yWindowMin)+yWindowMin), (x_*(xWindowMax-xWindowMin)+xWindowMin,y_*(yWindowMax-yWindowMin)+yWindowMin), width=2)
                        # check for mouse hover
                    if(self.mouseXY[0]>=x*(xWindowMax-xWindowMin)+xWindowMin-6 and self.mouseXY[0]<=x*(xWindowMax-xWindowMin)+xWindowMin+6 and self.mouseXY[1]>=y*(yWindowMax-yWindowMin)+yWindowMin-6 and self.mouseXY[1]<=y*(yWindowMax-yWindowMin)+yWindowMin+6):
                        captions.append(f"Ordered: {p[1]:.0f}")
                for i in range(len(usedPoints)):
                    p = usedPoints[i]
                    x = float(p[0]-xGraphMin)/float(xGraphMax-xGraphMin)
                    y = 1 - float(p[1]-yGraphMin)/float(yGraphMax-yGraphMin)
                    pygame.draw.circle(surface, BLUE, (x*(xWindowMax-xWindowMin)+xWindowMin,y*(yWindowMax-yWindowMin)+yWindowMin), 6)
                    # draw line to previous point
                    if(i>0):
                        p_ = usedPoints[i-1]
                        x_ = float(p_[0]-xGraphMin)/float(xGraphMax-xGraphMin)
                        y_ = 1 - float(p_[1]-yGraphMin)/float(yGraphMax-yGraphMin)                            
                        pygame.draw.line(surface, BLUE, (x*(xWindowMax-xWindowMin)+xWindowMin,y*(yWindowMax-yWindowMin)+yWindowMin), (x_*(xWindowMax-xWindowMin)+xWindowMin,y_*(yWindowMax-yWindowMin)+yWindowMin), width=2)
                        # check for mouse hover
                    if(self.mouseXY[0]>=x*(xWindowMax-xWindowMin)+xWindowMin-6 and self.mouseXY[0]<=x*(xWindowMax-xWindowMin)+xWindowMin+6 and self.mouseXY[1]>=y*(yWindowMax-yWindowMin)+yWindowMin-6 and self.mouseXY[1]<=y*(yWindowMax-yWindowMin)+yWindowMin+6):
                        captions.append(f"Used: {p[1]:.0f}")
                for i in range(len(remainingPoints)):
                    p = remainingPoints[i]
                    x = float(p[0]-xGraphMin)/float(xGraphMax-xGraphMin)
                    y = 1 - float(p[1]-yGraphMin)/float(yGraphMax-yGraphMin)
                    pygame.draw.circle(surface, RED, (x*(xWindowMax-xWindowMin)+xWindowMin,y*(yWindowMax-yWindowMin)+yWindowMin), 6)
                    # draw line to previous point
                    if(i>0):
                        p_ = remainingPoints[i-1]
                        x_ = float(p_[0]-xGraphMin)/float(xGraphMax-xGraphMin)
                        y_ = 1 - float(p_[1]-yGraphMin)/float(yGraphMax-yGraphMin)                            
                        pygame.draw.line(surface, RED, (x*(xWindowMax-xWindowMin)+xWindowMin,y*(yWindowMax-yWindowMin)+yWindowMin), (x_*(xWindowMax-xWindowMin)+xWindowMin,y_*(yWindowMax-yWindowMin)+yWindowMin), width=2)
                    # check for mouse hover
                    if(self.mouseXY[0]>=x*(xWindowMax-xWindowMin)+xWindowMin-6 and self.mouseXY[0]<=x*(xWindowMax-xWindowMin)+xWindowMin+6 and self.mouseXY[1]>=y*(yWindowMax-yWindowMin)+yWindowMin-6 and self.mouseXY[1]<=y*(yWindowMax-yWindowMin)+yWindowMin+6):
                        captions.append(f"Remaining: {p[1]:.0f}")
                # draw mouse hover text
                for i in range(len(captions)):
                    text = font.render(captions[i],True,(0,0,0),(255,255,255))
                    surface.blit(text,[self.mouseXY[0],self.mouseXY[1]-(font.size(captions[i])[1])*(len(captions)-i)])                
                break
    def drawRevenueGraph(self, productID, surface, SCALE):
        # when a product item is clicked
            # display revenue (blue), supply cost (red), and profit (green) for the last 7 days
        # when -1, no product item is clicked
            # display total revenue (blue), total supply cost (red), and total profit (green)
        xWindowMin = 162*SCALE
        xWindowMax = 316*SCALE
        yWindowMin = 30*SCALE
        yWindowMax = 96*SCALE 
        font = pygame.font.SysFont(None,40)
        text = font.render("Revenue History",True,(0,0,0))
        surface.blit(text,[163*SCALE,21*SCALE])
        xGraphMin = -1
        xGraphMax = 7
        yGraphMin = 0
        yGraphMax = 0
        revenuePoints = []
        costPoints = []
        profitPoints = []
        if(productID==-1):
            # draw totals here
            return
        # draw specific graph here
    def drawSalesGraph(self, productID, surface, SCALE):
        # when a product item is clicked
            # display total sales (blue) for the last 7 days
        # when -1, no product item is clicked
            # display text "No Data"
        xWindowMin = 162*SCALE
        xWindowMax = 316*SCALE
        yWindowMin = 110*SCALE
        yWindowMax = 176*SCALE
        font = pygame.font.SysFont(None,40)
        text = font.render("Sales History",True,(0,0,0))
        surface.blit(text,[163*SCALE,101*SCALE])
        if(productID==-1):
            text = font.render("No Data",True,(0,0,0))
            surface.blit(text,[(xWindowMin+xWindowMax)/2-font.size("No Data")[0]/2, (yWindowMin+yWindowMax)/2-font.size("No Data")[1]/2])
            return
        xGraphMin = -1
        xGraphMax = 7
        yGraphMin = 0
        yGraphMax = 0
        salesPoints = []
        # draw specific graph here        
    def drawEndOfDayGraph(self, surface, SCALE):
        # display revenue throughout the day (green), and points throughout the day (blue)
        xWindowMin = 83*SCALE
        xWindowMax = 237*SCALE
        yWindowMin = 52*SCALE
        yWindowMax = 118*SCALE
        font = pygame.font.SysFont(None,40)
        text = font.render("Today's Results",True,(0,0,0))
        surface.blit(text,[5*SCALE,4*SCALE])  
        xGraphMin = 5
        xGraphMax = 21
        yGraphMin = 0
        yGraphMax = 0
        revenuePoints = []
        scorePoints = []
        # draw specific graph here
    