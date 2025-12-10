import threading, pygame
from typing import Callable, Tuple, Dict

class Settings:
    def __init__(self,SCALE):
        self.Products = []
        self.Supplies = []
        self.money = 100.0
        self.mouseXY = [0,0]
        self.prevMouseXY = [0,0]
        self.lftClkSt = 0
        self.supplyScroll = 0.0
        self.productScroll = 0.0
        self.supplySelect = -1
        self.productSelect = -1
        self.scrollSelect = False
        self.supplySliderSelect = -1
        self.productSliderSelect = -1
        self.lock = threading.Lock()
        # image files
        self.SCALE = SCALE
        # list elements
        self.itemHigh = pygame.image.load("assets/graphics/list_item_1.png").convert_alpha()
        self.itemHigh = pygame.transform.scale_by(self.itemHigh,SCALE)
        self.itemLow = pygame.image.load("assets/graphics/list_item_2.png").convert_alpha()
        self.itemLow = pygame.transform.scale_by(self.itemLow,SCALE)
        self.scrlBarLow = pygame.image.load("assets/graphics/scrl_bar_1.png").convert_alpha()
        self.scrlBarLow = pygame.transform.scale_by(self.scrlBarLow,SCALE)
        self.scrlBarHigh = pygame.image.load("assets/graphics/scrl_bar_2.png").convert_alpha()
        self.scrlBarHigh = pygame.transform.scale_by(self.scrlBarHigh,SCALE)
        self.sldrKnbLow = pygame.image.load("assets/graphics/sldr_knb_1.png").convert_alpha()
        self.sldrKnbLow = pygame.transform.scale_by(self.sldrKnbLow,SCALE)
        self.sldrKnbHigh = pygame.image.load("assets/graphics/sldr_knb_2.png").convert_alpha()
        self.sldrKnbHigh = pygame.transform.scale_by(self.sldrKnbHigh,SCALE)
        # objects
        self.bttl = pygame.image.load("assets/graphics/bttl.png").convert_alpha()
        self.bttl = pygame.transform.scale_by(self.bttl,SCALE)
        self.chk_pwd = pygame.image.load("assets/graphics/chk_pwd.png").convert_alpha()
        self.chk_pwd = pygame.transform.scale_by(self.chk_pwd,SCALE)
        self.cof_bn = pygame.image.load("assets/graphics/cof_bn.png").convert_alpha()
        self.cof_bn = pygame.transform.scale_by(self.cof_bn,SCALE)
        self.cup_lg1 = pygame.image.load("assets/graphics/cup_lg_1.png").convert_alpha()
        self.cup_lg1 = pygame.transform.scale_by(self.cup_lg1,SCALE)
        self.cup_lg2 = pygame.image.load("assets/graphics/cup_lg_2.png").convert_alpha()
        self.cup_lg2 = pygame.transform.scale_by(self.cup_lg2,SCALE)
        self.cup_rg1 = pygame.image.load("assets/graphics/cup_rg_1.png").convert_alpha()
        self.cup_rg1 = pygame.transform.scale_by(self.cup_rg1,SCALE)
        self.cup_rg2 = pygame.image.load("assets/graphics/cup_rg_2.png").convert_alpha()
        self.cup_rg2 = pygame.transform.scale_by(self.cup_rg2,SCALE)
        self.cup_sm1 = pygame.image.load("assets/graphics/cup_sm_1.png").convert_alpha()
        self.cup_sm1 = pygame.transform.scale_by(self.cup_sm1,SCALE)
        self.cup_sm2 = pygame.image.load("assets/graphics/cup_sm_2.png").convert_alpha()
        self.cup_sm2 = pygame.transform.scale_by(self.cup_sm2,SCALE)
        self.mug = pygame.image.load("assets/graphics/mug.png").convert_alpha()
        self.mug = pygame.transform.scale_by(self.mug,SCALE)
        self.pstry = pygame.image.load("assets/graphics/pstry.png").convert_alpha()
        self.pstry = pygame.transform.scale_by(self.pstry,SCALE)
        self.shrt = pygame.image.load("assets/graphics/shrt.png").convert_alpha()
        self.shrt = pygame.transform.scale_by(self.shrt,SCALE)
        self.syrp = pygame.image.load("assets/graphics/syrp.png").convert_alpha()
        self.syrp = pygame.transform.scale_by(self.syrp,SCALE)
        self.tea_lvs = pygame.image.load("assets/graphics/tea_lvs.png").convert_alpha()
        self.tea_lvs = pygame.transform.scale_by(self.tea_lvs,SCALE)
        # object ID lists
        # Lists containing the orders that require each of the supply types so that emp1 knows where to get the proper supply item:
        self.sup_cof  = [1,2,3,4,5,6,7,8,9,10,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,87]    # coffee beans
        self.sup_tea  = [11,12,13,14,15,16,17,18,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57]                # tea leaves
        self.sup_coco = [19,20,21,58,59,60,61,62,63]                                                             # cocoa powders
        self.sup_syr  = [64,65,66,67]                                                                            # syrups
        self.sup_pas  = [69,70,71,72,73,74,75,76,77,78,79]                                                       # pastries
        self.sup_mug  = [82]                                                                                     # mugs
        self.sup_cup  = [83]                                                                                     # cups
        self.sup_shr  = [81]                                                                                     # shirts
        self.prod_wet = [22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,87]
        self.prod_dry = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,64,65,66,67,69,70,71,72,73,74,75,76,77,78,79,81,82,83]
        self.prod_sm  = [22,25,28,31,34,37,38,87]
        self.prod_rg  = [23,26,29,32,35,39,40,42,44,46,48,50,52,54,56,58,60,62]
        self.prod_lg  = [24,27,30,33,36,41,43,45,47,49,51,53,55,57,59,61,63]        
    def __str__(self):
        string = "Supplies:\n"
        for s in self.Supplies:
            string += f"{s.ID:d}, {s.name:s}, {s.price:.2f}, {s.amt:.2f}, {s.goalAmt:.2f}\n"
        string += "\nProducts:\n"
        for p in self.Products:
            string += f"{p.ID:d}, {p.name:s}, {p.price:.2f}\n"
        return string
    class Supply:
        def __init__(self,ID):
            self.ID = ID
            self.name = ""
            self.price = 0.0
            self.amt = 0.0
            self.goalAmt = 0.0
    class Product:
        def __init__(self,ID,name):
            self.ID = ID
            self.name = name
            self.price = 0.0
            self.supplies = []
            self.supAmts = []
    def addProd(self,ID,name,price):
        with self.lock:
            self.Products.append(self.Product(ID,name))
            self.Products[len(self.Products)-1].price = price
    def addSup(self,ID):
        with self.lock:
            self.Supplies.append(self.Supply(ID)) 
            self.Supplies[len(self.Supplies)-1].amt = 100.0
            self.Supplies[len(self.Supplies)-1].goalAmt = 100.0
    def addProdSup(self,prodID,supID,supAmt):
        with self.lock:
            i = 0
            while(i<len(self.Products) and self.Products[i].ID!=prodID):
                i += 1
            if(i>=len(self.Products)):
                return
            self.Products[i].supplies.append(supID)
            self.Products[i].supAmts.append(supAmt)
    def setSupPrice(self,ID,price):
        with self.lock:
            i = 0
            while(i<len(self.Supplies) and self.Supplies[i].ID!=ID):
                i += 1
            if(i>=len(self.Supplies)):
                return
            self.Supplies[i].price = price
    def setSupDesc(self,ID,name):
        with self.lock:
            i = 0
            while(i<len(self.Supplies) and self.Supplies[i].ID!=ID):
                i += 1
            if(i>=len(self.Supplies)):
                return
            self.Supplies[i].name = name
        return
    def getSups(self): # return list of ID's+Names
        sups = []
        for s in self.Supplies:
            sups.append([s.ID,s.name])
        return sups
    def getSupPrice(self,ID):
        i = 0
        while(i<len(self.Supplies) and self.Supplies[i].ID!=ID):
            i += 1
        if(i>=len(self.Supplies)): # if we didn't find the supply, return a price of 0
            return 0.0
        return self.Supplies[i].price
    def getSupAmt(self,ID):
        i = 0
        while(i<len(self.Supplies) and self.Supplies[i].ID!=ID):
            i += 1
        if(i>=len(self.Supplies)): # if we didn't find the supply, return an amount of 0
            return 0.0
        return self.Supplies[i].amt        
    def getSupGoal(self,ID):
        i = 0
        while(i<len(self.Supplies) and self.Supplies[i].ID!=ID):
            i += 1
        if(i>=len(self.Supplies)): # if we didn't find the supply, return a goalAmount of 0
            return 0.0
        return self.Supplies[i].goalAmt        
    def getProds(self): # return list of ID's+Names
        prods = []
        for p in self.Products:
            prods.append([p.ID,p.name])
        return prods
    def getProdPrice(self,ID):
        i = 0
        while(i<len(self.Products) and self.Products[i].ID!=ID):
            i += 1
        if(i>=len(self.Products)): # if we didn't find the supply, return a price of 0
            return 0.0
        return self.Products[i].price        
    def getProdSupCost(self,ID): # return total cost of all supplies and their amounts that go into the product
        i = 0
        cost = 0.0
        while(i<len(self.Products) and self.Products[i].ID!=ID):
            i += 1
        if(i>=len(self.Products)): # if we didn't find the supply, return a price of 0
            return 0.0
        j = 0
        while(j<len(self.Products[i].supplies) and j<len(self.Products[i].supAmts)):
            sCost = 0.0
            k = 0
            # get the price of the supply
            while(k<len(self.Supplies) and self.Supplies[k].ID!=self.Products[i].supplies[j]):
                k += 1
            if(k>=len(self.Supplies)):
                j += 1
                continue
            sCost = self.Supplies[k].price
            # multiply the price by the amount
            sCost *= self.Products[i].supAmts[j]
            # add to total cost
            cost += sCost
            # increment J
            j += 1
        return cost
    def storeInputs(self,MouseXY,lftClk): # Takes user input and converts them into a better format for the Sim to use
        self.prevMouseXY = self.mouseXY
        self.mouseXY = MouseXY
        if(self.lftClkSt==0 and lftClk): # mouse was clicked
            self.lftClkSt = 1
            # check if scroll bar was clicked
            if(self.mouseXY[0]>=154*self.SCALE and self.mouseXY[0]<158*self.SCALE and self.mouseXY[1]>=20*self.SCALE and self.mouseXY[1]<176*self.SCALE):
                self.scrollSelect = True
            # check if list element was clicked
            if(self.mouseXY[0]<4*self.SCALE or self.mouseXY[0]>159*self.SCALE or self.mouseXY[1]<20*self.SCALE or self.mouseXY[1]>176*self.SCALE):
                self.supplySelect = -1
                self.productSelect = -1
                self.supplySliderSelect = -1
                self.productSliderSelect = -1
            else: # something was clicked, we need to figure out what, it's easiest to do this for both supplies and products
                # as the list is scrolled up, the mouse should be offset down
                # then, the mouse height, minus twenty, should be integer divided by 17 to find the index of the element to be selected
                # then, the mouse height, minus twenty, should be modulus divided by 17, and if the height is between 9 and 15, then we should check the width to see if the slider knob was clicked
                # code for supply list
                h = self.mouseXY[1]/self.SCALE - (138 - 17*(len(self.Supplies)-1) )*self.supplyScroll # the offset equation is without scaling, so the mouse location needs to have the scale removed as well
                hi = int(float(h-20)/17.0)
                hm = int(h-20)%17
                self.supplySelect = self.Supplies[hi].ID
                # reverse engineer the location of the slider and see if the mouse width is within 6*SCALE units of it
                w = (27+108*(self.Supplies[hi].goalAmt/200))*self.SCALE
                if(hm>=9 and hm<=15 and self.mouseXY[0]>=w and self.mouseXY[0]<=w+6*self.SCALE): # the slider was potentially clicked
                    self.supplySliderSelect = self.Supplies[hi].ID
                else:
                    self.supplySliderSelect = -1
                # code for product list
                h = self.mouseXY[1]/self.SCALE - (138 - 17*(len(self.Supplies)-1) )*self.productScroll # the offset equation is without scaling, so the mouse location needs to have the scale removed as well
                hi = int(float(h-20)/17.0)
                hm = int(h-20)%17
                self.productSelect = self.Products[hi].ID     
                # reverse engineer the location of the slider and see if the mouse width is within 6*SCALE units of it
                w = (27+108*(self.Products[hi].price/50.0))*self.SCALE                
                if(hm>=9 and hm<=15 and self.mouseXY[0]>=w and self.mouseXY[0]<=w+6*self.SCALE): # the slider was potentially clicked
                    self.productSliderSelect = self.Products[hi].ID
                else:
                    self.productSliderSelect = -1                
                
            return
        if(self.lftClkSt==1 and lftClk): # mouse is held down
            self.lftClkSt = 2
            return
        if(self.lftClkSt>0 and not lftClk): # mouse was unclicked
            self.lftClkSt = 0
            self.scrollSelect = False
            self.supplySliderSelect = -1
            self.productSliderSelect = -1
            return    
    def resetObjects(self):
        self.money = 100.0
        for s in self.Supplies:
            s.amt = 100.0
            s.goalAmt = 100.0
    def resetMenus(self):
        self.supplyScroll = 0.0
        self.productScroll = 0.0
        self.supplySelect = -1
        self.productSelect = -1
        self.supplySliderSelect = -1
        self.productSliderSelect = -1
    def getObjImage(self,ID):
        img = None
        if(ID==81):
            img = self.shrt
        elif(ID==82):
            img = self.mug
        elif(ID==83):
            img = self.bttl
        elif(ID==84):
            img = self.cup_sm1
        elif(ID==85):
            img = self.cup_rg1
        elif(ID==86):
            img = self.cup_lg1
        elif(ID in self.sup_pas):
            img = self.pstry
        elif(ID in self.sup_syr):
            img = self.syrp
        elif(ID in self.prod_sm):
            img = self.cup_sm2
        elif(ID in self.prod_rg):
            img = self.cup_rg2
        elif(ID in self.prod_lg):
            img = self.cup_lg2
        elif(ID in self.sup_cof):
            img = self.cof_bn
        elif(ID in self.sup_tea):
            img = self.tea_lvs
        elif(ID in self.sup_coco):
            img = self.chk_pwd
        else:                            # this obj should only show up on the value sliders, if it shows up as an icon, we know something is wrong
            img = self.sldrKnbHigh
        return img        
    def displaySupplyMenu(self,surface):
        # highest the scroll bar can be drawn is (154,20)*SCALE
        # lowest it can be drawn is (154,160)*SCALE
        if(self.scrollSelect):
            # also make sure mouse does not push scroll bar from afar if it goes out of bounds            
            h = float(20.0+140.0*self.supplyScroll) + ( ((self.mouseXY[1]-self.prevMouseXY[1])/self.SCALE) if (self.mouseXY[1]>=20*self.SCALE and self.mouseXY[1]<=176*self.SCALE) else 0)
            self.supplyScroll = (h-20.0)/140.0
            if(self.supplyScroll<0):
                self.supplyScroll = 0.0
            if(self.supplyScroll>1):
                self.supplyScroll = 1.0
            surface.blit(self.scrlBarHigh,(154*self.SCALE,(20+140*self.supplyScroll)*self.SCALE))
        else:
            surface.blit(self.scrlBarLow,(154*self.SCALE,(20+140*self.supplyScroll)*self.SCALE))
        # the first list element should be drawn at (5,21)*SCALE
        # the height of each element is 16*SCALE
        # there should be a 1*SCALE spacing between elements
        # each element should be drawn at (5,21+17i)*SCALE where i starts and 0 and increments +1 per element
        # the scroll bar should modify the height so that the last element is drawn at (5,159)*SCALE when the scroll bar is at the bottom
        # height of the final element before scrolling is 21 + 17*(len(self.Supplies)-1)
        # height of the final element after scrolling should be 159
        # the difference is -138 + 17*(len(self.Supplies)-1)        
        # each element should be drawn at (5,21 + 17*i + (138 - 17*(len(self.Supplies)-1) )*self.supplyScroll )
        # if the height is less then 20 or greater than 160, the element should not be drawn
        i = 0
        font = pygame.font.SysFont(None,36)
        while(i<len(self.Supplies)):
            h = 21 + 17*i + (138 - 17*(len(self.Supplies)-1) )*self.supplyScroll
            if(h<20 or h>160):
                i += 1
                continue
            if(self.supplySelect==self.Supplies[i].ID):
                surface.blit(self.itemHigh, (5*self.SCALE, h*self.SCALE ))
            else:
                surface.blit(self.itemLow, (5*self.SCALE, h*self.SCALE ))
            # icons should be displayed at (7,24)*SCALE, plus the height offset of the element it cooresponds to
            img = self.getObjImage(self.Supplies[i].ID)
            surface.blit(img, (7*self.SCALE, (h+3)*self.SCALE ))
            # the slider knob should be displayed at height 30*SCALE plus the height offset of the element it cooresponds to
            # the slider knob should be displayed at width (27 + 108*Value/Max)*SCALE
            if(self.supplySliderSelect==self.Supplies[i].ID):
                # find the new location based on how much the mouse dragged
                # also make sure mouse does not push knob from afar if it goes out of bounds
                w = (27+108*(self.Supplies[i].goalAmt/200))*self.SCALE + ((self.mouseXY[0]-self.prevMouseXY[0]) if (self.mouseXY[0]>=27*self.SCALE and self.mouseXY[0]<=141*self.SCALE) else 0 )
                # don't let it go out of bounds
                if(w<27*self.SCALE):
                    w = 27*self.SCALE
                if(w>135*self.SCALE):
                    w = 135*self.SCALE
                # reverse engineer the new price
                self.Supplies[i].goalAmt = (((w/self.SCALE)-27)/108)*200
                # display the knob                
                surface.blit(self.sldrKnbHigh, ((27+108*(self.Supplies[i].goalAmt/200))*self.SCALE,(h+9)*self.SCALE) )
            else:
                surface.blit(self.sldrKnbLow, ((27+108*(self.Supplies[i].goalAmt/200))*self.SCALE,(h+9)*self.SCALE) )
            # text should be displayed at (28,23)*SCALE plus the height offset of the element it cooresponds to
            if(self.supplySliderSelect==self.Supplies[i].ID):
                s = f"Stock Amount: {self.Supplies[i].goalAmt:.0f}"
                text = font.render(s,True,(0,0,0))
                surface.blit(text,[28*self.SCALE,(h+2)*self.SCALE])                
            else:
                text = font.render(str(self.Supplies[i].name),True,(0,0,0))
                surface.blit(text,[28*self.SCALE,(h+2)*self.SCALE])
            i += 1
        return self.supplySelect
    def displayProductMenu(self,surface):
        # highest the scroll bar can be drawn is (154,20)*SCALE
        # lowest it can be drawn is (154,160)*SCALE        
        if(self.scrollSelect):
            # also make sure mouse does not push scroll bar from afar if it goes out of bounds            
            h = float(20.0+140.0*self.supplyScroll) + ( ((self.mouseXY[1]-self.prevMouseXY[1])/self.SCALE) if (self.mouseXY[1]>=20*self.SCALE and self.mouseXY[1]<=176*self.SCALE) else 0)
            self.productScroll = (h-20.0)/140.0
            if(self.productScroll<0):
                self.productScroll = 0.0
            if(self.productScroll>1):
                self.productScroll = 1.0            
            surface.blit(self.scrlBarHigh,(154*self.SCALE,(20+140*self.productScroll)*self.SCALE))
        else:
            surface.blit(self.scrlBarLow,(154*self.SCALE,(20+140*self.productScroll)*self.SCALE))
        # the first list element should be drawn at (5,21)*SCALE
        # the height of each element is 16*SCALE
        # there should be a 1*SCALE spacing between elements
        # each element should be drawn at (5,21+17i)*SCALE where i starts and 0 and increments +1 per element
        # the scroll bar should modify the height so that the last element is drawn at (5,159)*SCALE when the scroll bar is at the bottom
        # height of the final element before scrolling is 21 + 17*(len(self.Products)-1)
        # height of the final element after scrolling should be 159
        # the difference is -138 + 17*(len(self.Products)-1)        
        # each element should be drawn at (5,21 + 17*i + (138 - 17*(len(self.Products)-1) )*self.productScroll )
        # if the height is less then 20 or greater than 160, the element should not be drawn
        i = 0
        font = pygame.font.SysFont(None,36)
        while(i<len(self.Products)):
            h = 21 + 17*i + (138 - 17*(len(self.Products)-1) )*self.productScroll
            if(h<20 or h>160):
                i += 1
                continue            
            if(self.productSelect==self.Products[i].ID):
                surface.blit(self.itemHigh, (5*self.SCALE, h*self.SCALE ))
            else:
                surface.blit(self.itemLow, (5*self.SCALE, h*self.SCALE ))
            # icons should be displayed at (7,24)*SCALE, plus the height offset of the element is cooresponds to
            img = self.getObjImage(self.Products[i].ID)
            surface.blit(img, (7*self.SCALE, (h+3)*self.SCALE ))
            # the slider knob should be displayed at height 30*SCALE plus the height offset of the element it cooresponds to
            # the slider knob should be displayed at width (27 + 108*Value/Max)*SCALE
            if(self.productSliderSelect==self.Products[i].ID):
                # find the new location based on how much the mouse dragged
                # also make sure mouse does not push knob from afar if it goes out of bounds
                w = (27+108*(self.Products[i].price/50.0))*self.SCALE + ((self.mouseXY[0]-self.prevMouseXY[0]) if (self.mouseXY[0]>=27*self.SCALE and self.mouseXY[0]<=141*self.SCALE) else 0 )
                # don't let it go out of bounds
                if(w<27*self.SCALE):
                    w = 27*self.SCALE
                if(w>135*self.SCALE):
                    w = 135*self.SCALE
                # reverse engineer the new price
                self.Products[i].price = (((w/self.SCALE)-27)/108)*50.0
                # display the knob
                surface.blit(self.sldrKnbHigh, ((27+108*(self.Products[i].price/50.0))*self.SCALE,(h+9)*self.SCALE) )
            else:
                surface.blit(self.sldrKnbLow, ((27+108*(self.Products[i].price/50.0))*self.SCALE,(h+9)*self.SCALE) )
            # text should be displayed at (28,23)*SCALE plus the height offset of the element it cooresponds to
            if(self.productSliderSelect==self.Products[i].ID):
                s = f"Price: {self.Products[i].price:.2f}"
                text = font.render(s,True,(0,0,0))
                surface.blit(text,[28*self.SCALE,(h+2)*self.SCALE])                
            else:
                text = font.render(str(self.Products[i].name),True,(0,0,0))
                surface.blit(text,[28*self.SCALE,(h+2)*self.SCALE])
            i += 1
        return self.productSelect
# settings menu: In this menu you will get Volume,Music,Game speed Sliders and you be able to reset or go back to the game.
def clamp(v, a, b):
    return max(a, min(b, v))

class Slider:
    def __init__(self, rect: pygame.Rect, label: str, value: float = 0.5,
                 min_val: float = 0.0, max_val: float = 1.0,
                 on_change: Callable[[float], None] = None):
        self.rect = rect  # area for full slider (line + knob)
        self.label = label
        self.min = min_val
        self.max = max_val
        self.value = clamp(value, self.min, self.max)
        self.on_change = on_change

        # knob visuals
        self.knob_radius = int(rect.height * 0.45)
        self.knob_color = (230, 230, 230)
        self.knob_hover_color = (255, 255, 255)
        self.knob_pressed_color = (200, 200, 200)

        # interaction state
        self.hover = False
        self.dragging = False
        self._press_candidate = False  # true if press started on this knob

    def knob_center_x(self):
        # map value to x coordinate inside rect (padding by knob_radius)
        pad = self.knob_radius + 2
        usable_w = max(1, self.rect.w - pad*2)
        frac = (self.value - self.min) / (self.max - self.min) if self.max != self.min else 0
        return self.rect.x + pad + int(frac * usable_w)

    def knob_center(self):
        return (self.knob_center_x(), self.rect.centery)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        # track knob pos
        cx, cy = self.knob_center()
        # track hover scale
        base_r = self.knob_radius
        if self.dragging:
            r = int(base_r * 0.9)  # shrink while pressed
        elif self.hover:
            r = int(base_r * 1.15)  # expand while hover
        else:
            r = base_r
        # draw track line
        track_color = (120, 120, 120)
        pygame.draw.line(surface, track_color,
                         (self.rect.x + r + 2, self.rect.centery),
                         (self.rect.x + self.rect.w - r - 2, self.rect.centery), 4)
        # draw knob
        color = self.knob_color
        if self.dragging:
            color = self.knob_pressed_color
        elif self.hover:
            color = self.knob_hover_color
        pygame.draw.circle(surface, color, (cx, cy), r)
        # label and value
        label_surf = font.render(self.label, True, (240, 240, 240))
        val_surf = font.render(f"{self.value:.2f}", True, (200, 200, 200))
        surface.blit(label_surf, (self.rect.x, self.rect.y - 24))
        surface.blit(val_surf, (self.rect.right - val_surf.get_width(), self.rect.y - 24))

    def update_interaction(self, mouse_pos: Tuple[int, int], mouse_down: bool, prev_mouse_down: bool):
        mx, my = mouse_pos
        cx, cy = self.knob_center()
        dist2 = (mx - cx)**2 + (my - cy)**2
        hovered_now = dist2 <= (int(self.knob_radius * 1.6) ** 2)
        # begin press
        if not prev_mouse_down and mouse_down:
            # mouse was just pressed
            if hovered_now:
                self._press_candidate = True
                self.dragging = True
        # while held: update dragging behavior if this knob was the press candidate
        if mouse_down:
            if self._press_candidate:
                # when dragging, knob follows horizontal mouse only
                # compute new fraction relative to track
                pad = self.knob_radius + 2
                left = self.rect.x + pad
                right = self.rect.x + self.rect.w - pad
                newx = clamp(mx, left, right)
                frac = (newx - left) / max(1, (right - left))
                newval = self.min + frac * (self.max - self.min)
                if newval != self.value:
                    self.value = newval
                    if self.on_change:
                        self.on_change(self.value)
                # While dragging, the knob should appear pressed only if pointer is over the knob:
                self.hover = (abs(newx - cx) <= int(self.knob_radius * 1.8))
            else:
                # mouse is down but it wasn't pressed on this knob; ensure hover/drag false
                self.hover = hovered_now
                self.dragging = False
        else:
            # mouse released
            if prev_mouse_down and not mouse_down:
                # finalize press candidate if it was on this knob
                if self._press_candidate:
                    # release whether on or off the knob; we always stop dragging
                    self._press_candidate = False
                    self.dragging = False
            # hover behavior when mouse is not down
            self.hover = hovered_now

class Button:
    def __init__(self, rect: pygame.Rect, text: str, on_click: Callable[[], None] = None):
        self.rect = rect
        self.text = text
        self.on_click = on_click
        # visuals
        self.color = (100, 100, 100)
        self.hover_color = (120, 120, 120)
        self.pressed_color = (80, 80, 80)
        self.text_color = (245, 245, 245)
        # states
        self.hover = False
        self._press_candidate = False  # user pressed down on this button
        self.pressed_visual = False    # visual pressed state while mouse held AND over button

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        # size scaling
        scale = 1.05 if self.hover else 1.0
        if self.pressed_visual:
            scale = 0.95
        w = int(self.rect.w * scale)
        h = int(self.rect.h * scale)
        x = int(self.rect.centerx - w/2)
        y = int(self.rect.centery - h/2)
        # rectangle
        col = self.color
        if self.pressed_visual:
            col = self.pressed_color
        elif self.hover:
            col = self.hover_color
        pygame.draw.rect(surface, col, pygame.Rect(x,y,w,h), border_radius=8)
        # text
        txt_surf = font.render(self.text, True, self.text_color)
        tx = x + (w - txt_surf.get_width())//2
        ty = y + (h - txt_surf.get_height())//2
        surface.blit(txt_surf, (tx, ty))

    def update_interaction(self, mouse_pos: Tuple[int,int], mouse_down: bool, prev_mouse_down: bool):
        mx, my = mouse_pos
        hovered_now = self.rect.collidepoint(mx, my)
        # handle press start
        if not prev_mouse_down and mouse_down:
            if hovered_now:
                self._press_candidate = True
                # visual pressed state applied only while mouse is down AND cursor remains over button
                self.pressed_visual = True
            else:
                self._press_candidate = False
                self.pressed_visual = False
        elif mouse_down:
            # while held, update visual pressed depending on whether pointer is over button
            if self._press_candidate and hovered_now:
                self.pressed_visual = True
            else:
                self.pressed_visual = False
        else:
            # mouse released
            if prev_mouse_down and not mouse_down:
                if self._press_candidate and hovered_now:
                    # full click finished: invoke
                    if self.on_click:
                        self.on_click()
                self._press_candidate = False
                self.pressed_visual = False
        # hover state is independent: mouse-up hover expands
        if not mouse_down:
            self.hover = hovered_now
        else:
            # if mouse down and press candidate started elsewhere, don't set hover on other buttons (user story)
            # But if the candidate started on this button, show hover depending on current pointer location
            if self._press_candidate:
                self.hover = hovered_now
            else:
                self.hover = False
class SettingsMenu:
    def __init__(self, on_back: Callable[[], None] = None, on_reset: Callable[[], None] = None,
                 initial_values: Dict[str, float] = None):
        if initial_values is None:
            initial_values = {'volume': 0.8, 'music': 0.7, 'speed': 1.0}
        self.on_back = on_back
        self.on_reset = on_reset

        # UI layout constants (center vertical column)
        screen = pygame.display.get_surface()
        sw, sh = screen.get_size()
        center_x = sw // 2
        top_y = sh // 3

        slider_w = min(600, sw - 120)
        slider_h = 36
        gap = 80

        font = pygame.font.Font(None, 28)
        self.font = font

        # create sliders
        rect1 = pygame.Rect(center_x - slider_w//2, top_y, slider_w, slider_h)
        rect2 = pygame.Rect(center_x - slider_w//2, top_y + gap, slider_w, slider_h)
        rect3 = pygame.Rect(center_x - slider_w//2, top_y + gap*2, slider_w, slider_h)

        self.sliders = {
            'volume': Slider(rect1, "Volume", initial_values.get('volume', 0.8), on_change=self._on_volume_change),
            'music': Slider(rect2, "Music Volume", initial_values.get('music', 0.7), on_change=self._on_music_change),
            'speed': Slider(rect3, "Game Speed", initial_values.get('speed', 1.0), min_val=0.5, max_val=2.0, on_change=self._on_speed_change)
        }

        # Buttons underneath
        btn_w = 160
        btn_h = 52
        btn_y = top_y + gap*3 + 30
        reset_rect = pygame.Rect(center_x - btn_w - 20, btn_y, btn_w, btn_h)
        back_rect = pygame.Rect(center_x + 20, btn_y, btn_w, btn_h)
        self.button_reset = Button(reset_rect, "Reset", on_click=self._reset)
        self.button_back = Button(back_rect, "Back", on_click=self._back)

        # internal mouse state tracking
        self._prev_mouse_down = False
        self._mouse_pos = (0,0)
        # optional external callback pointers used to immediately apply settings externally
        self.external_set_volume = None     # signature: f(volume: float)
        self.external_set_music = None      # signature: f(music_volume: float)
        self.external_set_speed = None      # signature: f(speed: float)

    def _on_volume_change(self, v: float):
        # immediate effect
        if self.external_set_volume:
            self.external_set_volume(v)

    def _on_music_change(self, v: float):
        if self.external_set_music:
            self.external_set_music(v)

    def _on_speed_change(self, v: float):
        if self.external_set_speed:
            self.external_set_speed(v)

    def _reset(self):
        # default values
        defaults = {'volume': 0.8, 'music': 0.7, 'speed': 1.0}
        for k, s in self.sliders.items():
            s.value = defaults[k]
            if s.on_change:
                s.on_change(s.value)
        if self.on_reset:
            self.on_reset()

    def _back(self):
        if self.on_back:
            self.on_back()

    def store_inputs(self, mouse_pos: Tuple[int,int], mouse_down: bool):
        # Save mouse pos and handle transitions; call update next
        self._mouse_pos = mouse_pos
        self._mouse_down = mouse_down

    def update(self):
        # update sliders and buttons using current and previous mouse state
        md = getattr(self, '_mouse_down', False)
        pmd = self._prev_mouse_down
        for key, s in self.sliders.items():
            s.update_interaction(self._mouse_pos, md, pmd)
        # ensure that while dragging one slider, others do not react (per story)
        # find active slider
        active = None
        for key, s in self.sliders.items():
            if s.dragging:
                active = key
                break
        if active:
            # for others, if mouse is down they should not react
            for key, s in self.sliders.items():
                if key != active:
                    # pass mouse_down=False so they behave inertly
                    s.update_interaction(self._mouse_pos, False, pmd)
        # buttons
        self.button_reset.update_interaction(self._mouse_pos, md, pmd)
        self.button_back.update_interaction(self._mouse_pos, md, pmd)

        self._prev_mouse_down = md

    def draw(self, surface: pygame.Surface):
        # clear background area / optionally dim
        sw, sh = surface.get_size()
        # draw semi-transparent panel background
        panel = pygame.Surface((sw, sh), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 120))
        surface.blit(panel, (0, 0))

        # draw central card
        card_w = min(760, sw - 40)
        card_h = min(480, sh - 80)
        card_x = (sw - card_w) // 2
        card_y = (sh - card_h) // 2
        pygame.draw.rect(surface, (20, 20, 20), (card_x, card_y, card_w, card_h), border_radius=10)
        # title
        title_font = pygame.font.Font(None, 36)
        title_surf = title_font.render("Settings", True, (245, 245, 245))
        surface.blit(title_surf, (card_x + 24, card_y + 16))

        # draw sliders and buttons
        for s in self.sliders.values():
            s.draw(surface, self.font)
        self.button_reset.draw(surface, self.font)
        self.button_back.draw(surface, self.font)

    def get_values(self) -> Dict[str, float]:
        return {k: s.value for k, s in self.sliders.items()}

    def set_external_callbacks(self, set_volume_fn: Callable[[float], None], set_music_fn: Callable[[float], None],
                               set_speed_fn: Callable[[float], None]):
        self.external_set_volume = set_volume_fn
        self.external_set_music = set_music_fn
        self.external_set_speed = set_speed_fn