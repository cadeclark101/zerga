import pygame

class BlueBuilding(pygame.sprite.Sprite):
    def __init__(self, w, h, health, colour, resource_node):
        pygame.sprite.Sprite.__init__(self)
        self.health = health
        self.x = resource_node.x
        self.y = resource_node.y
        self.w = w
        self.h = h
        self.colour = colour
        self.image = pygame.Surface((w,h))

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)


        