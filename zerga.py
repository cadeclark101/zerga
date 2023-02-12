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

        self.font = pygame.font.SysFont("verdana", 32)
        
        self.Main()


    def drawResourceNodes(self, nResources):
        for i in range(nResources):
            resource_obj = ResourceNode(self.window_width, self.window_height, 5, 5, self.window_object)
            self.resource_sprites.add(resource_obj)

        

    def drawOverlay(self):
        green_resource_text = self.font.render(str(self.player.green_resource), True, (0, 255, 0), None)

        blue_resource_text = self.font.render(str(self.player.green_resource), True, (0, 0, 128), None)
        
        self.window_object.blit(green_resource_text, (0,0)) 
        self.window_object.blit(blue_resource_text, (0,35)) 

    def incomeTicker(self):
        self.player.incomeTicker()


    def buildingMenu(self):
        menu_container_rect = pygame.Rect(1890, 0, 30, 120)
        self.menu_container = pygame.draw.rect(self.window_object, (100, 123, 255), menu_container_rect)
        
        blue_building_button_obj = MenuButton(1890, 0, 30, 30, self.window_object, 1)
        self.menu_sprites.add(blue_building_button_obj)

        green_building_button_obj = MenuButton(1890, 50, 30, 30, self.window_object, 2)
        self.menu_sprites.add(green_building_button_obj)

        main_building_button_obj = MenuButton(1890, 100, 30, 30, self.window_object, 3)
        self.menu_sprites.add(main_building_button_obj)




    def handleClickEvent(self, mouse_pos, click):

        # PLACE RESOURCE BUILDING FUNCTION
        def placeResourceBuilding(button_id, resource_type):
            if button_id == resource_type: # Check clicked resource type is same as button id (green = 1, blue = 2)
                if resource_type == 1: # Check for green resource clicked
                    new_building = GreenBuilding(10, 10, 500, resource_node, self.window_object) # Place green resource building
                    self.player.increaseResourceIncome(resource_type, 1)
                elif resource_type == 2:
                    new_building = BlueBuilding(10, 10, 500, resource_node, self.window_object) # Place blue resource building
                    self.player.increaseResourceIncome(resource_type, 1)
                self.building_sprites.add(new_building)
            else:
                pass


        # CHECK FOR LEFT CLICK
        if click == (True, False, False): 
            # CHECK IF MENU BUTTON IS CLICKED
            for menu_sprite in self.menu_sprites:
                if menu_sprite.rect.collidepoint(mouse_pos):
                    self.player.selected_menu_button = menu_sprite # Set selected menu button
                    print(self.player.selected_menu_button.getButtonID())
                    break



            # CHECK IF RESOURCE NODE IS CLICKED
            for resource_node in self.resource_sprites: 
                if resource_node.rect.collidepoint(mouse_pos): 
                    if self.player.selected_menu_button is not None: # Check a selected button is not none 
                        placeResourceBuilding(self.player.selected_menu_button.getButtonID(), resource_node.resource_type)
                    else:
                        print("no building selected")
                        break  



            # CHECK IF DESIRED BUILDING WILL COLLIDE WITH OTHER BUILDINGS OR RESOURCES
            if self.player.selected_menu_button is not None:
                if self.player.selected_menu_button.getButtonID() == 3:
                    new_building = MainBuilding(mouse_pos[0], mouse_pos[1], 50, 50, 1000, self.window_object)
                    self.building_sprites.add(new_building)
            else:
                pass

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
                    print(mouse_pos)
                    self.handleClickEvent(mouse_pos, click)
 

            if len(self.resource_sprites) == 0:
                self.drawResourceNodes(25)
            else:
                pass
            
            self.drawOverlay()
            self.buildingMenu()

            pygame.display.update() 
        pygame.quit()


if __name__ == "__main__":
    MainRun(window_width, window_height, window_object)