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
    for i in index_peak(y): # for every peak there will be a list with 0 and the peak
        peaks.append([0]*24)
        for j in i:
            peaks[len(peaks) - 1][j] = y[j] # get the datapoints from the dataset in too the peak set
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

# plot the dataset with a max y line
def get_dataset(name): 
    dataset = get_dataset_list(f'datasets/dataset_{name}.csv')
    del dataset[0]
    return [[int(i[0]), int(i[1])] for i in dataset] # replaces the string with ints

# calculate total erea, belowe the line and above the line
def calculate_area(dataset, maxY):   
    # Compute the area using the composite Simpson's rule.
    totalArea = simps([i[1] for i in dataset], dx=1) # the total area    
    # get the dataset but only above the peak line
    datasetAbove = calculate_above_area(dataset, maxY)        

    aboveArea = simps([i[1] for i in datasetAbove] , dx=1) # calculate the above area with the simpson's rule
    return totalArea, aboveArea, totalArea - aboveArea # subtract the above area of the total area to get the under area

       
def recalculate_peaks(dataset, peaks, topFlatteningRate, curveRate, maxY):        
    for peak in peaks: # loop trough al peaks        
        indexes = [peak.index(i) for i in peak if i != 0] # get all the indexes of the peak
        topFlattening = maxY * topFlatteningRate # calculate the flattening rate
        for i in indexes: # set the datapoints of the peak to the new datapoint minus the flattening rate
            dataset[i][1] = maxY - topFlattening
        
        sumPeak = sum(peak) + topFlattening * len(peaks) # calculate the total peak
        
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
    

# calling all function to reschedule the heat request
def reschedule(dataset, topFlatteningRate, curveRate, maxY, yAxis, xAxis):
    
    plot(get_X(0, 1, dataset), get_Y(1, dataset), yAxis, xAxis, maxY) # plot datapoints
    totalArea, aboveArea, underArea = calculate_area(dataset, maxY)
    print(f'Gebruiker: {name}\nTotal: {totalArea}\nAbove: {aboveArea}\nUnder: {underArea}')
    
    peaks = get_peaks([i[1] for i in calculate_above_area(dataset, maxY)])
    recalculate_peaks(dataset, peaks, topFlatteningRate, curveRate, maxY)
    plot(get_X(0, 1, dataset), get_Y(1, dataset), yAxis, xAxis, maxY) # plot datapoints
    print(f'total area: {simps([i[1] for i in dataset], dx=1)}')

names = ["bejaard_koppel", "gezin_kinderen", "student", "koppel"]
bejaard = 200
gezin = 450
student = 300
koppel = 250
multiply = [bejaard, gezin, student, koppel]
datasets = []
for name in names:
    datasets.append([i[1] for i in get_dataset(name)])

datasets = [[energy * multiply[i] for energy in datasets[i]] for i in range(len(multiply))]
combineDataset = [0]*24
for i in range(len(datasets[0])):
    for j in range(len(datasets)):
        combineDataset[i] += datasets[j][i]
        
combineDataset = [[i, combineDataset[i]] for i in range(24)]

maxY = 2000000
reschedule(combineDataset, .025, .1, maxY, range(0, 25, 2), range(0, 4000000, 500000))
#plot(get_X(0, 1, combineDataset), get_Y(1, combineDataset), range(0, 25, 2), range(0, 4000000, 500000), maxY) # plot datapoints
