import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

asteroid = pygame.image.load('pictures/asteroid.png')
class Asteroiback(object):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = pygame.image.load("pictures/1.png")
        self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.mask = pygame.mask.from_surface(self.image)
        self.w = 70
        self.h = 70
        self.ranPoint = random.choice([(random.randrange(0, SCREEN_WIDTH-self.w), random.choice([-1*self.h - 5, SCREEN_HEIGHT + 5])), (random.choice([-1*self.w - 5, SCREEN_WIDTH + 5]), random.randrange(0, SCREEN_HEIGHT - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < SCREEN_WIDTH//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < SCREEN_HEIGHT//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1,3)
        self.yv = self.ydir * random.randrange(1,3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))