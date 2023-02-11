import numpy as np
import pygame

from ResourceNode import *
from Player import *
from MenuButton import *
from GreenBuilding import *

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


    def buildingMenu(self):
        blue_building_button_obj = MenuButton(1890, 0, 30, 30, self.window_object)
        self.menu_sprites.add(blue_building_button_obj)

        green_building_button_obj = MenuButton(1890, 50, 30, 30, self.window_object)
        self.menu_sprites.add(green_building_button_obj)
            

    def Main(self):
        run = True

        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = pygame.mouse.get_pressed()
                    mouse_pos = pygame.mouse.get_pos()

                    if click == (True, False, False): # Select building menu button
                        for menu_sprite in self.menu_sprites:
                            if menu_sprite.rect.collidepoint(mouse_pos):
                                self.player.selected_menu_button = menu_sprite
                                print(self.player.selected_menu_button)
                                break

                        for resource_node in self.resource_sprites:
                            if resource_node.rect.collidepoint(mouse_pos):
                                if self.player.selected_menu_button is not None:
                                    if resource_node.resource_type == 1:
                                        new_building = GreenBuilding(10, 10, resource_node, self.window_object)
                                        self.building_sprites.add(new_building)
                                    else: 
                                        print("create blue building")
                                else:
                                    print("no building selected")
                                break

                    elif click == (False, False, True): # Clear cursor on right click from menu selection
                        self.player.selected_menu_button = None
                        print("cleared cursor")

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