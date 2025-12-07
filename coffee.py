# External imports.
import math, random, pygame, sys, threading
from enum import IntEnum
from abc import ABC, abstractmethod # Not sure why abstract classes need to be imported like this, but they do.

# Import class files. IDE might complain that the file cannot be found, but it will still work.
import progress_manager as pm, accuracy_data as ac, settings as st, sim as sm


# "Button Animation" gives buttons border and a highlight
def draw_button_outline(surface, rect, thickness= 4):
    pygame.draw.rect(surface, (255, 255, 255), rect, thickness)

def draw_button_glow(surface, rect, alpha=35):
    glow_surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (255, 255, 255, alpha), (0, 0, rect.w, rect.h))
    surface.blit(glow_surf, rect.topleft)


# Game States
class GameState(IntEnum):
    gameIntro = 0
    gameMainMenu = 1
    gameSettings = 2
    gameSim = 3 
    gameEndDay = 4
    gameMenu = 5
    gameSupplyMenu = 6
    gameProductMenu = 7

simSpeed = 1.0 # Currently unused.

def main():
    # Pygame Initialization
    pygame.init()                                           # initialize game engine
    pygame.mixer.init()
    
    SCALE = 4                                               # set scale factor for graphics
    W=320*SCALE                                             # set window size
    H=180*SCALE
    size=(W,H)
    surface = pygame.display.set_mode(size)
    
    pygame.display.set_caption("Coffee Shop Simulator")      # window title
    icon = pygame.image.load("assets/graphics/icon.png")
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

    gameState = GameState.gameIntro
    
    salesDataThread = threading.Thread(target=data.readSalesData, args=(settings,progressBar,))   # DO NOT INCLUDE PARENTHESIS ON TARGET FUNCTION    # ARGS MUST BE ITERABLE, INCLUDE EXTRA COMMA FOR ONLY 1 ARG
    supplyDataThread = threading.Thread(target=data.readSupplyData, args=(settings,progressBar,))
    
    # Sound Files
    sounds = {
        "buttonClick": pygame.mixer.Sound("assets/sfx/click.wav")
    }
    
    # Image Files
    logo = pygame.image.load("assets/graphics/logo.png").convert_alpha(surface)

    logoFrame = 0.0 # Elapsed frames since game start.

    # Create surfaces for menu backgrounds.
    mainMenuBg = pygame.image.load("assets/graphics/Main Menu.png").convert_alpha()
    settingsMenuBg = pygame.image.load("assets/graphics/Settings.png").convert_alpha()
    endDayBg = pygame.image.load("assets/graphics/EndofDay Menu.png").convert_alpha()
    gameMenuBg = pygame.image.load("assets/graphics/Game Menu.png").convert_alpha()
    productMenubg = pygame.image.load("assets/graphics/Product Menu.png").convert_alpha()
    supplyMenubg = pygame.image.load("assets/graphics/Supply Menu.png").convert_alpha()

    # mainMenu
    playBtn = pygame.Rect(512, 276, 256, 64)
    settingsBtn = pygame.Rect(512, 424, 256, 64)
    quitBtn = pygame.Rect(512, 572, 256, 64)
    # settingsMenu
    resetBtn = pygame.Rect(512, 528, 256, 64)
    settingsBackBtn = pygame.Rect(512, 628, 256, 64)
    # gameMenu
    newGameBtn = pygame.Rect(512, 276, 256, 64)
    continueBtn = pygame.Rect(512, 424, 256, 64)
    gameBackBtn = pygame.Rect(512, 572, 256, 64)
    # endDay
    nextDayBtn = pygame.Rect(328, 492, 256, 64)
    endDayQuitBtn = pygame.Rect(696, 492, 256, 64)
    # gameSupplyMenu
    supplyStartBtn = pygame.Rect(1023,0,256,64)
    suppliesTabBtn = pygame.Rect(260,16,251,47)
    # gameProductsMenu
    productStartBtn = pygame.Rect(1023,0,256,64)
    productsTabBtn = pygame.Rect(0,16,251,47)

    def goBackToMain():
        nonlocal gameState
        gameState = GameState.gameMainMenu

    settingsMenu = st.SettingsMenu(
        on_back = goBackToMain,
        on_reset = None,
        initial_values = None
    )

    def volume_sfx_changed(value):
        for name, sound in sounds.items():
            sound.set_volume(value)
    def volume_music_changed(value):
        pygame.mixer.music.set_volume(value)
    def speed_changed(value):
        global simSpeed
        simSpeed = value

    settingsMenu.set_external_callbacks(
        volume_sfx_changed,
        volume_music_changed,
        speed_changed
    )

    while (True):
        mouseXY = pygame.mouse.get_pos()
        mouseDown = pygame.mouse.get_pressed()[0]

        # Captures state of the game - loops thru changes:
        for event in pygame.event.get():

            # Quits game on X window button or ESC key press:
            if ( event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): 
                pygame.quit()
                sys.exit()
        
            # Ongoing game logic here (repeats every 1/FPS second):
            # Button, mouse, or keyboard input logic here, selected by gameState:
            match gameState:
                # Intro
                case GameState.gameIntro:
                    if(logoFrame < LOGO_FRAME_FADEOUT and (event.type==pygame.MOUSEBUTTONDOWN or event.type==pygame.KEYDOWN)): # skip intro logo
                        logoFrame = LOGO_FRAME_FADEOUT
                # Main Menu
                case GameState.gameMainMenu:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if playBtn.collidepoint(mouseXY):
                            sounds["buttonClick"].play()
                            gameState = GameState.gameMenu
                        elif settingsBtn.collidepoint(mouseXY):
                            sounds["buttonClick"].play()
                            gameState = GameState.gameSettings
                        elif quitBtn.collidepoint(mouseXY):
                            sounds["buttonClick"].play()
                            pygame.quit()
                            sys.exit()
                # -TODO-
                case GameState.gameMenu:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if newGameBtn.collidepoint(mouseXY):
                            sounds["buttonClick"].play()
                            sim.newSim()
                            gameState = GameState.gameProductMenu
                        elif continueBtn.collidepoint(mouseXY):
                            sounds["buttonClick"].play()
                            sim.continueSim()
                            gameState = GameState.gameProductMenu
                        elif gameBackBtn.collidepoint(mouseXY):
                            sounds["buttonClick"].play()
                            gameState = GameState.gameMainMenu
                
                # Supplies Menu
                case GameState.gameSupplyMenu:
                    settings.mouseXY = mouseXY
                    settings.mouseDown = mouseDown

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if supplyStartBtn.collidepoint(mouseXY):
                            sounds["buttonClick"].play()
                            gameState = GameState.gameSim
                        elif suppliesTabBtn.collidepoint(mouseXY):
                            sounds["buttonClick"].play()
                            gameState = GameState.gameProductMenu
                
                # Products Menu
                case GameState.gameProductMenu:
                    settings.mouseXY = mouseXY
                    settings.mouseDown = mouseDown

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if productStartBtn.collidepoint(mouseXY):
                            sounds["buttonClick"].play()
                            gameState = GameState.gameSim
                        elif productsTabBtn.collidepoint(mouseXY):
                            sounds["buttonClick"].play()
                            gameState = GameState.gameSupplyMenu
                
                # Settings Menu
                case gameState.gameSettings:
                    settingsMenu.store_inputs(mouseXY, mouseDown)
                
                # End-of-Day Menu
                case GameState.gameEndDay:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if nextDayBtn.collidepoint(mouseXY):
                            sounds["buttonClick"].play()
                            sim.continueSim() # prepare sim for another day
                            gameState = GameState.gameProductMenu
                        elif endDayQuitBtn.collidepoint(mouseXY):
                            sounds["buttonClick"].play()
                            sim.continueSim()
                            gameState = GameState.gameMainMenu
            # End input logic ------------------
            
        # End event loop ------------------
        
        
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
        # End data processing logic ------------------
        
        
        # Drawing code goes here, selected by gameState:
        #Set background color
        surface.fill(BLACK)
        match gameState:
            # Intro
            case GameState.gameIntro:
                if(logoFrame<=LOGO_FRAME_FADEIN):  # Logo is fading in...
                    logo.set_alpha(int(255.0*logoFrame/LOGO_FRAME_FADEIN))
                if(logoFrame>LOGO_FRAME_FADEIN  and logoFrame<=LOGO_FRAME_FADEOUT): # Logo is displaying at full transparency...
                    logo.set_alpha(255)
                if(logoFrame>LOGO_FRAME_FADEOUT  and logoFrame<=LOGO_FRAME_TOTAL): # Logo is fading out...
                    logo.set_alpha(255 - int(255.0*(logoFrame-LOGO_FRAME_FADEOUT)/(LOGO_FRAME_TOTAL - LOGO_FRAME_FADEOUT)))
                if(logoFrame<=LOGO_FRAME_TOTAL): # Logo is being displayed...
                    surface.blit(logo, [(W-640)/2,0])
                if dataState > 0 and dataState < 4:
                    progressBar.displayProgress(surface, W*0.15, H*0.90, W*0.70, H*0.06, 5, WHITE, GREEN)
                if logoFrame > 180 and dataState >= 4:
                    sim.continueSim() # reset sim so demo displays properly
                    gameState = GameState.gameMainMenu
            
            # Main Menu
            case GameState.gameMainMenu:
                sim.demoSim()
                surface.blit(mainMenuBg, (0,0))

                mx, my = mouseXY
                if playBtn.collidepoint(mx, my):
                     draw_button_glow(surface, playBtn)
                     draw_button_outline(surface, playBtn)

                if settingsBtn.collidepoint(mx, my):
                     draw_button_glow(surface, settingsBtn)
                     draw_button_outline(surface, settingsBtn)

                if quitBtn.collidepoint(mx, my):
                     draw_button_glow(surface, quitBtn)
                     draw_button_outline(surface, quitBtn)    
            
            # -TODO-
            case GameState.gameMenu:
                sim.demoSim()
                surface.blit(gameMenuBg, (0,0))
            
                mx, my = mouseXY
                if newGameBtn.collidepoint(mx, my):
                    draw_button_glow(surface, newGameBtn)
                    draw_button_outline(surface, newGameBtn)

                if continueBtn.collidepoint(mx, my):
                    draw_button_glow(surface, continueBtn)
                    draw_button_outline(surface, continueBtn)

                if gameBackBtn.collidepoint(mx, my):
                    draw_button_glow(surface, gameBackBtn)
                    draw_button_outline(surface, gameBackBtn)
            
            # TODO: Supplies and Products Tab Buttons outlines need changed to fit shape 
            # Supplies Menu
            case GameState.gameSupplyMenu:
                surface.blit(supplyMenubg, (0,0))
                
                mx, my = mouseXY
                if supplyStartBtn.collidepoint(mx, my):
                    draw_button_glow(surface, supplyStartBtn)
                    draw_button_outline(surface, supplyStartBtn)

                if suppliesTabBtn.collidepoint(mx, my):
                    draw_button_glow(surface, suppliesTabBtn)
                    draw_button_outline(surface, suppliesTabBtn)

                if hasattr(settings, "displaySupplyMenu"):
                    settings.displaySupplyMenu(surface)
                # if hasattr(simData, "drawSupplyGraph"):
                #     simData.drawSupplyGraph(-1, surface)
            
            # Products Menu
            case GameState.gameProductMenu:
                surface.blit(productMenubg, (0,0))

                mx, my = mouseXY
                if supplyStartBtn.collidepoint(mx, my):
                    draw_button_glow(surface, supplyStartBtn)
                    draw_button_outline(surface, supplyStartBtn)

                if productsTabBtn.collidepoint(mx, my):
                    draw_button_glow(surface, productsTabBtn)
                    draw_button_outline(surface, productsTabBtn)

                if hasattr(settings, "displayProductMenu"):
                    settings.displayProductMenu(surface)
                # if hasattr(simData, "drawProductGraph"):
                #     simData.drawProductGraph(-1, surface)
            
            # Settings Menu
            case GameState.gameSettings:
                #surface.blit(settingsMenuBg, (0,0))
                sim.demoSim()
                settingsMenu.update()
                settingsMenu.draw(surface)

            # End-of-Day Menu
            case GameState.gameEndDay:
                sim.runSim()
                surface.blit(endDayBg, (0,0))

                mx, my = mouseXY
                if nextDayBtn.collidepoint(mx, my):
                    draw_button_glow(surface, nextDayBtn)
                    draw_button_outline(surface, nextDayBtn)

                if endDayQuitBtn.collidepoint(mx, my):
                    draw_button_glow(surface, endDayQuitBtn)
                    draw_button_outline(surface, endDayQuitBtn)
            
            # Sim
            case GameState.gameSim:
                sim.storeInputs(mouseXY, mouseDown)
                sim.runSim()
                
                if sim.time <= 0:
                    sim.storeInputs([0,0],False) # make sure if player clicks the moment the sim ends, the input is not continuously doing something
                    gameState = GameState.gameEndDay
        # End drawing code ------------------

        
        pygame.display.update()                        # Updates the screen
        clock.tick(FPS)                                  # Waits for the remaining time of the current frame
        
#----------------------------------------------------------------
main()                                                   #runs the game
