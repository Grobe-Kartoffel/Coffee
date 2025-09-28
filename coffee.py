import math, random, pygame, sys
pygame.init()                                           #initialize game engine

w=800                                                   #set window size
h=640
size=(w,h)
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



class Accuracy_Data:
    products = []   # product ID and description for each product
    supplies = []   # list of supplies needed for each product
    prices = []     # price of each product
    probabilitySpaces = []  # 7x13 (day of week/hour of day) matrix containing the probability of an item ordered at that time on that day, being that product
    
    # ----- These Are Python Constructors
    # def __new__(cls,parameters):
    #     instance = super(Accuracy_Data, cls).__new__(cls)
    #     return instance
    def __init__(self):
        self.products = []   # product ID and description for each product
        self.supplies = []   # list of supplies needed for each product
        self.prices = []     # price of each product
        self.probabilitySpaces = []  # 7x13 (day of week/hour of day) matrix containing the probability of an item ordered at that time on that day, being that product        
    
    def readSalesData(arg):
        date = ""
        weekDay = 0     # note that the Data begins on January 1st, 2023, which is a Sunday
                        # note that we will be keeping track of this internally as it is not in the data
        hour = 0        # note that we will be subtracting 7 from the hour in the data as the store opens at 7am
        quantity = 0
        product = 0
        price = 0.0
        desc = ""
        
        lines = []
        dataLoc = 0     # indicates which piece of data we are in, within a line
        try:
            salesFile = open("SalesData.csv", "r") # read the file
            salesFile.close()
        except:
            salesFile = open("SalesData.csv","w")  # write the file, just so it exists
            salesFile.close()
        
        salesFile = open("SalesData.csv", "r")     # read the file
        lines = salesFile.readlines()              # this returns a list with every line of text in it
        
        for x in range(len(lines)): # iterate through each line in the data
            dataLoc = 0
            i = 0
            quantity = 0
            product = 0
            price = 0
            desc = ""
            line = lines[x]
            if(x==0):
                continue
            if(x>=100):     # limit loop while testing so the size of the data does not break it
                break;
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
                        hour = int(line[i])*10 + int(line[i+1]) - 7
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
            prodIndex = 0
            while(prodIndex < len(Accuracy_Data.products)):
                if(Accuracy_Data.products[prodIndex][0]==product):
                    # price and product details only change once
                    # quantity is the only value that will need updated with every entry
                    Accuracy_Data.probabilitySpaces[prodIndex][weekDay][hour] += quantity
                    break
                prodIndex += 1
            if(prodIndex==len(Accuracy_Data.products)): # we have a new product that we have not read before
                Accuracy_Data.products.append([product,desc])
                Accuracy_Data.supplies.append([])
                Accuracy_Data.prices.append(price)
                Accuracy_Data.probabilitySpaces.append( [[0]*13]*7 ) # 7 days in a week, 13 hours a day
        salesFile.close()
        
# -------- Main Program Loop -----------
def main():                                             #every program should have a main function
                                                        #other functions go above main
    # local  variables
    data = Accuracy_Data()
    data.readSalesData()

    
    while (True):
        
        for event in pygame.event.get():                #captures state of the game - loops thru changes
            
            if ( event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): #end game
                pygame.quit()
                sys.exit()
        
            # button, mouse, or keyboard interaction here
        
        # ongoing game logic here  (repeats every 1/60 second)
        
        
        
      
        surface.fill(GREEN)                             #set background color
        
        #drawing code goes here
        
        
        
        
        
        pygame.display.update()                          #updates the screen-
        clock.tick(60)                                  # FPS for animation (lower number to slow)
        
        
#----------------------------------------------------------------
main()                                                   #runs the game