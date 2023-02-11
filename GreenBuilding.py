import pygame

class GreenBuilding(pygame.sprite.Sprite):
    def __init__(self, colour, w, h):
        super().__init__()

        self.surface = pygame.Surface([w, h])