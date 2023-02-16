import sys
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
        
        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        
    
    def update(self, target_pos):
        if self.checkReachedTarget(target_pos) == False:
            if target_pos[0] > self.rect.x:
                self.rect.x += 1
            elif target_pos[0] < self.rect.x:
                self.rect.x -= 1
            else:
                pass

            if target_pos[1] > self.rect.y:
                self.rect.y += 1
            elif target_pos[1] < self.rect.y:
                self.rect.y -= 1
            else:
                pass
        else:
            return

    def checkReachedTarget(self, target_pos):
        if target_pos[0] == self.rect.x and target_pos[1] == self.rect.y:
            return True
        else:
            return False

class InfantryProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, direction, speed, range, colour):
        pygame.sprite.Sprite.__init__(self)
        self.startX = x
        self.startY = y
        self.currentX = x
        self.currentY = y
        self.w = w
        self.h = h
        self.direction = direction
        self.speed = speed
        self.range = range
        self.colour = colour

        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.checkReachedRange() == False:
            self.rect.x += self.speed
            self.rect.y += self.speed
        else:
            return


    def checkReachedRange(self):
        if (self.currentX == (self.startX + self.range)) :
            return True
        elif (self.startY == self.currentY + self.range):
            return True
        else:
            return False