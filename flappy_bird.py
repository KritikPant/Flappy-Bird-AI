import pygame
import neat
import os
import time
import random

WIN_WIDTH = 600
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "pipe.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "bg.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "base.png")))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5 #Time between bird images switching
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
        
    def move(self):
        #tick_count is time
        self.tick_count += 1
        
        #Displacement - leads to an arc shaped movement of the bird
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        
        #Terminal Velocity to stop acceleration downwards being to high
        if d >= 16:
            d = 16
        if d < 0:
            d -= 2
        
        #Moves the bird in the y direction    
        self.y = self.y + d
        
        #Check movement direction in order to tilt the bird
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt < -90:
                self.tilt -= self.ROT_VEL #Allows the bird to tilt 90 degrees downwards into a nose dive
                
    def draw(self, win):
        self.img_count += 1
        
        #Animating the bird
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
            
        if self.tilt <= -80: #Don't want the wings to be flapping in a nose dive
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
            
        #Tilting the image
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center) #Rotates image around the center rather than around the topleft coordinate
        win.blit(rotated_img, new_rect.topleft)
        
    def get_mask(self):
        #Detecting collisions
        return pygame.mask.from_surface(self.img)
    