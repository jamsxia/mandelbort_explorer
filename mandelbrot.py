

import os,pygame
from pygame.locals import *
import random, math, time

pixelsize=2**7
width,height =640,480
screen = pygame.display.set_mode((width,height),pygame.RESIZABLE)
background = pygame.Surface(screen.get_size())
background = background.convert()
    # fill with a color so we can see if some pixels
    # are not colored
background.fill((64, 128, 255))
center=(0,0)
radius=1

colors = [(226, 143, 34),
          (127, 115, 100),
          (171, 92, 76),
          (132, 182, 62),
          (82, 202, 134),
          (29, 179, 154),
          (24, 82, 177),
          (53, 180, 205),
          (134,181,229),
          (12,53,248),
          (121,223,151),
          (248,201,95),
          (205,70,0),
          (24,168,7),
          (193,57,90),
          (127,52,8)]
        


def lerp(x,a, b,c,d):
    return ((x-a)/(b-a))*(d-c)+c

def screenToWorld(i,j,width, height,center,radius):
    aspect_ratio=width/height
    y=lerp(i,0,height-1,center[1]+2*radius,center[1]-2*radius)
    x=lerp(j,0,width-1,center[0]-2*radius*aspect_ratio,center[0]+2*radius*aspect_ratio)
    return (x,y)

def restart(w, h):
    global pixelsize, screen, background,width,height,center,radius,pixelsize
    width=w
    height=h
    screen = pygame.display.set_mode((width,height),pygame.RESIZABLE)
    pygame.display.set_caption('Colors!')
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    screen.blit(background, (0,0))
    pygame.display.update()

    
def handleInput(screen):
    """
    return False if we quit
    save image on S key
    """
    #Handle Input Events
    global center, width, height,radius,center,pixelsize
    for event in pygame.event.get():
        if event.type == QUIT:
            return False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False
            elif event.key == K_s:
                pygame.event.set_blocked(KEYDOWN|KEYUP)
                row=center[0]
                col=center[1]
                
                fname = "MandX{:.3f}Y{:.3f}R{:.3f}.png".format(row,col,radius)
                print (fname)
                pygame.image.save(screen,fname)
        elif event.type==MOUSEBUTTONDOWN:
            if event.button==1:
                center= screenToWorld(event.pos[0],event.pos[1],width,height,center,radius)
                pixelsize=2**7
                radius/=2
                restart(width,height)
            elif event.button==3:
                center= screenToWorld(event.pos[0],event.pos[1],width,height,center,radius)
                pixelsize=2**7
                radius*=2
                restart(width,height)
        elif event.type==VIDEORESIZE:
            width,height=event.dict['size']
            restart(width,height)
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

def mandelbrot(x1,y1):
    global colors
    x = 0
    y = 0
    iteration = 0
    max_iteration = 250
    while (x*x + y*y <=2*2 and iteration < max_iteration):
        xtemp = x*x - y*y + x1
        y = 2*x*y + y1
        x = xtemp
        iteration = iteration + 1
    return iteration
    

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the user quits."""
    global pixelsize, screen, background,width,height,center,radius,colors
#Initialize Everything
    pygame.init()
    width,height = 640,480
    screen = pygame.display.set_mode((width,height),pygame.RESIZABLE)
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
                    xn, yn = screenToWorld(y,x,width,height,center,radius)
                    step=mandelbrot(xn,yn)
                    if(step==250):
                        color=(0,0,0)
                    else:
                        color=colors[step%len(colors)]
##                    color = getColor(xn, yn)
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
                pass
            else:
                print('Done.  All renders took %g' % totaltime)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()

