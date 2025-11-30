import pygame, threading

class Progress_Manager: # manages a progress bar for when Accuracy Data is reading a file, so the rest of the game can continue running
    def __init__(self):
        self.Max = 1.0
        self.Value = 0.0
        self.lock = threading.Lock()
    def update(self,value):
        with self.lock: # Locks value while writing for thread safety.
            self.Value = value
    def displayProgress(self,surface,x,y,w,h,border,BORDERCOLOR,PROGRESSCOLOR):
        pygame.draw.rect(surface,BORDERCOLOR,(x-border,y-border,w+border*2,h+border*2),border)
        pygame.draw.rect(surface,PROGRESSCOLOR,(x,y,w*self.Value,h))