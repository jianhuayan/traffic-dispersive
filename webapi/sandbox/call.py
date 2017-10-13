#!/usr/bin/python2.7
import pexpect
import os
import sys
import csv
import numpy as np
import dvn
#This script is intend to parse the IxiaChariot saved log file and extract the data and perform the plot


# Process the csv file
dvn.impairments ('192.168.200.3','p1p1','70ms','5ms','0.55%')

