import Player
import random

import pygame

from Player import Player


class Enemy(Player):
    def __init__(self, green_resource, blue_resource, green_resource_income, blue_resource_income):
        Player.__init__(self, green_resource, blue_resource, green_resource_income, blue_resource_income)
        
        self.owned_troops = pygame.sprite.Group()
        self.owned_buildings = pygame.sprite.Group()

        self.basic_troops = pygame.sprite.Group()
        self.sniper_troops = pygame.sprite.Group()
        self.mortar_troops = pygame.sprite.Group()

        self.data = None


    def firstTurn(self):
        if len(self.owned_buildings) > 0:
            return True
        else:
            return False
        
        
    def getRandomCoord(self, range):
        x = random.randint(50, range - 50)
        return x
