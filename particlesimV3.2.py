
# coding: utf-8

# In[1]:


import numpy as np
import string 
import pygame
from pygame.locals import *
from sys import exit


# In[2]:


class Obj():
    def __init__(self, x = 0, y= 0, px = 0 , py = 0, color = (0,0,0)):
        self.x = x
        self.y = y
        self.px = px
        self.py = py
        self.color = color
        self.randomize()
    
    def draw(self, surf):
        draw_box(surf , self.color , self.position)
    
    def randomize(self):
        self.position = (np.random.randint(0, GRID_WIDTH-1) * GRIDSIZE, np.random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)
        
    


# In[3]:


FPS = 5
pygame.init()
fpsClock=pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((255,255,255))
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 40)

GRIDSIZE=10
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)
    
screen.blit(surface, (0,0))

def draw_box(surf, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE*2, GRIDSIZE*2))
    pygame.draw.rect(surf, color, r)
    
    
def gravity(objs, G = 100):
    for obj in objs:
        x_dist , y_dist , px_delta , py_delta = 0,0,0,0
        for i in range(len(objs)):
            x_dist += objs[i].x - obj.x
            y_dist += objs[i].y - obj.y
            dist = np.sqrt(x_dist**2 + y_dist**2)
            if dist != 0:
                px_delta += G * x_dist/dist**3
                py_delta += G * y_dist/dist**3
        obj.px += px_delta
        obj.py += py_delta
    
class Obj():
    def __init__(self, x = 0, y= 0, px = 0 , py = 0, color = (225,0,0)):
        self.x = x
        self.y = y
        self.px = px
        self.py = py
        self.color = color
    
    def draw(self, surf):
        draw_box(surf , self.color , (self.x,self.y)) 
        
    def move(self , c = 0.5):
        if np.abs(self.px) > SCREEN_WIDTH:
            self.px = SCREEN_WIDTH/2
        if np.abs(self.py) > SCREEN_HEIGHT:
            self.py = SCREEN_HEIGHT/2
        if self.x + self.px < 0:
            self.x =  np.abs(self.x + self.px)
            self.px = -c*self.px
        elif self.x + self.px >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - (np.abs(self.x + self.px) % SCREEN_WIDTH)
            self.px = -c*self.px
        else:
            self.x += self.px
        if self.y + self.py < 0:
            self.y =  np.abs(self.y + self.py)
            self.py = -c*self.py
        elif self.y + self.py >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - (np.abs(self.y + self.py) % SCREEN_HEIGHT)
            self.py = -c*self.py
        else:
            self.y += self.py
            
    def action(self, surf):
        draw_box(surf , (255,255,255) , (self.x , self.y))
        self.move()
        self.draw(surf)

        
objs = []       
for i in range(10):
    x = np.random.randint(SCREEN_WIDTH)
    y = np.random.randint(SCREEN_HEIGHT)
    px = np.random.randint(-3,3)
    py = np.random.randint(-3,3)
    objs.append(Obj(x,y,px,py))
    
player = Obj(100 , 100 ,0 ,0, (0,0,225))
objs.append(player)
speed = .5    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pressedKeys = pygame.key.get_pressed()
    
    if pressedKeys[K_LEFT]:
        player.px -= speed
    elif pressedKeys[K_RIGHT]:
        player.px += speed
    if pressedKeys[K_UP]:
        player.py -= speed
    elif pressedKeys[K_DOWN]:
        player.py += speed
    
    for obj in objs:
        obj.action(screen)
    #collision(objs)
    gravity(objs, 1000)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(15)


# In[1]:


def collision(objs):
    for obj in objs:
        for i in range(len(objs)):
            if objs[i] != obj:
                if np.abs(obj.x - objs[i].x) < 10:
                    obj.px = -1*obj.px
                if np.abs(obj.y - objs[i].y) < 10:
                    obj.py = -1*obj.py

