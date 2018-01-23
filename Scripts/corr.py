#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 12:02:55 2018

@author: raphael
"""

import csv
from os import listdir
from numpy import corrcoef

DATA = '../Data/'

def compute_list_egos():
    list_egos = [ego.split('_')[0] for ego in listdir(DATA) if 'k4' in ego]
    return list_egos

LIST_EGOS = compute_list_egos()
print LIST_EGOS

list_variables = []

for ego in LIST_EGOS:
    with open('../Data/Representativities/%s_k4.csv' % ego, 'r') as to_read:
        csv_r = csv.reader(to_read, delimiter = ';')
        for line in csv_r:
            list_variables.append([float(x) for x in line])
            
print list_variables
t = corrcoef(list_variables)
print t

with open('../Results/corrcoeff.csv', 'w') as to_write:
    csvw = csv.writer(to_write, delimiter = ';')
    for row in t:
        csvw.writerow(row)

