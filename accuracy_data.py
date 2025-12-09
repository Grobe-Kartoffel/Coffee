import random

class Accuracy_Data:
    def __init__(self):
        self.ids = []
        self.probabilitySpaces = []  # 7x15 (day of week/hour of day) matrix containing the probability of an item ordered at that time on that day, being that product
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
            while(prodIndex < len(self.ids)):
                if(self.ids[prodIndex]==product): # we found a matching entry
                    # price and product details only change once
                    # quantity is the only value that will need updated with every entry
                    self.probabilitySpaces[prodIndex][weekDay][hour] += quantity
                    break
                prodIndex += 1
            if(prodIndex>=len(self.ids)): # we have a new product that we have not read before
                settings.addProd(product,desc,price)
                self.probabilitySpaces.append( [[0.0]*15]*7 ) # 7 days in a week, 15 hours a day (6am - 9pm)
                self.ids.append(product)
            # update progress bar
            progressBar.update( float(x+1)/float(len(lines)) )
        # always close files after using them
        salesFile.close()
        
        # need to retroactively add chili mayan hot chocolate Rg and Lg because it is missing from the data
        # ratios of the popularities of chili mayan chocolate powder to other chocolate powders will be used to extrapolate chili mayan hot chocolate popularity from other hot chocolate drinks
        
        # initialize Chili Mayan Hot Chocolate Rg
        settings.addProd(62,"Drinking Chocolate|Hot chocolate|Chili Mayan Rg",4.75)
        self.probabilitySpaces.append( [[0.0]*15]*7 )
        self.ids.append(62)
        
        # initialize Chili Mayan Hot Chocolate Lg
        settings.addProd(63,"Drinking Chocolate|Hot chocolate|Chili Mayan Lg",6.25)
        self.probabilitySpaces.append( [[0.0]*15]*7 )
        self.ids.append(63)
        
        # vars needed for extrapolation
        darkPowIndex,organicPowIndex,chiliPowIndex = 0,0,0
        darkRgIndex,darkLgIndex = 0,0
        organicRgIndex,organicLgIndex = 0,0
        chiliRgIndex,chiliLgIndex = 0,0
        darkRatio,organicRatio = 0.0,0.0
        darkValue,organicValue,chiliValue = 0.0,0.0,0.0
        
        # find indexes
        prodIndex = 0
        while(prodIndex < len(self.ids)):
            match(self.ids[prodIndex]):
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
                for prod in range(len(self.ids)):
                    total += self.probabilitySpaces[prod][day][hour]
                for prod in range(len(self.ids)):
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
            while( i < len(line)-1):
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
            supIndex = 0 # the supply might already exist, so we need to search through the list for it first
            while(supIndex < len(settings.Supplies)):
                if(settings.Supplies[supIndex].ID==supply): # we found a matching entry
                    if(supplyAmt==1): # update price if we have an exact conversion on this line
                        settings.setSupPrice(supply,supplyAmtPrice)
                    break
                supIndex += 1
            if(supIndex==len(settings.Supplies)): # we have a new supply that we have not read before
                settings.addSup(supply)
                if(supplyAmt==1):
                    settings.setSupPrice(supply,supplyAmtPrice)
            # set the supply description
            if(supply==84):
                settings.setSupDesc(supply,"Cup Sm")
            elif(supply==85):
                settings.setSupDesc(supply,"Cup Rg")
            elif(supply==86):
                settings.setSupDesc(supply,"Cup Lg")
            else:
                prodIndex = 0
                while(prodIndex < len(self.ids)):
                    if(settings.Products[prodIndex].ID==supply):
                        settings.setSupDesc(supply,settings.Products[prodIndex].name)
                        break
                    prodIndex += 1
            # we should have handled the supply entry
            # now we need to update the related product entry
            settings.addProdSup(product,supply,supplyAmt)
            # update progress bar
            progressBar.update( float(x+1)/float(len(lines)) )
        # always close files after using them
        salesFile.close()
        return
    def getRndProd(self,hour):
        #return 58 # hot chocolate, placeholder for now
        # don't need to worry about the day, because all days are equal
        # look at self.probabilitySpaces[i][0][hour]
        # each cell contains the decimal representing a fraction of all orders that day
        # pick a random decimal from 0.0000 to 1.0000
        # sequencially subtract each product's decimal from the number
        # once we are <= zero, we found our product
        pick = random.random() # random decimal between 0,1
        i = 0
        while(i<len(self.ids)):
            pick -= self.probabilitySpaces[i][0][hour]
            if(pick<=0 or i==len(self.ids)-1): # break before i can be incremented past the valid range
                break
            i += 1
        return self.ids[i]