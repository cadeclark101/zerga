from queue import Queue
from threading import Thread, Timer
from profilehooks import profile
import pygame

from Enemy import *
from ResourceNode import *
from Player import *
from MenuButton import *
from Building import *
from BlueBuilding import *
from GreenBuilding import *
from Troop import *
from DataHandling import DataHandling
from Utils import roundCoords

pygame.init()

fps_clock = pygame.time.Clock()
game_clock = pygame.time.Clock()
framerate = 60

threads = []

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
        self.troop_groups_menu_sprites = pygame.sprite.Group()

        self.moving_troops = pygame.sprite.Group()

        self.selected_building_menu_container_rect = pygame.Rect(0, 1040, 1920, 40)
        self.building_menu_container_rect = pygame.Rect(1890, 0, 30, 150)
        self.troop_groups_menu_container_rect = pygame.Rect(0, 50, 540, 1870)

        self.resource_font = pygame.font.SysFont("verdana", 32)
        
        self.Main()


    # DRAW INFO OVERLAY
    def drawOverlay(self):
        green_resource_text = self.resource_font.render(str(self.player.green_resource), True, (0, 255, 0), None)
        blue_resource_text = self.resource_font.render(str(self.player.green_resource), True, (0, 0, 128), None)

        
        self.window_object.blit(green_resource_text, (0,0)) 
        self.window_object.blit(blue_resource_text, (0,35)) 



    # CREATE RIGHT SIDE BUILD MENU
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

        troop_spawner_building_button_obj = MenuButton(1890, 150, 30, 30, 4, (0,0,0))
        self.building_menu_sprites.add(troop_spawner_building_button_obj)
        all_sprites.add(troop_spawner_building_button_obj)
        pass
        
    # CREATE MAIN BUILDING TROOP MENU
    def createMainBuildingMenu(self):
        basic_troop_button_obj = MenuButton(960, 1050, 30, 30, 4, (0, 0, 0))
        self.selected_building_menu_sprites.add(basic_troop_button_obj)
        all_sprites.add(basic_troop_button_obj)
        pass

    # CREATE TROOP SPAWNER BUILDING MENU
    def createTroopSpawnerMenu(self):
        sniper_troop_button_obj = MenuButton(960, 1050, 30, 30, 5, (100, 0, 100))
        self.selected_building_menu_sprites.add(sniper_troop_button_obj)
        all_sprites.add(sniper_troop_button_obj)

        mortar_troop_button_obj = MenuButton(920, 1050, 30, 30, 6, (100, 0, 100))
        self.selected_building_menu_sprites.add(mortar_troop_button_obj)
        all_sprites.add(sniper_troop_button_obj)

    # CREATE TROOP GROUP MENU
    def createTroopGroupMenu(self):
        basic_troop_button_obj = MenuButton(0, 100, 50, 50, 7, (0,0,0))
        self.troop_groups_menu_sprites.add(basic_troop_button_obj)
        all_sprites.add(basic_troop_button_obj)

        sniper_troop_button_obj = MenuButton(0, 160, 50, 50, 8, (0,0,0))
        self.troop_groups_menu_sprites.add(sniper_troop_button_obj)
        all_sprites.add(sniper_troop_button_obj)

        mortar_troop_button_obj = MenuButton(0, 220, 50, 50, 9, (0,0,0))
        self.troop_groups_menu_sprites.add(mortar_troop_button_obj)
        all_sprites.add(mortar_troop_button_obj)


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
    def createTroop(self, owner, troop_type_id):
        def addNewTroop(owner, new_troop):
            owner.owned_troops.add(new_troop)
            all_troop_sprites.add(new_troop)
            all_sprites.add(new_troop)
            owner.addTroopToGroup(new_troop, new_troop.troop_type_id)

        if troop_type_id == 1: 
            new_troop = BasicTroop(10, 10, self.player.selected_building.x, self.player.selected_building.y, 10, (0, 0, 0), 4, owner, self.enemy, None, 100)
            addNewTroop(owner, new_troop)
        if troop_type_id == 2: 
            new_troop = SniperTroop(5, 5, self.player.selected_building.x, self.player.selected_building.y, 5, (3, 200, 100), 2, owner, self.enemy, None, 300)
            addNewTroop(owner, new_troop)
        if troop_type_id == 3: 
            new_troop = MortarTroop(15, 15, self.player.selected_building.x, self.player.selected_building.y, 20, (20, 30, 60), 1, owner, self.enemy, None, 500)
            addNewTroop(owner, new_troop)

        

    # FIRE PROJECTILE FROM ALL SELECTED SPRITES
    def fireProj(self):
        for sprite in all_troop_sprites:
            new_proj = Projectile(sprite.rect.x, sprite.rect.y, 5, 5, self.player.attack_target, 4, 100, (0,0,0), self.window_object)
            projectiles.add(new_proj)


    def handleClickEvent(self, mouse_pos, click):
        # PLACE BUILDING FUNCTION HANDLER
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
                new_building = MainBuilding(mouse_pos[0], mouse_pos[1], 50, 50, 1000, (123, 123, 123), owner) # Place main building
                if new_building.checkForCollision(all_sprites, self.building_menu_container_rect, self.selected_building_menu_container_rect) is True:
                    print("Collides")
                elif new_building.checkExists() is True:
                    print("Max building count reached")
                else:
                    owner.owned_buildings.add(new_building)
                    building_sprites.add(new_building)
                    all_sprites.add(new_building)

            # CREATE NEW TROOP SPAWNER TYPE
            if button_id == 4:
                new_building = TroopSpawner(mouse_pos[0], mouse_pos[1], 25, 25, 250, (0, 20, 255), owner) # Please troop spawner building
                if new_building.checkForCollision(all_sprites, self.building_menu_container_rect, self.selected_building_menu_container_rect) is True:
                    print("Collides")
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
                        break
                    else:
                        pass 
                else:
                    pass

            # CHECK IF BUILDING IS CLICKED
            for building_sprite in building_sprites:
                if building_sprite.rect.collidepoint(mouse_pos):
                    self.player.selected_menu_button = None
                    if isinstance(building_sprite, MainBuilding): # Check if main building is clicked
                        self.player.selected_building = building_sprite
                        self.createMainBuildingMenu()
                    if isinstance(building_sprite, TroopSpawner): # Check if troopspawner is clicked
                        self.player.selected_building = building_sprite
                        self.createTroopSpawnerMenu()
            
            # CHECK IF TROOP GROUP BUTTONS ARE CLICKED
            for troop_group_button in self.troop_groups_menu_sprites:
                if troop_group_button.rect.collidepoint(mouse_pos):
                    if troop_group_button.getButtonID() == 7:
                        self.player.selected_troop_group = self.player.basic_troops
                    if troop_group_button.getButtonID() == 8:
                        self.player.selected_troop_group = self.player.sniper_troops
                    if troop_group_button.getButtonID() == 9:
                        self.player.selected_troop_group = self.player.mortar_troops
                else:
                    pass


            # CHECK IF ANYWHERE NOT OCCUPIED BUT MENU OR RESOURCE IS CLICKED
            if self.player.selected_menu_button is not None:
                if self.player.selected_menu_button.getButtonID() == 3:
                    placeBuilding(self.player.selected_menu_button.getButtonID(), None, self.player)
                if self.player.selected_menu_button.getButtonID() == 4:
                    placeBuilding(self.player.selected_menu_button.getButtonID(), None, self.player)

        # CHECK FOR MIDDLE MOUSE CLICK 
        # CURRENTLY SET TO RIGHT CLICK BECAUSE IM ON MY LAPTOP
        # TODO: CHANGE TO AUTO FIRING AT CLOSEST TARGET
        if click == (False, False, True):
            if self.player.selected_troop_group != None:
                self.fireProj()

        # CLEAR CURSOR ON RIGHT CLICK             
        #if click == (False, False, True): 
         #   self.player.selected_menu_button = None
          #  print("cleared cursor")

                                    
            
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
                    if self.player.selected_building is not None: 
                        if isinstance(self.player.selected_building, MainBuilding): # Check if clicked rect is MainBuilding
                            if event.key == pygame.K_a:
                                self.createTroop(self.player, 1) # Spawn basic troop
                        if isinstance(self.player.selected_building, TroopSpawner): # Check if clicked rect is TroopSpawner
                            if event.key == pygame.K_a:
                                self.createTroop(self.player, 2) # Spawn sniper troop
                            elif event.key == pygame.K_s:
                                self.createTroop(self.player, 3) # Spawn mortar troop
                
                    if self.player.selected_troop_group is not None and len(self.player.owned_troops) is not None: # Make sure a troop group is selected
                        if event.key == pygame.K_SPACE:
                            target_pos = pygame.mouse.get_pos()
                            for sprite in self.player.selected_troop_group:
                                sprite.target = target_pos
                                self.moving_troops.add(sprite)
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
                self.createTroopGroupMenu()

                # CREATE AND START DATA GATHERING THREAD
                q = Queue()
                threads.append(DataHandling(q))
                threads[0].start()

                self.firstRun = False



            # MOVE ALL SELECTED TROOPS
            if len(self.moving_troops) != 0:
                self.moving_troops.update(self.moving_troops, all_sprites)
                self.moving_troops.draw(self.window_object)

            # MOVE ALL PROJECTILES
            projectiles.update()

        


            # DRAW ALL SPRITES AND MENUS
            self.drawOverlay()
            projectiles.draw(self.window_object)
            resource_sprites.draw(self.window_object)
            self.building_menu_sprites.draw(self.window_object)
            self.troop_groups_menu_sprites.draw(self.window_object)
            if self.player.selected_building is not None:
                self.selected_building_menu_sprites.draw(self.window_object)
            building_sprites.draw(self.window_object)
            all_troop_sprites.draw(self.window_object)



            # ENEMY ACTIONS
            if timer_for_enemy_action >= 5000:
                timer_for_enemy_action = 0

                # PLACE MAIN BUILDING
                if self.enemy.firstTurn() == False:
                    new_building = MainBuilding(self.enemy.getRandomCoord(self.window_width), self.enemy.getRandomCoord(self.window_height), 50, 50, 500, (255, 0, 0), self.enemy)
                    self.enemy.owned_buildings.add(new_building)
                    all_sprites.add(new_building)
                    building_sprites.add(new_building)

                    

            # DATA GATHERING
            if game_timer >= 2000:
                game_timer = 0
                
                threads[0].createDataset()
                new_data = (("green_resource_income", 1), ("blue_resource_income", 2), ("green_resource", 3), ("blue_resource", 4), ("troop_count", 5), ("building_count", 6), ("previous_move_id", 7), ("predicted_next_move_id", 8))
                threads[0].updateDataset(new_data)
            else:
                pass

            # UPDATE TIMERS
            timer_for_enemy_action += game_clock.get_time()
            timer_for_player_action += game_clock.get_time()
            game_timer += game_clock.get_time()


            pygame.display.update()
            fps_clock.tick(framerate)
            game_clock.tick()
        pygame.quit()


if __name__ == "__main__":
    mainrun = MainRun(window_width, window_height, window_object)


    