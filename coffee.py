import math, random, pygame, sys, threading
from abc import ABC, abstractmethod                     # not sure why abstract classes need to be imported like this, but they do
# import class files
# IDE might complain that the file cannot be found, but it will still work
import progress_manager as pm, accuracy_data as ac, settings as st, sim as sm


gameIntro = 0
gameMainMenu = 1
gameSettings = 2
gameSim = 3
gameEndDay = 4
gameMenu = 5
gameSupplyMenu = 6
gameProductMenu = 7


def main():
    # Pygame Initialization
    pygame.init()                                           # initialize game engine
    
    SCALE = 4                                               # set scale factor for graphics
    W=320*SCALE                                             # set window size
    H=180*SCALE
    size=(W,H)
    surface = pygame.display.set_mode(size)
    
    pygame.display.set_caption("Coffee Shop Simulator")      # window title
    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)
    
    clock = pygame.time.Clock()                             # Manage timing for screen updates    


     # General Constants
    FPS = 60                   # FPS for animations (lower number to slow down).
    
    # Logo Animation Constants
    LOGO_FRAME_FADEIN = 60     # Frame where logo finishes fading in.
    LOGO_FRAME_FADEOUT = 120   # Frame where logo starts to fade out (jumps here if intro skipped).
    LOGO_FRAME_TOTAL = 180     # Frame length of logo animation.
    
    # Color Constants
    BLACK = (0,  0,    0)
    WHITE = (255,255,255)
    GREEN = (0,  230,  0)
    

    # Local  Variables
    data = ac.Accuracy_Data()              # create class objects
    progressBar = pm.Progress_Manager()
    settings = st.Settings()
    sim = sm.Sim(surface,SCALE)
    sim.acDataRef = data
    
    mouseXY = [0,0]
    mouseDown = False
    
    dataState = 0 # Indicates the state of the data processing. (0 = processing not started, 1 = processing sales data, 2 = processing supply data, 3 = processing done)

    gameState = gameIntro

    
    salesDataThread = threading.Thread(target=data.readSalesData, args=(settings,progressBar,))   # DO NOT INCLUDE PARENTHESIS ON TARGET FUNCTION    # ARGS MUST BE ITERABLE, INCLUDE EXTRA COMMA FOR ONLY 1 ARG
    supplyDataThread = threading.Thread(target=data.readSupplyData, args=(settings,progressBar,))
    
    # image files
    logo = pygame.image.load("assets/logo.png").convert_alpha(surface)

    logoFrame = 0.0 # Elapsed frames since game start.

    
    mainMenuBg = pygame.image.load("assets/Main Menu.png").convert_alpha()
    settingsMenuBg = pygame.image.load("assets/Settings.png").convert_alpha()
    endDayBg = pygame.image.load("assets/EndofDay Menu.png").convert_alpha()
    gameMenuBg = pygame.image.load("assets/Game Menu.png").convert_alpha()
    productMenubg = pygame.image.load("assets/Product Menu.png").convert_alpha()
    supplyMenubg = pygame.image.load("assets/Supply Menu.png").convert_alpha()

    # mainMenu
    playBtn = pygame.Rect(512, 276, 256, 64)
    settingsBtn = pygame.Rect(512, 424, 256, 64)
    quitBtn = pygame.Rect(512, 572, 256, 64)
    #settingsMenu
    resetBtn = pygame.Rect(512, 528, 256, 64)
    settingsBackBtn = pygame.Rect(512, 628, 256, 64)
    #gameMenu
    newGameBtn = pygame.Rect(512, 276, 256, 64)
    continueBtn = pygame.Rect(512, 424, 256, 64)
    gameBackBtn = pygame.Rect(512, 572, 256, 64)
    #endDay
    nextDayBtn = pygame.Rect(328, 492, 256, 64)
    endDayQuitBtn = pygame.Rect(696, 492, 256, 64)
    #gameSupplyMenu
    supplyStartBtn = pygame.Rect(1023,0,256,64)
    suppliesTabBtn = pygame.Rect(260,16,251,47)
    #gameProductsMenu
    productStartBtn = pygame.Rect(1023,0,256,64)
    productsTabBtn = pygame.Rect(0,16,251,47)




    while (True):
        mouseXY = pygame.mouse.get_pos()
        mouseDown = pygame.mouse.get_pressed()[0]

        # Captures state of the game - loops thru changes:
        for event in pygame.event.get():

            # Quits game on X window button or ESC key press:
            if ( event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): 
                pygame.quit()
                sys.exit()
        
            # Button, mouse, or keyboard interaction here:
            if gameState == gameIntro:
                if(logoFrame < LOGO_FRAME_FADEOUT and (event.type==pygame.MOUSEBUTTONDOWN or event.type==pygame.KEYDOWN)): # skip intro logo
                    logoFrame = LOGO_FRAME_FADEOUT
        
        #Oongoing game logic here  (repeats every 1/FPS second):
        
            elif gameState == gameMainMenu:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if playBtn.collidepoint(mouseXY):
                        gameState = gameMenu
                    elif settingsBtn.collidepoint(mouseXY):
                        gameState = gameSettings
                    elif quitBtn.collidepoint(mouseXY):
                        pygame.quit()
                        sys.exit()

            elif gameState == gameMenu:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if newGameBtn.collidepoint(mouseXY):
                        sim.newSim()
                        gameState = gameProductMenu
                    elif continueBtn.collidepoint(mouseXY):
                        sim.continueSim()
                        gameState = gameProductMenu
                    elif gameBackBtn.collidepoint(mouseXY):
                        gameState = gameMainMenu

            elif gameState == gameSupplyMenu:

                settings.mouseXY = mouseXY
                settings.mouseDown = mouseDown

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if supplyStartBtn.collidepoint(mouseXY):
                         sim.newSim()
                         gameState = gameSim
                    elif suppliesTabBtn.collidepoint(mouseXY):
                         gameState = gameProductMenu

            elif gameState == gameProductMenu:

                settings.mouseXY = mouseXY
                settings.mouseDown = mouseDown

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if productStartBtn.collidepoint(mouseXY):
                         sim.newSim()
                         gameState = gameSim
                    elif productsTabBtn.collidepoint(mouseXY):
                         gameState = gameSupplyMenu
                    
    
                
            elif gameState == gameSettings:

                settings.mouseXY = mouseXY
                settings.mouseDown = mouseDown

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if resetBtn.collidepoint(mouseXY):
                        if hasattr(settings, "resetToDefault"):
                            settings.resetToDefault()
                        gameState = gameSettings
                    elif settingsBackBtn.collidepoint(mouseXY):
                        gameState = gameMainMenu

            elif gameState == gameEndDay:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if nextDayBtn.collidepoint(mouseXY):
                        gameState = gameProductMenu
                    elif endDayQuitBtn.collidepoint(mouseXY):
                        gameState = gameMainMenu

        # Thread logic for processing data
        if(progressBar.Value==0.0 and dataState==0): # If no data processed, start with sales data.
            dataState = 1 # indicate sales data is processing
            salesDataThread.start()
        if(progressBar.Value<0 and dataState==1): # Unable to find sales data.
            salesDataThread.join()
            print("ERROR: Sales Data could not be found. Aborting program.")
            return            
        if(progressBar.Value>=1.0 and dataState==1): # Finished sales data, begin supply data processing.
            salesDataThread.join()
            #return       # remove this once supplyData is written
            dataState = 2 # indicate supply data is processing
            supplyDataThread.start()
        if(progressBar.Value<0 and dataState==2): # Unable to find supply data.
            supplyDataThread.join()
            print("ERROR: Supply Data could not be found. Aborting program.")
            return            
        if(progressBar.Value>=1.0 and dataState==2): # Sales and supply data processed successfully.
            supplyDataThread.join()
            dataState = 3 # indicate data is done processing
        if(dataState==3):  # Used for debug.
            # print(settings)
            # print(data)
            dataState += 1
            # return
        # Intro logo logic
        if(dataState>0 and logoFrame<=LOGO_FRAME_TOTAL):
            logoFrame += 1
        #Set background color
        surface.fill(BLACK)
        
        # Drawing code goes here:
        if gameState == gameIntro:
            if(logoFrame<=LOGO_FRAME_FADEIN):  # Logo is fading in...
                logo.set_alpha(int(255.0*logoFrame/LOGO_FRAME_FADEIN))
            if(logoFrame>LOGO_FRAME_FADEIN  and logoFrame<=LOGO_FRAME_FADEOUT): # Logo is displaying at full transparency...
                logo.set_alpha(255)
            if(logoFrame>LOGO_FRAME_FADEOUT  and logoFrame<=LOGO_FRAME_TOTAL): # Logo is fading out...
                logo.set_alpha(255 - int(255.0*(logoFrame-LOGO_FRAME_FADEOUT)/(LOGO_FRAME_TOTAL - LOGO_FRAME_FADEOUT)))


            if(logoFrame<=LOGO_FRAME_TOTAL): # Logo is being displayed...
                surface.blit(logo, [(W-640)/2,(H-640)/2])

            if dataState > 0 and dataState < 4:
                progressBar.displayProgress(surface, W*0.15, H*0.90, W*0.70, H*0.06, 5, WHITE, GREEN)

            if logoFrame > 180 and dataState >= 4:
                gameState = gameMainMenu

        elif gameState == gameMainMenu:
            surface.blit(mainMenuBg, (0,0))

        elif gameState == gameMenu:
            surface.blit(gameMenuBg, (0,0))

        elif gameState == gameSupplyMenu:
            surface.blit(supplyMenubg, (0,0))

            if hasattr(settings, "displaySupplyMenu"):
                settings.displaySupplyMenu(surface)
            # if hasattr(simData, "drawSupplyGraph"):
            #     simData.drawSupplyGraph(-1, surface)

        elif gameState == gameProductMenu:
            surface.blit(productMenubg, (0,0))

            if hasattr(settings, "displayProductMenu"):
                settings.displayProductMenu(surface)
            # if hasattr(simData, "drawProductGraph"):
            #     simData.drawProductGraph(-1, surface)

        elif gameState == gameSettings:
            surface.blit(settingsMenuBg, (0,0))

            if hasattr(settings, "display"):
                settings.display(surface)

        elif gameState == gameEndDay:
            surface.blit(endDayBg, (0,0))

        elif gameState == gameSim:
            sim.storeInputs(mouseXY, mouseDown)
            sim.demoSim()
            
                

            if sim.time <= 0:
                gameState = gameEndDay

        
        
        
        pygame.display.update()                        # Updates the screen
        clock.tick(FPS)                                  # Waits for the remaining time of the current frame
        
#----------------------------------------------------------------
main()                                                   #runs the game
