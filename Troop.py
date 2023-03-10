import pygame
from pygame import gfxdraw

from Player import Player


class Troop(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, health, colour, speed, owner, target):
        pygame.sprite.Sprite.__init__(self)
        self.health = health
        self.colour = colour
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
        self.owner = owner
        self.target = target
        
    
    def update(self, moving_troops, all_sprites):
        if self.checkReachedTarget() == True:
            moving_troops.remove(self)

        collided_sprite = self.checkForCollision(all_sprites)
        if collided_sprite is not None:
            if self.rect.top <= collided_sprite.rect.bottom + (collided_sprite.rect.w / 2):
                self.rect.x += self.speed
                
            if self.rect.left <= collided_sprite.rect.right + (collided_sprite.rect.h / 2):
                self.rect.y += self.speed
            
        else:
            self.updateX()
            self.updateY()


    def updateX(self):
        if self.target[0] > self.rect.x:
            self.rect.x += self.speed
        elif self.target[0] < self.rect.x:
            self.rect.x -= self.speed
        else:
            pass

    def updateY(self):
        if self.target[1] > self.rect.y:
            self.rect.y += self.speed
        elif self.target[1] < self.rect.y:
            self.rect.y -= self.speed
        else:
            pass


    def checkReachedTarget(self):
        if self.target[0] == self.rect.x and self.target[1] == self.rect.y:
            return True
        else:
            return False


    def checkForCollision(self, all_sprites):
        hits_any_sprites = pygame.sprite.spritecollide(self, all_sprites, False) # Check if sprite will collide with any sprite
        if len(hits_any_sprites) > 0:
            for collided_sprite in hits_any_sprites:
                if hasattr(collided_sprite, "owner") is True: # Check if sprite has an owner
                    if isinstance(collided_sprite.owner, Player): # Check if owner is the player
                        pass 
                    else:
                        return collided_sprite 
                else:
                    return collided_sprite
        else:
            collided_sprite = None
            return collided_sprite

class BasicTroop(Troop):
    def __init__(self, w, h, x, y, health, colour, speed, owner, target):
        super().__init__(w, h, x, y, health, colour, speed, owner, target)

        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class SniperTroop(Troop):
    def __init__(self, w, h, x, y, health, colour, speed, owner, target):
        super().__init__(w, h, x, y, health, colour, speed, owner, target)
        self.starting_speed = speed

        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # OVERRIDES TROOP UPDATE CLASS 
    # Snipers can move through objects at 1/2 usual speed
    def update(self, moving_troops, all_sprites):
        if self.checkReachedTarget() == True:
            moving_troops.remove(self)
        else:
            collided_sprite = self.checkForCollision(all_sprites)
            if collided_sprite is not None:
                self.speed = self.speed / 2
            else:
                self.speed = self.starting_speed

            self.updateX()
            self.updateY()

class MortarTroop(Troop):
    def __init__(self, w, h, x, y, health, colour, speed, owner, target):
        super().__init__(w, h, x, y, health, colour, speed, owner, target)
        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, target, speed, range, colour, window):
        pygame.sprite.Sprite.__init__(self)
        self.w = w
        self.h = h
        self.startX = x
        self.startY = y
        self.target = target
        self.speed = speed
        self.range = range
        self.range_ticker = 0
        self.colour = colour

        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.window = window

    def update(self):
        if self.checkReachedRange() == True:
            pygame.gfxdraw.circle(self.window, self.rect.x, self.rect.y, self.w*3, (255,0,0))
            self.kill()
        else:
            self.updateX()
            self.updateY()


    def updateX(self):
        if self.target[0] > self.rect.x:
            self.rect.x += self.speed
            self.range_ticker += self.speed
        elif self.target[0] < self.rect.x:
            self.rect.x -= self.speed
            self.range_ticker += self.speed
        else:
            pass

    def updateY(self):
        if self.target[1] > self.rect.y:
            self.rect.y += self.speed
            self.range_ticker += self.speed
        elif self.target[1] < self.rect.y:
            self.rect.y -= self.speed
            self.range_ticker += self.speed
        else:
            pass
        

    def checkReachedRange(self):
        if (self.rect.x == self.target[0]) and (self.rect.y == self.target[1]):
            return True
        if (self.range_ticker >= self.range):
            return True
        return False
    
# Projectile for the mortar troop
# Has a slow speed because it will have a big explosion
class MortarProjecile(Projectile):
    def __init__(self, x, y, w, h, target, speed, range, colour, window):
        super().__init__(self, x, y, w, h, target, speed, range, colour, window)

        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.checkReachedRange() == True:
            pygame.gfxdraw.circle(self.window, self.rect.x, self.rect.y, self.w*6, (255,0,0))
            self.kill()
        else:
            self.updateX()
            self.updateY()
