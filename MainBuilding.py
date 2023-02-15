import pygame

class MainBuilding(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, health, colour):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.health = health
        self.colour = colour

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    # CHECK FOR NEW BUILDING COLLISION BEFORE PLACING
    def checkForCollision(self, building_sprites, resource_sprites, building_menu_container_rect):
        collides = False

        if self.rect.colliderect(building_menu_container_rect): # Check if building will collide with menu
            collides = True

        if len(building_sprites) != 0: # Check if building will collide with existing buildings
            for building_sprite in building_sprites:
                if self.rect.colliderect(building_sprite.rect):
                    collides = True

        for resource_sprite in resource_sprites: # Check if new building will collide with any resource nodes
            if self.rect.colliderect(resource_sprite.rect):
                collides = True 

        return collides