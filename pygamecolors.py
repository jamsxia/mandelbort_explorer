# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 09:07:41 2014

@author: matthews
"""

import os, pygame
from pygame.locals import *
import random, math, time

def handleInput(screen):
    """
    return False if we quit
    save image on S key
    """
    #Handle Input Events
    for event in pygame.event.get():
        if event.type == QUIT:
            return False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False
            elif event.key == K_s:
                pygame.event.set_blocked(KEYDOWN|KEYUP)
                id = random.randint(1000,9999)
                fname = 'savedimage%d.png' % id
                pygame.image.save(screen,fname)
    return True

def clamp(x,low,hi):
    if x < low:
        return low
    if x > hi:
        return hi
    return x

def screenToNorm(i,j,width,height):
    x = clamp(i/width, 0, 1)
    y = clamp(j/height, 0, 1)
    return (x,y)

def getColor(x,y):
    """ return color for x,y in [0,1) x [0,1) """
    x = clamp(x,0,1)
    y = clamp(y,0,1)
    r = x
    g = y
    b = 1-x
    return (int(255*r), int(255*g), int(255*b))

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the user quits."""
#Initialize Everything
    pygame.init()
    width,height = 1280, 720
    #width,height = 640,480
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Colors!')

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    # fill with a color so we can see if some pixels
    # are not colored
    background.fill((64, 128, 255))

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.update()

#Prepare Game Objects
    clock = pygame.time.Clock()
    pixelsize = 2**7  # so we can divide by 2
# Game loop
    while handleInput(screen):
        # start drawing loop
        totaltime = 0.0
        while pixelsize > 0:
            starttime = time.time()
            print('Begin %d x %d pixels' % (pixelsize,pixelsize))
            for x in range(0,width,pixelsize):
                # refresh screen at intervals:
                if x % (width//4) == 0:
                    print(int(100*(1-x/width)), 'percent remaining')
                    #draw background into screen
                    screen.blit(background, (0,0))
                    pygame.display.update()
                for y in range(0,height,pixelsize):
                    # draw into background surface
                    # find coordinates for color function:
                    xn, yn = screenToNorm((x + pixelsize/2),
                                          (y + pixelsize/2),
                                          width,
                                          height)
                    color = getColor(xn, yn)
                    # draw a single pixel on the screen
                    background.fill(color, ((x,y),(pixelsize,pixelsize)))
                    # be able to quit at any time:
                    if not handleInput(screen):
                        return
            # refresh screen
            screen.blit(background, (0,0))
            pygame.display.update()
            print('End %d x %d pixels' % (pixelsize, pixelsize))
            endtime = time.time()
            pixeltime = endtime - starttime
            totaltime += pixeltime
            print('That took %g seconds' % (pixeltime))
            pixelsize = pixelsize//2
            if pixelsize > 0:
                clock.tick(1/5)
            else:
                print('Done.  All renders took %g' % totaltime)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
