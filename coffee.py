import math, random, pygame, sys                                   
pygame.init()                                           #initialize game engine

w=800                                                   #set window size
h=640                                                   
size=(w,h)
surface = pygame.display.set_mode(size)

pygame.display.set_caption("I'm Making A Video Game!")          # window title

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






# -------- Main Program Loop -----------
def main():                                             #every program should have a main function
                                                        #other functions go above main
    # local  variables  


    
    while (True):
        
        for event in pygame.event.get():                #captures state of the game - loops thru changes
            
            if ( event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): #end game
                pygame.quit()                        
                sys.exit()
        
            # button, mouse, or keyboard interaction here
        
        # ongoing game logic here  (repeats every 1/60 second) 
        
        
        
      
        surface.fill(WHITE)                             #set background color
        
        #drawing code goes here
        
        
        
        
        
        pygame.display.update()                          #updates the screen-
        clock.tick(60)                                  # FPS for animation (lower number to slow)
        
        
#----------------------------------------------------------------            
main()                                                   #runs the game