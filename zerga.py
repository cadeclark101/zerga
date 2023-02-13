from threading import Thread
import numpy as np
import pygame

from ResourceNode import *
from Player import *
from MenuButton import *
from GreenBuilding import *
from BlueBuilding import *
from MainBuilding import *
from Infantry import *

pygame.init()

window_width = 1920
window_height = 1080
window_object = pygame.display.set_mode((window_width,window_height))
window_object.fill((255, 255, 255))

class MainRun(object):
    def __init__(self,window_width,window_height, window_object):
        self.window_width = window_width
        self.window_height = window_height
        self.window_object = window_object
        
        self.player = Player(0, 0, 0, 0)

        self.building_menu_sprites = pygame.sprite.Group()
        self.selected_building_menu_sprites = pygame.sprite.Group()
        self.resource_sprites = pygame.sprite.Group()
        self.building_sprites = pygame.sprite.Group()
        self.troops_sprites = pygame.sprite.Group()
        self.moving_sprites = pygame.sprite.Group()

        self.selected_troops_target = None

        self.selected_building_menu_container_rect = pygame.Rect(0, 1040, 1920, 40)
        self.building_menu_container_rect = pygame.Rect(1890, 0, 30, 150)

        self.font = pygame.font.SysFont("verdana", 32)
        
        self.Main()

    # REDRAW ALL SPRITES
    def redrawAllSpriteGroups(self):
        self.window_object.fill((255, 255, 255))
        self.drawResourceNodes()
        self.drawBuildMenu()
        self.drawBuildingSprites()
        self.drawMainBuildingMenu()
        self.drawTroopSprites()

    # DRAW ALL RESOURCE NODE SPRITES
    def drawResourceNodes(self):
        pygame.sprite.Group.draw(self.resource_sprites, self.window_object)

    # DRAW ALL MENU SPRITES
    def drawBuildMenu(self):
        building_menu_container_rect = pygame.draw.rect(self.window_object, (255, 255, 255), self.building_menu_container_rect)
        pygame.sprite.Group.draw(self.building_menu_sprites, self.window_object)


    # DRAW ALL BUILDING SPRITES
    def drawBuildingSprites(self):
        pygame.sprite.Group.draw(self.building_sprites, self.window_object)

    # DRAW TROOP MENU FOR MAIN BUILDING
    def drawMainBuildingMenu(self):
        selected_building_menu_container_rect = pygame.draw.rect(self.window_object, (255, 255, 255), self.selected_building_menu_container_rect)
        pygame.sprite.Group.draw(self.selected_building_menu_sprites, self.window_object)

    def drawTroopSprites(self):
        pygame.sprite.Group.draw(self.troops_sprites, self.window_object)

    # CREATE RIGHT SIDE MENU
    def createBuildMenu(self):
        blue_building_button_obj = MenuButton(1890, 0, 30, 30, 1, (0, 0, 0))
        self.building_menu_sprites.add(blue_building_button_obj)

        green_building_button_obj = MenuButton(1890, 50, 30, 30, 2, (0, 0, 0))
        self.building_menu_sprites.add(green_building_button_obj)

        main_building_button_obj = MenuButton(1890, 100, 30, 30, 3, (0, 0, 0))
        self.building_menu_sprites.add(main_building_button_obj)
        pass
        
    # CREATE BUILDING TROOP MENU
    def createMainBuildingMenu(self):
        basic_troop_button_obj = MenuButton(960, 1050, 30, 30, 100, (0, 0, 0))
        self.selected_building_menu_sprites.add(basic_troop_button_obj)
        pass


    def spawnTroop(self):
        new_troop = Infantry(10, 10, self.player.selected_building.x, self.player.selected_building.y, 5, (0, 0, 0))
        self.troops_sprites.add(new_troop)
        self.drawTroopSprites()



    def handleClickEvent(self, mouse_pos, click):

        # PLACE RESOURCE BUILDING FUNCTION
        def placeBuilding(button_id, resource_type):
            if button_id == resource_type: # Check clicked resource type is same as button id (green = 1, blue = 2)
                if resource_type == 1: # Check for green resource clicked
                    new_building = GreenBuilding(10, 10, 500, (0, 255, 0), resource_node) # Place green resource building
                elif resource_type == 2:
                    new_building = BlueBuilding(10, 10, 500, (0, 0, 128), resource_node) # Place blue resource building
                self.player.increaseResourceIncome(resource_type, 1)    
                self.building_sprites.add(new_building)
                self.drawBuildingSprites()
                self.drawBuildMenu()

            # CREATE NEW MAIN BUILDING TYPE
            elif button_id == 3:
                new_building = MainBuilding(mouse_pos[0], mouse_pos[1], 50, 50, 1000, (123, 123, 123))
                if checkForCollision(new_building.rect) == True:
                    print("collides")
                else:
                    self.building_sprites.add(new_building)
                    self.drawBuildingSprites() # Redraw all sprites
                    self.drawBuildMenu() # Redraw all sprites
            else:
                pass
        
        # CHECK FOR NEW BUILDING COLLISION BEFORE PLACING
        def checkForCollision(new_building_rect):
            collides = False

            if new_building_rect.colliderect(self.building_menu_container_rect): # Check if building will collide with menu
                collides = True

            if len(self.building_sprites) != 0: # Check if building will collide with existing buildings
                for building_sprite in self.building_sprites:
                    if new_building_rect.colliderect(building_sprite.rect):
                        collides = True

            for resource_sprite in self.resource_sprites: # Check if new building will collide with any resource nodes
                if new_building_rect.colliderect(resource_sprite.rect):
                    collides = True 

            return collides

        # CHECK FOR LEFT CLICK
        if click == (True, False, False): 
            # CHECK IF MENU BUTTON IS CLICKED
            for menu_sprite in self.building_menu_sprites:
                if menu_sprite.rect.collidepoint(mouse_pos):
                    self.player.selected_menu_button = menu_sprite # Set selected menu button
                    break
                else:
                    pass

            # CHECK IF RESOURCE NODE IS CLICKED
            for resource_node in self.resource_sprites: 
                if resource_node.rect.collidepoint(mouse_pos): 
                    if self.player.selected_menu_button is not None: # Check a selected button is not none 
                        placeBuilding(self.player.selected_menu_button.getButtonID(), resource_node.resource_type)
                    else:
                        print("no building selected")
                        break 
                else:
                    pass

            # CHECK IF BUILDING IS CLICKED
            for building_sprite in self.building_sprites:
                if building_sprite.rect.collidepoint(mouse_pos):
                    self.player.selected_menu_button = None
                    self.player.selected_building = building_sprite
                    self.createMainBuildingMenu()
                    self.drawMainBuildingMenu()
                    

            # CHECK IF ANYWHERE NOT OCCUPIED BY MENU OR RESOURCE IS CLICKED
            if self.player.selected_menu_button is not None:
                if self.player.selected_menu_button.getButtonID() == 3:
                    placeBuilding(self.player.selected_menu_button.getButtonID(), None)


        # CLEAR CURSOR ON RIGHT CLICK             
        elif click == (False, False, True): 
            self.player.selected_menu_button = None
            print("cleared cursor")

        
        
                                    
            

    def Main(self):
        run = True

        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = pygame.mouse.get_pressed()
                    mouse_pos = pygame.mouse.get_pos()
                    self.handleClickEvent(mouse_pos, click)

                # CHECK FOR KEYBOARD EVENTS
                if event.type == pygame.KEYDOWN:
                    if self.player.selected_building is not None: # Spawn troops if building is selected and "a" is pressed
                        if event.key == pygame.K_a:
                            self.spawnTroop()
                            print("spawned 1 troop")
                
                    self.player.selected_troop_group = self.troops_sprites # REMOVE THIS JUST FOR TESTING REMOVE THIS JUST FOR TESTING REMOVE THIS JUST FOR TESTING REMOVE THIS JUST FOR TESTING
                    if self.player.selected_troop_group == self.troops_sprites:
                        if event.key == pygame.K_SPACE:
                            self.selected_troops_target = pygame.mouse.get_pos() 
                            self.moving_sprites.add(self.player.selected_troop_group)
                    else:
                        pass
 
            # CHECK IF ANY THAT ANY SPRITES THAT ARE MOVING EXIST
            if len(self.moving_sprites) != 0:
                print("test")

            #  SPAWN X RESOURCE NODES IF NONE EXIST
            if len(self.resource_sprites) == 0:
                for i in range(25):
                    resource_obj = ResourceNode(self.window_width, self.window_height, 5, 5, self.window_object)
                    self.resource_sprites.add(resource_obj)
                self.drawResourceNodes() # First draw of nodes
            else:
                pass
            
            self.createBuildMenu()
            self.drawBuildMenu()
            self.drawTroopSprites()
            

            pygame.display.update() 
        pygame.quit()


if __name__ == "__main__":
    MainRun(window_width, window_height, window_object)