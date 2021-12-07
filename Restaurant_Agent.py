# -*- coding: utf-8 -*-
"""
Created on Thu Dec 2 21:55:39 2021

@authors: Bin Map & Vincent Bui

This program simulates waiting in line at a restaurant.

Assumptions:
- Each customer orders something from a list of food items
- Each food item will have a predetermined cost and preparation time. 
For example, a hamburger can be cooked between 10 - 12 mins.
- During the operational hours of the restaurant, customers will randomly enter in different intervals of the day.
- Customers will show up more during lunch and dinner hours
- Customer or group size can vary throughout the day
- Group size will increase time in a restaurant eating
- If there are not enough seats to fit a group, then the restaurant has to combine tables to fit the group
- If queue times are too long then the last customer in the queue will leave
- The number of customers that enters the queue is randomized
- Restaurant has a max capacity of people that be queued 
- If restaurant reaches max capacity inside the restaurant, the last person in queue needs to leave 
because there is no more room inside the restaurant
- Customers in a group order the same food

"""
# Imports

import numpy as np
import random
import matplotlib.pyplot as plt

# Constant variables 

RESTAURANT_WIDTH = 15 
RESTAURANT_LENGTH = 15
BEGINNING_HOURS_IN_MINUTES = 0 #time in minutes (10 am)
ENDING_HOURS_IN_MINUTES = 720 #time in minutes (10 pm)
menu = ["Hamburger","Pizza","Steak"] # Food menu
prep_time = [12,10,15] # the amount of time it take to make each meal 
food_cost = [15,12,20] # the cost of each food

# List of variables

total_number_of_customers = 0
lost_customers = 0
list_of_tables = [] # list to keep track of table
list_of_customers = [] # list to keep track of group
list_of_people_in_line = []
priority_list = []
preoccupied_table = []
operating_hours = BEGINNING_HOURS_IN_MINUTES
revenue = 0 # init revenue
lost_revenue = 0 # revenue lost by not being meet customer demand
served_customer = 0 # init served customer
unserved_customer = 0 # init not served customer
total_number_of_customers_in_line = 0 # checking the total number of people in line
time_step = 1 # minutes
payment = [] # Keeps list of all customers that paid
average_time = [] # Average time in the restaurant waiting (time used for cooking food + time in queue)
average_number_of_customers = [] # Average number of total customers
average_number_of_served_customers = [] # Average number of customers served
average_number_of_lost_customers = [] # Average number of lost customers
average_time_in_restaurant = [] # Average time in restaurant
average_revenue = [] # Average revenue
average_lost_revenue = [] # Average lost revenue

# Elements that can be changed to affect results

chairs = 4 # init chairs
MAXIMUM_WAITING_TIME = 120 # minutes
MAXIMUM_EATING_TIME = 60 # minutes
MAXIMUM_CAPACITY = 150 # maximum customer can be in restaurant
probability_of_large_group = 0.20
beginning_number_of_customers = 12
TABLES = 9 # init tables

# ------------------------------ Class: Customer ------------------------------ 
class Customer(object):
    """
    
    This class stores the information for each of the customer objects
    
    Each customer has:
        - state (whether the customer has order, waiting, been served, unserved, or paid)
        - food_order - what the customer orders
        - number_of_people - number of people in the group
        - waiting_time - time waiting in queue and food 
        - eating_time - time spent eating food
        - tableNumber - what table(s) the customers are located at
        
    """
    def __init__(self, food_order, number_of_people, eating_time):
        self.state = "Waiting"        
        self.food_order = food_order
        self.number_of_people = number_of_people
        self.waiting_time = 0
        self.time_in_restaurant = 0
        self.eating_time = eating_time
        self.tableNumber = []
    
# ----------------------- Class Function: state_as_int -----------------------    
    def state_as_int(self):
        """
        
        Checks the status of the customer
        
        Returns the integer equivalent for that particular state
        
        """
        if self.state == "Waiting":
            return 0
        if self.state == "Served":
            return 1
        if self.state == "Paid":
            return 2
        if self.state == "Order":
            return 3
        if self.state == "Unserved":
            return 4

# ------------------------- Class Function: location -------------------------
    def location(self):
        """
        
        Checks the location of where the customer is located in the tables
        
        Returns the list of where the customer is seated
        
        """
        return self.tableNumber

# ------------------------- Class Function: toString -------------------------
    def toString(self):
        """
        
        Prints some attributes of the customer object

        """
        print(self.food_order, self.number_of_people, self.waiting_time, self.eating_time)
    
# ----------------------------- Class: Restaurant -----------------------------
class Restaurant(object):
    """
    This class stores the information for all the table objects
    
    Each restaurant object has:
        - tables - list of tables

    """
    def __init__(self):
        self.restaurant_width = RESTAURANT_WIDTH
        self.restaurant_length = RESTAURANT_LENGTH
        self.tables = list_of_tables

# ---------------------- Class Function: availableTables ----------------------   
    def availableTables(self):
        """
        This function returns the number of available tables in the restaurant
        
        Returns:
            count - int with the number of tables that are available, ("Empty")
            
        """
        count = 0
        
        for i in list_of_tables:
            for j in i:
                if j.availability():
                    count += 1
        
        return count

# ------------------------- Class Function: toString -------------------------    
    def toString(self):
        print(self.tables, self.chairs, self.state)

class Table(object):
    
    def __init__(self, tableNumber):
        self.chairs = chairs
        self.state = "Empty"
        self.tableNumber = tableNumber
    
    def availability(self):
        if self.state == "Empty":
            return True
        else:
            return False
    
    def state(self):
        return self.state

# ---------------------- General Function: initialization ----------------------          
def initialization():
    """ Creates the environment for the restaurant
    
    Method Arguments:
        None
    Returns:
        None
       
    Output:
        - List of customer objects based on length of the beginning number
        customer 
        - 2D array of table objects
    """
    
    # create the beginning number of customers in line
    for i in range(beginning_number_of_customers):
        customer = createCustomer()
        list_of_people_in_line.append(customer)
    
    global list_of_tables
    
    # generate tables in the restaurant
    for i in range(1, TABLES + 1):
        table = Table(i)
        list_of_tables.append(table)
        
    # change the list into a 1D array and then reshape it
    # to make a 2D array. If it is unable to reshape, then it 
    # will display a ValueError 
    tab = np.array(list_of_tables)
    
    if (len(list_of_tables) % 2) == 0:
        tab = np.reshape(tab,(2,-1))
    elif (len(list_of_tables) % 3) == 0:
        tab = np.reshape(tab,(3,-1))
    elif (len(list_of_tables) % 5) == 0:
        tab = np.reshape(tab, (5, -1))
    else:
        raise ValueError("Choose a different number of tables")
    
    list_of_tables = tab
    
# ---------------------- General Function: createCustomer ---------------------
def createCustomer():
    
    #Customer select one of these options from the menu
    food_order = menu[random.randint(0, 2)]
        
    rand = random.random()
    
    #Set the probability for having a big group
    if probability_of_large_group > rand:
        number_of_people = random.randint(4, 6)
    else:
        number_of_people = random.randint(1, 4)
        
    #The bigger the group, the longer the eat time        
    if number_of_people >= 4:
        eating_time = random.randint(30, 60)
    else:
        eating_time = random.randint(15, 45)
    #Create customer        
    return Customer(food_order, number_of_people, eating_time)
 
# ---------------------- General Function: find_extra_table -------------------
def find_extra_table(customer):
    
    #look at each row of tables
    for row in range(len(list_of_tables)):
        #look at each table
        for table in range(len(list_of_tables[row])):
            #check if there is an extra table
            check = list_of_tables[row][table]
            
            #if the there is an extra table available
            if check.availability() == True:
                
                # set table to occupied
                list_of_tables[row][table].state = "Occupied"
                customer.state = "Order"
                customer.waiting_time += time_step
                list_of_customers.append(customer)
                #remove customer from the waitlist
                list_of_people_in_line.remove(customer)
                
                #add another table next to the assigned table
                customer.tableNumber.append(check.tableNumber)
                return True           
            
    #return false because there are no available table    
    return False
    
# ------------------- General Function: Check_Table_Next_To_It ----------------            
def Check_Table_Next_To_It(customer,temp_table):
    #go through each table
    for row in range(len(list_of_tables)):
        for table in range(len(list_of_tables[row])):
            row_length=len(list_of_tables)-1
            table_length=len(list_of_tables[row])-1
            # find empty tables around the current table
            if list_of_tables[row][table].tableNumber== temp_table.tableNumber:
                
                #if table fall in any of the condition
                if row==0 or row==row_length or table==0 or table==table_length:
                    
                    #if there is a row above
                    if row!=0:
                        
                        #if available bring them to tables
                        if list_of_tables[row-1][table].availability(): #top
                            return Bring_Big_Group_To_Tables(customer,row-1,table)
                    #if there is a row below
                    if row!= row_length:
                        
                        #if available bring them to tables
                        if list_of_tables[row+1][table].availability(): #bottom
                            return Bring_Big_Group_To_Tables(customer,row+1,table)
                    
                    #if there is a column on the left
                    if table!=0:
                        
                        #if available bring them to tables
                        if list_of_tables[row][table-1].availability(): #left
                            return Bring_Big_Group_To_Tables(customer,row,table-1)
                        
                    #if there is a column on the right
                    if table!=table_length:
                        
                        #if available bring them to tables
                        if list_of_tables[row][table+1].availability: #right
                            return Bring_Big_Group_To_Tables(customer,row,table+1)
            
            #if there are no boundary
            else:
                
                #if available combine with table above
                if list_of_tables[row-1][table].availability: #top
                    return Bring_Big_Group_To_Tables(customer,row-1,table)
                
                #if available combine with table below
                if list_of_tables[row+1][table].availability: #bottom
                    return Bring_Big_Group_To_Tables(customer,row+1,table)
                
                #if available combine with table on the left
                if list_of_tables[row][table-1].availability: #left
                    return Bring_Big_Group_To_Tables(customer,row,table-1)
                
                #if available combine with table on the right
                if list_of_tables[row][table+1].availability: #right
                    return Bring_Big_Group_To_Tables(customer,row,table+1)
                
                #if no table available
                else:
                    return False

# ---------------------- General Function: Bring_Big_Group_To_Tables ----------------------
# Check_Table_Next_To_It support function           
def Bring_Big_Group_To_Tables(customer,row,table):   
    # set table to occupied
    list_of_tables[row][table].state = "Occupied"
    customer.state = "Order"
    customer.waiting_time += time_step
    #add another table next to the assigned table
    customer.tableNumber.append(list_of_tables[row][table].tableNumber)
    list_of_customers.append(customer)
    #remove customer from the waitlist
    list_of_people_in_line.remove(customer)                  
    return True        

# ---------------------- General Function: eating_food ----------------------
#check customer eating time
def eating_food():
    
    global served_customer
    for people in list_of_customers:
        #if group is current being served
        if people.state == "Served":
            #increment eating time by one every minutes
            people.time_in_restaurant+=time_step
            #print(people.time_in_restaurant,people.eating_time)
            #if the time spend in restaurant is equal to approximate eating time
            #set customer to done eating
            if people.time_in_restaurant == people.eating_time:
                #print(people.time_in_restaurant)
                people.state = "Paid"
                served_customer = served_customer + people.number_of_people
                for row in range(len(list_of_tables)):
                    for table in range(len(list_of_tables[row])):
                        for customer_table in people.tableNumber:
                            check_table = list_of_tables[row][table].tableNumber
                            if customer_table==check_table:
                                list_of_tables[row][table].state = "Empty"
     
# ------------------------ General Function: order_food -----------------------
def order_food():
    
    # Loops through the list of customers and check to see if the customer is ordering
    # Then, updates the waiting time for food because of prep time and changes the customer's
    # state to reflect the customer being served
    for people in list_of_customers:
        if people.state == "Order":           
            if people.food_order == "Steak":
                payment.append(food_cost[2]*people.number_of_people)
                people.waiting_time += prep_time[2]
                people.state = "Served"
            if people.food_order == "Pizza":
                payment.append((food_cost[1]*people.number_of_people))
                people.waiting_time += prep_time[1]
                people.state = "Served"
            if people.food_order == "Hamburger":
                payment.append((food_cost[0]*people.number_of_people))
                people.waiting_time += prep_time[0]
                people.state = "Served"

# ------------------------ General Function: operations -----------------------
def operations():
    
    restaurant = Restaurant()
    global list_of_people_in_line
    global lost_customers
    global operating_hours
    global total_number_of_customers
    global revenue
    global lost_revenue
    global total_number_of_customers_in_line
    
    while (operating_hours != ENDING_HOURS_IN_MINUTES):
        
        if restaurant.availableTables() > 0:
        
            for i in range(len(list_of_tables)):
                for j in range(len(list_of_tables[i])):
                    temp = list_of_tables[i][j]
                    
                    if temp.availability() == True:
                        # check the priority list
                        # if it is not empty get the next customer
                        if len(priority_list) > 0:
                            customer = priority_list[0]
                            print("next group of",customer.number_of_people,"from the priority list")      
                            # add the next available table next to the assigned table                            
                            customer.tableNumber.append(temp.tableNumber)
                            customer.waiting_time += time_step
                            customer.state = "Order"
                            print("big group of",customer.number_of_people,"to tables", customer.tableNumber)
                            list_of_customers.append(customer)
                            list_of_tables[i][j].state= "Occupied"                                                     
                            priority_list.remove(customer)
                                                        
                        # if the priority list is empty                       
                        else:  
                            
                            # get the next customer in line
                            if len(list_of_people_in_line) > 0:
                                customer = list_of_people_in_line[0]
                                
                                #if the number of customer is less than the number of chair in a table
                                
                                if customer.number_of_people <= temp.chairs:            
                                    customer.tableNumber.append(temp.tableNumber)
                                    temp.state = "Occupied"
                                    customer.waiting_time += time_step
                                    customer.state = "Order"
                                    list_of_customers.append(customer)
                                    list_of_people_in_line.remove(customer)   
                                    print("next group of",customer.number_of_people,"to table",customer.tableNumber) 
                                                              
                                    #if the number of customer is greater than the number of chair in a table
                                else:
                                    customer.tableNumber.append(temp.tableNumber)
                                    temp.state = "Occupied"
                                    #is_table_available = find_extra_table(customer)
                                    is_table_available = Check_Table_Next_To_It(customer,temp)
                                    if is_table_available == False:
                                        print("move customer party of", customer.number_of_people, "to priority list and reserve a table")
                                        priority_list.append(customer)
                                        list_of_customers.append(customer)
                                        list_of_people_in_line.remove(customer)
                                    else:
                                        print("big group of",customer.number_of_people,"to tables", customer.tableNumber)
                                                                                               
        order_food()
        eating_food()                                                   
        
        # Customers geneally come into the resturant throughout the duration of operating hours
        if (operating_hours % 15) == 0:
            list_of_people_in_line.append(createCustomer())
            #for i in list_of_people_in_line:
            for i in list_of_people_in_line:
                total_number_of_customers_in_line = total_number_of_customers_in_line + i.number_of_people
                
        # Lunch and dinner
        elif (operating_hours == 120 or operating_hours == 480):
            rand = np.random.randint(5, 10)
            for i in range(rand):
                list_of_people_in_line.append(createCustomer())
                for i in list_of_people_in_line:
                    total_number_of_customers_in_line = total_number_of_customers_in_line + i.number_of_people
        # if number of customer exceeded the maximum capacity, stop taking in customer
        # 
        if total_number_of_customers_in_line > MAXIMUM_CAPACITY and len(list_of_people_in_line) > 0:
            total_number_of_customers_in_line = total_number_of_customers_in_line - list_of_people_in_line[-1].number_of_people
            list_of_people_in_line[-1].state = "Unserved"
            list_of_customers.append(list_of_people_in_line[-1])
            lost_customers = lost_customers + i.number_of_people
            list_of_people_in_line.remove(list_of_people_in_line[-1])
            
        
        for i in list_of_people_in_line: 
            i.waiting_time = i.waiting_time + time_step
            if i.waiting_time > MAXIMUM_WAITING_TIME:
                i.state = "Unserved"
                list_of_customers.append(i)
                lost_customers = lost_customers + i.number_of_people
                list_of_people_in_line.remove(i)
                
        
        operating_hours = operating_hours + time_step
    
    for i in list_of_customers:
        if i.state == "Paid":
            average_time.append(i.time_in_restaurant + i.waiting_time)
            
    for i in list_of_customers:
        total_number_of_customers = total_number_of_customers + i.number_of_people
    
    if len(list_of_people_in_line) > 0:        
        for person in list_of_people_in_line:
            list_of_customers.append(person) 
            lost_customers = lost_customers + person.number_of_people
            list_of_people_in_line.remove(person)
            
    
    for customer in payment:
        revenue = revenue + customer
        
    for customer in list_of_customers:
        if customer.state == "Unserved":
            order = customer.food_order
            if order == "Steak":
                lost_revenue = lost_revenue + food_cost[2] * customer.number_of_people
            if order == "Pizza":
                lost_revenue = lost_revenue + food_cost[1] * customer.number_of_people
            if order == "Hamburger":
                lost_revenue = lost_revenue + food_cost[0] * customer.number_of_people
                
    average_number_of_customers.append(total_number_of_customers)
    average_number_of_served_customers.append(served_customer)
    average_number_of_lost_customers.append(lost_customers)
    average_time_in_restaurant.append(round(np.average(average_time)))
    average_revenue.append(revenue)
    average_lost_revenue.append(lost_revenue)
 
# ------------------------- General Function: visual --------------------------
def visuals():
    
    # wait time for customers throughout the day
    
    # num_of_customers = []
    
    # for i in range(len(list_of_customers)):
    #     num_of_customers.append(i)
    
    # waiting_times = []
    
    # for i in list_of_customers:
    #     waiting_times.append(i.waiting_time)
    
    # plt.plot(num_of_customers, waiting_times)
    
    print("|-------------------------------------------------------------------------|")
    
    print("Total number of customers on average:", np.average(average_number_of_customers))
    
    print("Number of served customers within operating hours:", np.average(average_number_of_served_customers))
    
    print("Number of lost customers:", np.average(average_number_of_lost_customers))
    
    print("Customers spend this much time in the restaurant on average:", np.average(average_time_in_restaurant), "mins")
    
    print("Total Revenue:", np.average(average_revenue), "Dollars")
    
    print("Total Lost Revenue:", np.average(average_lost_revenue), "Dollars")

# ------------------------- General Function: reset ---------------------------
def reset():
    
    global list_of_people_in_line
    global lost_customers
    global operating_hours
    global total_number_of_customers
    global revenue
    global lost_revenue
    global total_number_of_customers_in_line
    global list_of_customers
    global list_of_people_in_line
    global list_of_tables
    global served_customer
    global payment
    
    list_of_people_in_line = 0
    lost_customers = 0
    operating_hours = 0
    total_number_of_customers = 0
    revenue = 0
    lost_revenue = 0
    total_number_of_customers_in_line = 0
    served_customer = 0
    list_of_customers = []
    list_of_people_in_line = []
    list_of_tables = []
    payment = []

# ---------------------- General Function: simulationDriver ------------------  
def simulationDriver():
    
    initialization()
    operations()
    reset()

# ------------------ General Function: multiplesimulationDriver ---------------
def multipleSimulationDriver(num):
    for i in range(num):
        simulationDriver()
    visuals()

multipleSimulationDriver(10)