# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 15:30:00 2021

@author: Vincent Bui
"""

import numpy as np

MINIMUM_SPD = 0
MAXIMUM_SPD = 75

# https://weatherspark.com/m/913/11/Average-Weather-in-November-in-Seattle-Washington-United-States
Probability_of_rain_min = 0.51
Probability_of_rain_max = 0.56

# How much rain fall in inches
Min_Rain_Fall = 6.6
Max_Rain_Fall = 7.7

Probability_of_light_rain_fall = 0.50
Probability_of_medium_rain_fall = 0.50

Starting_Point=3
Ending_Point=23

Probability_of_accidents = 0.02
Probability_of_light_traffic = 0.10
Probabllity_of_medium_traffic = 0.50
Probability_of_heavy_traffic = 0.25
Probability_of_no_traffic = 0.01

def simulation():
    time = 0
    while time != Ending_Point:
        rand = np.random.random()
        random_chance_of_rain = np.random.
        if rand < 