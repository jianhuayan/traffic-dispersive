#!/usr/bin/python2.7
import pexpect
import os
import sys
import csv
import numpy as np
import matplotlib
import pylab as pl

#This script is intend to parse the IxiaChariot saved log file and extract the data and perform the plot


# Process the csv file

with open('ixchariot.csv', 'rb') as ixiafile:
    csv_f = csv.reader(ixiafile)
    Avg_Throughput = []
    Avg_Mos = []
    Avg_RValue = []
    for row in csv_f:
        Avg_Throughput.append(row[4])
        Avg_Mos.append(row[51])
        Avg_RValue.append(row[55])

    Avg_Throughput.pop(0)
    Avg_Throughput=map(float, Avg_Throughput)
    AVG_Throughput=np.mean(Avg_Throughput)
    print AVG_Throughput

    Avg_Mos.pop(0)
    Avg_Mos=map(float, Avg_Mos)
    AVG_MOS=np.mean(Avg_Mos)
    print AVG_MOS

    Avg_RValue.pop(0)
    Avg_RValue=map(float, Avg_RValue)
    AVG_RValue=np.mean(Avg_RValue)
    print AVG_RValue

#x = [1, 2, 3, 4, 5]
#y = [1, 4, 9, 16, 25]
#pl.plot(x, y)
#pl.show()
    
