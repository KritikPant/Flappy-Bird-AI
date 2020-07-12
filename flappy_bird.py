import pygame
import neat
import os
import time
import random

WIN_WIDTH = 500
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
            d = d/abs(d) * 16
        if d < 0:
            d -= 2
        
        #Moves the bird in the y direction    
        self.y = self.y + d
        
        #Check movement direction in order to tilt the bird
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
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
        #Detecting pixel perfect collisions
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5
    
    def __init__(self, x): #Height is random so y is not needed
        self.x = x
        self.height = 0
        self.gap = 100
        
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) #Flips the image for PIPE_BOTTOM to use for PIPE_TOP
        self.PIPE_BOTTOM = PIPE_IMG
        
        self.passed = False #Indicates whether bird has passed this pipe or not
        self.set_height()
        
    def set_height(self): #Sets pipe at random heights
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
        
    def move(self):
        self.x -= self.VEL #Creates illusion of moving background
    
    def draw(self):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        #Tracking offsets
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        #Finding point of collision
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        
        #Check collision
        if t_point or b_point:
            return True
        
        return False
        
def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    
    run = True
    
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(win, bird)
    
    pygame.quit()          
    quit()
    
main()