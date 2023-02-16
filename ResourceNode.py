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
        self.colour = colour        
        self.resource_type = random.randint(1, 1 + 1)

        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        
