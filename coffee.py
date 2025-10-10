import math, random, pygame, sys, threading
pygame.init()                                           #initialize game engine

W=800                                                   #set window size
H=640
size=(W,H)
surface = pygame.display.set_mode(size)

pygame.display.set_caption("Coffee Shop Simulator")          # window title

#declare global variables here

BLACK    =  (   0,   0,   0)                             #Color Constants
WHITE    =  ( 255, 255, 255)
GREEN    =  (   0, 255,   0)
LGREEN   =  ( 128, 255, 128)
RED      =  ( 255,   0,   0)
BLUE     =  (   0,   0, 255)


#other global variables (WARNING: use sparingly):


clock = pygame.time.Clock()                            # Manage timing for screen updates

#Program helper functions:

class Progress_Manager: # manages a progress bar for when Accuracy Data is reading a file, so the rest of the game can continue running
    Max = 1.0
    Value = 0.0
    lock = threading.Lock()
    def __init(self):
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
    products = []       # product ID and description for each product
    prodSupplies = []   # list of supplies needed for each product
    prodSupplyAmt = []  # list of supply amounts needed for each product
    prodPrices = []     # price of each product
    probabilitySpaces = []  # 7x13 (day of week/hour of day) matrix containing the probability of an item ordered at that time on that day, being that product
    supplies = []       # supply ID and description for each supply
    supPrices = []      # price of each supply
    progress = 0.0
    def __init__(self):
        self.products = []       # product ID and description for each product
        self.prodSupplies = []   # list of supplies needed for each product
        self.prodSupplyAmt = []  # list of supply amounts needed for each product
        self.prodPrices = []     # price of each product
        self.probabilitySpaces = []  # 7x13 (day of week/hour of day) matrix containing the probability of an item ordered at that time on that day, being that product
        self.supplies = []       # supply ID and description for each supply
        self.supPrices = []      # price of each supply        
        self.progress = 0.0
    def __str__(self):
        string = ""
        i = 0
        while(i<len(self.products)):
            string += f"ID:\t\t{self.products[i][0]}\nDesc:\t\t{self.products[i][1]}\n" # product ID and Description
            j = 0
            string += "Supplies:\t"                                                     # supplies
            while(j<len(self.prodSupplies[i])):
                string += self.prodSupplies[i][j]
                if(j<len(self.prodSupplies[i])-1):
                    string += ", "
                j += 1
            string += "\n"
            string += f"Price:\t\t{self.prodPrices[i]}\n"                                   # price
            j = 0
            string += "ProbabilitySpace:\n"
            while(j<len(self.probabilitySpaces[i])):                                    # probability space
                string += "["
                k = 0                
                while(k<len(self.probabilitySpaces[i][j])):
                    string += f"{self.probabilitySpaces[i][j][k]}"
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
    def readSalesData(self,progressBar):
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
        self.progress = 0.0     # reset progress
        
        filename = "SalesData_Sorted.csv"
        try: # make sure the file exists before we start reading
            salesFile = open(filename, "r")
            salesFile.close()
        except:
            print("ERROR: SalesData.csv could not be found. Aborting processing.")
            return False
        
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
            #if(x>=2500):   # limit loop while testing so the size of the data does not break it
            #    break;
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
            while(prodIndex < len(self.products)):
                if(self.products[prodIndex][0]==product): # we found a matching entry
                    # price and product details only change once
                    # quantity is the only value that will need updated with every entry
                    self.probabilitySpaces[prodIndex][weekDay][hour] += quantity
                    break
                prodIndex += 1
            if(prodIndex==len(self.products)): # we have a new product that we have not read before
                self.products.append([product,desc])
                self.prodSupplies.append([]) # this file does not have supply data, append an empty list as a placeholder
                self.prodSupplyAmt.append([])
                self.prodPrices.append(price)
                self.probabilitySpaces.append( [[0]*15]*7 ) # 7 days in a week, 15 hours a day (6am - 9pm)
            # update progress bar
            self.progress = float(x+1)/float(len(lines))
            progressBar.update(self.progress)
        # always close files after using them
        salesFile.close()
        
        # need to retroactively add chili mayan hot chocolate Rg and Lg because it is missing from the data
        # ratios of the popularities of chili mayan chocolate powder to other chocolate powders will be used to extrapolate chili mayan hot chocolate popularity from other hot chocolate drinks
        
        # initialize Chili Mayan Hot Chocolate Rg
        self.products.append([62,"Drinking Chocolate|Hot chocolate|Chili Mayan Rg"])
        self.prodSupplies.append([])
        self.prodSupplyAmt.append([])
        self.prodPrices.append(4.75)
        self.probabilitySpaces.append( [[0]*15]*7 )
        
        # initialize Chili Mayan Hot Chocolate Lg
        self.products.append([63,"Drinking Chocolate|Hot chocolate|Chili Mayan Lg"])
        self.prodSupplies.append([])
        self.prodSupplyAmt.append([])
        self.prodPrices.append(6.25)
        self.probabilitySpaces.append( [[0]*15]*7 )
        
        # vars needed for extrapolation
        darkPowIndex,organicPowIndex,chiliPowIndex = 0,0,0
        darkRgIndex,darkLgIndex = 0,0
        organicRgIndex,organicLgIndex = 0,0
        chiliRgIndex,chiliLgIndex = 0,0
        darkRatio,organicRatio = 0.0,0.0
        darkValue,organicValue,chiliValue = 0.0,0.0,0.0
        
        # find indexes
        prodIndex = 0
        while(prodIndex < len(self.products)):
            match(self.products[prodIndex][0]):
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
    def readSupplyData(self,progressBar):
        return 42

# -------- Main Program Loop -----------
def main():                                             #every program should have a main function
                                                        #other functions go above main
    # local  variables
    data = Accuracy_Data()              # create class objects
    progressBar = Progress_Manager()
    
    dataRead = False
    
    salesDataThread = threading.Thread(target=data.readSalesData, args=(progressBar,))   # DO NOT INCLUDE PARENTHESIS ON TARGET FUNCTION    # ARGS MUST BE ITERABLE, INCLUDE EXTRA COMMA FOR ONLY 1 ARG
    supplyDataThread = threading.Thread(target=data.readSupplyData, args=(progressBar,))
    #thread.start()   
    
    while (True):
        
        for event in pygame.event.get():                #captures state of the game - loops thru changes
            
            if ( event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): #end game
                pygame.quit()
                sys.exit()
        
            # button, mouse, or keyboard interaction here
        
        # ongoing game logic here  (repeats every 1/60 second)
        if(data.progress==0.0 and not dataRead):
            salesDataThread.start()
        if(data.progress>=1.0 and not dataRead):
            salesDataThread.join()
            return                  # remove this once supplyData is written
            data.progress = 0.0
            supplyDataThread.start()
            dataRead = True
        if(data.progress>=1.0 and dataRead):
            supplyDataThread.join()
        
      
        surface.fill(BLACK)                             #set background color
        
        # drawing code goes here
        progressBar.displayProgress(W/16, H*6/13, W*7/8, H/13, 5, WHITE, GREEN)
        
        
        pygame.display.update()                          #updates the screen
        clock.tick(60)                                  # FPS for animation (lower number to slow)
        
#----------------------------------------------------------------
main()                                                   #runs the game