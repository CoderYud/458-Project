# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 15:30:00 2021

@author: Vincent Bui
"""

import numpy as np
import matplotlib.pyplot as plt

# Global Constants
MINIMUM_SPD = 0
MAXIMUM_SPD = 75

# Different Distances from one exit to another
DISTANCE = [1.21, 1.39, 1.09, 0.96, 0.895, 0.895, 0.94, 0.89, 1.72, 1.03, 1.03, \
            0.863, 0.863, 0.864, 0.68, 1.095, 1.095, 1.155, 1.155, 0.92]
    
STARTING_POINT = 3 # Exit Number
ENDING_POINT = 23 # Exit Number
TRAVEL_DISTANCE = np.sum(DISTANCE) # Miles

# Global Variables

# https://weatherspark.com/m/913/11/Average-Weather-in-November-in-Seattle-Washington-United-States
Probability_of_rain_min = 0.51
Probability_of_rain_max = 0.56

# How much rain fall in inches in a month
Min_Rain_Fall = 6.6
Max_Rain_Fall = 7.7

Probability_of_light_rain_fall = 0.43
Probability_of_medium_rain_fall = 0.13

Probability_of_accidents = 0.02

Probability_of_light_traffic = 0.10
Probabllity_of_medium_traffic = 0.80

List_of_times = []
Number_of_simulations = []

def simulation():
    
    # Keeps track of the exit number
    Exit_Number = STARTING_POINT
    
    Speed_Counter = 60
    
    Time_Elapsed = 0
    
    count = 0
    
    random_chance_of_rain = np.random.uniform(Probability_of_rain_min, Probability_of_rain_max)
    
    # Run the simulation until Duy reaches Exit 23
    while Exit_Number != ENDING_POINT:
        
        rand_traffic = np.random.random();
                
        if Exit_Number < 10:
            #if car is in light traffic, speed is from 50 to 60 mph
            if  rand_traffic < Probability_of_light_traffic:
                Speed_Counter = np.random.randint(50,60)
            #if car is in medium traffic, speed is from 10 to 30 mph
            elif rand_traffic < Probabllity_of_medium_traffic and rand_traffic >= Probability_of_light_traffic:
                Speed_Counter = np.random.randint(20,40)
            #if car is in heavy traffic, speed is from 1 to 10 mph
            else:
                Speed_Counter = np.random.randint(1,10)
                
        elif Exit_Number >= 12 and Exit_Number <= 14:
            
            Speed_Counter = np.random.randint(40, 60)
            
        else:
            Speed_Counter = 60
        
        #print(Speed_Counter)
        # Rain has the chance to slow down speed based on the severity of the rain fall
        
        # Run the probability of rain
        rand = np.random.random()
        
        if rand < random_chance_of_rain:
            
            # Determine the rain severity and the impact it may have on traffic speed
            
            rand = np.random.random()
            
            if rand < Probability_of_medium_rain_fall:
                
                #only change if current speed is greater than the slow speed
                if Speed_Counter > 10:   
                   Speed_Counter = Speed_Counter - np.random.randint(5,10)
                
            elif rand < Probability_of_light_rain_fall:
                
                choices = np.random.randint(0,2)
                
                if choices == 0:
                    # only change if current speed is greater than the slow speed
                    if Speed_Counter > 5:  
                        Speed_Counter = Speed_Counter - np.random.randint(0, 5)
              
        Time_Elapsed = Time_Elapsed + (DISTANCE[count] / Speed_Counter)
                
        # Update exit number
        Exit_Number = Exit_Number + 1
        
        # Update distance from one exit to another
        count += 1
        
        # print(Speed_Counter,"mph",rand_traffic)
        
    Time_Elapsed = int(Time_Elapsed * 60)
    
    # print("--------------------------")
    # print(Time_Elapsed, "mins")
    
    List_of_times.append(Time_Elapsed)

count = 1

for i in range (1, 1001):
        
    simulation()
    Number_of_simulations.append(count)
    
    count = count + 1
    
    if (i % 100) == 0:
        print("After", i ," one hundred runs ", np.ceil(np.average(List_of_times)), "mins")
    
plt.hist(List_of_times)
    
# plt.plot(Number_of_simulations, List_of_times)