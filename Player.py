import pygame

class Player(object):
    def __init__(self, green_resource, blue_resource, green_resource_income, blue_resource_income):
        self.green_resource = green_resource
        self.blue_resource = blue_resource

        self.green_resource_income = green_resource_income
        self.blue_resource_income = blue_resource_income

        self.owned_troops = pygame.sprite.Group()
        self.owned_buildings = pygame.sprite.Group()

        self.basic_troops = pygame.sprite.Group()
        self.sniper_troops = pygame.sprite.Group()
        self.mortar_troops = pygame.sprite.Group()

        self.selected_menu_button = None
        self.selected_building = None
        self.selected_troop_group = None

    def addTroopToGroup(self, troop, troop_id):
        if troop_id == 1:
            self.basic_troops.add(troop)
        elif troop_id == 2:
            self.sniper_troops.add(troop)
        elif troop_id == 3:
            self.mortar_troops.add(troop)

    def incomeTicker(self):
        self.green_resource += self.green_resource_income
        self.blue_resource += self.blue_resource_income

    def getOwnedTroops(self):
        return self.owned_troops
    
    def getOwnedBuildings(self):
        return self.owned_buildings
    
