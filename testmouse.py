
import os, pygame
from pygame.locals import *
import random, math
def lerp(x,a, b,c,d):
    return ((x-a)/(b-a))*(d-c)+c

def screenToWorld(i,j,width, height,center,radius):
    aspect_ratio=width/height
    y=lerp(i,0,height-1,center[1]+radius,center[1]-radius)
    x=lerp(j,0,width-1,center[0]-radius*aspect_ratio,center[0]+radius*aspect_ratio)
    return (x,y)
 
pygame.init()
screen = pygame.display.set_mode((640,480))
running = True
while running:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN :
            print('pos:', event.pos)
            print('screenToWorld',screenToWorld(event.pos[1],event.pos[0],640,480,(0,0),1))
            print('button:', event.button)
        elif event.type == QUIT:
            running = False
            break

pygame.quit()
