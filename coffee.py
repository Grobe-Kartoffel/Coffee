import math, random, pygame, sys, threading
from abc import ABC, abstractmethod                     # not sure why abstract classes need to be imported like this, but they do
# import class files
# IDE might complain that the file cannot be found, but it will still work
import progress_manager as pm, accuracy_data as ac, settings as st, sim as sm

def main():
    # pygame initializers
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
    
    # color constants
    BLACK = (0,0,0)
    
    # local  variables
    data = ac.Accuracy_Data()              # create class objects
    progressBar = pm.Progress_Manager()
    settings = st.Settings()
    sim = sm.Sim(surface,SCALE)
    sim.acDataRef = data
    
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
            #progressBar.displayProgress(surface, W/16, H*6/13, W*7/8, H/13, 5, WHITE, GREEN)
        
        
        pygame.display.update()                          #updates the screen
        clock.tick(60)                                  # FPS for animation (lower number to slow)
        
#----------------------------------------------------------------
main()                                                   #runs the game