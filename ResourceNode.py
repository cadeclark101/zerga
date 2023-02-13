import random
import numpy as np
import pygame


class ResourceNode(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, colour):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.randint(1, x - 30)
        self.y = random.randint(1, y - 30)
        self.w = w
        self.h = h            
        self.resource_type = random.randint(1, 1 + 1)
        self.rect = pygame.Rect(self.x, self.y, w, h)
        self.colour = colour