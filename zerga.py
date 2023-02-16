from threading import Event, Thread, Timer
import threading
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

building_sprites = pygame.sprite.Group()
troops_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

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

        self.moving_troops = pygame.sprite.Group()

        self.selected_building_menu_container_rect = pygame.Rect(0, 1040, 1920, 40)
        self.building_menu_container_rect = pygame.Rect(1890, 0, 30, 150)

        self.font = pygame.font.SysFont("verdana", 32)
        
        self.Main()

    def redrawAll(self):
        window_object.fill((255, 255, 255))
        self.drawBuildMenu()
        self.drawBuildingSprites()
        self.drawOverlay()
        self.drawMainBuildingMenu()
        self.drawTroopSprites()
        self.drawProjectiles()

    # DRAW ALL RESOURCE NODE SPRITES
    def drawResourceNodes(self):
        for resource_sprite in self.resource_sprites:
            pygame.draw.rect(self.window_object, resource_sprite.colour, (resource_sprite))

    # DRAW ALL MENU SPRITES
    def drawBuildMenu(self):
        pygame.draw.rect(self.window_object, (255, 255, 255), self.building_menu_container_rect)
        for sprite in self.building_menu_sprites:
            pygame.draw.rect(self.window_object, sprite.colour, (sprite.x, sprite.y, sprite.w, sprite.h))


    # DRAW ALL BUILDING SPRITES
    def drawBuildingSprites(self):
        for sprite in building_sprites:
            pygame.draw.rect(self.window_object, sprite.colour, (sprite.x, sprite.y, sprite.w, sprite.h))

    # DRAW INFO OVERLAY
    def drawOverlay(self):
        green_resource_text = self.font.render(str(self.player.green_resource), True, (0, 255, 0), None)

        blue_resource_text = self.font.render(str(self.player.green_resource), True, (0, 0, 128), None)
        
        self.window_object.blit(green_resource_text, (0,0)) 
        self.window_object.blit(blue_resource_text, (0,35)) 

    # DRAW TROOP MENU FOR MAIN BUILDING
    def drawMainBuildingMenu(self):
        pygame.draw.rect(self.window_object, (255, 255, 255), self.selected_building_menu_container_rect)
        for sprite in self.selected_building_menu_sprites:
            pygame.draw.rect(self.window_object, sprite.colour, (sprite.x, sprite.y, sprite.w, sprite.h))

    # DRAW ALL TROOP SPRITES
    def drawTroopSprites(self):
        for sprite in troops_sprites:
            pygame.draw.rect(self.window_object, sprite.colour, (sprite.x, sprite.y, sprite.w, sprite.h))

    # DRAW PROJECTILES
    def drawProjectiles(self):
        for proj in projectiles:
            pygame.draw.line(self.window_object, proj.colour, (proj.startX, proj.startY), (proj.endX, proj.endY), 3)

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

    # CREATE RESOURCE NODE OBJECTS
    def createResourceNodes(self):
        for i in range(20):
            green_resource_obj = ResourceNode(1920, 1080, 10, 10, (0, 255, 0))
            blue_resource_obj = ResourceNode(1920, 1080, 10, 10, (0, 0, 128))
            self.resource_sprites.add(green_resource_obj)
            self.resource_sprites.add(blue_resource_obj)
        self.drawResourceNodes()

    # SPAWN NEW TROOP
    def createTroop(self):
        new_troop = Infantry(10, 10, self.player.selected_building.x, self.player.selected_building.y, 5, (0, 0, 0))
        troops_sprites.add(new_troop)
        self.drawTroopSprites()

    # FIRE PROJECTILE FROM ALL SELECTED SPRITES
    def fireProj(self, sprite, proj_target):
        new_proj = InfantryProjectile(sprite.x, sprite.y, proj_target[0], proj_target[1], (0,0,0))
        projectiles.add(new_proj)
        self.drawProjectiles()
        remove_proj_thread = Timer(0.5, self.removeProj, [new_proj],{})
        remove_proj_thread.start()
        self.redrawAll()

    # REMOVE PROJECTILE AFTER X AMOUNT OF TIME
    def removeProj(self, proj):
        projectiles.remove(proj)


    def handleClickEvent(self, mouse_pos, click):

        # PLACE RESOURCE BUILDING FUNCTION
        def placeBuilding(button_id, resource_type):
            if button_id == resource_type: # Check clicked resource type is same as button id (green = 1, blue = 2)
                if resource_type == 1: # Check for green resource clicked
                    new_building = GreenBuilding(20, 20, 500, (0, 255, 0), resource_node, self.player) # Place green resource building
                    print(self.player.green_resource_income)
                elif resource_type == 2:
                    new_building = BlueBuilding(20, 20, 500, (0, 0, 128), resource_node, self.player) # Place blue resource building   
                    print(self.player.green_resource_income)
                building_sprites.add(new_building)
                self.drawBuildingSprites()

            # CREATE NEW MAIN BUILDING TYPE
            elif button_id == 3:
                new_building = MainBuilding(mouse_pos[0], mouse_pos[1], 50, 50, 1000, (123, 123, 123))
                if new_building.checkForCollision(building_sprites, self.resource_sprites, self.building_menu_container_rect) == True:
                    print("collides")
                else:
                    building_sprites.add(new_building)
                    self.drawBuildingSprites() # Redraw all sprites
            else:
                pass


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
            for building_sprite in building_sprites:
                if building_sprite.rect.collidepoint(mouse_pos):
                    self.player.selected_menu_button = None
                    self.player.selected_building = building_sprite
                    self.createMainBuildingMenu()
                    self.drawMainBuildingMenu()
                    

            # CHECK IF ANYWHERE NOT OCCUPIED BY MENU OR RESOURCE IS CLICKED
            if self.player.selected_menu_button is not None:
                if self.player.selected_menu_button.getButtonID() == 3:
                    placeBuilding(self.player.selected_menu_button.getButtonID(), None)

        # CHECK FOR MIDDLE MOUSE CLICK
        if click == (False, True, False):
            proj_target = pygame.mouse.get_pos()
            if self.player.selected_troop_group != None:
                proj_threads = [Thread(target=self.fireProj(sprite, proj_target)) for sprite in self.player.selected_troop_group]
                for thread in proj_threads:
                    thread.start()

        # CLEAR CURSOR ON RIGHT CLICK             
        if click == (False, False, True): 
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
                            self.createTroop()
                
                    self.player.selected_troop_group = troops_sprites # REMOVE THIS JUST FOR TESTING
                    if self.player.selected_troop_group == troops_sprites:
                        if event.key == pygame.K_SPACE:
                            target_pos = pygame.mouse.get_pos() 
                            [self.moving_troops.add(sprite) for sprite in self.player.selected_troop_group]
                    else:
                        pass
            
            # MOVE PLACED TROOPS
            if len(self.moving_troops) != 0:
                moving_troop_threads = [Thread(target=sprite.moveToTarget(target_pos)) for sprite in self.moving_troops]
                print(len(moving_troop_threads))
                for thread in moving_troop_threads:
                    thread.start()
                self.redrawAll()
                
            
            if len(self.resource_sprites) == 0:
                self.createResourceNodes()
            else:
                self.drawResourceNodes()
            self.createBuildMenu()
            self.drawBuildMenu()
            self.drawOverlay()
            self.drawTroopSprites()
            

            pygame.display.update() 
        pygame.quit()


if __name__ == "__main__":
    MainRun(window_width, window_height, window_object)

    