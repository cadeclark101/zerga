import numpy as np
import pygame

from ResourceNode import *
from Player import *
from MenuButton import *
from GreenBuilding import *
from BlueBuilding import *
from MainBuilding import *

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

        self.menu_sprites = pygame.sprite.Group()
        self.resource_sprites = pygame.sprite.Group()
        self.building_sprites = pygame.sprite.Group()

        self.building_menu_container_rect = pygame.Rect(1890, 0, 30, 120)

        self.font = pygame.font.SysFont("verdana", 32)
        
        self.Main()


    def drawResourceNodes(self, nResources):
        for i in range(nResources):
            resource_obj = ResourceNode(self.window_width, self.window_height, 5, 5, self.window_object)
            self.resource_sprites.add(resource_obj)



    def drawMenuSprites(self):
        menu_container = pygame.draw.rect(self.window_object, (100, 123, 255), self.building_menu_container_rect)
        for sprite in self.menu_sprites:
            pygame.draw.rect(self.window_object, sprite.colour, (sprite.x, sprite.y, sprite.w, sprite.h))



    def drawBuildingSprites(self):
        for sprite in self.building_sprites:
            pygame.draw.rect(self.window_object, sprite.colour, (sprite.x, sprite.y, sprite.w, sprite.h))


    def drawOverlay(self):
        green_resource_text = self.font.render(str(self.player.green_resource), True, (0, 255, 0), None)

        blue_resource_text = self.font.render(str(self.player.green_resource), True, (0, 0, 128), None)
        
        self.window_object.blit(green_resource_text, (0,0)) 
        self.window_object.blit(blue_resource_text, (0,35)) 



    def incomeTicker(self):
        self.player.incomeTicker()


    def buildingMenu(self):
        blue_building_button_obj = MenuButton(1890, 0, 30, 30, 1, (0, 0, 0))
        self.menu_sprites.add(blue_building_button_obj)

        green_building_button_obj = MenuButton(1890, 50, 30, 30, 2, (0, 0, 0))
        self.menu_sprites.add(green_building_button_obj)

        main_building_button_obj = MenuButton(1890, 100, 30, 30, 3, (0, 0, 0))
        self.menu_sprites.add(main_building_button_obj)
        pass
        



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
                self.drawMenuSprites()

            # CREATE NEW MAIN BUILDING TYPE
            elif button_id == 3:
                new_building = MainBuilding(mouse_pos[0], mouse_pos[1], 50, 50, 1000, (123, 123, 123))
                if checkForCollision(new_building.rect) == True:
                    print("collides")
                else:
                    self.building_sprites.add(new_building)
                    self.drawBuildingSprites()
                    self.drawMenuSprites()
            else:
                pass
        
        # Function that checks if new building will collide with anything else
        def checkForCollision(new_building_rect):
            collides = False
            if new_building_rect.colliderect(self.building_menu_container_rect): # Check if building will collide with menu
                collides = True
            for resource_sprite in self.resource_sprites: # Check if new building will collide with any resource nodes
                if new_building_rect.colliderect(resource_sprite.rect):
                    collides = True 
            return collides

        # CHECK FOR LEFT CLICK
        if click == (True, False, False): 
            # CHECK IF MENU BUTTON IS CLICKED
            for menu_sprite in self.menu_sprites:
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
            
            if self.player.selected_menu_button is not None:
                if self.player.selected_menu_button.getButtonID() == 3:
                    placeBuilding(self.player.selected_menu_button.getButtonID(), None)

            #for each menusprite
                #is the mouse position from current to mouse position + building width less than the 

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
 
            if len(self.resource_sprites) == 0:
                self.drawResourceNodes(25)
            else:
                pass
            
            self.drawMenuSprites()
            self.drawOverlay()
            self.buildingMenu()

            pygame.display.update() 
        pygame.quit()


if __name__ == "__main__":
    MainRun(window_width, window_height, window_object)