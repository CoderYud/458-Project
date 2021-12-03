# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 21:55:39 2021

@author: Bin Map & Vincent Bui
"""
import numpy as np
import random

# Constant variables no touch please

MAXIMUM_WAITING_TIME = 120 # minutes
MAXIMUM_EATING_TIME = 120 # minutes
MAXIMUM_CAPACITY = 300 # maximum customer can be in restaurant
RESTAURANT_WIDTH = 15 
RESTAURANT_LENGTH = 15
BEGINNING_HOURS = 10 # 10 o'clock am
ENDING_HOURS = 22 # 10 o'clock pm

# list of variable
menu = ["Hamburger","Pizza","Steak"] # Food menu
prep_time = [12,10,15] # the amount of time it take to make each meal 
food_cost = [15,12,20] # the cost of each food
total_number_of_customers = 0
list_of_tables = [] # list to keep track of table
list_of_customers = [] # list to keep track of group
list_of_people_in_line = []

# Other variables
waiting_time_spawn_customer = 0 # wait time to spawn each customer
chairs = 4 # init chairs
tables = 10 # init tables
group = 10 # init customer group
revenue = 0 # init revenue
average_time = 0 # init average time
served_customer = 0 # init served customer
unserved_customer = 0 # init not served customer
time_step = 0.5
beginning_number_of_customers = 16
probability_of_large_group = 0.20

#------------------------------------------------------------------------------
class Customer(object):

    def __init__(self, number_of_people, food_order, eating_time):
        self.state = "Away"        
        self.food_order = food_order
        self.number_of_people = number_of_people
        self.waiting_time = 0
        self.time_in_restaurant = 0
        self.eating_time = eating_time
        self.tableNumber = 0

    def state(self, status):
        if status == 0:
            self.state = "Waiting"
        if status == 1:
            self. state = "Served"
        if status == 2:
            self.state= "Left"
    
    def location(self):
        return self.tableNumber
    
    def toString(self):
        return self.food_order, self.number_of_people, self.waiting_time, self.eating_time
    
#------------------------------------------------------------------------------
class Restaurant(object):
    
    def __init__(self):
        self.restaurant_width = RESTAURANT_WIDTH
        self.restaurant_length = RESTAURANT_LENGTH
        self.tables = list_of_tables
        self.state ="Empty"

    def state(self, status):
        if status == 0:
            self.state = "Occupied"
        if status == 1:
            self.state = "Empty"
    
    def availableTables(self):
        
        count = 0
        
        for i in list_of_tables:
            if i.availability():
                count += 1
        
        return count
    
    def toString(self):
        return self.tables, self.chairs, self.state

class Table(object):
    
    def __init__(self, tableNumber):
        self.chairs = chairs
        self.state = "Empty"
        self.tableNumber = tableNumber
    
    def availability(self):
        return self.state == "Empty"
    
    def state(self):
        return self.state

def simulationDriver(phase):
    
    operating_hours = np.absolute(BEGINNING_HOURS - ENDING_HOURS)
    
    print("operating hours", operating_hours)
    
    while(operating_hours != ENDING_HOURS):
        if phase == 0:
            initialization()
            phase = 1
        elif phase == 1:
            operations()
            phase = 2
            break
        else:
            if total_number_of_customers == 0:
                break
            update()
            
def initialization():
    
    # create the number of customers
    
    for i in range(beginning_number_of_customers):
        customer = createCustomer()
        list_of_customers.append(customer)
    
    # for i in range(len(list_of_customers)):
    #     print(list_of_customers[i].toString())
        
    for i in range(1, tables + 1):
        table = Table(i)
        list_of_tables.append(table)
    
    # for i in list_of_tables:
    #     print(i.state)
    #     print(i.tableNumber)
    
    restaurant = Restaurant()
    
    print(restaurant.availableTables())
    
def createCustomer():
    
    food_order = menu[random.randint(0, 2)]
        
    rand = random.random()
    
    if probability_of_large_group > rand:
        number_of_people = random.randint(4, 6)
    else:
        number_of_people = random.randint(1, 4)
        
    if number_of_people >= 4:
        eating_time = random.randint(30, 60)
    else:
        eating_time = random.randint(15, 60)
            
    return Customer(food_order, number_of_people, eating_time)
    
def operations():
    
    for i in range(len(list_of_customers)):
        list_of_people_in_line.append(i)
    
    pass

def update():
    pass

simulationDriver(0)