import pygame

class InfantryBuilding(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, surface):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y

        self.rect = pygame.Rect(self.x, self.y, w, h)

        pygame.draw.rect(surface, (0,100,0), self.rect)
