#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 12:03:23 2018

@author: raphael
"""

from os import listdir

DATA = '../Data/Representativities/'

def compute_list_egos():
    list_egos = [ego.split('_')[0] for ego in listdir(DATA) if 'k4' in ego]
    return list_egos

LIST_EGOS = compute_list_egos()