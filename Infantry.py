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
        self.movement_target = None
        self.image = pygame.Surface((w,h))

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def moveToTarget(self, target_pos):
        print("here")
        if self.checkReachTarget != True:
            if target_pos[0] > self.x:
                self.x += 1
            elif target_pos[0] < self.x:
                self.x -= 1
            elif target_pos[1] > self.y:
                self.y += 1
            elif target_pos[1] < self.y:
                self.y -= 1

    def checkReachTarget(self, target_pos):
        if self.x == target_pos[0] and self.y == target_pos[1]:
            return True

class InfantryProjectile(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_range_x = 21
        self.bullet_range_y = 21
        self.target = target

        self.image = pygame.Surface([1, 2])
        self.image.fill((255, 255, 255))
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3
