import pandas as pd
import threading
from queue import Queue
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from collections import defaultdict


class DataHandling(threading.Thread):
    def  __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.dataset_list = defaultdict(list, {"green_resource_income":[0, 1], "blue_resource_income":[0, 1], "green_resource":[0, 1], "blue_resource":[0, 1], "troop_count":[0, 1], "building_count":[0, 1], "previous_move_id":[0, 1], "predicted_next_move_id":[0, 1]})

        self.queue = queue
        self.daemon = True
        
    def updateDataset(self, new_data):
        for col in new_data:
            self.dataset_list[col[0]].append(col[1])
        self.createDataset()

    def createDataset(self):
        self.dataset = pd.DataFrame(self.dataset_list)
            

    def getData(self):
        return self.dataset
    
    
    def splitDataset(self):
        self.x = self.dataset.iloc[:, :-1].values
        self.y = self.dataset.iloc[:, -1:].values

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=0.2, random_state=0)
        return self.x_train, self.x_test, self.y_train, self.y_test


    def trainModel(self):
        self.model = DecisionTreeClassifier(random_state=0)
        self.model.fit(self.x_train, self.y_train)


    def predictNextMove(self):
        self.prediction = self.model.predict(self.x_test)
        return self.prediction
    
    def getModelAccuracy(self):
        return accuracy_score(self.y_test, self.prediction)

    


