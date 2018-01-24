#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 12:02:45 2018

@author: raphael
"""

import csv
import random
import pandas as pd
from sklearn.metrics import silhouette_samples
from sklearn import KMeans
import numpy as np

from utils import LIST_EGOS, POS

random.seed()
DATA = '../Data/Representativities/'

def get_data(list_egos):
    alters, orbits_per_alter, all_orbits = [], {}, {i : 0 for i in POS}
    ego_per_alter = {}
    
    for ego in list_egos:
        with open('../Data/Orbits/%s_k4.csv', 'r') as to_read:
            csvr = csv.reader(to_read, delimiter = ';')
            for line in csvr:
                
                if sum([float(i) for i in line[1:]]) == 0:
                    continue
                
                alter = line[0]
                alters.append(alter)
                orbits_per_alter[alter] = line[[x+1 for x in POS]]
                for i in POS:
                    all_orbits[i] += line[i+1]
                ego_per_alter[alter] = ego
        
                
    prop_all = {orbit : all_orbits[orbit] / float(sum(all_orbits.values())) for orbit in all_orbits}
    repr_per_alter = {alter : {} for alter in alters}
    for alter in alters:
        for orbit in orbits_per_alter[alter]:
            this_repr = (orbits_per_alter[alter][orbit] / float(sum(orbits_per_alter[alter].values()))) / prop_all[orbit]
            if this_repr > 2:
                this_repr = 2 - 1 / this_repr
            repr_per_alter[alter][orbit] = this_repr 
                
    return alters, orbits_per_alter, repr_per_alter, prop_all, ego_per_alter


ALTERS, ORBITS_PER_ALTER, REPR_PER_ALTER, RELATIVE_FREQ, EGO_PER_ALTER = get_data(LIST_EGOS)


def get_classe_representativity(list_of_alters):
    s = {x : 0 for x in ORBITS_PER_ALTER[ORBITS_PER_ALTER.keys()[0]]}
    for alter in list_of_alters:
        for orbit in ORBITS_PER_ALTER[alter]:
            s[orbit] += int(ORBITS_PER_ALTER[alter][orbit])
    
    all_orbits = float(sum(s.values()))
    local_representativities = {x : s[x]/all_orbits for x in s}
    
    result = {}
    for orbit in local_representativities:
        if local_representativities[orbit] / float(RELATIVE_FREQ[orbit]) < 1:
            result[orbit] = local_representativities[orbit] / float(RELATIVE_FREQ[orbit])
        else:
            result[orbit] = 2 - 1 / (local_representativities[orbit] / float(RELATIVE_FREQ[orbit]))
    return result
            

def kmeans_all(data):
    for k_value in K_VALUES :
        s_max = 0
        labels_max = False
        for i in range(100):
            kmeans = KMeans(n_clusters = k_value)
            kmeans.fit(data)
            s = np.average(silhouette_samples(data, kmeans.labels_))
            if s > s_max:
                labels_max = kmeans.labels_
                s_max = s
            
        directory = '../Results/KMeans/Typo_%s' % k_value
        alters_par_classe = {}
        
        members_per_cluster = [[labels_max == k] for k in range(k_value)]
        
        for axe_2 in range(1, len(data.T)):
            for k in range(k_value):
                my_members = members_per_cluster[k][0]
                alters_par_classe[k] = []
                with open('%s/alters_classe_%s.csv' % (directory, k), 'w') as to_write:
                    csv_w = csv.writer(to_write, delimiter = ';')
                    csv_w.writerow(['ego_id', 'alter_id'] + [x+1 for x in POS])
                    for i in range(len(ALTERS)):
                        if my_members[i]:
                            alter = ALTERS[i]
                            alters_par_classe[k].append(alter)
                            csv_w.writerow([EGO_PER_ALTER[alter], alter] + [REPR_PER_ALTER[alter][j] for j in [x+1 for x in POS]])

        repr_par_classe= {}
        for classe in alters_par_classe:
            repr_par_classe[classe] = get_classe_representativity(alters_par_classe[classe])
            
        with open('%s/kmeans_stats.csv' % directory, 'w') as to_write:
            csv_w = csv.writer(to_write, delimiter = ';')
            csv_w.writerow(['classe', 'nb', 'prop'] + [""] + [x+1 for x in POS])
            classe_par_taille = [classe for classe in alters_par_classe]
            classe_par_taille.sort(key = lambda classe : len(alters_par_classe[classe]))
            for classe in classe_par_taille:
                nb = len(alters_par_classe[classe])
                prop = round(nb/float(len(ALTERS)), 2)
                
                row = [classe, nb, prop] + [""]
                for key in [x+1 for x in POS]:
                    row.append(repr_par_classe[classe][key])                    
                csv_w.writerow(row)      

        print 'silhouette k = %s : %s' % (k_value, round(s_max,3))  
        print kmeans.cluster_centers_
        
        
corpus = 'facebook'
k = 5
K_VALUES = [5]

DATA_CALC = pd.DataFrame.from_dict(REPR_PER_ALTER, orient = 'index')
kmeans_all(DATA_CALC)