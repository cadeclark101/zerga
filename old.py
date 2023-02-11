self.Menu(event)
                self.CreateResourceNodes(event)




                
    def CreateResourceNodes(self, event):
        def action(mouse): 
            print(self.GetClickedNode(mouse))

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos() 
            action(mouse)


    def GetClickedNode(self, mouse):
            for node in self.resource_node_list:
                if node.collidepoint(mouse):
                    return node


    def Menu(self, event):
        def action(mouse): #SELECT MENU ITEM HERE
            for menu_button in self.menu_button_list:
                if menu_button.rect_object.collidepoint(mouse):
                    self.selected_building = menu_button

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

            if self.menu_button_list is None:
                self.menu_button_list = []
                self.menu_button_list.append(MenuButton(miner_button, "miner_button"))
                self.menu_button_list.append(MenuButton(power_plant_button, "power_plant_button"))
                self.menu_button_list.append(MenuButton(artillery_button, "artillery_button"))

        DrawMenu()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos() 
            action(mouse)



    # WORKING HERE # WORKING HERE# WORKING HERE# WORKING HERE# WORKING HERE# WORKING HERE# WORKING HERE# WORKING HERE# WORKING HERE# WORKING HERE# WORKING HERE
    def PlaceBuilding(self, event):
        def PlacePowerPlant(mouse):
            #self.GetClickedNode(mouse)
            print(self.selected_building)
        def PlaceMinerBuilding(mouse):
            self.GetClickedNode(mouse)
        def PlaceArtillery(mouse):
            self.GetClickedNode(mouse)
        
        if self.selected_building is not None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.selected_building.name == "miner_button":
                    PlacePowerPlant(mouse)
                elif self.selected_building.name == "power_plant_button":
                    PlaceMinerBuilding(mouse)
                elif self.selected_building.name == "artillery_button":
                    PlaceArtillery(mouse) 


class ResourceNode(object):
    def __init__(self, x, y, resource_type):
        self.x = x
        self.y = y
        self.owner = None              
        self.resource_type = resource_type

class MenuButton(object):
    def __init__(self, rect_object, name):
        self.rect_object = rect_object
        self.name = name

class Building(pygame.sprite.Sprite):
    def __init__(self, x, y, hp, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.hp = hp

class Miner(Building):
    def __init__(self, x, y):
        Building.__init__(self, x, y, hp)
        self.crps = 10

class PowerPlant(Building):
    def __init__(self, x, y):
        Building.__init__(self, x, y)
        self.erps = 10

class Artillery(Building):
    def __init__(self, x, y):
        Building.__init__(self, x, y)
        self.dmg = 100
        self.range = 100