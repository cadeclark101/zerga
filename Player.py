from ResourceNode import *

class Player(object):
    def __init__(self, green_resource, blue_resource, green_resource_income, blue_resource_income):
        self.green_resource = green_resource
        self.blue_resource = blue_resource

        self.green_resource_income = green_resource_income
        self.blue_resource_income = blue_resource_income

        self.selected_menu_button = None
        self.selected_building = None
        self.selected_troop_group = None

    def incomeTicker(self):
        self.green_resource += self.green_resource_income
        self.blue_resource += self.blue_resource_income

    def increaseResourceIncome(self, resource, amount):
        if resource == 1:
            self.green_resource_income += amount
        else:
            self.blue_resource_income += amount


    