import pandas as pd
import threading
import time
from queue import Queue


class DataHandling(threading.Thread):
    def  __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        starting_data = {"green_resource_income":[0, 0], "blue_resource_income":[0, 0], "green_resource":[0,0], "blue_resourece":[0,0], "troop_count":[0, 0], "building_count":[0, 0]}
        self.all_data = pd.DataFrame(starting_data)

        self.queue = queue
        self.daemon = True

    def addData(self, increment, **kwargs):
        for key, value in kwargs.items():
            print(self.all_data.loc[int(key), [value]])
            self.all_data.loc[int(key), [value]] += [increment]
            print(self.all_data.loc[int(key), [value]])

    def getData(self):
        return self.all_data
