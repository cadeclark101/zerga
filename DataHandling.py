import pandas as pd

class DataHandling(object):
    def  __init__(self):
        starting_data = {"green_resource_income":[0, 0], "blue_resource_income":[0, 0], "troop_count":[0, 0], "building_count":[0, 0]}
        self.all_data = pd.DataFrame(starting_data)

        print(self.all_data)

