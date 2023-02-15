import pygame


class Infantry(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, health, colour):
        pygame.sprite.Sprite.__init__(self)
        self.health = health
        self.colour = colour
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def moveToTarget(self, target_pos):
        if self.checkReachedTarget(target_pos) == False:
            if target_pos[0] > self.x:
                self.x += 1
            elif target_pos[0] < self.x:
                self.x -= 1
            else:
                pass

            if target_pos[1] > self.y:
                self.y += 1
            elif target_pos[1] < self.y:
                self.y -= 1
            else:
                pass

    def checkReachedTarget(self, target_pos):
        if target_pos[0] == self.x and target_pos[1] == self.y:
            return True
        else:
            return False

class InfantryProjectile(pygame.sprite.Sprite):
    def __init__(self, startX, startY, endX, endY, colour):
        pygame.sprite.Sprite.__init__(self)
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        self.colour = colour
