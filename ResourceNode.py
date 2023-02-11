import random
import numpy as np


class ResourceNode(object):
    def __init__(self, windowX, windowY):
        self.x = random.randint(1, windowX - 30)
        self.y = random.randint(1, windowY - 30)
        self.coords = np.array([self.x, self.y])
        self.owner = None              
        self.resource_type = random.randint(1, 1 + 1)

    def getResourceCoords(self):
        return self.coords

        


