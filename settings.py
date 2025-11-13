import threading

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