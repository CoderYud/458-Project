# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 21:55:39 2021

@author: Bin Map & Vincent Bui
"""
import numpy as np
import random

#Constant variables no touch please

maximum_waiting_time = 120 #minutes
maximum_eating_time = 120 #minutes
maximum_capacity = 300 #maximum customer can be in restaurant
restaurant_width = 15 
restaurant_length = 15

#list of variable
menu = ["Hamburger","Pizza","Steak"] #Food menu
prep_time = [12,10,15] #the amount of time it take to make each meal 
food_cost = [15,12,20] #the cost of each food
list_of_tables = [] #list to keep track of table
list_of_groups = [] #list to keep track of group

# Other variables
waiting_time_spawn_customer = 0 #wait time to spawn each customer
chairs = 4 #init chairs
tables = 10 #init tables
group = 10 #init customer group
revenue = 0 #init revenue
average_time = 0 #init average time
Served_customer = 0 #init served customer
Unserved_customer = 0 #init not served customer

#------------------------------------------------------------------------------
class Customer:
    def __init__(self):
        self.state = "Away"        
        # Customer order from the menu
        # i represent the quantity
        # Order is random
        self.order_food = random.choices(menu, i = 2)
        self.number_of_people = random.randint(1 , 6)
        self.waiting_time = 0
        self.eating_time= random.randint(15,maximum_eating_time)
        
    def State(self, status):
        if status == 0:
            self.state = "Waiting"
        if status == 1:
            self. state = "Served"
        if status == 2:
            self.state= "Left"
#------------------------------------------------------------------------------
class Restaurant:
    def __init__(self, tables , chairs, restaurant_width, restaurant_length):
        self.restaurant_width = restaurant_width
        self.restaurant_length = restaurant_length
        self.tables = tables
        self.chairs = chairs
        self.state ="Empty"
    
    def State(self,status):
        if status == 0:
            self.state = "Occupied"
        if status ==1:
            self.state = "Empty"