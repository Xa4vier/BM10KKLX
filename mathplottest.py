# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from scipy.integrate import simps

from preprocessing import get_dataset_list, get_X, get_Y

def plot(x, y, xas, yas, hlines = False):
    plt.plot(x, y)
    if hlines:
        plt.hlines(hlines, 0, 23, colors='red', linestyles='solid')
    plt.xticks(xas)
    plt.yticks(yas)
    plt.show()
 
    
def calculate_above_area(dataset, maxi):
    yAbove = []
    for i in range(len(dataset)):
        if dataset[i][1] >= maxi:
            temp = dataset[i].copy()
            temp[1] -= maxi
            yAbove.append(temp)
        else :
            temp = dataset[i].copy()
            temp[1] = 0
            yAbove.append(temp)
    return yAbove
 
# get all peaks
def get_peaks(y):
    # get the indexes of the peaks   
    peaks = []        
    for i in index_peak(y):
        peaks.append([0]*24)
        for j in i:
            peaks[len(peaks) - 1][j] = y[j]
    return peaks    

# generator for the indexes of 
def index_peak(y):
    temp = []
    for i in range(len(y)): 
        if y[i] != 0: # begin of a peak
            temp.append(i)
        if y[i] == 0 and len(temp) != 0: # end of a peak
            yield temp
            temp = []

names = ["bejaard_koppel", "gezin_kinderen", "student", "koppel"]
#name = names[0]
for name in names:
	
    # get the dataset
    dataset = get_dataset_list(f"datasets/dataset_{name}.csv")
    del dataset[0]
    
    # get the X and Y and plot the dataset 
    x = get_X(0, 1, dataset) # get X
    y = get_Y(1, dataset) # get Y
    plot(x, y, range(0, 25, 2), range(0, 6001, 500), 2500) # plot datapoints
    dataset = [[int(i[0]), int(i[1])] for i in dataset] # make a list with 2 int in a list
    
    # Compute the area using the composite Simpson's rule.
    y = [i[1] for i in dataset] # get all the Y 
    totalArea = simps(y, dx=1) # the total area
    
    # get the dataset but only above the peak line
    datasetAbove = calculate_above_area(dataset, 2500)    
    y = [i[1] for i in datasetAbove] # get only the y variable
    
    aboveArea = simps(y, dx=1) # calculate the above area with the simpson's rule
    underArea = totalArea - aboveArea # subtract the above area of the total area to get the under area
    
    # plot the above area
    plot(get_X(0, 1, datasetAbove), get_Y(1, datasetAbove), range(0, 25, 2), range(0, 6001, 500))
    
      
    print(f'Gebruiker: {name}\nTotal: {totalArea}\nAbove: {aboveArea}\nUnder: {underArea}')
    
    # get all peaks 
    peaks = get_peaks(y)
    for i in range(len(peaks)):
        print(f'peak {i}: {simps(peaks[i], dx=1)}')
    
    topCreamingRate = .025 # this is the rate where the peaks will be cut off
    curveRate = .1 # dit is het percentage waarmee het eerst volgende datapunt word verminderd
    maxY = 2500 # this is the max where the graph has to be under
    for peak in peaks: # loop trough al peaks
        
        indexes = [peak.index(i) for i in peak if i != 0] # get all the indexes of the peak
        topCreaming = maxY * topCreamingRate # calculate the creaming rate
        for i in indexes: # set the datapoints of the peak to the new datapoint minus the creaming rate
            dataset[i][1] = maxY - topCreaming
        
        sumPeak = sum(peak) + topCreaming * len(peaks) # calculate the total peak
        
        previousIndex = indexes[0] - 1 # get the index before the begining of the peak
        while sumPeak > 0 and previousIndex != 0: # loops till sumPeak is 0
            maxPrevious = dataset[previousIndex + 1][1] * (1 - curveRate)
            diffrence = maxPrevious - dataset[previousIndex][1]
            if sumPeak < diffrence:
                dataset[previousIndex][1] += sumPeak
                sumPeak -= sumPeak
            else :
                dataset[previousIndex][1] += diffrence
                sumPeak -= diffrence
            previousIndex -= 1
        i = 1
    
    plot(get_X(0, 1, dataset), get_Y(1, dataset), range(0, 25, 2), range(0, 6001, 500), 2500) # plot datapoints
    y = [i[1] for i in dataset] # get all the Y 
    print(f'total area: {simps(y, dx=1)}')