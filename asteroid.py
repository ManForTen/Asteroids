import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

asteroid50 = pygame.image.load('pictures/asteroid.png')

class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = asteroid50
        self.w = 50 * rank
        self.h = 50 * rank
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