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
        self.shelfSpace = [0,0]
        self.prod_order = []
        self.demoStarted = False
        # image assets
        # floorplan
        self.floorPlan = pygame.image.load("assets/floorplan.png").convert_alpha()
        self.floorPlan = pygame.transform.scale_by(self.floorPlan,SCALE)
        # customers
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
        # employees
        self.emp11 = pygame.image.load("assets/emp_1_1.png").convert_alpha()
        self.emp11 = pygame.transform.scale_by(self.emp11,SCALE)
        self.emp12 = pygame.image.load("assets/emp_1_2.png").convert_alpha()
        self.emp12 = pygame.transform.scale_by(self.emp12,SCALE)
        self.emp13 = pygame.image.load("assets/emp_1_3.png").convert_alpha()
        self.emp13 = pygame.transform.scale_by(self.emp13,SCALE)
        self.emp14 = pygame.image.load("assets/emp_1_4.png").convert_alpha()
        self.emp14 = pygame.transform.scale_by(self.emp14,SCALE)
        self.emp21 = pygame.image.load("assets/emp_2_1.png").convert_alpha()
        self.emp21 = pygame.transform.scale_by(self.emp21,SCALE)
        self.emp22 = pygame.image.load("assets/emp_2_2.png").convert_alpha()
        self.emp22 = pygame.transform.scale_by(self.emp22,SCALE)
        self.emp23 = pygame.image.load("assets/emp_2_3.png").convert_alpha()
        self.emp23 = pygame.transform.scale_by(self.emp23,SCALE)
        self.emp24 = pygame.image.load("assets/emp_2_4.png").convert_alpha()
        self.emp24 = pygame.transform.scale_by(self.emp24,SCALE)
        self.emp31 = pygame.image.load("assets/emp_3_1.png").convert_alpha()
        self.emp31 = pygame.transform.scale_by(self.emp31,SCALE)
        self.emp32 = pygame.image.load("assets/emp_3_2.png").convert_alpha()
        self.emp32 = pygame.transform.scale_by(self.emp32,SCALE)
        self.emp33 = pygame.image.load("assets/emp_3_3.png").convert_alpha()
        self.emp33 = pygame.transform.scale_by(self.emp33,SCALE)
        self.emp34 = pygame.image.load("assets/emp_3_4.png").convert_alpha()
        self.emp34 = pygame.transform.scale_by(self.emp34,SCALE)
        self.emp41 = pygame.image.load("assets/emp_4_1.png").convert_alpha()
        self.emp41 = pygame.transform.scale_by(self.emp41,SCALE)
        self.emp42 = pygame.image.load("assets/emp_4_2.png").convert_alpha()
        self.emp42 = pygame.transform.scale_by(self.emp42,SCALE)
        self.emp43 = pygame.image.load("assets/emp_4_3.png").convert_alpha()
        self.emp43 = pygame.transform.scale_by(self.emp43,SCALE)
        self.emp44 = pygame.image.load("assets/emp_4_4.png").convert_alpha()
        self.emp44 = pygame.transform.scale_by(self.emp44,SCALE)
    class Emp:
        # static vars belonging to class, not one individual instance
        # lists containing the orders that require each of the supply types so that emp1 knows where to get the proper supply item
        sup_cof  = [1,2,3,4,5,6,7,8,9,10,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,87]    # coffee beans
        sup_tea  = [11,12,13,14,15,16,17,18,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57]                # tea leaves
        sup_coco = [19,20,21,58,59,60,61,62,63]                                                             # cocoa powders
        sup_syr  = [64,65,66,67]                                                                            # syrups
        sup_pas  = [69,70,71,72,73,74,75,76,77,78,79]                                                       # pastries
        sup_mug  = [82]                                                                                     # mugs
        sup_cup  = [83]                                                                                     # cups
        sup_shr  = [81]                                                                                     # shirts
        prod_wet = [22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,87]
        prod_dry = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,64,65,66,67,69,70,71,72,73,74,75,76,77,78,79,81,82,83]
        def __init__(self,ID,loc,job,task):
            self.ID = ID
            self.loc = [loc[0],loc[1]]
            self.offset = [0,0]
            self.dir = 0
            self.hand = None
            self.job = job
            self.task = task
            self.order = 0
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
            self.customers.append(self.Cust(random.randint(0,3),[-1,1],58,1)) # spawn a customer off screen, wanting a reg Dark Hot Chocolate, with the task of walking into the shop to order
            self.employees.append(self.Emp(random.randint(0,3),[5,4],0,0)) # spawn an employee to take orders, with the task of waiting for a customer to order
            self.employees.append(self.Emp(random.randint(0,3),[5,8],1,0)) # spawn an employee to give orders, with the task of waiting for an order to be made
            self.employees.append(self.Emp(random.randint(0,3),[15,1],2,0)) # spawn an employee to clean tables, with the task of waiting for food to be left on the table
            return
        # handle customers
        i = 0
        while(i<len(self.customers)):
            unit = self.customers[i]
            match(unit.task):
                case 0: # walking zombie to test loop
                    unit.offset[0] += 2
                    if(unit.offset[0]>=32): # check if we've walked forward into the next space
                        unit.offset[0] -= 64
                        unit.loc[0] += 1
                        if(unit.loc[0]>=21): # delete if walked off screen
                            unit.loc[0] = -1 # unit is a separate object from the list element, we cannot delete it here. We'll have to mark it for deletion later
                            unit.loc[1] = -1 # spawning off screen and walking offscreen will only ever result in 1 negative coord. 2 negative coords will indicate deletion
                            # for now, this will trigger a new customer being spawned
                            self.customers.append(self.Cust(random.randint(0,3),[-1,1],58,0))
                case 1: # walking into the coffee shop to order
                    if(unit.offset[0]<0 and unit.loc[1]==1):    # centering onto current tile
                        unit.offset[0] += 2
                        if(unit.offset[0]==0 and unit.loc[0]==8):
                            unit.dir = 3
                    elif(unit.offset[1]<0 and unit.loc[0]==8):  # ^
                        unit.offset[1] += 2
                        if(unit.offset[1]==0 and unit.loc[1]==4):
                            unit.dir = 2
                    elif(unit.offset[0]>0 and unit.loc[1]==4):  # ^
                        unit.offset[0] -= 2
                        if(unit.offset[0]==0): # if we got to the front of the line, we are now ordering
                            unit.task += 1
                    elif(unit.loc[0]<8 and unit.loc[1]==1):     # need to walk to next tile to the right / obey line rules
                        space = True
                        for c in self.customers:
                            if(c.loc[0] == unit.loc[0]+1 and c.loc[1] == 1):
                                space = False
                                break
                        if(space):
                            unit.offset[0] += 2
                            if(unit.offset[0]>=32):
                                unit.offset[0] -= 64
                                unit.loc[0] += 1
                                if(unit.loc[0]==0): # we're going to spawn more on screen as they get in the store
                                    self.customers.append(self.Cust(random.randint(0,3),[-1,1],58,1))
                    elif(unit.loc[0]==8 and unit.loc[1]<4):     # need to walk to next tile below / obey line rules
                        space = True
                        for c in self.customers:
                            if(c.task==1 and c.loc[0] == 8 and c.loc[1] == unit.loc[1]+1):
                                space = False
                                break
                        if(space):
                            unit.offset[1] += 2
                            if(unit.offset[1]>=32):
                                unit.offset[1] -= 64
                                unit.loc[1] += 1
                    elif(unit.loc[0]==8 and unit.loc[1]==4):    # need to walk to next tile to the left / obey line rules
                        space = True
                        for c in self.customers:
                            if((c.task==1 or c.task==2) and c.loc[0] == 7 and c.loc[1] == 4):
                                space = False
                                break
                        if(space):
                            unit.offset[0] -= 2
                            if(unit.offset[0]<=-32):
                                unit.offset[0] += 64
                                unit.loc[0] -= 1
                case 2: # ordering
                    if(self.mouseXY[0]==7 and self.mouseXY[1]==3 and self.lftClkSt==1):
                        for e in self.employees:
                            if(e.job==0 and e.task==0 and e.loc[0]==5 and e.loc[1]==4):
                                unit.task += 1
                                unit.dir = 3
                                break
                case 3: # walking to the pick-up line
                    if(unit.offset[0]<0):                                           # centering onto current tile
                        unit.offset[0] += 2
                        if(unit.offset[0]==0 and unit.loc[0]==9):
                            unit.dir = 1
                    elif(unit.loc[0]==7 and unit.loc[1]==5 and unit.offset[1]<0):   # ^
                        unit.offset[1] += 2
                        if(unit.offset[1]==0):
                            unit.dir = 0
                    elif(unit.loc[0]==9 and unit.offset[1]>0):                      # ^
                        unit.offset[1] -= 2
                        if(unit.offset[1]==0 and unit.loc[1]==1):
                            unit.task += 1 # start waiting in line
                            unit.dir = 3
                    elif(unit.loc[0]==7 and unit.loc[1]==4):                        # walk down / out of ordering line
                        unit.offset[1] += 2
                        if(unit.offset[1]>=32):
                            unit.offset[1] -= 64
                            unit.loc[1] += 1
                    elif(unit.loc[0]<9 and unit.loc[1]==5):                         # walk to the right
                        unit.offset[0] += 2
                        if(unit.offset[0]>=32):
                            unit.offset[0] -= 64
                            unit.loc[0] += 1
                    elif(unit.loc[0]==9):                                           # walk up to start waiting in line
                        unit.offset[1] -= 2
                        if(unit.offset[1]<=-32):
                            unit.offset[1] += 64
                            unit.loc[1] -= 1
                case 4: # pick-up line
                    if(unit.offset[1]<0):                   # centering onto current tile
                        unit.offset[1] += 2
                        if(unit.offset[1]==0 and unit.loc[1]==8):
                            unit.dir = 2
                    elif(unit.offset[0]>0):                 # ^
                        unit.offset[0] -= 2
                        if(unit.offset[0]==0 and unit.loc[0]==7 and unit.loc[1]==8):
                            unit.task += 1 # wait for order pickup
                    elif(unit.loc[0]==9 and unit.loc[1]<8): # walk down / obey line rules
                        space = True
                        for c in self.customers:
                            if(c.task==4 and c.loc[0] == 9 and (c.loc[1] == unit.loc[1]+1 or (c.loc[1]==unit.loc[1] and c.offset[1]>unit.offset[1]) ) ):
                                space = False
                                break
                        if(space):
                            unit.offset[1] += 2
                            if(unit.offset[1]>=32):
                                unit.offset[1] -= 64
                                unit.loc[1] += 1 
                    elif(unit.loc[1]==8):                   # walk left / obey line rules
                        space = True
                        for c in self.customers:
                            if((c.task==4 or c.task==5) and c.loc[0] == unit.loc[0]-1 and c.loc[1] == 8):
                                space = False
                                break
                        if(space):
                            unit.offset[0] -= 2
                            if(unit.offset[0]<=-32):
                                unit.offset[0] += 64
                                unit.loc[0] -= 1
                case 5: # picking up order
                    if(self.mouseXY[0]==5 and self.mouseXY[1]==7 and self.lftClkSt==1):
                        unit.task += 1
                        unit.dir = 3
                case 6: # finding a seat
                    if(unit.offset[0]<0):                                                   # centering onto current tile
                        unit.offset[0] += 2
                        if(unit.offset[0]==0 and (unit.loc[0] == 10 or unit.loc[0] == 19)):     # start walking up
                            unit.dir = 1
                            if(unit.loc[0]==10): # check if the very first seat is available first
                                spaceR = True
                                for c in self.customers:
                                    if(c.task==7 and c.loc[0]==unit.loc[0]+1 and c.loc[1]==unit.loc[1]):
                                        spaceR = False
                                    if(spaceR and c.task==7 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==0):
                                        spaceR = False
                                if(spaceR):
                                    unit.task = 7
                                    unit.dir = 0
                        if(unit.offset[0]==0 and unit.loc[0] == 15):                            # start walking down
                            unit.dir = 3
                    elif(unit.offset[1]<0 and (unit.loc[0] == 7 or unit.loc[0] == 15)):     # ^
                        unit.offset[1] += 2
                        if(unit.offset[1]==0 and unit.loc[0] == 7 and unit.loc[1] == 9):        # start walking right
                            unit.dir = 0
                        elif(unit.offset[1]==0 and unit.loc[0] == 15 and unit.loc[1] == 10):    # start walking right
                            unit.dir = 0
                        elif(unit.offset[1]==0 and unit.loc[0]==15):                            # look for seats
                            spaceL = True
                            spaceR = True
                            for c in self.customers:
                                if(c.task==7 and c.loc[0]==unit.loc[0]-1 and c.loc[1]==unit.loc[1]):
                                    spaceL = False
                                if(spaceL and c.task==7 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==2):
                                    spaceL = False
                                if(c.task==7 and c.loc[0]==unit.loc[0]+1 and c.loc[1]==unit.loc[1]):
                                    spaceR = False
                                if(spaceR and c.task==7 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==0):
                                    spaceR = False
                            if(spaceL):
                                unit.task = 7
                                unit.dir = 2
                            elif(spaceR):
                                unit.task = 7
                                unit.dir = 0
                    elif(unit.offset[1]>0 and (unit.loc[0] == 10 or unit.loc[0] == 19)):    # ^
                        unit.offset[1] -= 2
                        if(unit.offset[1]==0 and (unit.loc[0] == 10 or unit.loc[0] == 19) and unit.loc[1] == 2):    # start walking right
                            unit.dir = 0
                            if(unit.loc[0]==19): # leave the shop
                                unit.task = 8
                        elif(unit.offset[1]==0 and unit.loc[0]==10):                                                # look for a seat on the right
                            spaceR = True
                            for c in self.customers:
                                if(c.task==7 and c.loc[0]==unit.loc[0]+1 and c.loc[1]==unit.loc[1]):
                                    spaceR = False
                                if(spaceR and c.task==7 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==0):
                                    spaceR = False
                            if(spaceR):
                                unit.task = 7
                                unit.dir = 0
                        elif(unit.offset[1]==0 and unit.loc[0]==19):                                                # look for a seat on the left
                            spaceL = True
                            for c in self.customers:
                                if(c.task==7 and c.loc[0]==unit.loc[0]-1 and c.loc[1]==unit.loc[1]):
                                    spaceL = False
                                if(spaceL and c.task==7 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==2):
                                    spaceL = False
                            if(spaceL):
                                unit.task = 7
                                unit.dir = 0
                    elif(unit.loc[0]==7 and unit.loc[1]==8):                                # down / out of pick-up line
                        unit.offset[1] += 2
                        if(unit.offset[1]>=32):
                            unit.offset[1] -= 64
                            unit.loc[1] += 1
                    elif((unit.loc[0]==10 or unit.loc[0]==19) and unit.loc[1]>2):           # up
                        unit.offset[1] -= 2
                        if(unit.offset[1]<=-32):
                            unit.offset[1] += 64
                            unit.loc[1] -= 1
                    elif(unit.loc[0]==15 and unit.loc[1]<10):                               # down
                        unit.offset[1] += 2
                        if(unit.offset[1]>=32):
                            unit.offset[1] -= 64
                            unit.loc[1] += 1
                    else:                                                                   # move right otherwise
                        unit.offset[0] += 2
                        if(unit.offset[0]>=32):
                            unit.offset[0] -= 64
                            unit.loc[0] += 1
                case 7: # sitting down / eating
                    if(unit.offset[0]==0 and (unit.loc[0]==11 or unit.loc[0]==14 or unit.loc[0]==16 or unit.loc[0]==19)):   # eat food
                        unit.patience -= 1
                        if(unit.patience<=0):
                            unit.task += 1
                            unit.dir = 1
                    elif(unit.dir==0 and ((unit.loc[0]!=11 and unit.loc[0]!=16) or unit.offset[0]!=0) ):                    # take a seat to the right
                        unit.offset[0] += 2
                        if(unit.offset[0]>=32):
                            unit.offset[0] -= 64
                            unit.loc[0] += 1
                    elif(unit.dir==2 and unit.loc[0]!=19 and (unit.loc[0]!=14 or unit.offset[0]!=0)):                       # take a seat to the left (not including back row)
                        unit.offset[0] -= 2
                        if(unit.offset[0]<=-32):
                            unit.offset[0] += 64
                            unit.loc[0] -= 1
                case 8: # exiting
                    if(unit.offset[1]>0):   # centering onto current tile
                        unit.offset[1] -= 2
                        if(unit.offset[1]==0 and unit.loc[1]==2):
                            unit.dir = 0
                    elif(unit.offset[0]<0): # ^
                        unit.offset[0] += 2
                        if(unit.offset[0]==0 and unit.loc[0]==21):
                            unit.loc[0] = -1
                            unit.loc[1] = -1
                    elif(unit.loc[1]>2):    # walk up
                        unit.offset[1] -= 2
                        if(unit.offset[1]<=-32):
                            unit.offset[1] += 64
                            unit.loc[1] -= 1
                    elif(unit.loc[0]<21):   # walk right off screen
                        unit.offset[0] += 2
                        if(unit.offset[0]>32):
                            unit.offset[0] -= 64
                            unit.loc[0] += 1
            i += 1
        # handle employees
        i = 0
        while(i<len(self.employees)):
            unit = self.employees[i]
            match(unit.job):
                case 0: # take orders
                    match(unit.task):
                        case 0: # wait for a customer to order
                            if(self.mouseXY[0]==7 and self.mouseXY[1]==3 and self.lftClkSt==1):
                                unit.order = 0
                                for c in self.customers:
                                    if(c.task==3 and c.loc[0]==7 and c.loc[1]==4):
                                        unit.order = c.order
                                        break
                                if(unit.order!=0): # make sure we actually got an order from the customer
                                    unit.task += 1
                                else:
                                    i += 1
                                    continue
                                # face the correct way toward the supply item
                                if unit.order in unit.sup_cof or unit.order in unit.sup_tea or unit.order in unit.sup_coco or unit.order in unit.sup_syr:
                                    unit.dir = 2
                                elif unit.order in unit.sup_pas:
                                    unit.dir = 1
                                else:
                                    unit.dir = 3
                        case 1: # grabbing a base ingredient
                            if(unit.offset[0]>0):                   # centering
                                unit.offset[0] -= 2
                                if(unit.offset[0]==0):
                                    if(unit.order in unit.sup_cof and unit.loc[0]==1) or (unit.order in unit.sup_tea and unit.loc[0]==2) or (unit.order in unit.sup_coco and unit.loc[0]==3) or (unit.order in unit.sup_syr and unit.loc[0]==4):
                                        unit.dir = 1
                            elif(unit.offset[1]<0 and unit.dir==3): # ^
                                unit.offset[1] += 2
                                if(unit.offset[1]==0):
                                    if(unit.order in unit.sup_mug and unit.loc[1]==5) or (unit.order in unit.sup_cup and unit.loc[1]==6) or (unit.order in unit.sup_shr and unit.loc[1]==7):
                                        unit.dir = 0
                                        # put object in hand
                                        unit.task += 1
                            elif(unit.offset[1]>0 and unit.dir==1): # ^
                                unit.offset[1] -= 2
                                if(unit.offset[1]==0 and unit.loc[1]==3):
                                    if(unit.order in unit.sup_cof and unit.loc[0]==1) or (unit.order in unit.sup_tea and unit.loc[0]==2) or (unit.order in unit.sup_coco and unit.loc[0]==3) or (unit.order in unit.sup_syr and unit.loc[0]==4) or (unit.order in unit.sup_pas and unit.loc[0]==5):
                                        # put object in hand
                                        unit.task += 1
                            elif(unit.dir==2):                      # moving left
                                unit.offset[0] -= 2
                                if(unit.offset[0]<=32):
                                    unit.offset[0] += 64
                                    unit.loc[0] -= 1
                            elif(unit.dir==1):                      # moving up
                                unit.offset[1] -= 2
                                if(unit.offset[1]<=-32):
                                    unit.offset[1] += 64
                                    unit.loc[1] -= 1
                            elif(unit.dir==3):                      # moving down
                                unit.offset[1] += 2
                                if(unit.offset[1]>=32):
                                    unit.offset[1] -= 64
                                    unit.loc[1] += 1
                        case 2: # placing a base ingredient on the back counter
                            space = -1 # vertical offset from top of shelf, indicating where to place product
                                       # if -1, no space, don't move
                                       # otherwise, location is [0,4+space]
                            if(unit.order in unit.prod_wet):
                                space = self.shelfSpace[0]
                            elif(unit.order in unit.prod_dry):
                                if(self.shelfSpace[1]<0):
                                    space = -1
                                else:
                                    space = self.shelfSpace[1]+3
                            # try to move if there is room to place the product
                            if(space<0):            # move on to next unit, this one cannot do anything this frame
                                i += 1
                                continue
                            if(unit.dir<2):         # turn around and take 1 frame to do so
                                unit.dir += 2
                                i += 1
                                continue
                            if(unit.offset[1]<0):   # centering
                                unit.offset[1] += 2
                                if(unit.offset[1]==0):
                                    if(unit.loc[1]==space+4):
                                        unit.dir = 2
                            elif(unit.offset[0]>0): # ^
                                unit.offset[0] -= 2
                                if(unit.offset[0]==0):
                                    if(unit.loc[0]==1):     # we are in front of the space to place the product
                                        # place product
                                        # update shelf space
                                        if(unit.order in unit.prod_wet):
                                            self.shelfSpace[0] += 1
                                            if(self.shelfSpace[0]>2):
                                                self.shelfSpace[0] = -1
                                        elif(unit.order in unit.prod_dry):
                                            self.shelfSpace[1] += 1
                                            if(self.shelfSpace[1]>1):
                                                self.shelfSpace[1] = -1
                                        # inform other employee of order
                                        self.prod_order.append(unit.order)
                                        unit.task += 1
                                        unit.dir = 1
                                        if(unit.loc[1]==4):
                                            unit.dir = 0
                                    elif(unit.loc[1]==3):   # double check that we are in front of the correct product location
                                        if(unit.loc[1]!=space+4):
                                            unit.dir = 3
                            elif(unit.dir==2):      # walk left
                                unit.offset[0] -= 2
                                if(unit.offset[0]<=-32):
                                    unit.offset[0] += 64
                                    unit.loc[0] -= 1
                            elif(unit.dir==3):      # walk down
                                unit.offset[1] += 2
                                if(unit.offset[1]>=32):
                                    unit.offset[1] -= 64
                                    unit.loc[1] += 1
                        case 3: # return to take order
                            if(unit.offset[1]>0):   # centering
                                unit.offset[1] -= 2
                                if(unit.offset[1]==0 and unit.loc[1]==4):
                                    unit.dir = 0
                            elif(unit.offset[0]<0): # ^
                                unit.offset[0] += 2
                                if(unit.offset[0]==0 and unit.loc[0]==5):
                                    unit.task = 0
                            elif(unit.dir==1):      # move up
                                unit.offset[1] -= 2
                                if(unit.offset[1]<=-32):
                                    unit.offset[1] += 64
                                    unit.loc[1] -= 1
                            elif(unit.dir==0):      # move right
                                unit.offset[0] += 2
                                if(unit.offset[0]>=32):
                                    unit.offset[0] -= 64
                                    unit.loc[0] += 1
                case 1: # give orders
                    pass
                case 2: # clean tables
                    pass
            i += 1
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
        self.mouseXY = [int(MouseXY[0]/(16*SCALE)),int(MouseXY[1]/(16*SCALE))] #scale down to the 20x12 grid of the simulation (first and last 16x are offscreen and ignored)
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
        # coffeeshop
        surface.blit(self.floorPlan, [0,0])
        #customers
        custs = [[self.cust11,self.cust12,self.cust13,self.cust14],[self.cust21,self.cust22,self.cust23,self.cust24],[self.cust31,self.cust32,self.cust33,self.cust34],[self.cust41,self.cust42,self.cust43,self.cust44]]
        i = len(self.customers)-1 # draw customers newest to oldest so that oldest customers show up on top
        while(i>-1):
            unit = self.customers[i]
            surface.blit(custs[unit.ID][unit.dir],[unit.loc[0]*16*SCALE+unit.offset[0],unit.loc[1]*16*SCALE+unit.offset[1]])
            i -= 1
        # employees
        emps = [[self.emp11,self.emp12,self.emp13,self.emp14],[self.emp21,self.emp22,self.emp23,self.emp24],[self.emp31,self.emp32,self.emp33,self.emp34],[self.emp41,self.emp42,self.emp43,self.emp44]]
        for unit in self.employees:
            surface.blit(emps[unit.ID][unit.dir],[unit.loc[0]*16*SCALE+unit.offset[0],unit.loc[1]*16*SCALE+unit.offset[1]])
# -------- Main Program Loop -----------
def main():                                             #every program should have a main function
                                                        #other functions go above main
    # local  variables
    data = Accuracy_Data()              # create class objects
    progressBar = Progress_Manager()
    settings = Settings()
    sim = Sim()
    mouseXY = [0,0]
    mouseDown = False
    
    dataState = 0 # indicate data has not started processing yet
    
    salesDataThread = threading.Thread(target=data.readSalesData, args=(settings,progressBar,))   # DO NOT INCLUDE PARENTHESIS ON TARGET FUNCTION    # ARGS MUST BE ITERABLE, INCLUDE EXTRA COMMA FOR ONLY 1 ARG
    supplyDataThread = threading.Thread(target=data.readSupplyData, args=(settings,progressBar,))
    
    # image files
    logo = pygame.image.load("assets/logo.png").convert_alpha(surface)
    logoFrame = 0.0
    
    while (True):
        mouseXY = pygame.mouse.get_pos()
        mouseDown = pygame.mouse.get_pressed()[0]
        for event in pygame.event.get():                #captures state of the game - loops thru changes
            
            if ( event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): #end game
                pygame.quit()
                sys.exit()
        
            # button, mouse, or keyboard interaction here
            if(logoFrame<120 and (event.type==pygame.MOUSEBUTTONDOWN or event.type==pygame.KEYDOWN)): # skip intro logo
                logoFrame = 120
        
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
            #print(settings)
            #print(data)
            dataState += 1
            # return
        # intro logo logic
        if(dataState>0 and logoFrame<=180):
            logoFrame += 1
        #set background color
        surface.fill(BLACK)
        
        # drawing code goes here
        if(logoFrame<=60):
            logo.set_alpha(int(255.0*logoFrame/60.0))
        if(logoFrame>60 and logoFrame<=120):
            logo.set_alpha(255)
        if(logoFrame>120 and logoFrame<=180):
            logo.set_alpha(255 - int(255.0*(logoFrame-120)/60.0) )
        if(logoFrame<=180):
            surface.blit(logo, [(W-640)/2,(H-640)/2])
        else:
            sim.storeInputs(mouseXY,mouseDown)
            sim.demoSim()
            #progressBar.displayProgress(W/16, H*6/13, W*7/8, H/13, 5, WHITE, GREEN)
        
        
        pygame.display.update()                          #updates the screen
        clock.tick(60)                                  # FPS for animation (lower number to slow)
        
#----------------------------------------------------------------
main()                                                   #runs the game