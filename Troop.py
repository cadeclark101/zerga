import pygame
from pygame import gfxdraw

from Player import Player


class Troop(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, health, colour, speed, owner, enemy, target, range, attack_target=None):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.health = health
        self.colour = colour
        self.speed = speed
        self.owner = owner
        self.enemy = enemy
        self.target = target
        self.range = range
        self.attack_target = attack_target

        self.range_rect = pygame.Rect(self.x, self.y, self.range, self.range)
        
    
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

        self.getSpritesInRange()


    def updateX(self):
        if self.target[0] > self.rect.x:
            self.rect.x += self.speed
            self.range_rect.x += self.speed
        elif self.target[0] < self.rect.x:
            self.rect.x -= self.speed
            self.range_rect.x -= self.speed
        else:
            pass

    def updateY(self):
        if self.target[1] > self.rect.y:
            self.rect.y += self.speed
            self.range_rect.y += self.speed
        elif self.target[1] < self.rect.y:
            self.rect.y -= self.speed
            self.range_rect.y -= self.speed
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
        
    def getTroopTypeID(self):
        return self.troop_type_id
    
    def getSpritesInRange(self):
        enemy_buildings = self.enemy.getOwnedBuildings()
        enemy_sprites_in_range = self.range_rect.collidelistall(list(enemy_buildings))
        if len(enemy_sprites_in_range) != 0:
            self.attack_target = list(enemy_buildings)[0] # select first sprite in range as target for projectiles
        else:
            pass  


class BasicTroop(Troop):
    def __init__(self, w, h, x, y, health, colour, speed, owner, enemy, target, range, attack_target):
        super().__init__(w, h, x, y, health, colour, speed, owner, enemy, target, range, attack_target)
        self.troop_type_id = 1

        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y




class SniperTroop(Troop):
    def __init__(self, w, h, x, y, health, colour, speed, owner, enemy, target, range, attack_target):
        super().__init__(w, h, x, y, health, colour, speed, owner, enemy, target, range, attack_target)

        self.troop_type_id = 2

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
    def __init__(self, w, h, x, y, health, colour, speed, owner, enemy, target, range, attack_target):
        super().__init__(w, h, x, y, health, colour, speed, owner, enemy, target, range, attack_target)

        self.troop_type_id = 3

        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, target, speed, colour, window):
        pygame.sprite.Sprite.__init__(self)
        self.w = w
        self.h = h
        self.startX = x
        self.startY = y
        self.target = target
        self.speed = speed
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
        

    def checkReachedRange(self):
        if (self.rect.x == self.target[0]) and (self.rect.y == self.target[1]):
            return True
        return False
    
