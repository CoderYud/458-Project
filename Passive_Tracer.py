# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 15:30:00 2021

@author: Vincent Bui
"""

import numpy as np
import random 

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
Probabllity_of_medium_traffic = 0.50
Probability_of_heavy_traffic = 0.25
Probability_of_no_traffic = 0.01

def simulation():
    
    # Keeps track of the exit number
    Exit_Number = STARTING_POINT
    
    Speed_Counter = 60
    
    Time_Elapsed = 0
        
    # Run the simulation until Duy reaches Exit 23
    while Exit_Number != ENDING_POINT:
        
        # Run the probability of rain
        rand = np.random.random()
        random_chance_of_rain = np.random.uniform(Probability_of_rain_min, Probability_of_rain_max)
        
        # Rain has the chance to slow down speed based on the severity of the rain fall
        if rand < random_chance_of_rain:
            
            # Determine the rain severity and the impact it may have on traffic speed
            
            rand = np.random.random()
            
            if rand < Probability_of_medium_rain_fall:
                
                Speed_Counter = Speed_Counter - 10
                
            elif rand < Probability_of_light_rain_fall:
                
                choices = np.random.randint(0,2)
                
                if choices == 0:
                    
                    Speed_Counter = Speed_Counter - np.random.randint(0, 5)
                
        Time_Elapsed = Time_Elapsed + (1 / Speed_Counter)
                
        # Update exit number
        Exit_Number = Exit_Number + 1
    
    Time_Elapsed = int(Time_Elapsed * 60)
    
    print(Time_Elapsed)
        
simulation()