import numpy as np
import pygame

from ResourceNode import *
from Player import *
from MenuButton import *

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
        self.resource_node_list = []

        self.font = pygame.font.SysFont("verdana", 32)
        
        self.Main()


    def drawResourceNodes(self, nResources):
        for i in range(nResources):
            resource_obj = ResourceNode(self.window_width, self.window_height)
            self.resource_node_list.append(resource_obj)
            resource_rect =  pygame.Rect(resource_obj.getResourceCoords()[0], resource_obj.getResourceCoords()[1], 10, 10)
            if resource_obj.resource_type == 1:
                pygame.draw.rect(self.window_object, (0, 255, 0), resource_rect) # GREEN
            else:
                pygame.draw.rect(self.window_object, (0, 0, 128), resource_rect) # BLUE

        

    def drawOverlay(self):
        green_resource_text = self.font.render(str(self.player.green_resource), True, (0, 255, 0), None)

        blue_resource_text = self.font.render(str(self.player.green_resource), True, (0, 0, 128), None)
        
        self.window_object.blit(green_resource_text, (0,0)) 
        self.window_object.blit(blue_resource_text, (0,35)) 


    def drawBuildingMenu(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        blue_building_button_obj = MenuButton(1890, 0, 30, 30, "not none")
        green_building_button_obj = MenuButton(1890, 50, 30, 30, "not none")

        green_resource_building_rect = pygame.Rect(blue_building_button_obj.x, blue_building_button_obj.y, blue_building_button_obj.w, blue_building_button_obj.h)
        blue_resource_building_rect = pygame.Rect(green_building_button_obj.x, green_building_button_obj.y, green_building_button_obj.w, green_building_button_obj.h)

        if blue_building_button_obj.x + blue_building_button_obj.w > mouse[0] > blue_building_button_obj.x and blue_building_button_obj.y + blue_building_button_obj.h > mouse[1] > blue_building_button_obj.y:
            pygame.draw.rect(self.window_object, (0, 0, 0), blue_resource_building_rect)
            if click[0] == 1 and blue_building_button_obj.action is not None:
                print("clicked green") # ADD BUTTON ACTION CALLING HERE

        elif green_building_button_obj.x + green_building_button_obj.w > mouse[0] > green_building_button_obj.x and green_building_button_obj.y + green_building_button_obj.h > mouse[1] > green_building_button_obj.y:
            pygame.draw.rect(self.window_object, (0, 0, 0), green_resource_building_rect)
            if click[0] == 1 and blue_building_button_obj.action is not None:
                print("clicked blue") # ADD BUTTON ACTION CALLING HERE

        else:
            pygame.draw.rect(self.window_object, (0, 0, 0), blue_resource_building_rect)
            pygame.draw.rect(self.window_object, (0, 0, 0), green_resource_building_rect)
            

    def Main(self):
        run = True

        while run:
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if len(self.resource_node_list) == 0:
                self.drawResourceNodes(25)
            else:
                pass

            self.drawOverlay()
            self.drawBuildingMenu()

            pygame.display.update() 
        pygame.quit()


if __name__ == "__main__":
    MainRun(window_width, window_height, window_object)