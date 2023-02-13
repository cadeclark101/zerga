import pygame

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, id, colour):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.id = id
        self.colour = colour
        self.image = pygame.Surface((w, h))
        self.rect = pygame.Rect(x, y, w, h)

    def getButtonID(self):
        return self.id
    

    

