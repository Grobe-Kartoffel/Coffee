import math, random, pygame, sys, threading
from abc import ABC, abstractmethod                     # not sure why abstract classes need to be imported like this, but they do

pygame.init()                                           # initialize game engine

SCALE = 4                                               # set scale factor for graphics
W=320*SCALE                                             # set window size
H=180*SCALE
size=(W,H)
surface = pygame.display.set_mode(size)

pygame.display.set_caption("Claire's Coffee Shop")      # window title
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)

#declare global variables here

BLACK    =  (   0,   0,   0)                            #Color Constants
WHITE    =  ( 255, 255, 255)
GREEN    =  (   0, 255,   0)
LGREEN   =  ( 128, 255, 128)
RED      =  ( 255,   0,   0)
BLUE     =  (   0,   0, 255)


#other global variables (WARNING: use sparingly):


clock = pygame.time.Clock()                             # Manage timing for screen updates

#Program helper functions:

class Progress_Manager: # manages a progress bar for when Accuracy Data is reading a file, so the rest of the game can continue running
    def __init__(self):
        self.Max = 1.0
        self.Value = 0.0
        self.lock = threading.Lock()
    def update(self,value):
        with self.lock:
            self.Value = value
    def displayProgress(self,x,y,w,h,border,BORDERCOLOR,PROGRESSCOLOR):
        pygame.draw.rect(surface,BORDERCOLOR,(x-border,y-border,w+border*2,h+border*2),border)
        pygame.draw.rect(surface,PROGRESSCOLOR,(x,y,w*self.Value,h))        
class Accuracy_Data:
    def __init__(self):
        self.probabilitySpaces = []  # 7x13 (day of week/hour of day) matrix containing the probability of an item ordered at that time on that day, being that product
    def __str__(self): # function is called when class object is placed in the print() function
        string = ""
        i = 0
        while(i<len(self.probabilitySpaces)):
            j = 0
            string += "ProbabilitySpace:\n"
            while(j<len(self.probabilitySpaces[i])):                                    # probability space
                string += "["
                k = 0                
                while(k<len(self.probabilitySpaces[i][j])):
                    string += f"{self.probabilitySpaces[i][j][k]:.5f}"
                    if(k==len(self.probabilitySpaces[i][j])-1):
                        string += "]\n"
                    else:
                        string += ", "
                    k += 1
                if(j==len(self.probabilitySpaces[i])-1):
                    string += "\n\n"
                j += 1
            i += 1
        return string
    def readSalesData(self,settings,progressBar):
        progressBar.update(0)
        
        date = ""               # this is just to know when the day changes
        weekDay = 0             # note that the Data begins on January 1st, 2023, which is a Sunday
                                # note that we will be keeping track of this internally as it is not in the data
        hour = 0                # note that we will be subtracting 6 from the hour in the data as the store opens at 6am
        quantity = 0
        product = 0
        price = 0.0
        desc = ""
        
        lines = []              # contains all lines of data within the file
        dataLoc = 0             # indicates which piece of data we are in, within a line
        
        filename = "SalesData_Sorted.csv"
        try: # make sure the file exists before we start reading
            salesFile = open(filename, "r")
            salesFile.close()
        except:
            print("ERROR: '"+filename+"' could not be found. Aborting processing.")
            progressBar.update(-1) # threads do not have return values, but we can manipulate the progress bar to indicate an error
            return
        
        salesFile = open(filename, "r")
        lines = salesFile.readlines()              # this returns a list with every line of text in it
        
        for x in range(len(lines)): # iterate through each line in the data
            i = 0           # iterator through each line
            dataLoc = 0     # reset data values
            quantity = 0
            product = 0
            price = 0
            desc = ""
            line = lines[x]
            if(x==0):       # skip the header
                continue
            while( i < len(line)): # iterate through each character in the line (uses while loop so we can also directly access the characters ourselves)
                match(dataLoc): # how to handle each piece of data
                    case 0: # transaction_id
                        if(line[i]=='|'):
                            dataLoc += 1
                    case 1: # transaction_date
                        if(date==""):
                            date = line[i:i+10] # date is a substring starting from c and ending 10 characters later
                        else:
                            if(date!=line[i:i+10]):    # if the date changed
                                date = line[i:i+10]    # update it
                                weekDay += 1        # increment the day of the week
                                if(weekDay >= 7):
                                    weekDay = 0
                        i += 10 # skip to the end of the date
                        dataLoc += 1
                    case 2: # transaction_time
                        hour = int(line[i])*10 + int(line[i+1]) - 6 # earliest hour found is 6am
                        i += 8
                        dataLoc += 1
                    case 3: # transaction_qty
                        while(line[i]!='|'):
                            quantity = quantity*10 + int(line[i])
                            i += 1
                        dataLoc += 1
                    case 4: # store_id
                        if(line[i]=='|'):
                            dataLoc += 1
                    case 5: # store_location
                        if(line[i]=='|'):
                            dataLoc += 1
                    case 6: # product_id
                        while(line[i]!='|'):
                            product = product*10 + int(line[i])
                            i += 1
                        dataLoc += 1
                    case 7: # unit_price
                        j = 0
                        while(line[i+j]!='|'):
                            j += 1
                        price = float(line[i:i+j])
                        i += j
                        dataLoc += 1
                    case 8: # product descriptions
                        desc = line[i:-1]
                        break
                i += 1
            # we have read all the data from the line, now we have to store it
            prodIndex = 0   # I can't be bothered to sort the data right now, so we search the entire list to find which entry we are editing
            while(prodIndex < len(settings.products)):
                if(settings.products[prodIndex][0]==product): # we found a matching entry
                    # price and product details only change once
                    # quantity is the only value that will need updated with every entry
                    self.probabilitySpaces[prodIndex][weekDay][hour] += quantity
                    break
                prodIndex += 1
            if(prodIndex==len(settings.products)): # we have a new product that we have not read before
                settings.addProd(product,desc,price)
                self.probabilitySpaces.append( [[0.0]*15]*7 ) # 7 days in a week, 15 hours a day (6am - 9pm)
            # update progress bar
            progressBar.update( float(x+1)/float(len(lines)) )
        # always close files after using them
        salesFile.close()
        
        # need to retroactively add chili mayan hot chocolate Rg and Lg because it is missing from the data
        # ratios of the popularities of chili mayan chocolate powder to other chocolate powders will be used to extrapolate chili mayan hot chocolate popularity from other hot chocolate drinks
        
        # initialize Chili Mayan Hot Chocolate Rg
        settings.addProd(62,"Drinking Chocolate|Hot chocolate|Chili Mayan Rg",4.75)
        self.probabilitySpaces.append( [[0.0]*15]*7 )
        
        # initialize Chili Mayan Hot Chocolate Lg
        settings.addProd(63,"Drinking Chocolate|Hot chocolate|Chili Mayan Lg",6.25)
        self.probabilitySpaces.append( [[0.0]*15]*7 )
        
        # vars needed for extrapolation
        darkPowIndex,organicPowIndex,chiliPowIndex = 0,0,0
        darkRgIndex,darkLgIndex = 0,0
        organicRgIndex,organicLgIndex = 0,0
        chiliRgIndex,chiliLgIndex = 0,0
        darkRatio,organicRatio = 0.0,0.0
        darkValue,organicValue,chiliValue = 0.0,0.0,0.0
        
        # find indexes
        prodIndex = 0
        while(prodIndex < len(settings.products)):
            match(settings.products[prodIndex][0]):
                case 19: # dark chocolate powder
                    darkPowIndex = prodIndex
                case 20: # organic chocolate powder
                    organicPowIndex = prodIndex
                case 21: # chili chocolate powder
                    chiliPowIndex = prodIndex
                case 58: # dark Rg
                    darkRgIndex = prodIndex
                case 59: # dark Lg
                    darkLgIndex = prodIndex
                case 60: # organic Rg
                    organicRgIndex = prodIndex
                case 61: # organic Lg
                    organicLgIndex = prodIndex
                case 62: # chili Rg
                    chiliRgIndex = prodIndex
                case 63: # chili Lg
                    chiliLgIndex = prodIndex
            prodIndex += 1        
        
        # extrapolate data
        # get an average ratio across an entire day (some hours, powder is not ordered at all, leading to an inaccurate ratio)
        for hour in range(15): # we don't need to worry about a new ratio for each day, because all days are identical
            darkValue += float(self.probabilitySpaces[darkPowIndex][0][hour])
            organicValue += float(self.probabilitySpaces[organicPowIndex][0][hour])
            chiliValue += float(self.probabilitySpaces[chiliPowIndex][0][hour])
        darkRatio = chiliValue / darkValue
        organicRatio = chiliValue / organicValue
        # use the ratios to find a value for the chili hot chocolate
        for day in range(7):
            for hour in range(15):
                # Rg
                darkValue = float(self.probabilitySpaces[darkRgIndex][day][hour]) * darkRatio
                organicValue = float(self.probabilitySpaces[organicRgIndex][day][hour]) * organicRatio
                    # use the average of the two results to hopefully be more accurate
                self.probabilitySpaces[chiliRgIndex][day][hour] = int((darkValue+organicValue)/2.0)
                # Lg
                darkValue = float(self.probabilitySpaces[darkLgIndex][day][hour]) * darkRatio
                organicValue = float(self.probabilitySpaces[organicLgIndex][day][hour]) * organicRatio
                    # use the average of the two results to hopefully be more accurate
                self.probabilitySpaces[chiliLgIndex][day][hour] = int((darkValue+organicValue)/2.0)
        
        # go through probability data of all products and convert them to decimals to be used in sim calculations
        total = 0
        for day in range(7):
            for hour in range(15):
                total = 0
                for prod in range(len(settings.products)):
                    total += self.probabilitySpaces[prod][day][hour]
                for prod in range(len(settings.products)):
                    self.probabilitySpaces[prod][day][hour] = float(self.probabilitySpaces[prod][day][hour]) / float(total)
        return
    def readSupplyData(self,settings,progressBar):
        progressBar.update(0)
        
        product = 0
        supply = 0
        supplyAmt = 0.0
        supplyAmtPrice = 0.0
        
        lines = []
        dataLoc = 0
        
        filename = "SupplyData.csv"
        try: # make sure the file exists before we start reading
            salesFile = open(filename, "r")
            salesFile.close()
        except:
            print("ERROR: '"+filename+"' could not be found. Aborting processing.")
            progressBar.update(-1) # threads do not have return values, but we can manipulate the progress bar to indicate an error
            return
        
        salesFile = open(filename, "r")
        lines = salesFile.readlines()              # this returns a list with every line of text in it
        
        for x in range(len(lines)): # iterate through each line in the data
            i = 0           # iterator through each line
            dataLoc = 0     # reset data values
            product = 0
            supply = 0
            supplyAmt = 0.0
            supplyAmtPrice = 0.0            
            line = lines[x]
            if(x==0):       # skip the header
                continue
            while( i < len(line)):
                match(dataLoc):
                    case 0: # product id
                        while(line[i]!='|'):
                            product = product*10 + int(line[i])
                            i += 1
                        dataLoc += 1                        
                    case 1: # supply id
                        while(line[i]!='|'):
                            supply = supply*10 + int(line[i])
                            i += 1
                        dataLoc += 1                        
                    case 2: # supply amount
                        j = 0
                        while(line[i+j]!='|'):
                            j += 1
                        supplyAmt = float(line[i:i+j])
                        i += j
                        dataLoc += 1                        
                    case 3: # supply amount price
                        supplyAmtPrice = float(line[i:-1])
                        dataLoc += 1                        
                i += 1
            # we have read all the data from the line, now we have to store it
            supIndex = 0   # I can't be bothered to sort the data right now, so we search the entire list to find which entry we are editing
            while(supIndex < len(settings.supplies)):
                if(settings.supplies[supIndex][0]==supply): # we found a matching entry
                    if(supplyAmt==1): # update price if we have an exact conversion on this line
                        settings.setSupPrice(supIndex,supplyAmtPrice)
                    break
                supIndex += 1
            if(supIndex==len(settings.supplies)): # we have a new supply that we have not read before
                settings.addSup(supply)
                if(supplyAmt==1):
                    settings.setSupPrice(supIndex,supplyAmtPrice)
            prodIndex = 0
            while(prodIndex < len(settings.products)): # set the desc of the supply
                if(settings.products[prodIndex][0]==supply):
                    settings.setSupDesc(supIndex,settings.products[prodIndex][1])
                if(supply==84):
                    settings.setSupDesc(supIndex,"Cup Sm")
                if(supply==85):
                    settings.setSupDesc(supIndex,"Cup Rg")
                if(supply==86):
                    settings.setSupDesc(supIndex,"Cup Lg")
                prodIndex += 1
            # we should have handled the supply entry
            # now we need to update the related product entry
            prodIndex = 0
            while(prodIndex < len(settings.products)):
                if(settings.products[prodIndex][0]==product):
                    settings.addProdSup(prodIndex,supply,supplyAmt)
                    break
                prodIndex += 1
            # update progress bar
            progressBar.update( float(x+1)/float(len(lines)) )
        # always close files after using them
        salesFile.close()            
        return
class Settings:
    def __init__(self):
        self.products = []       # product ID and description for each product
        self.prodSupplies = []   # list of supplies needed for each product
        self.prodSupplyAmt = []  # list of supply amounts needed for each product
        self.prodPrices = []     # price of each product
        self.supplies = []       # supply ID and description for each supply
        self.supPrices = []      # price of each supply
        self.lock = threading.Lock()
    def __str__(self): # function is called when class object is placed in the print() function
        string = ""
        i = 0
        while(i<len(self.products)):
            string += f"ID:\t\t{self.products[i][0]}\nDesc:\t\t{self.products[i][1]}\n" # product ID and Description
            j = 0
            string += "Supplies:\t"                                                     # supplies
            while(j<len(self.prodSupplies[i])):
                string += f"[ID: {self.prodSupplies[i][j]}"
                k = 0
                while(k<len(self.supplies)):
                    if(self.supplies[k][0]==self.prodSupplies[i][j]):
                        string += f"; Desc: {self.supplies[k][1]}"
                        break
                    k += 1
                string += f"; Amt: {self.prodSupplyAmt[i][j]}]"
                j += 1
                if(j<len(self.prodSupplies[i])):
                    string += ", "
            string += "\n"
            string += f"Price:\t\t{self.prodPrices[i]}\n\n\n"                                   # price
            i += 1
        return string
    def addProd(self,ID,desc,price):
        with self.lock:
            self.products.append([ID,desc])
            self.prodSupplies.append([])
            self.prodSupplyAmt.append([])
            self.prodPrices.append(price)
    def addSup(self,ID):
        with self.lock:
            self.supplies.append([ID,""])
            self.supPrices.append(0) 
    def addProdSup(self,prodID,supID,supAmt):
        with self.lock:
            self.prodSupplies[prodID].append(supID)
            self.prodSupplyAmt[prodID].append(supAmt)     
    def setSupPrice(self,ID,price):
        with self.lock:
            self.supPrices[ID] = price
    def setSupDesc(self,ID,desc):
        with self.lock:
            self.supplies[ID][1] = desc
        return
class Sim:
    # movement speed will be 1 pixel per frame, or just under 1 unit of space per second
    def __init__(self):
        self.mouseXY = [0,0]
        self.lftClkSt = 0
        self.employees = []
        self.customers = []
        self.objects = []
        self.demoStarted = False
        # image assets
        self.floorPlan = pygame.image.load("assets/floorplan.png").convert_alpha()
        self.floorPlan = pygame.transform.scale_by(self.floorPlan,SCALE)
        self.cust11 = pygame.image.load("assets/cust_1_1.png").convert_alpha()
        self.cust11 = pygame.transform.scale_by(self.cust11,SCALE)
        self.cust12 = pygame.image.load("assets/cust_1_2.png").convert_alpha()
        self.cust12 = pygame.transform.scale_by(self.cust12,SCALE)
        self.cust13 = pygame.image.load("assets/cust_1_3.png").convert_alpha()
        self.cust13 = pygame.transform.scale_by(self.cust13,SCALE)
        self.cust14 = pygame.image.load("assets/cust_1_4.png").convert_alpha()
        self.cust14 = pygame.transform.scale_by(self.cust14,SCALE)
        self.cust21 = pygame.image.load("assets/cust_2_1.png").convert_alpha()
        self.cust21 = pygame.transform.scale_by(self.cust21,SCALE)
        self.cust22 = pygame.image.load("assets/cust_2_2.png").convert_alpha()
        self.cust22 = pygame.transform.scale_by(self.cust22,SCALE)
        self.cust23 = pygame.image.load("assets/cust_2_3.png").convert_alpha()
        self.cust23 = pygame.transform.scale_by(self.cust23,SCALE)
        self.cust24 = pygame.image.load("assets/cust_2_4.png").convert_alpha()
        self.cust24 = pygame.transform.scale_by(self.cust24,SCALE)
        self.cust31 = pygame.image.load("assets/cust_3_1.png").convert_alpha()
        self.cust31 = pygame.transform.scale_by(self.cust31,SCALE)
        self.cust32 = pygame.image.load("assets/cust_3_2.png").convert_alpha()
        self.cust32 = pygame.transform.scale_by(self.cust32,SCALE)
        self.cust33 = pygame.image.load("assets/cust_3_3.png").convert_alpha()
        self.cust33 = pygame.transform.scale_by(self.cust33,SCALE)
        self.cust34 = pygame.image.load("assets/cust_3_4.png").convert_alpha()
        self.cust34 = pygame.transform.scale_by(self.cust34,SCALE)
        self.cust41 = pygame.image.load("assets/cust_4_1.png").convert_alpha()
        self.cust41 = pygame.transform.scale_by(self.cust41,SCALE)
        self.cust42 = pygame.image.load("assets/cust_4_2.png").convert_alpha()
        self.cust42 = pygame.transform.scale_by(self.cust42,SCALE)
        self.cust43 = pygame.image.load("assets/cust_4_3.png").convert_alpha()
        self.cust43 = pygame.transform.scale_by(self.cust43,SCALE)
        self.cust44 = pygame.image.load("assets/cust_4_4.png").convert_alpha()
        self.cust44 = pygame.transform.scale_by(self.cust44,SCALE)
    class Emp:
        def __init__(self,ID,loc,job,task):
            self.ID = ID
            self.loc = [loc[0],loc[1]]
            self.offset = [0,0]
            self.dir = 0
            self.hand = None
            self.job = job
            self.task = task
            self.patience = 3600
    class Cust:
        def __init__(self,ID,loc,order,task):
            self.ID = ID
            self.loc = [loc[0],loc[1]]
            self.offset = [0,0]
            self.dir = 0
            self.order = order
            self.hand = None
            self.task = task
            self.patience = 300
    class Obj:
        def __init__(self,ID,loc):
            self.ID = ID
            self.loc = [loc[0],loc[1]]
            self.offset = [0,0]
    def demoSim(self):
        if(not self.demoStarted):
            self.demoStarted = True
            self.customers.append(self.Cust(random.randint(0,3),[-1,1],58,0)) # spawn a customer off screen, wanting a reg Dark Hot Chocolate, with the task of walking right forever (for testing purposes)
            return
        for unit in self.customers:
            if(unit.task==0): # walk forward
                unit.offset[0] += 1
                if(unit.offset[0]>=32): # check if we've walked forward into the next space
                    unit.offset[0] -= 64
                    unit.loc[0] += 1
                    if(unit.loc[0]>=21): # delete if walked off screen
                        unit.loc[0] = -1 # unit is a separate object from the list element, we cannot delete it here. We'll have to mark it for deletion later
                        unit.loc[1] = -1 # spawning off screen and walking offscreen will only ever result in 1 negative coord. 2 negative coords will indicate deletion
                        # for now, this will trigger a new customer being spawned
                        self.customers.append(self.Cust(random.randint(0,3),[-1,1],58,0))
        # check for deleted customers
        i = 0
        while(i<len(self.customers)):
            if(self.customers[i].loc[0]==-1 and self.customers[i].loc[1]==-1):
                del self.customers[i]
                continue
            i += 1
        self.draw()
    def newSim(self):
        pass
    def continueSim(self):
        pass
    def runSim(self):
        pass
    def storeInputs(self,MouseXY,lftClk):
        self.mouseXY = [(int(MouseXY[0])/(16*scale))+1,int(MouseXY[1])/(16*scale)] #scale down to the 22x12 grid of the simulation (first and last 16x are offscreen and ignored)
        if(self.lftClkSt==0 and lftClk): # mouse was clicked
            self.lftClkSt = 1
            return
        if(self.lftClkSt==1 and lftClk): # mouse is held down
            self.lftClkSt = 2
            return
        if(self.lftClkSt>0 and not lftClk): # mouse was unclicked
            self.lftClkSt = 0
            return
    def draw(self):
        surface.blit(self.floorPlan, [0,0])                       # coffeeshop
        custs = [[self.cust11,self.cust12,self.cust13,self.cust14],[self.cust21,self.cust22,self.cust23,self.cust24],[self.cust31,self.cust32,self.cust33,self.cust34],[self.cust41,self.cust42,self.cust43,self.cust44]]
        for unit in self.customers:
            surface.blit(custs[unit.ID][unit.dir],[unit.loc[0]*16*SCALE+unit.offset[0],unit.loc[1]*16*SCALE+unit.offset[1]])
# -------- Main Program Loop -----------
def main():                                             #every program should have a main function
                                                        #other functions go above main
    # local  variables
    data = Accuracy_Data()              # create class objects
    progressBar = Progress_Manager()
    settings = Settings()
    sim = Sim()
    
    dataState = 0 # indicate data has not started processing yet
    
    salesDataThread = threading.Thread(target=data.readSalesData, args=(settings,progressBar,))   # DO NOT INCLUDE PARENTHESIS ON TARGET FUNCTION    # ARGS MUST BE ITERABLE, INCLUDE EXTRA COMMA FOR ONLY 1 ARG
    supplyDataThread = threading.Thread(target=data.readSupplyData, args=(settings,progressBar,))
    
    # image files
    logo = pygame.image.load("assets/logo.png").convert_alpha(surface)
    #logo = pygame.transform.scale(logo, (160,160))
    logoFrame = 0.0
    
    while (True):
        
        for event in pygame.event.get():                #captures state of the game - loops thru changes
            
            if ( event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): #end game
                pygame.quit()
                sys.exit()
        
            # button, mouse, or keyboard interaction here
            if(logoFrame<240 and (event.type==pygame.MOUSEBUTTONDOWN or event.type==pygame.KEYDOWN)): # skip intro logo
                logoFrame = 240
        
        # ongoing game logic here  (repeats every 1/60 second)
        
        # thread logic for processing data
        if(progressBar.Value==0.0 and dataState==0):
            dataState = 1 # indicate sales data is processing
            salesDataThread.start()
        if(progressBar.Value<0 and dataState==1):
            salesDataThread.join()
            print("ERROR: Sales Data could not be found. Aborting program.")
            return            
        if(progressBar.Value>=1.0 and dataState==1):
            salesDataThread.join()
            #return                  # remove this once supplyData is written
            dataState = 2 # indicate supply data is processing
            supplyDataThread.start()
        if(progressBar.Value<0 and dataState==2):
            supplyDataThread.join()
            print("ERROR: Supply Data could not be found. Aborting program.")
            return            
        if(progressBar.Value>=1.0 and dataState==2):
            supplyDataThread.join()
            dataState = 3 # indicate data is done processing
        if(dataState==3):
            print(settings)
            print(data)
            dataState += 1
            # return
        # intro logo logic
        if(dataState>0 and logoFrame<=360):
            logoFrame += 1
        #set background color
        surface.fill(BLACK)
        
        # drawing code goes here
        if(logoFrame<=120):
            logo.set_alpha(int(255.0*logoFrame/120.0))
        if(logoFrame>120 and logoFrame<=240):
            logo.set_alpha(255)
        if(logoFrame>240 and logoFrame<=360):
            logo.set_alpha(255 - int(255.0*(logoFrame-240)/120.0) )
        if(logoFrame<=360):
            surface.blit(logo, [(W-640)/2,(H-640)/2])
        else:
            sim.demoSim()
            #progressBar.displayProgress(W/16, H*6/13, W*7/8, H/13, 5, WHITE, GREEN)
            
        
        
        pygame.display.update()                          #updates the screen
        clock.tick(120)                                  # FPS for animation (lower number to slow)
        
#----------------------------------------------------------------
main()                                                   #runs the game