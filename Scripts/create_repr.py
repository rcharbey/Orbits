#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 11:01:25 2018

@author: raphael
"""

import csv
from os.path import expanduser
from os import listdir

DATA = '%s/results/positions_per_alters/' % expanduser('~')
NEW_DATA = '../Data/'

def compute_list_egos():
    list_egos = [ego.split('_')[0] for ego in listdir(DATA) if 'k4' in ego]
    return list_egos

LIST_EGOS = compute_list_egos()
POS = range(4,15)

def compute_global_repr():
    sum_each = {i : 0 for i in POS}
    for ego in listdir(DATA):
        with open(DATA + ego, 'r') as to_read:
            csvr = csv.reader(to_read, delimiter = ';')
            for line in csvr:
                for i in POS:
                    sum_each[i] += int(line[i])
    
    with open(NEW_DATA+'global_representativities.csv', 'w') as to_write:
        csvw = csv.writer(to_write, delimiter = ';')
        global_repr = [sum_each[i] / float(sum(sum_each.values())) for i in POS]
        csvw.writerow(global_repr) 
    
    return global_repr
        
GLOBAL_REPR = compute_global_repr()

def compute_local_repr(ego):
    loc_repr = []
    with open(DATA+'%s_k4.csv' % ego, 'r') as to_read:
        csv_r = csv.reader(to_read, delimiter = ';')
        for line in csv_r:
            temp = []
            i = 0
            for pos in POS:
                temp.append(int(line[pos]))
            
            sum_temp = sum(temp)
            if sum_temp == 0:
                continue
                
            temp2 = []
            for nb_count in temp:
                temp2.append(nb_count / float(sum(temp)))
                
            temp3 = []
            for nb_count in temp2:
                v = nb_count / float(GLOBAL_REPR[i])
                i += 1
                if v > 2:
                    v = 2 - 1 / v
                temp3.append(v)
                
            loc_repr.append(temp3)
    
    with open(NEW_DATA+'Representativities/%s_k4.csv' % ego, 'w') as to_write:    
        print ego
        csv_w = csv.writer(to_write, delimiter = ';')
        for alter in loc_repr:
            csv_w.writerow(alter)
            
for ego in LIST_EGOS:
    compute_local_repr(ego)