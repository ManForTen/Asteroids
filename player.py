import pygame
import math

playerRocket = pygame.transform.scale(pygame.image.load('pictures/player.png'),(100,100))

playerRocketdm1 = pygame.transform.scale(pygame.image.load('pictures/playerdm1.png'),(100,100))
playerRocketdm2 = pygame.transform.scale(pygame.image.load('pictures/playerdm2.png'),(100,100))
playerRocketdm3 = pygame.transform.scale(pygame.image.load('pictures/playerdm3.png'),(100,100))

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

class Player(object):
    def __init__(self):
        self.img = playerRocket
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = SCREEN_WIDTH//2
        self.y = SCREEN_HEIGHT//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def draw(self, win, attack):
        if attack == 0:
            self.img = playerRocket
        if attack == 1:
            self.img = playerRocketdm1
        if attack == 2:
            self.img = playerRocketdm2
        if attack == 3:
            self.img = playerRocketdm3
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        win.blit(self.rotatedSurf, self.rotatedRect)

    def turnLeft(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def turnRight(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def moveForward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def updateLocation(self):
        if self.x > SCREEN_WIDTH + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = SCREEN_WIDTH
        elif self.y < -50:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT + 50:
            self.y = 0