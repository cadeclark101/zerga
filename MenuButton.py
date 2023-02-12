import pygame

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, surface, id, action=None):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.id = id
        self.rect = pygame.Rect(x, y, w, h)

        pygame.draw.rect(surface, (0, 0, 0), self.rect)

    def getX(self):
        return self.x

    def getButtonID(self):
        return self.id
    

    

