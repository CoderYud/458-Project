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
- The average wait time includes waiting in line and waiting for a customer’s food to be served to them

"""

# Imports

import numpy as np
import random
import matplotlib.pyplot as plt

# Constant variables 

BEGINNING_HOURS_IN_MINUTES = 0 #time in minutes (10 am)
ENDING_HOURS_IN_MINUTES = 720 #time in minutes (10 pm)
menu = ["Hamburger","Pizza","Steak"] # Food menu
prep_time = [12,10,15] # the amount of time it take to make each meal 
food_cost = [15,12,20] # the cost of each food

# List of variables
total_takeout = 0
takeout_payment=0
total_number_of_customers = 0
lost_customers = 0
list_of_tables = [] # list to keep track of table
list_of_customers = [] # list to keep track of group
list_of_people_in_line = []
list_of_people_in_line_take_out = [] 
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
average_takeout_revenue = [] # Average takeout revenue
average_takeout_customers = [] # Average number of takeout customers

# Elements that can be changed to affect results
OrderID = 1
chairs = 4 # init chairs
TABLES = 9 # init tables
probability_of_take_for_family = 0.30
customer_interval = 15 # mins
MAXIMUM_WAITING_TIME = 60 # minutes
MAXIMUM_EATING_TIME = 60 # minutes
MAXIMUM_CAPACITY = 150 # maximum length of customer can be in the waiting line at a restaurant
probability_of_large_group = 0.20
beginning_number_of_customers = 12
probability_of_takeout_normal_hour = 0.20
probability_of_takeout_dinner_lunch_hour = 0.50
probability_of_takeout_for_self = 0.70

# --------------------------- Class: Takeout_Customer -------------------------
class Takeout_Customer(object):
    
    """
    Description:
        - This class stores the information for each of the takeout customer objects   
    Each takeout customer has:
        - state (whether the customer has order, waiting, prepared, served)
        - takeout_order - what the customer want to order togo
        - waiting_time - the current waitting time for this customer 
        - estimate_waiting_time - time waiting for food to be prepare               
    """
    
    def __init__(self,takeout_order,orderID):
        self.number_of_people = 1
        self.orderID = orderID
        self.state= "Waiting"
        self.takeout_order= takeout_order
        self.waiting_time = 0
        self.estimate_waiting_time = 0
        
# ----------------------- Class Function: state_as_int -----------------------   
    def state_as_int(self):
        """
        Description:
            - Checks the status of the customer       
        Return:
            - Returns the integer equivalent for that particular state
        
        """
        if self.state == "Waiting":
            return 0
        if self.state == "Ordered":
            return 1
        if self.state == "Served":
            return 2   
# ------------------------------ Class: Customer ------------------------------ 
class Customer(object):
    """
    Description:
        - This class stores the information for each of the customer objects  
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
        Description:
            - Checks the status of the customer
        Return:
            - Returns the integer equivalent for that particular state
        
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
        Description:
            - Checks the location of where the customer is located in the tables
        Return:            
            - Returns the list of where the customer is seated       
        """
        return self.tableNumber

# ------------------------- Class Function: toString --------------------------
    def toString(self):
        """
        Description:
            - Prints some attributes of the customer object
        Output:
            - the food order, number of people, waiting time and eating time
        """
        print(self.food_order, self.number_of_people, self.waiting_time, self.eating_time)
    
# ----------------------------- Class: Restaurant -----------------------------
class Restaurant(object):
    """  
    Description:        
        - This class stores the information for all the table objects    
    Each restaurant object has:
        - tables - list of tables
    """
    def __init__(self):
        self.tables = list_of_tables

# ---------------------- Class Function: availableTables ----------------------   
    def availableTables(self):
        """
        Description:
            - This function returns the number of available tables in the restaurant        
        Return:
            - count - int with the number of tables that are available, ("Empty")            
        """
        count = 0
       
        for i in list_of_tables:
            for j in i:
                if j.availability():
                    count += 1       
        return count

# ------------------------- Class Function: toString -------------------------    
    def toString(self):
        """
        Description:
            - Print out a list of table, chair in the restaurant
        Output
            - The number of tables and chairs for each of those table
        """
        print(self.tables, self.chairs)

# -------------------------------- Class: Table ------------------------------
class Table(object):
    """
    Description:     
        - This class store the information for the table object    
    Each table object has:
        - chairs - the number of chair
        - state - the state of the table
        - tableNumber - the table number       
    """
    def __init__(self, tableNumber):
        self.chairs = chairs
        self.state = "Empty"
        self.tableNumber = tableNumber
# ----------------------- Class Function: availability ------------------------ 
    def availability(self):
        """
        Description:
            - Check the current state of the table
        Return:
            - Return the state of the table                 
        """
        if self.state == "Empty":
            return True
        else:
            return False
# -------------------------- Class Function: state ----------------------------
    def state(self):
        """
        Description:
            - Which access to the state
        Return:
            - Return the state of the table               
        """
        return self.state

# ---------------------- General Function: initialization ----------------------          
def initialization():
    """ 
    Description:
        - Creates the environment for the restaurant
    
    Variable and list:
        - OrderID
        - list_of tables
    Method Arguments:
        None
    Returns:
        None
       
    Output:
        - List of customer objects based on length of the beginning number
        customer 
        - List of takeout customer objects based on the length of the 
        beginning number customer
        - 2D array of table objects
    Error:
        raise error if the number of table is invalid
    """
    global OrderID
    
    # create the beginning number of customers in line
    for i in range(beginning_number_of_customers):
        customer = createCustomer()
        list_of_people_in_line.append(customer)
    
    for j in range(beginning_number_of_customers):
        rand = random.randint(0, 2)
        if rand == 1:
            takeout_customer = create_takeout_Customer(OrderID)
            OrderID += 1
            list_of_people_in_line_take_out.append(takeout_customer)
    
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
    
# ---------------- General Function: create_takeout_Customer ----------------- 
def create_takeout_Customer(OrderID):
    takeout_order=[]
    """
    Description:    
        - Create a customer for takeout with randomized items in each order        
    Parameter:
        - OrderID - The id number for each order
    Variable and list:
        - takeout_order - Store food the customer is ordering          
    Return:
        - The newly created takeout customer object            
    """
    #Loop 5 times and get a random number between 0 to 2 each time
    for i in range(5):        
        rand  = random.randint(0, 2)
        
        #If the random number is 1
        #Add order to the customer list
        if rand == 1:
            takeout_order.append(menu[random.randint(0, 2)])
            
    #If there are no order even after the loop, add one order to the list
    if not takeout_order:
        
        takeout_order.append(menu[random.randint(0, 2)])
        
    #Create takeout customer
    return Takeout_Customer(takeout_order,OrderID)

# ---------------------- General Function: createCustomer ---------------------
def createCustomer():
    """
    Description:
        - create a dine in customer and put them in queue for the restaurant and what
        they want to order.    
    Argument:
        None
    List and variable:
        - food_order - The food the customer want to order
        - number_of_people - The number of people that is in a group
        - eating_time - How long it will take for them to eat
    Return:
        - A newly created customer object
    """
    #Customer select one of these options from the menu
    food_order = menu[random.randint(0, 2)]
        
    rand = random.random()
    
    #Set the probability for having a big group
    if probability_of_large_group > rand:
        number_of_people = random.randint(5, 6)
    else:
        number_of_people = random.randint(1, 4)
        
    # The bigger the group, the longer they will take the time to eat        
    if number_of_people >= 4:
        eating_time = random.randint(30, MAXIMUM_EATING_TIME)
    else:
        eating_time = random.randint(15, 30)
        
    #Create customer        
    return Customer(food_order, number_of_people, eating_time)

# --------------------- General Function: prepare_take_out --------------------
def prepare_take_out():
    """   
    Description:
        - Check if the order is ready for each customer who already order their food
    
    Variable and list:
        - list_of_people_in_line_take_out - a list to keep track of people order takeout
        - total_takeout - the total number of customer order takeout
        
    Output:
        - Remove the served customer from the queue
        - Call out the finishes order
        
    """
    global total_takeout
    
    #check each customer in the takeout list
    for customer in list_of_people_in_line_take_out:
        
        #If the customer is already ordered      
        if customer.state == "Ordered":
            
            #Increment waiting time by each minutes
            customer.waiting_time+=time_step
            
            #Once the customer waiting time is equal to the foods preparation time           
            if customer.waiting_time == customer.estimate_waiting_time:
                customer.state = "Served"
                #served_customer+= 1
                #Increnemt the number of takeout customer by one
                total_takeout+=1

                
                #Remove the customer from the takeout list
                list_of_people_in_line_take_out.remove(customer)
                
# ------------------ General Function: check_for_takeout_food -----------------               
def check_for_takeout_food():
    """
    Description:
        - Check if there are any customer in the list for takeout order and take their order
    
    Variable and list:
        - list_of_people_in_line_take_out - a list to keep track of people order takeout
        - takeout_payment - the payment for the takeout order
        
    Output:
        Set customer's status from waiting to ordered
    """
    global takeout_payment
    
    #If there are people in the takeout list
    if list_of_people_in_line_take_out:
        
        #Check each customer in the takeout list
        for customer in list_of_people_in_line_take_out:
            
            #If the current customer is waiting to order
            if customer.state == "Waiting":
                
                #Check what the current customer want to order
                #Get estimate waiting time based on the amount of food and prep time
                #Customer then pay for the food and set status to ordered                
                for food in customer.takeout_order:
                                       
                    if food == "Steak":
                        #payment.append(food_cost[2])
                        takeout_payment+=food_cost[2]
                        customer.estimate_waiting_time += prep_time[2]
                        
                    if food == "Pizza":
                        #payment.append(food_cost[1])
                        takeout_payment+=food_cost[1]
                        customer.estimate_waiting_time += prep_time[1]
                        
                    if food == "Hamburger":
                        #payment.append(food_cost[0])
                        takeout_payment+=food_cost[0]
                        customer.estimate_waiting_time += prep_time[0]
                        
                customer.state = "Ordered"
        
# ---------------------- General Function: find_extra_table -------------------
def find_extra_table(customer):
    
    """
    Description:
        - Find an extra table anywhere in the restaurant for the big group because one 
        table isnt enough due to having a limit amount of chairs
    
    Parameter:
        - customer - The customer object
    Variable and list:
        - list_of_tables - Keep track of tables that are in the restaurant
        - list_of_customers - Keep track of how many customer are in the restaurant
        - list_of_people_in_line - The queue line waiting for table
    Returns:
        True - There is an available table in the restaurant
        False - There is no available table in the restaurant
        
    """
    
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
                list_of_people_in_line.remove(customer)
                
                #add another table next to the assigned table
                customer.tableNumber.append(check.tableNumber)
                return True           
            
    #return false because there are no available table    
    return False
    
# ------------------- General Function: Check_Table_Next_To_It ----------------           
def Check_Table_Next_To_It(customer,temp_table):
    """
    Description:
        - Find an extra table around the current table in the restaurant for the big
        group because on table isnt enough due to having a limit amount of chairs
        and bring the group to the table.    
    Parameter:
        - customer - the customer object
        - temp_table - the current table number
    Variable and list:
        - row_length - the max number of row 
        - table_length - the max length of each row
        - list_of_tables - keep track of tables that are in the restaurant        
    Return:
        True - if there is an empty table next to the current table
        False - if there is no empty table next to the current table
    """
    #go through each table
    for row in range(len(list_of_tables)):
        for table in range(len(list_of_tables[row])):
            row_length=len(list_of_tables)-1
            table_length=len(list_of_tables[row])-1
            # find empty tables around the current table
            if list_of_tables[row][table].tableNumber== temp_table:
                
                #if table fall in any of the condition
                #if row==0 or row==row_length or table==0 or table==table_length:
                    
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
                return False
            
# --------------- General Function: Bring_Big_Group_To_Tables -----------------
# Check_Table_Next_To_It support function           
def Bring_Big_Group_To_Tables(customer,row,table):
    """
    Description:
        - If there is an empty table, bring the customer to the table    
    Parameter:
        customer - The customer object
        row - The row the table is in
        table - Where the table is in that row        
    Variable and list:
        list_of_customers - Keep track of customers in the restaurant
        list_of_people_in_line - Keep track of customer who are in the waitlist
    Return:
        True - The customer is moved to the table
    """
    # set table to occupied
    list_of_tables[row][table].state = "Occupied"
    
    # set the customer state to order and increment waiting time
    customer.state = "Order"
    customer.waiting_time += time_step
    
    #add another table next to the assigned table
    customer.tableNumber.append(list_of_tables[row][table].tableNumber)
    
    #add customer to restaurant list
    list_of_customers.append(customer)
    
    #remove customer from the waitlist
    try:
        list_of_people_in_line.remove(customer)  
    except ValueError:
        #print("Customer is already removed")
        pass                   
    return True        

# ---------------------- General Function: eating_food ----------------------
#check customer eating time
def eating_food():
    """
    Description:
        - Check on each customer if they finish eating to prepare the table for the 
        next customer 
    Variable and list:
        - list_of_customers - Keep track of customers in the restaurant
        - list_of_tables - Keep track of tables in the restaurant
        - served_customer - The total customers served in restaurant
    """
    global served_customer
    #check each customer in the restaurant
    for customer in list_of_customers:
        
        #if group is current being served
        if customer.state == "Served":
            
            #increment eating time by one every minutes
            customer.time_in_restaurant+=time_step
            
 
            #if the time spend in restaurant is equal to approximate eating time
            #set customer to done eating
            if customer.time_in_restaurant == customer.eating_time:
 
                customer.state = "Paid"
                served_customer = served_customer + customer.number_of_people
                
                #find and set the table to empty for the next customer
                for row in range(len(list_of_tables)):
                    for table in range(len(list_of_tables[row])):
                        for customer_table in customer.tableNumber:
                            check_table = list_of_tables[row][table].tableNumber
                            if customer_table==check_table:
                                list_of_tables[row][table].state = "Empty"
     
# ------------------------ General Function: order_food -----------------------
def order_food():
    """
    Description:
        - Check on each customer who havent order yet and take their order    
    Variable and list:
        - list_of_customers - keep track of customers in the restaurant
        - payment - keep track of customers payment         
    """
    # Loops through the list of customers and check to see if the customer is ordering
    # Then, updates the waiting time for food because of prep time and changes the customer's
    # state to reflect the customer being served
    for customer in list_of_customers:
        if customer.state == "Order":           
            if customer.food_order == "Steak":
                payment.append(food_cost[2]*customer.number_of_people)
                customer.waiting_time += prep_time[2]
                customer.state = "Served"
            if customer.food_order == "Pizza":
                payment.append((food_cost[1]*customer.number_of_people))
                customer.waiting_time += prep_time[1]
                customer.state = "Served"
            if customer.food_order == "Hamburger":
                payment.append((food_cost[0]*customer.number_of_people))
                customer.waiting_time += prep_time[0]
                customer.state = "Served"

# ------------------------ General Function: operations -----------------------
def operations():
    """
    Description:
        - The main operation, this will run the restaurant by moving customers to their
        table, take their order and update customer status at the same time simulating
        a real restaurant. At the end of the day, it will calculate the average data
        for each selected metric using the information collected throughout the day
    
    Variable and list:
        - list_of_people_in_line - Keep track of customers in the waitlist
        - lost_customers - The total number of customers not served
        - operating_hours - The open hour in minutes
        - total_number_of_customers - The total number of customer dine in
        - revenue - The total revenue make per day
        - lost_revenue - The total lost revenue per day
        - total_number_of_customers_in_line - The length of the waitlist
        - OrderID - The next takeout order id
        - list_of_tables - Keep track of tables in the restaurant
        - priority_list - Keep track of prioritize customer
        
    Method:
        - check_for_takeout_food
        - prepare_take_out
        - order_food
        - eating_food
        - Check_Table_Next_To_It
        
    Output:
        - Display the interaction between restaurant and customer during operation hour
        - Display the calculated average for each selected metric
    """
    
    #Set up the restaurant
    restaurant = Restaurant()
    
    # global list and variable
    global list_of_people_in_line
    global lost_customers
    global operating_hours
    global total_number_of_customers
    global revenue
    global lost_revenue
    global total_number_of_customers_in_line
    global OrderID
    while (operating_hours != ENDING_HOURS_IN_MINUTES):
        
        #Every minute check if there are any takeout order
        #If yes, check on customer and get their food ready
        #Otherwise, continue on with other customer
        if list_of_people_in_line_take_out:
            check_for_takeout_food()
            prepare_take_out()
            
        #If there are tables within the restaurant
        if restaurant.availableTables() > 0:
        
            #Check each table in the restaurant
            for i in range(len(list_of_tables)):
                for j in range(len(list_of_tables[i])):
                    temp = list_of_tables[i][j]
                    
                    #If there is an empty table
                    if temp.availability() == True:
                        
                        # First, check the priority list for next customer
                        # if it is not empty, move on to customer on waitlist
                        if len(priority_list) > 0:
                            
                            #Get the first customer in the waitlist
                            customer = priority_list[0]
                            
                            #Check if there is a table available
                            is_table_available = Check_Table_Next_To_It(customer,customer.tableNumber[0])
                            
                            #If there is a table available, move them to the table
                            #Remove the customer from the priority_list
                            if is_table_available:
 
                                priority_list.remove(customer)
                            else:
                                pass
                            
                        # if the priority list is empty                       
                        else:  
                            
                            # get the next customer in line
                            if len(list_of_people_in_line) > 0:
                                customer = list_of_people_in_line[0]
                                
                                #If the number of customer is less than the number of chairs in a table   
                                #Call in the customer and the customer from waitlist
                                #Take the customer order
                                if customer.number_of_people <= temp.chairs:            
                                    customer.tableNumber.append(temp.tableNumber)
                                    temp.state = "Occupied"
                                    customer.waiting_time += time_step
                                    customer.state = "Order"
                                    list_of_customers.append(customer)
                                    list_of_people_in_line.remove(customer)   
                                    
                                                              
                                #If the number of customer is greater than the number of chairs in a table
                                else:
                                    
                                    #Preoccupied the current table
                                    customer.tableNumber.append(temp.tableNumber)
                                    temp.state = "Occupied"
                                    #is_table_available = find_extra_table(customer)
                                    
                                    #Check if there are available tables next to it
                                    is_table_available = Check_Table_Next_To_It(customer,temp.tableNumber)
                                    
                                    #If there are no available tables
                                    #Move the customer to the priority list
                                    if is_table_available == False:                                 
                                        priority_list.append(customer)
                                        list_of_customers.append(customer)
                      
                                    #If there are available tables next to it
                                    #Move customer to one of the available tables
                                    else:
                                        pass
                                        
        #Customer will order food                                                                                       
        order_food()
        
        #Customer will eat food
        eating_food()                                                   
        
        # Customers geneally come into the resturant throughout the duration of operating hours
        if (operating_hours % random.randint(12, customer_interval)) == 0:
            rand = np.random.random()
            
            #Set random probability to spawn in takeout customer
            if rand < probability_of_takeout_normal_hour:
                list_of_people_in_line_take_out.append(create_takeout_Customer(OrderID))
                OrderID += 1
            else:
                list_of_people_in_line.append(createCustomer())
                
            #for i in list_of_people_in_line:
            for i in list_of_people_in_line:
                total_number_of_customers_in_line = total_number_of_customers_in_line + i.number_of_people
                
        # Lunch hour and dinner hours 
        elif (operating_hours == 120 or operating_hours == 480 or operating_hours == 540 or operating_hours == 600):
            rand = np.random.randint(5, 10)
            takeout_rand = random.random()
            
            #Set random probability to spawn in takeout customer
            if takeout_rand < probability_of_takeout_dinner_lunch_hour:
                
                for i in range(rand):
                    list_of_people_in_line_take_out.append(create_takeout_Customer(OrderID))
                    OrderID += 1
                    
            for i in range(rand):
                list_of_people_in_line.append(createCustomer())
                for i in list_of_people_in_line:
                    total_number_of_customers_in_line = total_number_of_customers_in_line + i.number_of_people
                    
        # if number of customer exceeded the maximum capacity, stop taking in customer
        if total_number_of_customers_in_line > MAXIMUM_CAPACITY and len(list_of_people_in_line) > 0:
            total_number_of_customers_in_line = total_number_of_customers_in_line - list_of_people_in_line[-1].number_of_people
            list_of_people_in_line[-1].state = "Unserved"
            list_of_customers.append(list_of_people_in_line[-1])
            lost_customers = lost_customers + list_of_people_in_line[-1].number_of_people
            list_of_people_in_line.remove(list_of_people_in_line[-1])
            
        # Check the waiting time of each customer
        # If they are waiting too long, they will leave
        # Update the lost customer and remove customer from the list
        for i in list_of_people_in_line: 
            i.waiting_time = i.waiting_time + time_step
            if i.waiting_time > MAXIMUM_WAITING_TIME:
                i.state = "Unserved"
                list_of_customers.append(i)
                lost_customers = lost_customers + i.number_of_people
                list_of_people_in_line.remove(i)
        # Increment the restaurant hour by a minute        
        operating_hours = operating_hours + time_step
    
    # Once the customer finish eating and paid
    # Append the customer time spend in restaurant to a list for calculation
    for i in list_of_customers:
        if i.state == "Paid":
            average_time.append(i.time_in_restaurant + i.waiting_time)
    
    # Increment the total number of customer in restaurant          
    total_number_of_customers = served_customer + lost_customers + total_takeout
    
    # Once the resturant close, check the waitlist and update lost customer
    if len(list_of_people_in_line) > 0:        
        for person in list_of_people_in_line:
            list_of_customers.append(person) 
            lost_customers = lost_customers + person.number_of_people
            list_of_people_in_line.remove(person)
    
    # Get the revenue for today 
    for customer in payment:
        revenue = revenue + customer
        
    # Calculate lost revenue    
    for customer in list_of_customers:
        if customer.state == "Unserved":
            order = customer.food_order
            if order == "Steak":
                lost_revenue = lost_revenue + food_cost[2] * customer.number_of_people
            if order == "Pizza":
                lost_revenue = lost_revenue + food_cost[1] * customer.number_of_people
            if order == "Hamburger":
                lost_revenue = lost_revenue + food_cost[0] * customer.number_of_people
    
                
    # Append data to corresponded list to calculate the average
    average_takeout_revenue.append(takeout_payment) # Average takeout revenue           
    average_number_of_customers.append(total_number_of_customers) # Average # of customer
    average_number_of_served_customers.append(served_customer) # Average # of served customer
    average_number_of_lost_customers.append(lost_customers) # Average # of lost customer
    average_time_in_restaurant.append(round(np.average(average_time))) # Average time spent
    average_revenue.append(revenue) # Average revenue
    average_lost_revenue.append(lost_revenue) # Average lost revenue
    average_takeout_customers.append(total_takeout) # Average # of takeout customer

    
def operations_option_2():
    """
    The main operation, this will run the restaurant by moving customers to their
    table, take their order and update customer status at the same time simulating
    a real restaurant. At the end of the day, it will calculate the average data
    for each selected metric using the information collected throughout the day
    
    Variable and list:
        - list_of_people_in_line - Keep track of customers in the waitlist
        - lost_customers - The total number of customers not served
        - operating_hours - The open hour in minutes
        - total_number_of_customers - The total number of customer dine in
        - revenue - The total revenue make per day
        - lost_revenue - The total lost revenue per day
        - total_number_of_customers_in_line - The length of the waitlist
        - OrderID - The next takeout order id
        - list_of_tables - Keep track of tables in the restaurant
        - priority_list - Keep track of prioritize customer        
    Method:
        - check_for_takeout_food
        - prepare_take_out
        - order_food
        - eating_food
        - Check_Table_Next_To_It
        
    Output:
        - Display the interaction between restaurant and customer during operation hour
        - Display the calculated average for each selected metric
    """
    
    #Set up the restaurant
    restaurant = Restaurant()
    
    # global list and variable
    global list_of_people_in_line
    global lost_customers
    global operating_hours
    global total_number_of_customers
    global revenue
    global lost_revenue
    global total_number_of_customers_in_line
    global OrderID
    while (operating_hours != ENDING_HOURS_IN_MINUTES):
        
        #Every minute check if there are any takeout order
        #If yes, check on customer and get their food ready
        #Otherwise, continue on with other customer
        if list_of_people_in_line_take_out:
            check_for_takeout_food()
            prepare_take_out()
            
        #If there are tables within the restaurant
        if restaurant.availableTables() > 0:
        
            #Check each table in the restaurant
            for i in range(len(list_of_tables)):
                for j in range(len(list_of_tables[i])):
                    temp = list_of_tables[i][j]
                    
                    #If there is an empty table
                    if temp.availability() == True:
                        
                        # First, check the priority list for next customer
                        # if it is not empty, move on to customer on waitlist
                        if len(priority_list) > 0:
                            
                            #Get the first customer in the waitlist
                            #Call the customer to the table
                            customer = priority_list[0]
   
                            # add the next available table next to the assigned table                            
                            customer.tableNumber.append(temp.tableNumber)
                            customer.waiting_time += time_step
                            customer.state = "Order"

                            #list_of_customers.append(customer)
                            list_of_tables[i][j].state= "Occupied"            
                            try:
                                list_of_people_in_line.remove(customer)  
                            except ValueError:
                                pass
                                #print("Customer is already removed")                   
                            
                            #Remove the customer from the priority list                                         
                            priority_list.remove(customer)
                          
                        # if the priority list is empty                       
                        else:  
                            
                            # get the next customer in line
                            if len(list_of_people_in_line) > 0:
                                customer = list_of_people_in_line[0]
                                
                                #If the number of customer is less than the number of chairs in a table   
                                #Call in the customer and the customer from waitlist
                                #Take the customer order
                                if customer.number_of_people <= temp.chairs:            
                                    customer.tableNumber.append(temp.tableNumber)
                                    temp.state = "Occupied"
                                    customer.waiting_time += time_step
                                    customer.state = "Order"
                                    list_of_customers.append(customer)
                                    list_of_people_in_line.remove(customer)   
                                    #print("next group of",customer.number_of_people,"to table",customer.tableNumber) 
                                                              
                                #If the number of customer is greater than the number of chairs in a table
                                else:
                                    
                                    #Preoccupied the current table
                                    customer.tableNumber.append(temp.tableNumber)
                                    temp.state = "Occupied"
                                    #Check if there available table anywhere in restaurant
                                    is_table_available = find_extra_table(customer)
                                    
                                    #Check if there are available tables next to it
                                    #is_table_available = Check_Table_Next_To_It(customer,temp.tableNumber)
                                    
                                    #If there are no available tables
                                    #Move the customer to the priority list
                                    if is_table_available == False:
                                        
                                        priority_list.append(customer)
                                        list_of_customers.append(customer)
                                        #list_of_people_in_line.remove(customer)
                                    #If there are available tables next to it
                                    #Move customer to one of the available tables
                                    else:
                                        pass
                             
        #Customer will order food                                                                                       
        order_food()
        
        #Customer will eat food
        eating_food()                                                   
        
        # Customers geneally come into the resturant throughout the duration of operating hours
        if (operating_hours % random.randint(12, customer_interval)) == 0:
            rand = np.random.random()
            
            #Set random probability to spawn in takeout customer
            if rand < probability_of_takeout_normal_hour:
                list_of_people_in_line_take_out.append(create_takeout_Customer(OrderID))
                OrderID += 1
            else:
                list_of_people_in_line.append(createCustomer())
                
            #for i in list_of_people_in_line:
            for i in list_of_people_in_line:
                total_number_of_customers_in_line = total_number_of_customers_in_line + i.number_of_people
                
        # Lunch hour and dinner hours 
        elif (operating_hours == 120 or operating_hours == 480 or operating_hours == 540 or operating_hours == 600):
            rand = np.random.randint(5, 10)
            takeout_rand = random.random()
            
            #Set random probability to spawn in takeout customer
            if takeout_rand < probability_of_takeout_dinner_lunch_hour:
                
                for i in range(rand):
                    list_of_people_in_line_take_out.append(create_takeout_Customer(OrderID))
                    OrderID += 1
                    
            for i in range(rand):
                list_of_people_in_line.append(createCustomer())
                for i in list_of_people_in_line:
                    total_number_of_customers_in_line = total_number_of_customers_in_line + i.number_of_people
                    
        # if number of customer exceeded the maximum capacity, stop taking in customer
        if total_number_of_customers_in_line > MAXIMUM_CAPACITY and len(list_of_people_in_line) > 0:
            total_number_of_customers_in_line = total_number_of_customers_in_line - list_of_people_in_line[-1].number_of_people
            list_of_people_in_line[-1].state = "Unserved"
            list_of_customers.append(list_of_people_in_line[-1])
            lost_customers = lost_customers + list_of_people_in_line[-1].number_of_people
            list_of_people_in_line.remove(list_of_people_in_line[-1])
            
        # Check the waiting time of each customer
        # If they are waiting too long, they will leave
        # Update the lost customer and remove customer from the list
        for i in list_of_people_in_line: 
            i.waiting_time = i.waiting_time + time_step
            if i.waiting_time > MAXIMUM_WAITING_TIME:
                i.state = "Unserved"
                list_of_customers.append(i)
                lost_customers = lost_customers + i.number_of_people
                list_of_people_in_line.remove(i)
        # Increment the restaurant hour by a minute        
        operating_hours = operating_hours + time_step
    
    # Once the customer finish eating and paid
    # Append the customer time spend in restaurant to a list for calculation
    for i in list_of_customers:
        if i.state == "Paid":
            average_time.append(i.time_in_restaurant + i.waiting_time)
    
    # Increment the total number of customer in restaurant          
    total_number_of_customers = served_customer + lost_customers + total_takeout
     
    # Once the resturant close, check the waitlist and update lost customer
    if len(list_of_people_in_line) > 0:        
        for person in list_of_people_in_line:
            list_of_customers.append(person) 
            lost_customers = lost_customers + person.number_of_people
            list_of_people_in_line.remove(person)
    
    # Get the revenue for today 
    for customer in payment:
        revenue = revenue + customer
        
    # Calculate lost revenue    
    for customer in list_of_customers:
        if customer.state == "Unserved":
            order = customer.food_order
            if order == "Steak":
                lost_revenue = lost_revenue + food_cost[2] * customer.number_of_people
            if order == "Pizza":
                lost_revenue = lost_revenue + food_cost[1] * customer.number_of_people
            if order == "Hamburger":
                lost_revenue = lost_revenue + food_cost[0] * customer.number_of_people
    
                
    # Append data to corresponded list to calculate the average
    average_takeout_revenue.append(takeout_payment) # Average takeout revenue           
    average_number_of_customers.append(total_number_of_customers) # Average # of customer
    average_number_of_served_customers.append(served_customer) # Average # of served customer
    average_number_of_lost_customers.append(lost_customers) # Average # of lost customer
    average_time_in_restaurant.append(round(np.average(average_time))) # Average time spent
    average_revenue.append(revenue) # Average revenue
    average_lost_revenue.append(lost_revenue) # Average lost revenue
    average_takeout_customers.append(total_takeout) # Average # of takeout customer
    
# ------------------------- General Function: visual --------------------------
def visuals():
    """
    Description:
        - Display the average calculation for each metric into the console
    Output:
        - Print out the average for each metric
    """
    
    
#--------------------------------------Output----------------------------------
    print("|-------------------------------------------------------------------------|")
    
    print("Scenerio 1: If a group has to sit close to each other")
            
    print("Total number of customers on average:", np.average(average_number_of_customers))
    
    print("Number of served customers within operating hours:", np.average(average_number_of_served_customers))
    
    print("Number of lost customers:", np.average(average_number_of_lost_customers))
    
    print("Customers spend this much time in the restaurant on average:", np.average(average_time_in_restaurant), "mins")
    
    print("Total Revenue From Dine In:", np.average(average_revenue), "Dollars")
    
    print("Total Lost Revenue:", np.average(average_lost_revenue), "Dollars")
    
    print("Total Takeout Orders:", np.average(average_takeout_customers))
    
    print("Total Takeout Revenue:", np.average(average_takeout_revenue), "Dollars")
    
    print("Total Revenue for the day:", round(np.average(average_takeout_revenue) + np.average(average_revenue)), "Dollars")

def visuals_2():
    """
    Description:
        - Display the average calculation for each metric into the console
    Output:
        - Print out the average for each metric
    """
    
    
#--------------------------------------Output----------------------------------
    print("|-------------------------------------------------------------------------|")
    
    print("Scenerio 2: If a group can sit far away from each other")
            
    print("Total number of customers on average:", np.average(average_number_of_customers))
    
    print("Number of served customers within operating hours:", np.average(average_number_of_served_customers))
    
    print("Number of lost customers:", np.average(average_number_of_lost_customers))
    
    print("Customers spend this much time in the restaurant on average:", np.average(average_time_in_restaurant), "mins")
    
    print("Total Revenue From Dine In:", np.average(average_revenue), "Dollars")
    
    print("Total Lost Revenue:", np.average(average_lost_revenue), "Dollars")
    
    print("Total Takeout Orders:", np.average(average_takeout_customers))
    
    print("Total Takeout Revenue:", np.average(average_takeout_revenue), "Dollars")
    
    print("Total Revenue for the day:", round(np.average(average_takeout_revenue) + np.average(average_revenue)), "Dollars")
# ------------------------- General Function: reset ---------------------------
def reset():
    """
    Reset all variable and list at the end of the run
    
    Variable and list:
        list_of_people_in_line - Keep track of customers in waitlist
        lost_customers - Total unserved customer per day
        operating_hours - Open restaurant hour
        total_number_of_customers - Total number of customer dine in
        revenue - Total revenue make per day
        lost_revenue - Total lost revenue per day
        total_number_of_customers_in_line - Total number of customers in waitlist
        list_of_customers - Keep track of each customer        
        list_of_tables - Keep track of tables in the restaurant
        served_customer - total number of served customer per day
        payment - payment dine-in order
        list_of_people_in_line_take_out - Keep track of takeout customers
        takeout_payment - payment from take-out order
        OrderID - The take-out order ID
        total_takeout - Total amount of takeout order per day
    """
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
    global list_of_people_in_line_take_out
    global takeout_payment 
    global OrderID
    global total_takeout
    
    list_of_people_in_line_take_out = 0
    list_of_people_in_line = 0
    lost_customers = 0
    operating_hours = 0
    total_number_of_customers = 0
    revenue = 0
    takeout_payment = 0
    total_takeout = 0
    lost_revenue = 0
    total_number_of_customers_in_line = 0
    served_customer = 0
    OrderID = 1
    
    list_of_customers = []
    list_of_people_in_line = []
    list_of_tables = []
    payment = []
    list_of_people_in_line_take_out = []
    
# ---------------------- General Function: simulationDriver ------------------

def simulationDriver():
    """
    Description:
        - Set up and run the restaurant simulation with only table next to each other. 
        At the end of the, reset everything for a new day.
    Method:
        - initialization
        - operations
        - reset
    """
    
    #Set up the restaurant, tables and ready to take in customers
    initialization()
    
    #Open and serve customers
    operations()
    
    #Reset everything
    reset()
    
    
def simulationDriver_option_2():
    """
    Description:
        - Set up and run the restaurant simulation with table can be anywhere. 
        At the end of the, reset everything for a new run.
    Method:
        - initialization
        - operations_option_2
        - reset
    """
    
    #Set up the restaurant, tables and ready to take in customers
    initialization() 
    
    #Open and serve customers
    operations_option_2()
    
    #Reset everything
    reset()
    
def reset_average_list():
    """
    Description:
        Resets all the average list after used
        
    Returns:
        None
    
    """
    
    global average_time # Average time in the restaurant waiting (time used for cooking food + time in queue)
    global average_number_of_customers # Average number of total customers
    global average_number_of_served_customers # Average number of customers served
    global average_number_of_lost_customers # Average number of lost customers
    global average_time_in_restaurant # Average time in restaurant
    global average_revenue # Average revenue
    global average_lost_revenue # Average lost revenue
    global average_takeout_revenue  # Average takeout revenue
    global average_takeout_customers 
    
    average_time = [] # Average time in the restaurant waiting (time used for cooking food + time in queue)
    average_number_of_customers = [] # Average number of total customers
    average_number_of_served_customers = [] # Average number of customers served
    average_number_of_lost_customers = [] # Average number of lost customers
    average_time_in_restaurant = [] # Average time in restaurant
    average_revenue = [] # Average revenue
    average_lost_revenue = [] # Average lost revenue
    average_takeout_revenue = [] # Average takeout revenue
    average_takeout_customers = [] # Average number of takeout customers
    
# ------------------ General Function: multiplesimulationDriver ---------------

def multipleSimulationDriver(num, condition):
    """    
    Run the simulation ahead of time to calculate any possible outcome and display
    it to the console
    
    Parameter:
        num - the number of runs 
        condition - whether to use the method of combining any tables and comparing the data
        
    Method:
        simulationDriver
        visuals
    """
    
    for i in range(num):
        simulationDriver()
    visuals()
    
    if condition == True:
        reset_average_list()
    
        for i in range(num):
            simulationDriver_option_2()
            
        visuals_2()
        reset_average_list()

# Call functions here
multipleSimulationDriver(10, True)

# ------------------ General Function: Testing -------------------------------
def TestingCustomerObject():
    customer = createCustomer()
    customer.toString()    

# ------------------ General Function: Testing -------------------------------
def TestingRestaurantObject():
    
    initialization()
    restaurant = Restaurant()
    print(restaurant.availableTables())

# ------------------ General Function: Testing -------------------------------
def TestTables():
    
    initialization()
    for i in range(len(list_of_tables)):
        for j in range(len(list_of_tables[i])):
            if list_of_tables[i][j].availability() == True:
                print("Table", list_of_tables[i][j].tableNumber, "is available")
    
# ------------------ General Function: Testing -------------------------------
def TestTakeOut():
    
    count = 1
    test_take_out=[]
    for i in range(10):
        rand = random.randint(0,2)
        food = menu[rand]
        takeout = Takeout_Customer(food,count)
        takeout.estimate_waiting_time += prep_time[rand]
        test_take_out.append(takeout)
        count+=1

    while(len(test_take_out) != 0):

        for customer in test_take_out:
            if customer.state == "Waiting":
                customer.waiting_time+=1
                if customer.waiting_time==customer.estimate_waiting_time:
                    print("The order is given")
                    test_take_out.remove(customer)
   
# ------------------ General Function: Testing -------------------------------    
def TestCustomerTraffic():
    
    orderID = 1
    operating_hours = 0
    while operating_hours != ENDING_HOURS_IN_MINUTES:
        
        if operating_hours % (random.randint(10, 15)):
            rand = random.random()
            if rand < probability_of_takeout_normal_hour:
                rand = random.randint(0, 2)
                list_of_people_in_line_take_out.append(Takeout_Customer(rand, orderID))
                orderID = orderID + 1
            else: 
                list_of_people_in_line.append(createCustomer())
        
        operating_hours = operating_hours + 10
        
    print(len(list_of_people_in_line))
    print(len(list_of_people_in_line_take_out))
    
    for i in range(len(list_of_people_in_line_take_out)):
        print(list_of_people_in_line_take_out[i].orderID)