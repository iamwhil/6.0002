# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 06:55:44 2018

@author: Whil
"""
def break_temp(temp):
    temp = ([0], 0, 0)
    
temp = ([1], 2, 3)
print(temp)
print(temp[0][0] + 5)
temp[0][0] = temp[0][0] + 5
print(temp)
break_temp(temp)
print(temp)
#temp[0] = temp[0] + 7