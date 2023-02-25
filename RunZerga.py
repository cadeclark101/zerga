from threading import Thread, Timer
from profilehooks import profile
import numpy as np
import pygame

from Enemy import *
from ResourceNode import *
from Player import *
from MenuButton import *
from GreenBuilding import *
from BlueBuilding import *
from MainBuilding import *
from Infantry import *

pygame.init()

fps_clock = pygame.time.Clock()
game_clock = pygame.time.Clock()
framerate = 60

all_sprites = pygame.sprite.Group()
building_sprites = pygame.sprite.Group()
all_troop_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
resource_sprites = pygame.sprite.Group()

window_width = 1920
window_height = 1080
window_object = pygame.display.set_mode((window_width,window_height))
window_object.fill((255, 255, 255))

class MainRun(object):
    def __init__(self,window_width,window_height, window_object):
        self.firstRun = True

        self.window_width = window_width
        self.window_height = window_height
        self.window_object = window_object
        
        self.player = Player(0, 0, 0, 0)
        self.enemy = Enemy(0, 0, 0, 0)

        self.building_menu_sprites = pygame.sprite.Group()
        self.selected_building_menu_sprites = pygame.sprite.Group()

        self.moving_troops = pygame.sprite.Group()

        self.selected_building_menu_container_rect = pygame.Rect(0, 1040, 1920, 40)
        self.building_menu_container_rect = pygame.Rect(1890, 0, 30, 150)

        self.font = pygame.font.SysFont("verdana", 32)
        
        self.Main()


    # DRAW INFO OVERLAY
    def drawOverlay(self):
        green_resource_text = self.font.render(str(self.player.green_resource), True, (0, 255, 0), None)

        blue_resource_text = self.font.render(str(self.player.green_resource), True, (0, 0, 128), None)
        
        self.window_object.blit(green_resource_text, (0,0)) 
        self.window_object.blit(blue_resource_text, (0,35)) 

    # CREATE RIGHT SIDE MENU
    def createBuildMenu(self):
        blue_building_button_obj = MenuButton(1890, 0, 30, 30, 1, (0, 0, 0))
        self.building_menu_sprites.add(blue_building_button_obj)
        all_sprites.add(blue_building_button_obj)

        green_building_button_obj = MenuButton(1890, 50, 30, 30, 2, (0, 0, 0))
        self.building_menu_sprites.add(green_building_button_obj)
        all_sprites.add(green_building_button_obj)

        main_building_button_obj = MenuButton(1890, 100, 30, 30, 3, (0, 0, 0))
        self.building_menu_sprites.add(main_building_button_obj)
        all_sprites.add(main_building_button_obj)
        pass
        
    # CREATE BUILDING TROOP MENU
    def createMainBuildingMenu(self):
        basic_troop_button_obj = MenuButton(960, 1050, 30, 30, 100, (0, 0, 0))
        self.selected_building_menu_sprites.add(basic_troop_button_obj)
        all_sprites.add(basic_troop_button_obj)
        pass

    # CREATE RESOURCE NODE OBJECTS
    def createResourceNodes(self):
        for i in range(20):
            green_resource_obj = ResourceNode(1920, 1080, 10, 10, (0, 255, 0))
            blue_resource_obj = ResourceNode(1920, 1080, 10, 10, (0, 0, 128))
            resource_sprites.add(green_resource_obj)
            resource_sprites.add(blue_resource_obj)
            all_sprites.add(green_resource_obj)
            all_sprites.add(blue_resource_obj)

    # SPAWN NEW TROOP
    def createTroop(self, owner):
        new_troop = Infantry(10, 10, self.player.selected_building.x, self.player.selected_building.y, 5, (0, 0, 0), owner)
        owner.owned_troops.add(new_troop)
        all_troop_sprites.add(new_troop)
        all_sprites.add(new_troop)


    # FIRE PROJECTILE FROM ALL SELECTED SPRITES
    def fireProj(self, proj_direction):
        for sprite in all_troop_sprites:
            new_proj = InfantryProjectile(sprite.rect.x, sprite.rect.y, 5, 5, proj_direction, 2, 100, (0,0,0), self.window_object)
            projectiles.add(new_proj)
            all_sprites.add(new_proj)


    def handleClickEvent(self, mouse_pos, click):
        # PLACE RESOURCE BUILDING FUNCTION
        def placeBuilding(button_id, resource_node, owner):
            if button_id == 1 and resource_node.resource_type == 1:
                new_building = GreenBuilding(20, 20, 500, (0, 255, 0), resource_node, owner) # Place green resource building
                building_sprites.add(new_building)
                all_sprites.add(new_building)
                owner.owned_buildings.add(new_building)
                resource_node.kill()
            else:
                pass

            if button_id == 2 and resource_node.resource_type == 2:
                new_building = BlueBuilding(20, 20, 500, (0, 0, 128), resource_node, owner) # Place blue resource building   
                building_sprites.add(new_building)
                all_sprites.add(new_building)
                owner.owned_buildings.add(new_building)
                resource_node.kill()
            else:
                pass

            # CREATE NEW MAIN BUILDING TYPE
            if button_id == 3:
                new_building = MainBuilding(mouse_pos[0], mouse_pos[1], 50, 50, 1000, (123, 123, 123), owner)
                if new_building.checkForCollision(all_sprites, self.building_menu_container_rect, self.selected_building_menu_container_rect) is True:
                    print("Collides")
                elif new_building.checkExists() is True:
                    print("Max building count reached")
                else:
                    owner.owned_buildings.add(new_building)
                    building_sprites.add(new_building)
                    all_sprites.add(new_building)

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
            for resource_node in resource_sprites: 
                if resource_node.rect.collidepoint(mouse_pos): 
                    if self.player.selected_menu_button is not None: # Check a selected button is not none 
                        placeBuilding(self.player.selected_menu_button.getButtonID(), resource_node, self.player)
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
                    

            # CHECK IF ANYWHERE NOT OCCUPIED BY MENU OR RESOURCE IS CLICKED
            if self.player.selected_menu_button is not None:
                if self.player.selected_menu_button.getButtonID() == 3:
                    placeBuilding(self.player.selected_menu_button.getButtonID(), None, self.player)

        # CHECK FOR MIDDLE MOUSE CLICK
        if click == (False, True, False):
            proj_direction = pygame.mouse.get_pos()
            if self.player.selected_troop_group != None:
                self.fireProj(proj_direction)

        # CLEAR CURSOR ON RIGHT CLICK             
        if click == (False, False, True): 
            self.player.selected_menu_button = None
            print("cleared cursor")

                                    
            
    @profile
    def Main(self):
        run = True

        while run:
            self.window_object.fill((255,255,255))
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
                            self.createTroop(self.player)
                
                    self.player.selected_troop_group = all_troop_sprites # REMOVE THIS JUST FOR TESTING # REMOVE THIS JUST FOR TESTING # REMOVE THIS JUST FOR TESTING # REMOVE THIS JUST FOR TESTING
                    if self.player.selected_troop_group == all_troop_sprites:
                        if event.key == pygame.K_SPACE:
                            target_pos = pygame.mouse.get_pos() 
                            [self.moving_troops.add(sprite) for sprite in self.player.selected_troop_group]
                    else:
                        pass
            
            # FIRST RUN STUFF
            if self.firstRun == True:
                # SET TIMERS FOR ENEMY, PLAYER AND GAME TIMER
                timer_for_enemy_action = 0
                timer_for_player_action = 0
                game_timer = 0
                # CREATE FIRST TIME RESOURCE NODES AND MENU NODES
                self.createResourceNodes()
                self.createBuildMenu()
                self.firstRun = False

            # MOVE ALL SELECTED TROOPS
            if len(self.moving_troops) != 0:
                self.moving_troops.update(target_pos, self.moving_troops, all_sprites)
                self.moving_troops.draw(self.window_object)

            # MOVE ALL PROJECTILES
            projectiles.update()
        
            # DRAW ALL SPRITES AND MENUS
            self.drawOverlay()
            projectiles.draw(self.window_object)
            resource_sprites.draw(self.window_object)
            self.building_menu_sprites.draw(self.window_object)
            if self.player.selected_building is not None:
                self.selected_building_menu_sprites.draw(self.window_object)
            building_sprites.draw(self.window_object)
            all_troop_sprites.draw(self.window_object)

            # UPDATE TIMERS
            timer_for_enemy_action += game_clock.tick()
            timer_for_player_action += game_clock.tick()
            game_timer += game_clock.tick()

            pygame.display.flip()
            fps_clock.tick(framerate)
        pygame.quit()


if __name__ == "__main__":
    mainrun = MainRun(window_width, window_height, window_object)


    