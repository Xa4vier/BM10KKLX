#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 10:08:04 2018

@author: xaviervanegdom
"""

import sys

def setup():
    
    global eq
    
    eq = input("provide equation in terms of x: ")
    
    leftend = int(input("enter a: "))
    rightend = int(input("enter b: "))
    
    n = int(input("enter the number of rectangles: "))
    
    deltaX = (rightend - leftend) / n
    
    print(deltaX)
    print(f"the leftend in sum is {LeftEndSum(n, leftend, deltaX)}")
    print(f"the right in sum is {RightEndSum(n, leftend, deltaX)}")

# left end sum calculation
def LeftEndSum(num, leftend, deltaX):
    leftSum = 0.0
    for i in range(num):
        x = leftend + i * deltaX
        h = eval(eq)
        leftSum += h * deltaX
    return leftSum
        
# left end sum calculation
def RightEndSum(num, rightend, deltaX):
    rightSum = 0.0
    for i in range(num):
        x = rightend + (i + 1) * deltaX
        h = eval(eq)
        rightSum += h * deltaX
    return rightSum   
    

if __name__ == '__main__':
    setup()