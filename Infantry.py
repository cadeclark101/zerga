import pygame
from threading import Thread

class Infantry(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, health, colour, zerga):
        pygame.sprite.Sprite.__init__(self)
        self.health = health
        self.colour = colour
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.zerga = zerga

        self.movement_thread = None
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def createMovementThread(self, movement_target_pos):
        movement_thread = Thread(target=self.moveToTarget(movement_target_pos)) 
        self.movement_thread = movement_thread
        print(self.movement_thread)
        self.movement_thread.start()

    def moveToTarget(self, movement_target_pos):
        while self.checkReachedTarget(movement_target_pos) == False:
            if movement_target_pos[0] > self.x:
                self.x += 1
            elif movement_target_pos[0] < self.x:
                self.x -= 1
            else:
                pass

            if movement_target_pos[1] > self.y:
                self.y += 1
            elif movement_target_pos[1] < self.y:
                self.y -= 1
            else:
                pass
            self.zerga.redrawAll()

    def checkReachedTarget(self, movement_target_pos):
        if movement_target_pos[0] == self.x and movement_target_pos[1] == self.y:
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
