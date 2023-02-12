import pygame

class MainBuilding(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, health, surface):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.health = health

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        pygame.draw.rect(surface, (0,100,0), self.rect)
