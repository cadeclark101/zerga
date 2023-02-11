import pygame

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, surface, action=None):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)

        pygame.draw.rect(surface, (0, 0, 0), self.rect)


    def isClicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()) 
    

    

