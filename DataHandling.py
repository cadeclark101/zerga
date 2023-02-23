import pandas as pd

class DataHandling(object):
    def  __init__(self):
        starting_data = {"green_resource_income":[0,0], "blue_resource_income":[0,0], "troop_count":[0,0], "building_count":[0,0]}
        self.players_stats = pd.DataFrame(starting_data)

    def updateGreenResourceIncome(self, player_num, amount):
        self.players_stats.loc[player_num, ["green_resource_income"]] = [self.players_stats.loc[player_num, ["green_resource_income"]] + amount]
 

    def updateBlueResourceIncome(self, player_num, amount):
        self.players_stats.loc[player_num, ["blue_resource_income"]] = [self.players_stats.loc[player_num, ["blue_resource_income"]] + amount]
 

    def updateTroopCount(self, player_num, amount):
        self.players_stats.loc[player_num, ["troop_count"]] = [self.players_stats.loc[player_num, ["troop_count"]] + amount]

    def updateBuildingCount(self, player_num, amount):
        self.players_stats.loc[player_num, ["building_count"]] = [self.players_stats.loc[player_num, ["building_count"]] + amount]

        

