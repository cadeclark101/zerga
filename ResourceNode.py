import random
import numpy as np
import pygame


class ResourceNode(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, surface):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.randint(1, x - 30)
        self.y = random.randint(1, y - 30)
        self.coords = np.array([self.x, self.y])
        self.owner = None              
        self.resource_type = random.randint(1, 1 + 1)
        self.rect = pygame.Rect(self.x, self.y, w, h)

        if self.resource_type == 1:
            pygame.draw.rect(surface, (0, 255, 0), self.rect) # GREEN
        else:
            pygame.draw.rect(surface, (0, 0, 128), self.rect) # BLUE
        
    def isClicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()) 

