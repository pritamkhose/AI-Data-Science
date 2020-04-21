# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 10:11:30 2020

@author: Pritam
"""

per = 0.01 # 70 35 24
per = 0.02 # 35 18 11
amt = 1000
margin = 2
brokageTax = 0.004

for row in range(20):  
#    print(row, amt, amt*per)
    amt=amt+ (amt*per*margin)
    amt = amt - (amt * brokageTax)
    print(row , amt*per, amt)
    
print(100*brokageTax)