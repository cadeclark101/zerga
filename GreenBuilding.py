import pygame

class GreenBuilding(pygame.sprite.Sprite):
    def __init__(self, w, h, health, resource_node, surface):
        pygame.sprite.Sprite.__init__(self)
        self.health = health
        
        self.rect = pygame.Rect(resource_node.x, resource_node.y, w, h)

        pygame.draw.rect(surface, (0, 255, 0), self.rect)
        