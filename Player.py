from ResourceNode import *

class Player(object):
    def __init__(self, green_resource, blue_resource, green_resource_income, blue_resource_income):
        self.green_resource = green_resource
        self.blue_resource = blue_resource

        self.green_resource_income = green_resource_income
        self.blue_resource_income = blue_resource_income

        self.claimed_green_resource_node = []
        self.claimed_blue_resource_node = []

        self.active_units = []

        self.selected_building = None

    def claimResource(self, resource):
        self.claimed_blue_resource_node.append(resource)
        if resource.resource_type == 1:
            self.green_resource_income += 10
        else:
            self.blue_resource += 5

    