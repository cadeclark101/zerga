import numpy as np
import pygame
import random

pygame.init()

w = 1000
h = 1000
window = pygame.display.set_mode((w,h))

class MainRun(object):
    def __init__(self,w,h, window):
        self.w = w
        self.h = h
        self.window = window
        self.resource_positions = None
        self.Main()

    def Main(self):
        self.selected_building = None
        stopped = False

        while stopped == False:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
    
                self.Menu(event)
                self.CreateResourceNodes()


                
    def CreateResourceNodes(self):
        def SelectRandomCoordinate():
            coord1 = random.randint(1, self.w - 30)
            coord2 = random.randint(1, self.w - 30)
            coords = np.array([coord1, coord2])
            return coords

        def SelectRandomResourceType():
            resource_type = random.randint(1, 1 + 1)
            return resource_type

        def DrawResourceNodes():
            self.resources_list = np.empty(shape=[0])
            self.resource_node_list = [] # Can't be a Numpy array because I want the objects

            for i in range(len(self.resource_positions)):
                coords = self.resource_positions[i, [0]]
                self.resources_list = np.append(self.resources_list, [ResourceNode(coords[0][0], coords[0][1], self.resource_positions[i, [1]])], axis=0)

                node = pygame.Rect(coords[0][0], coords[0][1], 10, 10)
                self.resource_node_list.append(node)
                pygame.draw.rect(self.window, (100,100,100), node)

                pygame.display.update() #UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE 
        
        if self.resource_positions is None:
            self.resource_positions = np.empty(shape=[0,2])
            for i in range(random.randint(10, 50 + 1)):
                self.resource_positions = np.append(self.resource_positions, [[SelectRandomCoordinate(), SelectRandomResourceType()]], axis=0)
    
    
            DrawResourceNodes()


    def Menu(self, event):
        def action(mouse): # MOVE THIS TO NODE RESOURCES FUNCTIONS -> CHANGE THIS TO HANDLE THE MENU ITEMS
            for node in self.resource_node_list:
                if node.collidepoint(mouse):
                    print("clicked") # WORKING ON HERE WORKING ON HERE WORKING ON HERE WORKING ON HERE WORKING ON HERE WORKING ON HERE WORKING ON HERE WORKING ON HERE

        def DrawMenu():
            miner_button = pygame.Rect(0, 0, 20, 20)
            miner_button.center = (self.w - 20, self.h - 980)
            pygame.draw.rect(self.window, (255,0,0), miner_button)

            power_plant_button = pygame.Rect(0, 0, 20, 20)
            power_plant_button.center = (self.w - 20, self.h - 955)
            pygame.draw.rect(self.window, (0,255,0), power_plant_button)

            artillery_button = pygame.Rect(0, 0, 20, 20)
            artillery_button.center = (self.w - 20, self.h - 20)
            pygame.draw.rect(self.window, (0,0,255), artillery_button) 

        DrawMenu()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos() 
            action(mouse)
        

        

class ResourceNode(object):
    def __init__(self, x, y, resource_type):
        self.x = x
        self.y = y
        self.owner = None              
        self.resource_type = resource_type

class Building(object):
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp

class Miner(Building):
    def __init__(self, x, y):
        Building.__init__(self, x, y)
        self.grps = 10

class PowerPlant(Building):
    def __init__(self, x, y):
        Building.__init__(self, x, y)
        self.erps = 10

class Artillery(Building):
    def __init__(self, x, y):
        Building.__init__(self, x, y)
        self.dmg = 100
        self.range = 100

if __name__ == "__main__":
    MainRun(w, h, window)