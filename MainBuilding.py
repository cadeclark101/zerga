import pygame

class MainBuilding(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, health, colour, owner):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.health = health
        self.colour = colour

        self.owner = owner

        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.amount_allowed = 1

    # CHECK FOR NEW BUILDING COLLISION BEFORE PLACING
    def checkForCollision(self, all_sprites, building_menu_container_rect, selected_building_menu_container_rect):
        collides = False

        if self.rect.colliderect(building_menu_container_rect): # Check if building will collide with menu
            collides = True
        
        if self.rect.colliderect(selected_building_menu_container_rect): # Check if SELECTED building will collide with menu
            collides = True

        hits_any_sprites = pygame.sprite.spritecollide(self, all_sprites, False) # Check if sprite will collide with any sprite
        if len(hits_any_sprites) > 0: 
            collides = True

        return collides


    def checkExists(self):
        exists = False
        for building in self.owner.owned_buildings:
            if isinstance(building, MainBuilding):
                exists = True
        return exists