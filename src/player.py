import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/images/player.png')
        self.x = x
        self.y = y
        self.speed = 1

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Asegurar que el jugador no salga de la pantalla
        self.x = max(0, min(self.x, 800 - self.image.get_width()))
        self.y = max(0, min(self.y, 600 - self.image.get_height()))

