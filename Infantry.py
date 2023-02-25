import sys
import pygame
from pygame import gfxdraw

from Player import Player


class Infantry(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, health, colour, owner):
        pygame.sprite.Sprite.__init__(self)
        self.health = health
        self.colour = colour
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.owner = owner
        
        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self, target_pos, moving_troops, all_sprites):
        if self.checkReachedTarget(target_pos) == True:
            moving_troops.remove(self)


        collided_sprite = self.checkForCollision(all_sprites)
        if collided_sprite is not None:
            pass
            # WORKING HERE # WORKING HERE # WORKING HERE # WORKING HERE # WORKING HERE # WORKING HERE

        else:
            self.updateX(target_pos)
            self.updateY(target_pos)


    def updateX(self, target_pos):
        if target_pos[0] > self.rect.x:
            self.rect.x += 1
        elif target_pos[0] < self.rect.x:
            self.rect.x -= 1
        else:
            pass

    def updateY(self, target_pos):
        if target_pos[1] > self.rect.y:
            self.rect.y += 1
        elif target_pos[1] < self.rect.y:
            self.rect.y -= 1
        else:
            pass


    def checkReachedTarget(self, target_pos):
        if target_pos[0] == self.rect.x and target_pos[1] == self.rect.y:
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



class InfantryProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, target, speed, range, colour, window):
        pygame.sprite.Sprite.__init__(self)
        self.w = w
        self.h = h
        self.startX = x
        self.startY = y
        self.target = target
        self.speed = speed
        self.range = range
        self.colour = colour

        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.window = window

    def update(self):
        if self.checkReachedRange() == False:
            if self.target[0] > self.rect.x:
                self.rect.x += self.speed
            elif self.target[0] < self.rect.x:
                self.rect.x -= self.speed
            else:
                pass

            if self.target[1] > self.rect.y:
                self.rect.y += self.speed
            elif self.target[1] < self.rect.y:
                self.rect.y -= self.speed
            else:
                pass
        else:
            pygame.gfxdraw.circle(self.window, self.rect.x, self.rect.y, self.w*3, (255,0,0))
            self.kill()
        

    def checkReachedRange(self): 
        if (self.rect.x == self.target[0]) and (self.rect.y == self.target[1]):
            return True
        elif (self.startX - self.rect.x == -abs(self.range)):
            return True
        elif (self.startX - self.rect.x == self.range):
            return True
        elif (self.startY - self.rect.y == -abs(self.range)):
            return True
        elif (self.startY - self.rect.y == self.range):
            return True
        else:
            return False