# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from scipy.integrate import simps

from preprocessing import get_dataset_list, get_X, get_Y

def plot(title, ylabel, xlabel, x, y, xas, yas, hlines = False):
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.plot(x, y)
    if hlines:
        plt.hlines(hlines, 0, 23, colors='red', linestyles='solid')
    plt.xticks(xas)
    plt.yticks(yas)
    plt.show()
  
# give back the dataset minues the maxY [time, energy]
def calculate_above_area(dataset, maxY):
    yAbove = []
    for i in range(len(dataset)):
        if dataset[i][1] >= maxY:
            temp = dataset[i].copy()
            temp[1] -= maxY
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
    for peak in index_peaks(y): 
        peaks.append(make_peak_list(peak, y))
    return peaks    

# make a list of 24 * 0 and fill in the peak in this list 
def make_peak_list(peak, y):
    temp = [0] * 24
    for i in peak: # for every peak there will be a list with 0 and the peak
        temp[i] = y[i] # get the datapoints from the dataset in too the peak set
    return temp

# generator for the indexes of 
def index_peaks(y):
    templ = []
    temp = []
    for i in range(len(y)): 
        if y[i] != 0: # begin of a peak
            temp.append(i)
        if y[i] == 0 and len(temp) != 0: # end of a peak
            templ.append(temp)
            temp = []
    return templ

# if there is a peak in the combine dataset the function will look if there is a one on one 
# hit with a peak of a sub dataset. Only finds one on one hits.
# hits = [N,N] first is the index of the dataset, second is the index of the peak in that dataset            
def find_peaks_sub_dataset(combineDataset, datasets, maxY, maxYC):
    combinePeaks = index_peaks([i[1] for i in calculate_above_area(combineDataset, maxYC)])
    
    datasetPeaks = []
    for dataset in datasets:
        datasetPeaks.append(index_peaks([i[1] for i in calculate_above_area(dataset, maxY)]))
    
    hits = []
    for dataset in datasetPeaks:
        for peaks in dataset:
            for combinePeak in combinePeaks:
                if peaks == combinePeak:
                    hits.append([datasetPeaks.index(dataset), dataset.index(peaks)])
     
    return datasetPeaks, hits

# plot the dataset with a max y line
def get_dataset(name): 
    dataset = get_dataset_list(f'datasets/dataset_{name}.csv')
    del dataset[0]
    return [[int(i[0]), int(i[1])] for i in dataset] # replaces the string with ints

# check if there is a number in the list thats higher then the max
def check_max(y, maxY):
    check = False
    for i in y:
        if i > maxY:
            check = True
            break
    return check

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
            if sumPeak < diffrence: # this will empty sumPeak
                dataset[previousIndex][1] += sumPeak
                sumPeak -= sumPeak
            else :
                dataset[previousIndex][1] += diffrence # puts the diffrence in the previouse X
                sumPeak -= diffrence
            previousIndex -= 1
    
# calling all function to reschedule the heat request
def reschedule(name, dataset, topFlatteningRate, curveRate, maxY, yAxis, xAxis):
    
    plot(f'{name} dataset', 'MW', 'uren', get_X(0, 1, dataset), get_Y(1, dataset), yAxis, xAxis, maxY) # plot datapoints
    totalArea, aboveArea, underArea = calculate_area(dataset, maxY)
    print(f'Gebruiker: {name}\nTotal: {totalArea}\nAbove: {aboveArea}\nUnder: {underArea}')
    
    peaks = get_peaks([i[1] for i in calculate_above_area(dataset, maxY)])
    recalculate_peaks(dataset, peaks, topFlatteningRate, curveRate, maxY)
    plot(f'{name} dataset', 'MW', 'uren', get_X(0, 1, dataset), get_Y(1, dataset), yAxis, xAxis, maxY) # plot datapoints
    print(f'total area: {simps([i[1] for i in dataset], dx=1)}')

def make_combine_dataset(datasets, multiply):
    datasetsTemp = []
    for dataset in datasets:
        datasetsTemp.append([i[1] for i in dataset])
    
    datasetsTemp = [[energy * multiply[i] for energy in datasetsTemp[i]] for i in range(len(multiply))]
    combineDataset = [0]*24
    for i in range(len(datasetsTemp[0])):
        for j in range(len(datasetsTemp)):
            combineDataset[i] += datasetsTemp[j][i]
        
    return [[i, combineDataset[i]] for i in range(24)]

def recalculate_subpeaks_by_combinedataset(combineDataset, datasets):
    datasetPeaks, hits = find_peaks_sub_dataset(combineDataset, datasets, maxY, maxYC)
    for hit in hits: 
        peakList = [make_peak_list(datasetPeaks[hit[0]][hit[1]], [i[1] for i in calculate_above_area(datasets[hit[0]], maxY)])]
        recalculate_peaks(datasets[hit[0]], peakList, .025, .1, maxY)

    return hits

names = ["bejaard_koppel", "gezin_kinderen", "student", "koppel"]
datasets = [get_dataset(f'{name}') for name in names]

# set max y lines
maxYC = 1000000
maxY = 2000

combineDataset = make_combine_dataset(datasets, [100, 200, 100, 100])
#plot('combine dataset', 'MW', 'uren', get_X(0, 1, combineDataset), get_Y(1, combineDataset), range(0, 25, 2), range(0, 2500000, 500000), maxYC) # plot datapoints
#plot(f'gezin met kinderen', 'MW', 'uren', get_X(0, 1, datasets[1]), get_Y(1, datasets[1]), range(0, 25, 2), range(0, 6001, 500), maxY)
#plot(f'koppel', 'MW', 'uren', get_X(0, 1, datasets[3]), get_Y(1, datasets[3]), range(0, 25, 2), range(0, 6001, 500), maxY)

hits = recalculate_subpeaks_by_combinedataset(combineDataset, datasets)

combineDataset = make_combine_dataset(datasets, [100, 200, 100, 100])
plot('combine dataset', 'MW', 'uren', get_X(0, 1, combineDataset), get_Y(1, combineDataset), range(0, 25, 2), range(0, 2500001, 500000), maxYC) # plot datapoints
#plot(f'gezin met kinderen', 'MW', 'uren', get_X(0, 1, datasets[1]), get_Y(1, datasets[1]), range(0, 25, 2), range(0, 6001, 500), maxY)
#plot(f'koppel', 'MW', 'uren', get_X(0, 1, datasets[3]), get_Y(1, datasets[3]), range(0, 25, 2), range(0, 6001, 500), maxY)

i = 0
roundOne = True
while check_max([i[1] for i in combineDataset], maxYC): # loops till the dataset has no points above the max
    peaks = index_peaks([i[1] for i in calculate_above_area(combineDataset, maxYC)])
    for j in range(i, len(datasets)): 
        if i in [i[0] for i in hits] and roundOne: # check for the dataset hit
        
        else :
            
            
    roundOne = False

#reschedule('combine', combineDataset, .025, .1, maxYC, range(0, 25, 2), range(0, 4000000, 500000))
#plot(get_X(0, 1, combineDataset), get_Y(1, combineDataset), range(0, 25, 2), range(0, 4000000, 500000), maxYC) # plot datapoints
