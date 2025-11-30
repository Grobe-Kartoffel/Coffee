import math, random, pygame, sys, threading
from abc import ABC, abstractmethod                     # not sure why abstract classes need to be imported like this, but they do
# import class files
# IDE might complain that the file cannot be found, but it will still work
import progress_manager as pm, accuracy_data as ac, settings as st, sim as sm

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
    
    # Local Variables
    data = ac.Accuracy_Data()              # create class objects
    progressBar = pm.Progress_Manager()
    settings = st.Settings()
    sim = sm.Sim(surface,SCALE)
    sim.acDataRef = data
    
    mouseXY = [0,0]
    mouseDown = False
    
    dataState = 0 # Indicates the state of the data processing. (0 = processing not started, 1 = processing sales data, 2 = processing supply data, 3 = processing done)
    
    salesDataThread = threading.Thread(target=data.readSalesData, args=(settings,progressBar,))   # DO NOT INCLUDE PARENTHESIS ON TARGET FUNCTION    # ARGS MUST BE ITERABLE, INCLUDE EXTRA COMMA FOR ONLY 1 ARG
    supplyDataThread = threading.Thread(target=data.readSupplyData, args=(settings,progressBar,))
    
    # image files
    logo = pygame.image.load("assets/logo.png").convert_alpha(surface)
    
    logoFrame = 0.0 # Elapsed frames since game start.
    
    while (True):
        mouseXY = pygame.mouse.get_pos()
        mouseDown = pygame.mouse.get_pressed()[0]

        # Captures state of the game - loops thru changes:
        for event in pygame.event.get():
            
            # Quits game on X window button or ESC key press:
            if (event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
                pygame.quit()
                sys.exit()
        
            # Button, mouse, or keyboard interaction here:
            if(logoFrame<LOGO_FRAME_FADEOUT and (event.type==pygame.MOUSEBUTTONDOWN or event.type==pygame.KEYDOWN)): # Skip intro logo.
                logoFrame = LOGO_FRAME_FADEOUT
        
        # Ongoing game logic here (repeats every 1/FPS second):
        
        # Thread logic for processing data:
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
        '''if(dataState==3): # Used for debug.
            print(settings)
            print(data)
            dataState += 1
            return'''
        
        # Intro logo logic:
        if(dataState>0 and logoFrame<=LOGO_FRAME_TOTAL):
            logoFrame += 1
        
        # Set background color:
        surface.fill(BLACK)
        
        # Drawing code goes here:
        if(logoFrame<=LOGO_FRAME_FADEIN): # Logo is fading in...
            logo.set_alpha(int(255.0*logoFrame/LOGO_FRAME_FADEIN))
        if(logoFrame>LOGO_FRAME_FADEIN and logoFrame<=LOGO_FRAME_FADEOUT): # Logo is displaying at full transparency...
            logo.set_alpha(255)
        if(logoFrame>LOGO_FRAME_FADEOUT and logoFrame<=LOGO_FRAME_TOTAL): # Logo is fading out...
            logo.set_alpha(255 - int(255.0*(logoFrame-LOGO_FRAME_FADEOUT)/(LOGO_FRAME_TOTAL - LOGO_FRAME_FADEOUT)))
        if(logoFrame<=LOGO_FRAME_TOTAL): # Logo is being displayed...
            surface.blit(logo, [(W-640)/2,(H-640)/2])
        else:
            sim.storeInputs(mouseXY,mouseDown)
            sim.demoSim()
            #progressBar.displayProgress(surface, W/16, H*6/13, W*7/8, H/13, 5, WHITE, GREEN)
        
        pygame.display.update()                         # Updates the screen
        clock.tick(FPS)                                  # Waits for the remaining time of the current frame
        
#----------------------------------------------------------------
main()                                                   #runs the game