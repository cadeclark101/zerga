import Player
import DataHandling
import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

class Enemy(Player):
    def __init__(self, green_resource, blue_resource, green_resource_income, blue_resource_income):
        Player.__init__(self, green_resource, blue_resource, green_resource_income, blue_resource_income)