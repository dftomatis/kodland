import pygame
import random

class Enemy:
    def __init__(self, x, y, speed):
        self.image = pygame.image.load('assets/images/enemy.png')
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.speed
        if self.y > 600:
            self.y = 0
            self.x = random.randint(0, 800 - self.image.get_width())
        self.rect.topleft = (self.x, self.y)
