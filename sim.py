import random, pygame
# IDE may complain that functions from class references from other files aren't defined
# the program will work anyway

# TO DO
# stocks of supplies seem to immediately run out on the second day of having a goal amount of 0
    # I suspect order of operations with ContinueSim and the management screens could be an issue
    # can't really troubleshoot until graphs are working
class Sim:
    # movement speed will be 1 pixel per frame, or just under 1 unit of space per second
    def __init__(self,surface,SCALE):
        self.surface = surface      # Surface to draw on.
        self.SCALE = SCALE          # Graphics scale factor.
        
        self.mouseXY = [0,0]        # Mouse position.
        self.lftClkSt = 0
        self.points = 0
        self.profit = 0.00
        self.pointMax = 40.0
        self.time = 3600            # Number of frames remaining in the current day.
        self.maxTime = 3600         # Length of sim days in frames. # game feels like a good length at 2 minutes, 7200 frames, but for demo, set to 1 minute
        self.hoursInDay = 14        # Number of hours in one sim day (for converting time to UI display).
        self.startHour = 6          # Hour to start the sim at (for UI display).
        self.employees = []         # Employee instances.
        self.customers = []         # Customer instances.
        self.objects = []           # Object instances.
        self.shelfSpace = [0,0,0,0,0]
        self.prod_order = []        # list of product orders wanted by customers
        self.demoStarted = False    # (Used to determine the first simulation frame.)
        # class references
        self.acDataRef = None
        self.settingsRef = None
        self.simDataRef = None
        # during-sim prod/supply trackers
        self.supplies = [] # [supplies[ID, price, goal amount, ordered amount, current amount, used amount] ]
        self.products = [] # [products[ID, price, sales, [supplies[ID,amount]] ] ]
        self.transactions = [] # [transaction[time, money earned, sale revenue, sale points]] # each point holds the change in the 3, not the absolute value
        
        # Load Image Assets as Surfaces ------------------------------------
        # Floorplan:
        self.floorPlan = pygame.image.load("assets/graphics/floorplan.png").convert_alpha()
        self.floorPlan = pygame.transform.scale_by(self.floorPlan,SCALE)
        self.hud = pygame.image.load("assets/graphics/hud.png").convert_alpha()
        self.hud = pygame.transform.scale_by(self.hud,SCALE)
        self.tmr_cap = pygame.image.load("assets/graphics/tmr_cap.png").convert_alpha()
        self.tmr_cap = pygame.transform.scale_by(self.tmr_cap,SCALE)
        # Customers:
        self.cust11 = pygame.image.load("assets/graphics/cust_1_1.png").convert_alpha()
        self.cust11 = pygame.transform.scale_by(self.cust11,SCALE)
        self.cust12 = pygame.image.load("assets/graphics/cust_1_2.png").convert_alpha()
        self.cust12 = pygame.transform.scale_by(self.cust12,SCALE)
        self.cust13 = pygame.image.load("assets/graphics/cust_1_3.png").convert_alpha()
        self.cust13 = pygame.transform.scale_by(self.cust13,SCALE)
        self.cust14 = pygame.image.load("assets/graphics/cust_1_4.png").convert_alpha()
        self.cust14 = pygame.transform.scale_by(self.cust14,SCALE)
        self.cust21 = pygame.image.load("assets/graphics/cust_2_1.png").convert_alpha()
        self.cust21 = pygame.transform.scale_by(self.cust21,SCALE)
        self.cust22 = pygame.image.load("assets/graphics/cust_2_2.png").convert_alpha()
        self.cust22 = pygame.transform.scale_by(self.cust22,SCALE)
        self.cust23 = pygame.image.load("assets/graphics/cust_2_3.png").convert_alpha()
        self.cust23 = pygame.transform.scale_by(self.cust23,SCALE)
        self.cust24 = pygame.image.load("assets/graphics/cust_2_4.png").convert_alpha()
        self.cust24 = pygame.transform.scale_by(self.cust24,SCALE)
        self.cust31 = pygame.image.load("assets/graphics/cust_3_1.png").convert_alpha()
        self.cust31 = pygame.transform.scale_by(self.cust31,SCALE)
        self.cust32 = pygame.image.load("assets/graphics/cust_3_2.png").convert_alpha()
        self.cust32 = pygame.transform.scale_by(self.cust32,SCALE)
        self.cust33 = pygame.image.load("assets/graphics/cust_3_3.png").convert_alpha()
        self.cust33 = pygame.transform.scale_by(self.cust33,SCALE)
        self.cust34 = pygame.image.load("assets/graphics/cust_3_4.png").convert_alpha()
        self.cust34 = pygame.transform.scale_by(self.cust34,SCALE)
        self.cust41 = pygame.image.load("assets/graphics/cust_4_1.png").convert_alpha()
        self.cust41 = pygame.transform.scale_by(self.cust41,SCALE)
        self.cust42 = pygame.image.load("assets/graphics/cust_4_2.png").convert_alpha()
        self.cust42 = pygame.transform.scale_by(self.cust42,SCALE)
        self.cust43 = pygame.image.load("assets/graphics/cust_4_3.png").convert_alpha()
        self.cust43 = pygame.transform.scale_by(self.cust43,SCALE)
        self.cust44 = pygame.image.load("assets/graphics/cust_4_4.png").convert_alpha()
        self.cust44 = pygame.transform.scale_by(self.cust44,SCALE)
        # Employees:
        self.emp11 = pygame.image.load("assets/graphics/emp_1_1.png").convert_alpha()
        self.emp11 = pygame.transform.scale_by(self.emp11,SCALE)
        self.emp12 = pygame.image.load("assets/graphics/emp_1_2.png").convert_alpha()
        self.emp12 = pygame.transform.scale_by(self.emp12,SCALE)
        self.emp13 = pygame.image.load("assets/graphics/emp_1_3.png").convert_alpha()
        self.emp13 = pygame.transform.scale_by(self.emp13,SCALE)
        self.emp14 = pygame.image.load("assets/graphics/emp_1_4.png").convert_alpha()
        self.emp14 = pygame.transform.scale_by(self.emp14,SCALE)
        self.emp21 = pygame.image.load("assets/graphics/emp_2_1.png").convert_alpha()
        self.emp21 = pygame.transform.scale_by(self.emp21,SCALE)
        self.emp22 = pygame.image.load("assets/graphics/emp_2_2.png").convert_alpha()
        self.emp22 = pygame.transform.scale_by(self.emp22,SCALE)
        self.emp23 = pygame.image.load("assets/graphics/emp_2_3.png").convert_alpha()
        self.emp23 = pygame.transform.scale_by(self.emp23,SCALE)
        self.emp24 = pygame.image.load("assets/graphics/emp_2_4.png").convert_alpha()
        self.emp24 = pygame.transform.scale_by(self.emp24,SCALE)
        self.emp31 = pygame.image.load("assets/graphics/emp_3_1.png").convert_alpha()
        self.emp31 = pygame.transform.scale_by(self.emp31,SCALE)
        self.emp32 = pygame.image.load("assets/graphics/emp_3_2.png").convert_alpha()
        self.emp32 = pygame.transform.scale_by(self.emp32,SCALE)
        self.emp33 = pygame.image.load("assets/graphics/emp_3_3.png").convert_alpha()
        self.emp33 = pygame.transform.scale_by(self.emp33,SCALE)
        self.emp34 = pygame.image.load("assets/graphics/emp_3_4.png").convert_alpha()
        self.emp34 = pygame.transform.scale_by(self.emp34,SCALE)
        self.emp41 = pygame.image.load("assets/graphics/emp_4_1.png").convert_alpha()
        self.emp41 = pygame.transform.scale_by(self.emp41,SCALE)
        self.emp42 = pygame.image.load("assets/graphics/emp_4_2.png").convert_alpha()
        self.emp42 = pygame.transform.scale_by(self.emp42,SCALE)
        self.emp43 = pygame.image.load("assets/graphics/emp_4_3.png").convert_alpha()
        self.emp43 = pygame.transform.scale_by(self.emp43,SCALE)
        self.emp44 = pygame.image.load("assets/graphics/emp_4_4.png").convert_alpha()
        self.emp44 = pygame.transform.scale_by(self.emp44,SCALE)
        # Objects:
        self.bttl = pygame.image.load("assets/graphics/bttl.png").convert_alpha()
        self.bttl = pygame.transform.scale_by(self.bttl,SCALE)
        self.chk_pwd = pygame.image.load("assets/graphics/chk_pwd.png").convert_alpha()
        self.chk_pwd = pygame.transform.scale_by(self.chk_pwd,SCALE)
        self.cof_bn = pygame.image.load("assets/graphics/cof_bn.png").convert_alpha()
        self.cof_bn = pygame.transform.scale_by(self.cof_bn,SCALE)
        self.cof_mkr1 = pygame.image.load("assets/graphics/cof_mkr_1.png").convert_alpha()
        self.cof_mkr1 = pygame.transform.scale_by(self.cof_mkr1,SCALE)
        self.cof_mkr2 = pygame.image.load("assets/graphics/cof_mkr_2.png").convert_alpha()
        self.cof_mkr2 = pygame.transform.scale_by(self.cof_mkr2,SCALE)
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
        # Order Bubbles:
        self.bbl1 = pygame.image.load("assets/graphics/bbl1.png").convert_alpha()
        self.bbl1 = pygame.transform.scale_by(self.bbl1,SCALE)
        self.bbl2 = pygame.image.load("assets/graphics/bbl2.png").convert_alpha()
        self.bbl2 = pygame.transform.scale_by(self.bbl2,SCALE)
        self.bbl3 = pygame.image.load("assets/graphics/bbl3.png").convert_alpha()
        self.bbl3 = pygame.transform.scale_by(self.bbl3,SCALE)
        self.bbl4 = pygame.image.load("assets/graphics/bbl4.png").convert_alpha()
        self.bbl4 = pygame.transform.scale_by(self.bbl4,SCALE)
        self.bbl5 = pygame.image.load("assets/graphics/bbl5.png").convert_alpha()
        self.bbl5 = pygame.transform.scale_by(self.bbl5,SCALE)
        self.bbl6 = pygame.image.load("assets/graphics/bbl6.png").convert_alpha()
        self.bbl6 = pygame.transform.scale_by(self.bbl6,SCALE)
        self.bbl7 = pygame.image.load("assets/graphics/bbl7.png").convert_alpha()
        self.bbl7 = pygame.transform.scale_by(self.bbl7,SCALE)
        self.bbl8 = pygame.image.load("assets/graphics/bbl8.png").convert_alpha()
        self.bbl8 = pygame.transform.scale_by(self.bbl8,SCALE)
        self.bbl9 = pygame.image.load("assets/graphics/bbl9.png").convert_alpha()
        self.bbl9 = pygame.transform.scale_by(self.bbl9,SCALE)
        self.bbl10 = pygame.image.load("assets/graphics/bbl10.png").convert_alpha()
        self.bbl10 = pygame.transform.scale_by(self.bbl10,SCALE)
        self.bbl11 = pygame.image.load("assets/graphics/bbl11.png").convert_alpha()
        self.bbl11 = pygame.transform.scale_by(self.bbl11,SCALE)
        self.bbl12 = pygame.image.load("assets/graphics/bbl12.png").convert_alpha()
        self.bbl12 = pygame.transform.scale_by(self.bbl12,SCALE)
        self.bbl13 = pygame.image.load("assets/graphics/bbl13.png").convert_alpha()
        self.bbl13 = pygame.transform.scale_by(self.bbl13,SCALE)
        self.bbl14 = pygame.image.load("assets/graphics/bbl14.png").convert_alpha()
        self.bbl14 = pygame.transform.scale_by(self.bbl14,SCALE)
        self.bbl15 = pygame.image.load("assets/graphics/bbl15.png").convert_alpha()
        self.bbl15 = pygame.transform.scale_by(self.bbl15,SCALE)
        self.bbl16 = pygame.image.load("assets/graphics/bbl16.png").convert_alpha()
        self.bbl16 = pygame.transform.scale_by(self.bbl16,SCALE)
        self.bbl17 = pygame.image.load("assets/graphics/bbl17.png").convert_alpha()
        self.bbl17 = pygame.transform.scale_by(self.bbl17,SCALE)
        self.bbl18 = pygame.image.load("assets/graphics/bbl18.png").convert_alpha()
        self.bbl18 = pygame.transform.scale_by(self.bbl18,SCALE)
        self.bbl19 = pygame.image.load("assets/graphics/bbl19.png").convert_alpha()
        self.bbl19 = pygame.transform.scale_by(self.bbl19,SCALE)
        self.bbl20 = pygame.image.load("assets/graphics/bbl20.png").convert_alpha()
        self.bbl20 = pygame.transform.scale_by(self.bbl20,SCALE)
        self.bbl21 = pygame.image.load("assets/graphics/bbl21.png").convert_alpha()
        self.bbl21 = pygame.transform.scale_by(self.bbl21,SCALE)
        self.bbl22 = pygame.image.load("assets/graphics/bbl22.png").convert_alpha()
        self.bbl22 = pygame.transform.scale_by(self.bbl22,SCALE)
        self.bbl23 = pygame.image.load("assets/graphics/bbl23.png").convert_alpha()
        self.bbl23 = pygame.transform.scale_by(self.bbl23,SCALE)
        self.bbl24 = pygame.image.load("assets/graphics/bbl24.png").convert_alpha()
        self.bbl24 = pygame.transform.scale_by(self.bbl24,SCALE)
        self.bbl25 = pygame.image.load("assets/graphics/bbl25.png").convert_alpha()
        self.bbl25 = pygame.transform.scale_by(self.bbl25,SCALE)
        self.bbl26 = pygame.image.load("assets/graphics/bbl26.png").convert_alpha()
        self.bbl26 = pygame.transform.scale_by(self.bbl26,SCALE)
        self.bbl27 = pygame.image.load("assets/graphics/bbl27.png").convert_alpha()
        self.bbl27 = pygame.transform.scale_by(self.bbl27,SCALE)
        self.bbl28 = pygame.image.load("assets/graphics/bbl28.png").convert_alpha()
        self.bbl28 = pygame.transform.scale_by(self.bbl28,SCALE)
        self.bbl29 = pygame.image.load("assets/graphics/bbl29.png").convert_alpha()
        self.bbl29 = pygame.transform.scale_by(self.bbl29,SCALE)
        self.bbl30 = pygame.image.load("assets/graphics/bbl30.png").convert_alpha()
        self.bbl30 = pygame.transform.scale_by(self.bbl30,SCALE)
        self.bbl31 = pygame.image.load("assets/graphics/bbl31.png").convert_alpha()
        self.bbl31 = pygame.transform.scale_by(self.bbl31,SCALE)
        self.bbl32 = pygame.image.load("assets/graphics/bbl32.png").convert_alpha()
        self.bbl32 = pygame.transform.scale_by(self.bbl32,SCALE)
        self.bbl33 = pygame.image.load("assets/graphics/bbl33.png").convert_alpha()
        self.bbl33 = pygame.transform.scale_by(self.bbl33,SCALE)
        self.bbl34 = pygame.image.load("assets/graphics/bbl34.png").convert_alpha()
        self.bbl34 = pygame.transform.scale_by(self.bbl34,SCALE)
        self.bbl35 = pygame.image.load("assets/graphics/bbl35.png").convert_alpha()
        self.bbl35 = pygame.transform.scale_by(self.bbl35,SCALE)
        self.bbl36 = pygame.image.load("assets/graphics/bbl36.png").convert_alpha()
        self.bbl36 = pygame.transform.scale_by(self.bbl36,SCALE)
        self.bbl37 = pygame.image.load("assets/graphics/bbl37.png").convert_alpha()
        self.bbl37 = pygame.transform.scale_by(self.bbl37,SCALE)
        self.bbl38 = pygame.image.load("assets/graphics/bbl38.png").convert_alpha()
        self.bbl38 = pygame.transform.scale_by(self.bbl38,SCALE)
        self.bbl39 = pygame.image.load("assets/graphics/bbl39.png").convert_alpha()
        self.bbl39 = pygame.transform.scale_by(self.bbl39,SCALE)
        self.bbl40 = pygame.image.load("assets/graphics/bbl40.png").convert_alpha()
        self.bbl40 = pygame.transform.scale_by(self.bbl40,SCALE)
        self.bbl41 = pygame.image.load("assets/graphics/bbl41.png").convert_alpha()
        self.bbl41 = pygame.transform.scale_by(self.bbl41,SCALE)
        self.bubbles = [self.bbl1,self.bbl2,self.bbl3,self.bbl4,self.bbl5,self.bbl6,self.bbl7,self.bbl8,self.bbl9,self.bbl10,self.bbl11,self.bbl12,self.bbl13,self.bbl14,self.bbl15,self.bbl16,self.bbl17,self.bbl18,self.bbl19,self.bbl20,self.bbl21,self.bbl22,self.bbl23,self.bbl24,self.bbl25,self.bbl26,self.bbl27,self.bbl28,self.bbl29,self.bbl30,self.bbl31,self.bbl32,self.bbl33,self.bbl34,self.bbl35,self.bbl36,self.bbl37,self.bbl38,self.bbl39,self.bbl40,self.bbl41]
        
    class Emp:
        # Static vars belonging to class, not one individual instance:
        # Lists containing the orders that require each of the supply types so that emp1 knows where to get the proper supply item:
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
        prod_sm  = [22,25,28,31,34,37,38,87]
        prod_rg  = [23,26,29,32,35,39,40,42,44,46,48,50,52,54,56,58,60,62]
        prod_lg  = [24,27,30,33,36,41,43,45,47,49,51,53,55,57,59,61,63]
        def __init__(self,ID,loc,job,task):
            # Instance vars:
            self.ID = ID
            self.loc = [loc[0],loc[1]]
            self.offset = [0,0]
            self.dir = 0
            self.job = job
            self.task = task
            self.order = 0
            self.orderLoc = -1
            self.patience = 20
    
    class Cust:
        def __init__(self,ID,loc,order,task):
            self.ID = ID
            self.loc = [loc[0],loc[1]]
            self.offset = [0,0]
            self.dir = 0
            self.order = order
            self.task = task
            self.patience = 620 # Max customer waiting time in ticks - 620 = 10.33 seconds at 60FPS (0.33 for 20-tick order animation).
    class Obj:
        def __init__(self,ID,loc):
            self.ID = ID
            self.loc = [loc[0],loc[1]]
    
    def getObjImg(self,ID,x):
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
        elif(ID in self.Emp.sup_pas):
            img = self.pstry
        elif(ID in self.Emp.sup_syr):
            img = self.syrp
        elif(ID in self.Emp.prod_wet and x==0):
            img = self.cof_mkr2
        elif(ID in self.Emp.prod_sm):
            img = self.cup_sm2
        elif(ID in self.Emp.prod_rg):
            img = self.cup_rg2
        elif(ID in self.Emp.prod_lg):
            img = self.cup_lg2
        elif(ID in self.Emp.sup_cof):
            img = self.cof_bn
        elif(ID in self.Emp.sup_tea):
            img = self.tea_lvs
        elif(ID in self.Emp.sup_coco):
            img = self.chk_pwd
        else:                            # this obj should only show up on the back counter, if we see it on the tables, we know something's wrong
            img = self.cof_mkr1
        return img
    def demoSim(self):
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
                            if((c.task>0 and c.task<4) and c.loc[0] == 7 and c.loc[1] == 4):
                                space = False
                                break
                        if(space):
                            unit.offset[0] -= 2
                            if(unit.offset[0]<=-32):
                                unit.offset[0] += 64
                                unit.loc[0] -= 1
                case 2: # order animation
                    if(unit.patience>=600):
                        unit.patience -= 1
                    else:
                        unit.task += 1
                case 3: # ordering
                    for e in self.employees:
                        if(e.job==0 and e.task==0 and e.loc[0]==5 and e.loc[1]==4):
                            unit.task += 1
                            unit.dir = 3
                            break
                case 4: # walking to the pick-up line
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
                case 5: # pick-up line
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
                            if((c.task==5 or c.task==6) and c.loc[0] == unit.loc[0]-1 and c.loc[1] == 8):
                                space = False
                                break
                        if(space):
                            unit.offset[0] -= 2
                            if(unit.offset[0]<=-32):
                                unit.offset[0] += 64
                                unit.loc[0] -= 1
                case 6: # picking up order
                    for e in self.employees:
                        if(e.job==1 and e.task==5 and e.loc[0]==5 and e.loc[1]==8):
                            unit.task += 1
                            unit.dir = 3
                            # spawn a new customer
                            self.customers.append(self.Cust(random.randint(0,3),[-1,1],self.acDataRef.getRndProd(random.randint(0,14)),1))                            
                case 7: # finding a seat
                    if(unit.offset[0]<0):                                                   # centering onto current tile
                        unit.offset[0] += 2
                        if(unit.offset[0]==0 and (unit.loc[0] == 10 or unit.loc[0] == 19)):     # start walking up
                            unit.dir = 1
                            if(unit.loc[0]==10): # check if the very first seat is available first
                                spaceR = True
                                for c in self.customers:
                                    if(c.task==8 and c.loc[0]==unit.loc[0]+1 and c.loc[1]==unit.loc[1]): # someone is sitting there
                                        spaceR = False
                                        break
                                    if(spaceR and c.task==8 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==0): # someone is planning on sitting there
                                        spaceR = False
                                        break
                                if(spaceR):
                                    for o in self.objects:
                                        if(o.loc[0]==unit.loc[0]+2 and o.loc[1]==unit.loc[1]): # someone left their food there
                                            spaceR = False
                                            break
                                if(spaceR):
                                    unit.task += 1
                                    unit.dir = 0
                                    unit.patience = 300
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
                                if(c.task==8 and c.loc[0]==unit.loc[0]-1 and c.loc[1]==unit.loc[1]):
                                    spaceL = False
                                    continue
                                if(spaceL and c.task==8 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==2):
                                    spaceL = False
                                    continue
                                if(c.task==8 and c.loc[0]==unit.loc[0]+1 and c.loc[1]==unit.loc[1]):
                                    spaceR = False
                                    continue
                                if(spaceR and c.task==8 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==0):
                                    spaceR = False
                                    continue
                            if(spaceL or spaceR):
                                for o in self.objects:
                                    if(o.loc[0]==unit.loc[0]-2 and o.loc[1]==unit.loc[1]): # someone left their food there
                                        spaceL = False
                                        continue
                                    if(o.loc[0]==unit.loc[0]+2 and o.loc[1]==unit.loc[1]): # someone left their food there
                                        spaceR = False
                                        continue
                            if(spaceL):
                                unit.task += 1
                                unit.dir = 2
                                unit.patience = 300
                            elif(spaceR):
                                unit.task += 1
                                unit.dir = 0
                                unit.patience = 300
                    elif(unit.offset[1]>0 and (unit.loc[0] == 10 or unit.loc[0] == 19)):    # ^
                        unit.offset[1] -= 2
                        if(unit.offset[1]==0 and (unit.loc[0] == 10 or unit.loc[0] == 19) and unit.loc[1] == 2):    # start walking right
                            unit.dir = 0
                            if(unit.loc[0]==19): # leave the shop
                                unit.task += 2
                        elif(unit.offset[1]==0 and unit.loc[0]==10):                                                # look for a seat on the right
                            spaceR = True
                            for c in self.customers:
                                if(c.task==8 and c.loc[0]==unit.loc[0]+1 and c.loc[1]==unit.loc[1]):
                                    spaceR = False
                                    break
                                if(spaceR and c.task==8 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==0):
                                    spaceR = False
                                    break
                            if(spaceR):
                                for o in self.objects:
                                    if(o.loc[0]==unit.loc[0]+2 and o.loc[1]==unit.loc[1]):
                                        spaceR = False
                                        break
                            if(spaceR):
                                unit.task += 1
                                unit.dir = 0
                                unit.patience = 300
                        elif(unit.offset[1]==0 and unit.loc[0]==19):                                                # look for a seat on the left
                            spaceL = True
                            for c in self.customers:
                                if(c.task==8 and c.loc[0]==unit.loc[0]-1 and c.loc[1]==unit.loc[1]):
                                    spaceL = False
                                    break
                                if(spaceL and c.task==8 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==2):
                                    spaceL = False
                                    break
                            if(spaceL):
                                for o in self.objects:
                                    if(o.loc[0]==unit.loc[0]-1 and o.loc[1]==unit.loc[1]):
                                        spaceL = False
                                        break
                            if(spaceL):
                                unit.task += 1
                                unit.dir = 2
                                unit.patience = 300
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
                case 8: # sitting down / eating
                    if(unit.offset[0]==0 and (unit.loc[0]==11 or unit.loc[0]==14 or unit.loc[0]==16 or unit.loc[0]==19)):   # eat food
                        if(unit.patience==300):
                            self.objects.append(self.Obj(unit.order,[unit.loc[0]+(1 if unit.dir==0 else -1),unit.loc[1]]))
                        unit.patience -= 1
                        if(unit.patience<=0):
                            for o in self.objects: # turn full cups into empty cups
                                if(o.loc[0]==unit.loc[0]+(1 if unit.dir==0 else -1) and o.loc[1]==unit.loc[1]):
                                    if(o.ID in self.Emp.prod_lg):
                                        o.ID = 86
                                        break
                                    elif(o.ID in self.Emp.prod_rg):
                                        o.ID = 85
                                        break
                                    elif(o.ID in self.Emp.prod_sm):
                                        o.ID = 84
                                        break
                                    else:
                                        o.loc[0] = -1
                                        o.loc[1] = -1
                                        break
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
                case 9: # exiting
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
                            unit.order = 0
                            for c in self.customers:
                                if(c.task==4 and c.loc[0]==7 and c.loc[1]==4):
                                    unit.order = c.order
                                    unit.task += 1
                                    # face the correct way toward the supply item
                                    if unit.order in unit.sup_cof or unit.order in unit.sup_tea or unit.order in unit.sup_coco or unit.order in unit.sup_syr:
                                        unit.dir = 2
                                    elif unit.order in unit.sup_pas:
                                        unit.dir = 1
                                    else:
                                        unit.dir = 3                                    
                                    break
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
                                        unit.task += 1
                            elif(unit.offset[1]>0 and unit.dir==1): # ^
                                unit.offset[1] -= 2
                                if(unit.offset[1]==0 and unit.loc[1]==3):
                                    if(unit.order in unit.sup_cof and unit.loc[0]==1) or (unit.order in unit.sup_tea and unit.loc[0]==2) or (unit.order in unit.sup_coco and unit.loc[0]==3) or (unit.order in unit.sup_syr and unit.loc[0]==4) or (unit.order in unit.sup_pas and unit.loc[0]==5):
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
                            if(unit.orderLoc==-1): # vertical offset from top of shelf, indicating where to place product
                                                   # if -1, no space, don't move
                                                   # otherwise, location is [0,4+space]
                                if(unit.order in unit.prod_wet):
                                    j = 0
                                    while(j<3):
                                        if(self.shelfSpace[j]==0):
                                            unit.orderLoc = j
                                            break
                                        j += 1
                                elif(unit.order in unit.prod_dry):
                                    j = 3
                                    while(j<5):
                                        if(self.shelfSpace[j]==0):
                                            unit.orderLoc = j
                                            break
                                        j += 1
                            # try to move if there is room to place the product
                            if(unit.orderLoc<0):                        # move on to next unit, this one cannot do anything this frame
                                i += 1
                                continue
                            if(unit.dir<2):                             # turn around and take 1 frame to do so
                                unit.dir += 2
                                i += 1
                                continue
                            if(unit.offset[1]<0):                       # centering
                                unit.offset[1] += 2
                                if(unit.offset[1]==0 and unit.loc[1]==unit.orderLoc+4):
                                    unit.dir = 2
                                    unit.offset[0] += 2
                            if(unit.offset[0]>0):                       # ^
                                unit.offset[0] -= 2
                                if(unit.offset[0]==0):
                                    if(unit.loc[0]==1):     # we are in front of the space to place the product
                                        # place product
                                        self.objects.append(self.Obj(unit.order,[0,unit.loc[1]]) )
                                        # update shelf space
                                        self.shelfSpace[unit.loc[1]-4] = 1
                                        # inform other employee of order
                                        self.prod_order.append(unit.order)
                                        unit.task += 1
                                        unit.dir = 1
                                        unit.orderLoc = -1
                                        if(unit.loc[1]==4):
                                            unit.dir = 0
                                    elif(unit.loc[1]==3):   # double check that we are in front of the correct product location
                                        if(unit.loc[1]!=unit.orderLoc+4):
                                            unit.dir = 3
                            elif(unit.offset[0]<=0 and unit.dir==2):    # walk left
                                unit.offset[0] -= 2
                                if(unit.offset[0]<=-32):
                                    unit.offset[0] += 64
                                    unit.loc[0] -= 1
                            elif(unit.offset[1]>=0 and unit.dir==3):    # walk down
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
                    match(unit.task):
                        case 0: # wait for an order to be ready
                            if(len(self.prod_order)!=0):
                                unit.task += 1
                                unit.dir = 2
                        case 1: # grab order from back counter
                            if(unit.offset[0]>0):                       # centering
                                unit.offset[0] -= 2
                                if(unit.offset[0]==0):
                                    if(unit.loc[0]==1):
                                        unit.dir = 1
                                        unit.offset[1] += 2 # push down so that next centering will automatically trigger and check for an object
                            if(unit.offset[1]>0):                       # ^
                                unit.offset[1] -= 2
                                if(unit.offset[1]==0):
                                    for o in self.objects:
                                        if(o.loc[0]==0 and o.loc[1]==unit.loc[1] and o.ID==self.prod_order[0]):
                                            unit.dir = 2
                                            # grab object
                                            o.loc[0] = -1
                                            o.loc[1] = -1
                                            unit.order = o.ID
                                            # update shelfSpace
                                            self.shelfSpace[unit.loc[1]-4] = 0
                                            # update prod_order
                                            del self.prod_order[0]
                                            unit.task += 1
                                            if(unit.order in unit.prod_dry): # skip putting it in a cup if it's dry
                                                unit.task += 1
                                            break
                            elif(unit.offset[0]<=0 and unit.dir==2):    # move left
                                unit.offset[0] -= 2
                                if(unit.offset[0]<=-32):
                                    unit.offset[0] += 64
                                    unit.loc[0] -= 1
                            elif(unit.offset[1]<=0 and unit.dir==1):    # move right
                                unit.offset[1] -= 2
                                if(unit.offset[1]<=-32):
                                    unit.offset[1] += 64
                                    unit.loc[1] -= 1
                        case 2: # put order in cup
                            if(unit.dir==2): # take one frame to turn south
                                unit.dir += 1
                                i += 1
                                continue
                            if(unit.offset[1]<0):                       # centering
                                unit.offset[1] += 2
                                if(unit.offset[1]==0 and unit.loc[1]==9):
                                    unit.dir = 0
                                    unit.offset[0] -= 2
                            if(unit.offset[0]<0):                       # ^
                                unit.offset[0] += 2
                                if(unit.offset[0]==0):
                                    if(unit.loc[0]==1 and unit.order in unit.prod_lg) or (unit.loc[0]==2 and unit.order in unit.prod_rg) or (unit.loc[0]==3 and unit.order in unit.prod_sm):
                                        if(unit.loc[1]<7):
                                            unit.dir = 3
                                        if(unit.loc[1]==7):
                                            unit.dir = 0
                                        if(unit.loc[1]>7):
                                            unit.dir = 1
                                        unit.task += 1
                            elif(unit.offset[1]>=0 and unit.dir==3):    # move down
                                unit.offset[1] += 2
                                if(unit.offset[1]>=32):
                                    unit.offset[1] -= 64
                                    unit.loc[1] += 1
                            elif(unit.offset[0]>=0 and unit.dir==0):    # move right
                                unit.offset[0] += 2
                                if(unit.offset[0]>=32):
                                    unit.offset[0] -= 64
                                    unit.loc[0] += 1
                        case 3: # bring order to pick-up counter
                            if(unit.dir==2):
                                if(unit.loc[1]<8):
                                    unit.dir = 3
                                if(unit.loc[1]==8):
                                    unit.dir = 0
                                if(unit.loc[1]>8):
                                    unit.dir = 1
                                i += 1
                                continue
                            if(unit.offset[0]<0):                   # centering
                                unit.offset[0] += 2
                                if(unit.offset[0]==0 and unit.loc[0]==5):
                                    self.objects.append(self.Obj(unit.order,[6,8]))
                                    unit.task += 1
                            elif(unit.offset[1]<0 and unit.dir==3): # ^
                                unit.offset[1] += 2
                                if(unit.offset[1]==0 and unit.loc[1]==8):
                                    unit.dir = 0
                            elif(unit.offset[1]>0 and unit.dir==1): # ^
                                unit.offset[1] -= 2
                                if(unit.offset[1]==0 and unit.loc[1]==8):
                                    unit.dir = 0
                            elif(unit.dir==0):                      # move right
                                unit.offset[0] += 2
                                if(unit.offset[0]>=32):
                                    unit.offset[0] -= 64
                                    unit.loc[0] += 1
                            elif(unit.dir==1):                      # move up
                                unit.offset[1] -= 2
                                if(unit.offset[1]<=-32):
                                    unit.offset[1] += 64
                                    unit.loc[1] -= 1
                            elif(unit.dir==3):                      # move down
                                unit.offset[1] += 2
                                if(unit.offset[1]>=32):
                                    unit.offset[1] -= 64
                                    unit.loc[1] += 1
                        case 4: # announce order
                            unit.patience -= 1
                            if(unit.patience <= 0):
                                unit.task += 1
                        case 5: # wait for order pick-up
                            for c in self.customers:
                                if(c.task==7 and c.loc[0]==7 and c.loc[1]==8 and c.order==unit.order):
                                    # give customer order
                                    for o in self.objects:
                                        if(o.loc[0]==6 and o.loc[1]==8 and o.ID==c.order):
                                            o.loc[0] = -1
                                            o.loc[1] = -1
                                            break
                                    unit.task = 0
                                    unit.patience = 20
                                    break
                case 2: # clean tables
                    match(unit.task):
                        case 0: # wait for cups to be left on table
                            unit.dir = 3
                            for o in self.objects:
                                if(o.ID in [84,85,86]):
                                    unit.orderLoc = [o.loc[0],o.loc[1]]
                                    unit.task += 1
                                    break
                        case 1: # walk toward cup
                            if(unit.offset[1]<0):                   # centering
                                unit.offset[1] += 2
                                if(unit.offset[1]==0):
                                    if(unit.loc[1]==2 and unit.orderLoc[0]==unit.loc[0]-3):
                                        unit.dir = 2
                                    elif(unit.loc[1]==2 and unit.orderLoc[0]==unit.loc[0]+3):
                                        unit.dir = 0
                                    elif(unit.loc[1]==unit.orderLoc[1]):
                                        unit.dir = 0 if(unit.loc[0]<unit.orderLoc[0]) else 2
                                        unit.task += 1
                            elif(unit.dir==0 and unit.offset[0]<0): # ^
                                unit.offset[0] += 2
                                if(unit.offset[0]==0 and unit.loc[0]==19):
                                    unit.dir = 3
                            elif(unit.dir==2 and unit.offset[0]>0): # ^
                                unit.offset[0] -= 2
                                if(unit.offset[0]==0 and unit.loc[0]==10):
                                    unit.dir = 3
                            elif(unit.dir==3):                      # walk down
                                unit.offset[1] += 2
                                if(unit.offset[1]>=32):
                                    unit.offset[1] -= 64
                                    unit.loc[1] += 1
                            elif(unit.dir==0):                      # walk right
                                unit.offset[0] += 2
                                if(unit.offset[0]>=32):
                                    unit.offset[0] -= 64
                                    unit.loc[0] += 1
                            elif(unit.dir==2):                      # walk left
                                unit.offset[0] -= 2
                                if(unit.offset[0]<=-32):
                                    unit.offset[0] += 64
                                    unit.loc[0] -= 1
                        case 2: # grab cup
                            if(unit.dir==0 and unit.offset[0]<0):   # centering
                                unit.offset[0] += 2
                                if(unit.offset[0]==0):
                                    if(unit.loc[0]==11 or unit.loc[0]==16):
                                        for o in self.objects:
                                            if(o.loc[0]==unit.orderLoc[0] and o.loc[1]==unit.orderLoc[1]):
                                                o.loc[0] = -1
                                                o.loc[1] = -1
                                                unit.dir = 2
                                                break
                                    elif(unit.loc[0]==15):
                                        unit.dir = 1
                                        unit.task += 1
                            elif(unit.dir==2 and unit.offset[0]>0): # ^
                                unit.offset[0] -= 2
                                if(unit.offset[0]==0):
                                    if(unit.loc[0]==14):
                                        for o in self.objects:
                                            if(o.loc[0]==unit.orderLoc[0] and o.loc[1]==unit.orderLoc[1]):
                                                o.loc[0] = -1
                                                o.loc[1] = -1
                                                unit.dir = 0
                                                break
                                    elif(unit.loc[0]==10 or unit.loc[0]==15):
                                        unit.dir = 1
                                        unit.task += 1   
                            elif(unit.dir==0):                      # move right
                                unit.offset[0] += 2
                                if(unit.offset[0]>=32):
                                    unit.offset[0] -= 64
                                    unit.loc[0] += 1
                            elif(unit.dir==2):                      # move left
                                if(unit.loc[0]==19):
                                    for o in self.objects:
                                        if(o.loc[0]==unit.orderLoc[0] and o.loc[1]==unit.orderLoc[1]):
                                            o.loc[0] = -1
                                            o.loc[1] = -1
                                            unit.dir = 1
                                            unit.task += 1
                                            break                                    
                                else:
                                    unit.offset[0] -= 2
                                    if(unit.offset[0]<=-32):
                                        unit.offset[0] += 64
                                        unit.loc[0] -= 1
                        case 3: # throw out cup
                            if(unit.offset[1]>0):                   # centering
                                unit.offset[1] -= 2
                                if(unit.offset[1]==0):
                                    if(unit.loc[1]==2 and unit.loc[0]!=19):
                                        unit.dir = 0
                                    elif(unit.loc[1]==1):
                                        unit.dir = 3
                                        unit.task = 0
                            elif(unit.dir==0 and unit.offset[0]<0): # ^
                                unit.offset[0] += 2
                                if(unit.offset[0]==0 and unit.loc[0]==19):
                                    unit.dir = 1
                            elif(unit.dir==2 and unit.offset[0]>0): # ^
                                unit.offset[0] -= 2
                                if(unit.offset[0]==0 and unit.loc[0]==15):
                                    unit.dir = 1
                            elif(unit.dir==1):                      # move up
                                if(unit.loc[0]==19 and unit.loc[1]==2):
                                    unit.dir = 2
                                else:
                                    unit.offset[1] -= 2
                                    if(unit.offset[1]<=-32):
                                        unit.offset[1] += 64
                                        unit.loc[1] -=1
                            elif(unit.dir==0):                      # move right
                                unit.offset[0] += 2
                                if(unit.offset[0]>=32):
                                    unit.offset[0] -= 64
                                    unit.loc[0] += 1
                            elif(unit.dir==2):                      # move left
                                unit.offset[0] -=2
                                if(unit.offset[0]<=-32):
                                    unit.offset[0] += 64
                                    unit.loc[0] -= 1
            i += 1
        # check for deleted customers
        i = 0
        while(i<len(self.customers)):
            if(self.customers[i].loc[0]==-1 and self.customers[i].loc[1]==-1):
                del self.customers[i]
                continue
            i += 1
        # check for deleted objects
        i = 0
        while(i<len(self.objects)):
            if(self.objects[i].loc[0]==-1 and self.objects[i].loc[1]==-1):
                del self.objects[i]
                continue
            i += 1
        self.draw(False)
    
    def newSim(self): # Resets sim and sim data in preparation for a new game
        # code to reset all save data
        # for now, just reset money and supply amounts/goals, product prices should ideally be reset as well
        # call reset objects in settings
        self.settingsRef.resetObjects()
        # build objects lists in simData if they don't exist
        if(len(self.simDataRef.supplies)==0):
            sups = self.settingsRef.getSups()
            for s in sups:
                self.simDataRef.addSupply(s[0],s[1])
        if(len(self.simDataRef.products)==0):
            prods = self.settingsRef.getProds()
            for p in prods:
                self.simDataRef.addProduct(p[0],p[1])
        # call erase history in sim_data
        self.simDataRef.eraseHistory()
        # add one day of history so the graphs can display something
        for s in self.simDataRef.supplies:
            s.history.append([self.settingsRef.getSupPrice(s.ID),self.settingsRef.getSupGoal(s.ID),0,0,self.settingsRef.getSupGoal(s.ID)])
        for p in self.simDataRef.products:
            p.history.append([self.settingsRef.getProdPrice(p.ID),0,self.settingsRef.getProdSupCost(p.ID)])
        # prepare to run the sim again
        self.continueSim()
    def continueSim(self): # Prepares sim for a new day
        # delete all customers
        while(len(self.customers)>0):
            del self.customers[0]
        # delete all employees
        while(len(self.employees)>0):
            del self.employees[0]
        # delete all objects
        while(len(self.objects)>0):
            del self.objects[0]
        # reset all product/order data
        while(len(self.prod_order)>0):
            del self.prod_order[0]
        for i in range(len(self.shelfSpace)):
            self.shelfSpace[i] = 0
        # spawn new
        self.customers.append(self.Cust(random.randint(0,3),[-1,1],self.acDataRef.getRndProd(random.randint(0,14)),1)) # spawn a customer off screen, wanting a reg Dark Hot Chocolate, with the task of walking into the shop to order
        self.employees.append(self.Emp(random.randint(0,3),[5,4],0,0)) # spawn an employee to take orders, with the task of waiting for a customer to order
        self.employees.append(self.Emp(random.randint(0,3),[5,8],1,0)) # spawn an employee to give orders, with the task of waiting for an order to be made
        self.employees.append(self.Emp(random.randint(0,3),[15,1],2,0)) # spawn an employee to clean tables, with the task of waiting for food to be left on the table
        self.time = self.maxTime
        self.points = 0
        self.profit = 0.00
        
        # reset supply/product menus in settings
        self.settingsRef.resetMenus()
        
        # grab supply/product information needed for the day
        self.supplies = []
        self.products = []
        self.transactions = []
        self.simDataRef.clearTransactions()
        lst = self.settingsRef.getSups()
        ID = 0
        price = 0
        goal = 0
        ordered, current = 0,0
        used = 0
        for s in lst:
            ID = s[0]
            price = self.settingsRef.getSupPrice(ID)
            goal = self.settingsRef.getSupGoal(ID)
            ordered, current = self.settingsRef.orderSupply(ID)
            used = 0            
            self.supplies.append([ID,price,goal,ordered,current,used])
        lst = self.settingsRef.getProds()
        for p in lst:
            ID = p[0]
            price = self.settingsRef.getProdPrice(ID)
            ordered = 0 # sales, but reusing a variable
            pSups = self.settingsRef.getProdSups(ID)
            self.products.append([ID,price,ordered,pSups])
        self.transactions.append([0,self.settingsRef.getMoney(),0,0])
    def runSim(self):
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
                                    self.customers.append(self.Cust(random.randint(0,3),[-1,1],self.acDataRef.getRndProd(random.randint(0,14)),1))
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
                            if((c.task>0 and c.task<4) and c.loc[0] == 7 and c.loc[1] == 4):
                                space = False
                                break
                        if(space):
                            unit.offset[0] -= 2
                            if(unit.offset[0]<=-32):
                                unit.offset[0] += 64
                                unit.loc[0] -= 1
                case 2: # order animation
                    if(unit.patience>=600):
                        unit.patience -= 1
                    else:
                        unit.task += 1
                case 3: # ordering
                    unit.patience -= 1
                    if(self.mouseXY[0]==7 and self.mouseXY[1]==3 and self.lftClkSt==1):
                        for e in self.employees:
                            if(e.job==0 and e.task==0 and e.loc[0]==5 and e.loc[1]==4):
                                # see if we can order the product
                                canOrder, profit = self.orderProduct(unit.order)
                                if(canOrder):
                                    unit.task += 1
                                    unit.dir = 3
                                    self.points += int((float(unit.patience)/600.0)*self.pointMax)
                                    self.transactions.append([self.maxTime-self.time,profit,profit,int((float(unit.patience)/600.0)*self.pointMax)])
                                else:
                                    unit.patience = 0
                                break
                    if(unit.patience<=0 and unit.task!=4):
                        unit.task = 9 # exiting
                        unit.dir = 1 # face north
                        if(self.time>0): # only calculate points/profits if there is still time
                            self.points -= int(self.pointMax)
                            self.transactions.append([self.maxTime-self.time,0,0,-1*int(self.pointMax)])
                case 4: # walking to the pick-up line
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
                case 5: # pick-up line
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
                            if((c.task==5 or c.task==6) and c.loc[0] == unit.loc[0]-1 and c.loc[1] == 8):
                                space = False
                                break
                        if(space):
                            unit.offset[0] -= 2
                            if(unit.offset[0]<=-32):
                                unit.offset[0] += 64
                                unit.loc[0] -= 1
                case 6: # picking up order
                    if(self.mouseXY[0]==5 and self.mouseXY[1]==7 and self.lftClkSt==1):
                        for e in self.employees:
                            if(e.job==1 and e.task==5 and e.loc[0]==5 and e.loc[1]==8):
                                unit.task += 1
                                unit.dir = 3
                                if(self.time>0): # only calculate points/profit if there is still time
                                    self.points += int(self.pointMax/4)
                                    self.transactions.append([self.maxTime-self.time,0,0,int(self.pointMax/4)])
                case 7: # finding a seat
                    if(unit.offset[0]<0):                                                   # centering onto current tile
                        unit.offset[0] += 2
                        if(unit.offset[0]==0 and (unit.loc[0] == 10 or unit.loc[0] == 19)):     # start walking up
                            unit.dir = 1
                            if(unit.loc[0]==10): # check if the very first seat is available first
                                spaceR = True
                                for c in self.customers:
                                    if(c.task==8 and c.loc[0]==unit.loc[0]+1 and c.loc[1]==unit.loc[1]): # someone is sitting there
                                        spaceR = False
                                        break
                                    if(spaceR and c.task==8 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==0): # someone is planning on sitting there
                                        spaceR = False
                                        break
                                if(spaceR):
                                    for o in self.objects:
                                        if(o.loc[0]==unit.loc[0]+2 and o.loc[1]==unit.loc[1]): # someone left their food there
                                            spaceR = False
                                            break
                                if(spaceR):
                                    unit.task += 1
                                    unit.dir = 0
                                    unit.patience = 300
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
                                if(c.task==8 and c.loc[0]==unit.loc[0]-1 and c.loc[1]==unit.loc[1]):
                                    spaceL = False
                                    continue
                                if(spaceL and c.task==8 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==2):
                                    spaceL = False
                                    continue
                                if(c.task==8 and c.loc[0]==unit.loc[0]+1 and c.loc[1]==unit.loc[1]):
                                    spaceR = False
                                    continue
                                if(spaceR and c.task==8 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==0):
                                    spaceR = False
                                    continue
                            if(spaceL or spaceR):
                                for o in self.objects:
                                    if(o.loc[0]==unit.loc[0]-2 and o.loc[1]==unit.loc[1]): # someone left their food there
                                        spaceL = False
                                        continue
                                    if(o.loc[0]==unit.loc[0]+2 and o.loc[1]==unit.loc[1]): # someone left their food there
                                        spaceR = False
                                        continue
                            if(spaceL):
                                unit.task += 1
                                unit.dir = 2
                                unit.patience = 300
                            elif(spaceR):
                                unit.task += 1
                                unit.dir = 0
                                unit.patience = 300
                    elif(unit.offset[1]>0 and (unit.loc[0] == 10 or unit.loc[0] == 19)):    # ^
                        unit.offset[1] -= 2
                        if(unit.offset[1]==0 and (unit.loc[0] == 10 or unit.loc[0] == 19) and unit.loc[1] == 2):    # start walking right
                            unit.dir = 0
                            if(unit.loc[0]==19): # leave the shop
                                unit.task += 2
                        elif(unit.offset[1]==0 and unit.loc[0]==10):                                                # look for a seat on the right
                            spaceR = True
                            for c in self.customers:
                                if(c.task==8 and c.loc[0]==unit.loc[0]+1 and c.loc[1]==unit.loc[1]):
                                    spaceR = False
                                    break
                                if(spaceR and c.task==8 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==0):
                                    spaceR = False
                                    break
                            if(spaceR):
                                for o in self.objects:
                                    if(o.loc[0]==unit.loc[0]+2 and o.loc[1]==unit.loc[1]):
                                        spaceR = False
                                        break
                            if(spaceR):
                                unit.task += 1
                                unit.dir = 0
                                unit.patience = 300
                        elif(unit.offset[1]==0 and unit.loc[0]==19):                                                # look for a seat on the left
                            spaceL = True
                            for c in self.customers:
                                if(c.task==8 and c.loc[0]==unit.loc[0]-1 and c.loc[1]==unit.loc[1]):
                                    spaceL = False
                                    break
                                if(spaceL and c.task==8 and c.loc[0]==unit.loc[0] and c.loc[1]==unit.loc[1] and c.dir==2):
                                    spaceL = False
                                    break
                            if(spaceL):
                                for o in self.objects:
                                    if(o.loc[0]==unit.loc[0]-1 and o.loc[1]==unit.loc[1]):
                                        spaceL = False
                                        break
                            if(spaceL):
                                unit.task += 1
                                unit.dir = 2
                                unit.patience = 300
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
                case 8: # sitting down / eating
                    if(unit.offset[0]==0 and (unit.loc[0]==11 or unit.loc[0]==14 or unit.loc[0]==16 or unit.loc[0]==19)):   # eat food
                        if(unit.patience==300):
                            self.objects.append(self.Obj(unit.order,[unit.loc[0]+(1 if unit.dir==0 else -1),unit.loc[1]]))
                        unit.patience -= 1
                        if(unit.patience<=0):
                            for o in self.objects: # turn full cups into empty cups
                                if(o.loc[0]==unit.loc[0]+(1 if unit.dir==0 else -1) and o.loc[1]==unit.loc[1]):
                                    if(o.ID in self.Emp.prod_lg):
                                        o.ID = 86
                                        break
                                    elif(o.ID in self.Emp.prod_rg):
                                        o.ID = 85
                                        break
                                    elif(o.ID in self.Emp.prod_sm):
                                        o.ID = 84
                                        break
                                    else:
                                        o.loc[0] = -1
                                        o.loc[1] = -1
                                        break
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
                case 9: # exiting
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
                                    if(c.task==4 and c.loc[0]==7 and c.loc[1]==4):
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
                                        unit.task += 1
                            elif(unit.offset[1]>0 and unit.dir==1): # ^
                                unit.offset[1] -= 2
                                if(unit.offset[1]==0 and unit.loc[1]==3):
                                    if(unit.order in unit.sup_cof and unit.loc[0]==1) or (unit.order in unit.sup_tea and unit.loc[0]==2) or (unit.order in unit.sup_coco and unit.loc[0]==3) or (unit.order in unit.sup_syr and unit.loc[0]==4) or (unit.order in unit.sup_pas and unit.loc[0]==5):
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
                            if(unit.orderLoc==-1): # vertical offset from top of shelf, indicating where to place product
                                                   # if -1, no space, don't move
                                                   # otherwise, location is [0,4+space]
                                if(unit.order in unit.prod_wet):
                                    j = 0
                                    while(j<3):
                                        if(self.shelfSpace[j]==0):
                                            unit.orderLoc = j
                                            break
                                        j += 1
                                elif(unit.order in unit.prod_dry):
                                    j = 3
                                    while(j<5):
                                        if(self.shelfSpace[j]==0):
                                            unit.orderLoc = j
                                            break
                                        j += 1
                            # try to move if there is room to place the product
                            if(unit.orderLoc<0):                        # move on to next unit, this one cannot do anything this frame
                                i += 1
                                continue
                            if(unit.dir<2):                             # turn around and take 1 frame to do so
                                unit.dir += 2
                                i += 1
                                continue
                            if(unit.offset[1]<0):                       # centering
                                unit.offset[1] += 2
                                if(unit.offset[1]==0 and unit.loc[1]==unit.orderLoc+4):
                                    unit.dir = 2
                                    unit.offset[0] += 2
                            if(unit.offset[0]>0):                       # ^
                                unit.offset[0] -= 2
                                if(unit.offset[0]==0):
                                    if(unit.loc[0]==1):     # we are in front of the space to place the product
                                        # place product
                                        self.objects.append(self.Obj(unit.order,[0,unit.loc[1]]) )
                                        # update shelf space
                                        self.shelfSpace[unit.loc[1]-4] = 1
                                        # inform other employee of order
                                        self.prod_order.append(unit.order)
                                        unit.task += 1
                                        unit.dir = 1
                                        unit.orderLoc = -1
                                        if(unit.loc[1]==4):
                                            unit.dir = 0
                                    elif(unit.loc[1]==3):   # double check that we are in front of the correct product location
                                        if(unit.loc[1]!=unit.orderLoc+4):
                                            unit.dir = 3
                            elif(unit.offset[0]<=0 and unit.dir==2):    # walk left
                                unit.offset[0] -= 2
                                if(unit.offset[0]<=-32):
                                    unit.offset[0] += 64
                                    unit.loc[0] -= 1
                            elif(unit.offset[1]>=0 and unit.dir==3):    # walk down
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
                    match(unit.task):
                        case 0: # wait for an order to be ready
                            if(len(self.prod_order)!=0):
                                unit.task += 1
                                unit.dir = 2
                        case 1: # grab order from back counter
                            if(unit.offset[0]>0):                       # centering
                                unit.offset[0] -= 2
                                if(unit.offset[0]==0):
                                    if(unit.loc[0]==1):
                                        unit.dir = 1
                                        unit.offset[1] += 2 # push down so that next centering will automatically trigger and check for an object
                            if(unit.offset[1]>0):                       # ^
                                unit.offset[1] -= 2
                                if(unit.offset[1]==0):
                                    for o in self.objects:
                                        if(o.loc[0]==0 and o.loc[1]==unit.loc[1] and o.ID==self.prod_order[0]):
                                            unit.dir = 2
                                            # grab object
                                            o.loc[0] = -1
                                            o.loc[1] = -1
                                            unit.order = o.ID
                                            # update shelfSpace
                                            self.shelfSpace[unit.loc[1]-4] = 0
                                            # update prod_order
                                            del self.prod_order[0]
                                            unit.task += 1
                                            if(unit.order in unit.prod_dry): # skip putting it in a cup if it's dry
                                                unit.task += 1
                                            break
                            elif(unit.offset[0]<=0 and unit.dir==2):    # move left
                                unit.offset[0] -= 2
                                if(unit.offset[0]<=-32):
                                    unit.offset[0] += 64
                                    unit.loc[0] -= 1
                            elif(unit.offset[1]<=0 and unit.dir==1):    # move right
                                unit.offset[1] -= 2
                                if(unit.offset[1]<=-32):
                                    unit.offset[1] += 64
                                    unit.loc[1] -= 1
                        case 2: # put order in cup
                            if(unit.dir==2): # take one frame to turn south
                                unit.dir += 1
                                i += 1
                                continue
                            if(unit.offset[1]<0):                       # centering
                                unit.offset[1] += 2
                                if(unit.offset[1]==0 and unit.loc[1]==9):
                                    unit.dir = 0
                                    unit.offset[0] -= 2
                            if(unit.offset[0]<0):                       # ^
                                unit.offset[0] += 2
                                if(unit.offset[0]==0):
                                    if(unit.loc[0]==1 and unit.order in unit.prod_lg) or (unit.loc[0]==2 and unit.order in unit.prod_rg) or (unit.loc[0]==3 and unit.order in unit.prod_sm):
                                        if(unit.loc[1]<7):
                                            unit.dir = 3
                                        if(unit.loc[1]==7):
                                            unit.dir = 0
                                        if(unit.loc[1]>7):
                                            unit.dir = 1
                                        unit.task += 1
                            elif(unit.offset[1]>=0 and unit.dir==3):    # move down
                                unit.offset[1] += 2
                                if(unit.offset[1]>=32):
                                    unit.offset[1] -= 64
                                    unit.loc[1] += 1
                            elif(unit.offset[0]>=0 and unit.dir==0):    # move right
                                unit.offset[0] += 2
                                if(unit.offset[0]>=32):
                                    unit.offset[0] -= 64
                                    unit.loc[0] += 1
                        case 3: # bring order to pick-up counter
                            if(unit.dir==2):
                                if(unit.loc[1]<8):
                                    unit.dir = 3
                                if(unit.loc[1]==8):
                                    unit.dir = 0
                                if(unit.loc[1]>8):
                                    unit.dir = 1
                                i += 1
                                continue
                            if(unit.offset[0]<0):                   # centering
                                unit.offset[0] += 2
                                if(unit.offset[0]==0 and unit.loc[0]==5):
                                    self.objects.append(self.Obj(unit.order,[6,8]))
                                    unit.task += 1
                            elif(unit.offset[1]<0 and unit.dir==3): # ^
                                unit.offset[1] += 2
                                if(unit.offset[1]==0 and unit.loc[1]==8):
                                    unit.dir = 0
                            elif(unit.offset[1]>0 and unit.dir==1): # ^
                                unit.offset[1] -= 2
                                if(unit.offset[1]==0 and unit.loc[1]==8):
                                    unit.dir = 0
                            elif(unit.dir==0):                      # move right
                                unit.offset[0] += 2
                                if(unit.offset[0]>=32):
                                    unit.offset[0] -= 64
                                    unit.loc[0] += 1
                            elif(unit.dir==1):                      # move up
                                unit.offset[1] -= 2
                                if(unit.offset[1]<=-32):
                                    unit.offset[1] += 64
                                    unit.loc[1] -= 1
                            elif(unit.dir==3):                      # move down
                                unit.offset[1] += 2
                                if(unit.offset[1]>=32):
                                    unit.offset[1] -= 64
                                    unit.loc[1] += 1
                        case 4: # announce order
                            unit.patience -= 1
                            if(unit.patience <= 0):
                                unit.task += 1
                        case 5: # wait for order pick-up
                            if(self.mouseXY[0]==5 and self.mouseXY[1]==7 and self.lftClkSt==1):
                                for c in self.customers:
                                    if(c.task==7 and c.loc[0]==7 and c.loc[1]==8 and c.order==unit.order):
                                        # give customer order
                                        for o in self.objects:
                                            if(o.loc[0]==6 and o.loc[1]==8 and o.ID==c.order):
                                                o.loc[0] = -1
                                                o.loc[1] = -1
                                                break
                                        break
                                unit.task = 0
                                unit.patience = 20
                case 2: # clean tables
                    match(unit.task):
                        case 0: # wait for cups to be left on table
                            unit.dir = 3
                            for o in self.objects:
                                if(o.ID in [84,85,86]):
                                    unit.orderLoc = [o.loc[0],o.loc[1]]
                                    unit.task += 1
                                    break
                        case 1: # walk toward cup
                            if(unit.offset[1]<0):                   # centering
                                unit.offset[1] += 2
                                if(unit.offset[1]==0):
                                    if(unit.loc[1]==2 and unit.orderLoc[0]==unit.loc[0]-3):
                                        unit.dir = 2
                                    elif(unit.loc[1]==2 and unit.orderLoc[0]==unit.loc[0]+3):
                                        unit.dir = 0
                                    elif(unit.loc[1]==unit.orderLoc[1]):
                                        unit.dir = 0 if(unit.loc[0]<unit.orderLoc[0]) else 2
                                        unit.task += 1
                            elif(unit.dir==0 and unit.offset[0]<0): # ^
                                unit.offset[0] += 2
                                if(unit.offset[0]==0 and unit.loc[0]==19):
                                    unit.dir = 3
                            elif(unit.dir==2 and unit.offset[0]>0): # ^
                                unit.offset[0] -= 2
                                if(unit.offset[0]==0 and unit.loc[0]==10):
                                    unit.dir = 3
                            elif(unit.dir==3):                      # walk down
                                unit.offset[1] += 2
                                if(unit.offset[1]>=32):
                                    unit.offset[1] -= 64
                                    unit.loc[1] += 1
                            elif(unit.dir==0):                      # walk right
                                unit.offset[0] += 2
                                if(unit.offset[0]>=32):
                                    unit.offset[0] -= 64
                                    unit.loc[0] += 1
                            elif(unit.dir==2):                      # walk left
                                unit.offset[0] -= 2
                                if(unit.offset[0]<=-32):
                                    unit.offset[0] += 64
                                    unit.loc[0] -= 1
                        case 2: # grab cup
                            if(unit.dir==0 and unit.offset[0]<0):   # centering
                                unit.offset[0] += 2
                                if(unit.offset[0]==0):
                                    if(unit.loc[0]==11 or unit.loc[0]==16):
                                        for o in self.objects:
                                            if(o.loc[0]==unit.orderLoc[0] and o.loc[1]==unit.orderLoc[1]):
                                                o.loc[0] = -1
                                                o.loc[1] = -1
                                                unit.dir = 2
                                                break
                                    elif(unit.loc[0]==15):
                                        unit.dir = 1
                                        unit.task += 1
                            elif(unit.dir==2 and unit.offset[0]>0): # ^
                                unit.offset[0] -= 2
                                if(unit.offset[0]==0):
                                    if(unit.loc[0]==14):
                                        for o in self.objects:
                                            if(o.loc[0]==unit.orderLoc[0] and o.loc[1]==unit.orderLoc[1]):
                                                o.loc[0] = -1
                                                o.loc[1] = -1
                                                unit.dir = 0
                                                break
                                    elif(unit.loc[0]==10 or unit.loc[0]==15):
                                        unit.dir = 1
                                        unit.task += 1   
                            elif(unit.dir==0):                      # move right
                                unit.offset[0] += 2
                                if(unit.offset[0]>=32):
                                    unit.offset[0] -= 64
                                    unit.loc[0] += 1
                            elif(unit.dir==2):                      # move left
                                if(unit.loc[0]==19):
                                    for o in self.objects:
                                        if(o.loc[0]==unit.orderLoc[0] and o.loc[1]==unit.orderLoc[1]):
                                            o.loc[0] = -1
                                            o.loc[1] = -1
                                            unit.dir = 1
                                            unit.task += 1
                                            break                                    
                                else:
                                    unit.offset[0] -= 2
                                    if(unit.offset[0]<=-32):
                                        unit.offset[0] += 64
                                        unit.loc[0] -= 1
                        case 3: # throw out cup
                            if(unit.offset[1]>0):                   # centering
                                unit.offset[1] -= 2
                                if(unit.offset[1]==0):
                                    if(unit.loc[1]==2 and unit.loc[0]!=19):
                                        unit.dir = 0
                                    elif(unit.loc[1]==1):
                                        unit.dir = 3
                                        unit.task = 0
                            elif(unit.dir==0 and unit.offset[0]<0): # ^
                                unit.offset[0] += 2
                                if(unit.offset[0]==0 and unit.loc[0]==19):
                                    unit.dir = 1
                            elif(unit.dir==2 and unit.offset[0]>0): # ^
                                unit.offset[0] -= 2
                                if(unit.offset[0]==0 and unit.loc[0]==15):
                                    unit.dir = 1
                            elif(unit.dir==1):                      # move up
                                if(unit.loc[0]==19 and unit.loc[1]==2):
                                    unit.dir = 2
                                else:
                                    unit.offset[1] -= 2
                                    if(unit.offset[1]<=-32):
                                        unit.offset[1] += 64
                                        unit.loc[1] -=1
                            elif(unit.dir==0):                      # move right
                                unit.offset[0] += 2
                                if(unit.offset[0]>=32):
                                    unit.offset[0] -= 64
                                    unit.loc[0] += 1
                            elif(unit.dir==2):                      # move left
                                unit.offset[0] -=2
                                if(unit.offset[0]<=-32):
                                    unit.offset[0] += 64
                                    unit.loc[0] -= 1
            i += 1
        # check for deleted customers
        i = 0
        while(i<len(self.customers)):
            if(self.customers[i].loc[0]==-1 and self.customers[i].loc[1]==-1):
                del self.customers[i]
                continue
            i += 1
        # check for deleted objects
        i = 0
        while(i<len(self.objects)):
            if(self.objects[i].loc[0]==-1 and self.objects[i].loc[1]==-1):
                del self.objects[i]
                continue
            i += 1
        self.draw(True)
        if(self.time>0):
            self.time -= 1
        if(self.time==0): # compile and send the day's data to simData
            # price, goal amounts, and ordered amounts for supplies need to be obtained at the start of a simulated day
                # used amounts for each supply need to be tracked throughout the day as products are ordered
                # if there is not enough of a supply for a product, the customer should be turned away when they are clicked
            # price and supply cost for products need to be obtained at the start of a simulated day
                # sales for products need to be tracked throughout the day as they are ordered
            # at the end of the day, these values need to be compiled and reported as new history entries in SimData
            for s in self.supplies:
                self.simDataRef.addSupplyHistory(s[0],s[1],s[2],s[3],s[5],s[4])
                self.settingsRef.useSupply(s[0],s[5])
            for p in self.products:
                self.simDataRef.addProductHistory(p[0],p[1],p[2],self.settingsRef.getProdSupCost(p[0]))
                self.settingsRef.earnMoney(p[1]*p[2])
            for t in self.transactions:
                self.simDataRef.addTransaction(t[0],t[1],t[2],t[3])
            self.time = -1
    def orderProduct(self,ID):
        # when a product is ordered, the list of supplies and their amounts need to be retrieved from Settings
            # check each supply amount against the amount of supplies available that day (this amount should be tracked)
            # if there is enough of all the supplies:
                # subtract the product amounts from each of them, add the price of the product to the day's profits (this value should be tracked), approve the order in the sim
        success = True
        profit = 0.0
        for p in self.products:
            if(p[0]==ID):
                for ps in p[3]: # go through each supply/amount to make sure there is enough
                    if(not success):
                        break
                    for s in self.supplies:
                        if(s[0]==ps[0] and s[4]<ps[1]): # if the supplies match and there is less in stock than there is required
                            success = False
                            break
                break
        if(success): # now go through each supply/amount again to actually make the order
            for p in self.products:
                if(p[0]==ID):
                    self.profit += p[1] # record the profit from selling a product
                    p[2] += 1 # record a sale of the product
                    profit = p[1] # record the profit so the customer can record a transaction
                    for ps in p[3]: # go through each supply/amount to make sure there is enough
                        for s in self.supplies:
                            if(s[0]==ps[0]): # we know that there is enough of the supply now, so we can order
                                s[4] -= ps[1] # subtract the amount used for the product from the total supply
                                s[5] += ps[1] # record the amount used for the product
                                break
                    break            
        return success, profit
    def storeInputs(self,MouseXY,lftClk): # Takes user input and converts them into a better format for the Sim to use
        self.mouseXY = [int(MouseXY[0]/(16*self.SCALE)),int(MouseXY[1]/(16*self.SCALE))] #scale down to the 20x12 grid of the simulation (first and last 16x are offscreen and ignored)
        if(self.lftClkSt==0 and lftClk): # mouse was clicked
            self.lftClkSt = 1
            return
        if(self.lftClkSt==1 and lftClk): # mouse is held down
            self.lftClkSt = 2
            return
        if(self.lftClkSt>0 and not lftClk): # mouse was unclicked
            self.lftClkSt = 0
            return
    
    def ticksToString(self, time): # Determines the sim time in 12-hour format based on the number of ticks passed.
        timeRemaining = time/self.maxTime
        minutesPassed = (1-timeRemaining)*self.hoursInDay*60
        startMinute = self.startHour*60
        currentMinute = startMinute + minutesPassed # Minutes past midnight.
        
        minutePortion = currentMinute % 60
        # maybe looks cleaner without minutes buzzing about
        minutePortion = 0
        hourPortion = currentMinute // 60
        ampm = "am"
        if hourPortion >= 12:
            ampm = "pm"
            hourPortion -= 12
        if hourPortion == 0:
            hourPortion = 12
        
        # :02d ensures min width of two digits.
        return f"{int(hourPortion):02d}:{int(minutePortion):02d}{ampm}"
    
    def draw(self,drawHud): # Draws the simulation to the screen.
        # Color Constants
        BLUE = (18,83,175)
        
        # Draw coffee shop building:
        self.surface.blit(self.floorPlan, [0,0])
        
        # Draw HUD:
        if(drawHud):
            # Draw HUD
            self.surface.blit(self.hud, [0,0])
            # Draw Time-Remaining Bar:
            pygame.draw.rect(self.surface,BLUE,(4*self.SCALE,2*self.SCALE,int(152.0*(float(self.time)/self.maxTime))*self.SCALE,12*self.SCALE))
            self.surface.blit(self.tmr_cap, [4*self.SCALE + int(152.0*(float(self.time)/float(self.maxTime)))*self.SCALE,2*self.SCALE])
            # Draw HUD Text
            font = pygame.font.SysFont(None,40)
            timeText = self.ticksToString(self.time)
            profitText = f"{self.profit:.2f}"
            pointText = str(self.points)
            text = font.render(timeText,True,(0,0,0))
            self.surface.blit(text,[5*self.SCALE,4*self.SCALE])
            text = font.render(profitText,True,(0,0,0))
            self.surface.blit(text,[176*self.SCALE,4*self.SCALE])
            text = font.render(pointText,True,(0,0,0))
            self.surface.blit(text,[256*self.SCALE,4*self.SCALE])
        
        # Draw permanent objects:
        self.surface.blit(self.cof_bn,  [1*16*self.SCALE +3*self.SCALE,  2*16*self.SCALE +1*self.SCALE])
        self.surface.blit(self.tea_lvs, [2*16*self.SCALE +3*self.SCALE,  2*16*self.SCALE +1*self.SCALE])
        self.surface.blit(self.chk_pwd, [3*16*self.SCALE +3*self.SCALE,  2*16*self.SCALE +1*self.SCALE])
        self.surface.blit(self.syrp,    [4*16*self.SCALE +3*self.SCALE,  2*16*self.SCALE +1*self.SCALE])
        self.surface.blit(self.pstry,   [5*16*self.SCALE +3*self.SCALE,  2*16*self.SCALE +1*self.SCALE])
        self.surface.blit(self.mug,     [6*16*self.SCALE +3*self.SCALE,  5*16*self.SCALE +3*self.SCALE])
        self.surface.blit(self.bttl,    [6*16*self.SCALE +3*self.SCALE,  6*16*self.SCALE +3*self.SCALE])
        self.surface.blit(self.shrt,    [6*16*self.SCALE +3*self.SCALE,  7*16*self.SCALE +3*self.SCALE])
        self.surface.blit(self.cup_lg1, [1*16*self.SCALE +3*self.SCALE, 10*16*self.SCALE +5*self.SCALE])
        self.surface.blit(self.cup_rg1, [2*16*self.SCALE +3*self.SCALE, 10*16*self.SCALE +5*self.SCALE])
        self.surface.blit(self.cup_sm1, [3*16*self.SCALE +3*self.SCALE, 10*16*self.SCALE +5*self.SCALE])
        self.surface.blit(self.cof_mkr1,[0*16*self.SCALE +3*self.SCALE,  4*16*self.SCALE +3*self.SCALE])
        self.surface.blit(self.cof_mkr1,[0*16*self.SCALE +3*self.SCALE,  5*16*self.SCALE +3*self.SCALE])
        self.surface.blit(self.cof_mkr1,[0*16*self.SCALE +3*self.SCALE,  6*16*self.SCALE +3*self.SCALE])
        
        # Draw customers:
        custs = [[self.cust11,self.cust12,self.cust13,self.cust14],[self.cust21,self.cust22,self.cust23,self.cust24],[self.cust31,self.cust32,self.cust33,self.cust34],[self.cust41,self.cust42,self.cust43,self.cust44]]
        i = len(self.customers)-1 # draw customers newest to oldest so that oldest customers show up on top
        while(i>-1):
            unit = self.customers[i]
            self.surface.blit(custs[unit.ID][unit.dir],[unit.loc[0]*16*self.SCALE+unit.offset[0],unit.loc[1]*16*self.SCALE+unit.offset[1]])
            i -= 1
        
        # Draw employees:
        emps = [[self.emp11,self.emp12,self.emp13,self.emp14],[self.emp21,self.emp22,self.emp23,self.emp24],[self.emp31,self.emp32,self.emp33,self.emp34],[self.emp41,self.emp42,self.emp43,self.emp44]]
        for unit in self.employees:
            self.surface.blit(emps[unit.ID][unit.dir],[unit.loc[0]*16*self.SCALE+unit.offset[0],unit.loc[1]*16*self.SCALE+unit.offset[1]])
        
        # Draw objects:
        for o in self.objects:
            img = self.getObjImg(o.ID,o.loc[0])
            self.surface.blit(img,[o.loc[0]*16*self.SCALE +3*self.SCALE, o.loc[1]*16*self.SCALE +3*self.SCALE])
        
        # Draw order bubbles:
        for unit in self.customers:
            if(unit.task==2 or unit.task==3): # draw order bubble
                # bubble
                if(unit.patience>600):
                    self.bbl1.set_alpha(int(255.0*( ((20.0-float(unit.patience-600))/20.0) )))
                    self.surface.blit(self.bbl1,[unit.loc[0]*16*self.SCALE+unit.offset[0],(unit.loc[1]-1)*16*self.SCALE+unit.offset[1]])
                    self.bbl1.set_alpha(255.0)
                else:
                    i = int((1-(float(unit.patience)/600.0))*(40))
                    self.surface.blit(self.bubbles[i],[unit.loc[0]*16*self.SCALE+unit.offset[0],(unit.loc[1]-1)*16*self.SCALE+unit.offset[1]])
                # order
                img = self.getObjImg(unit.order,-1)
                img.set_alpha(int(255.0*( ((20.0-float(unit.patience-600))/20.0) if unit.patience>600 else (1.0) )))
                self.surface.blit(img,[unit.loc[0]*16*self.SCALE +3*self.SCALE,(unit.loc[1]-1)*16*self.SCALE +3*self.SCALE])
                img.set_alpha(255.0) # python means that img is a reference to the class image object, so we need to share it's opacity
        for unit in self.employees:
            if(unit.job==1 and unit.task>3): # draw order bubble
                # bubble
                self.bbl1.set_alpha(int(255.0*( (float(20.0-unit.patience)/20.0) if unit.patience>0 else (1.0) )))
                self.surface.blit(self.bbl1,[unit.loc[0]*16*self.SCALE+unit.offset[0],(unit.loc[1]-1)*16*self.SCALE+unit.offset[1]])
                self.bbl1.set_alpha(255.0)
                # order
                img = self.getObjImg(unit.order,-1)
                img.set_alpha(int(255.0*( (float(20.0-unit.patience)/20.0) if unit.patience>0 else (1.0) )))
                self.surface.blit(img,[unit.loc[0]*16*self.SCALE +3*self.SCALE,(unit.loc[1]-1)*16*self.SCALE +3*self.SCALE])
                img.set_alpha(255.0) # python means that img is a reference to the class image object, so we need to share it's opacity