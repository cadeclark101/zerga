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

        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def getButtonID(self):
        return self.id
    

    

