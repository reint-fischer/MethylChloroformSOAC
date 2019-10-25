# -*- coding: utf-8 -*-
"""
Bottom up emissions

From AFEAS data of cumulative sales of CFC-11 products, compute bank sizes and emissions at all levels from production to installation to banks
Created on Thu Oct 24 15:00:20 2019

@author: reint fischer
"""

import numpy as np
import pandas as pd

AFEAS_df = pd.read_excel('em_cfc_11')

### Emission rates ###
rPnD = 0.015 #Production & Distribution
riRAC = 0.100 #Refrigeration and Air Conditioning Installation
riClosed = 0.300 #Closed Foams Installation
riOpen = 0.980 #Open Foams and Emissive Uses Installation
rRAC = 0.040 #Refrigeration and Air Conditioning Banks
rClosed = 0.100 #Closed Foams Banks
rOpen = 0.700 #Open Foams and Emissive Uses Banks

### Cumulative sales ###
RAC = AFEAS_df['S_rnonhermetic']+AFEAS_df['S_rhermetic']
Closed = AFEAS_df['S_closed']
Open = AFEAS_df['S_open']

### Production and Distribution Emissions ###
PRAC1 = []
PCLO1 = []
POPE1 = []
for i in range(len(RAC)-1):
    PRAC1 += (RAC[i+1]-RAC[i])*rPnD
    PCLO1 += (Closed[i+1]-Closed[i])*rPnD
    POPE1 += (Open[i+1]-Open[i])*rPnD

#Leftover after production
RAC = RAC - PRAC1
Closed = Closed - PCLO1
Open = Open - POPE1

### Installation ###
PRAC2 = RAC*riRAC
PCLO2 = Closed*riClosed
POPE2 = Open*riOpen

#Leftover after production
RAC = RAC - PRAC1
Closed = Closed - PCLO1
Open = Open - POPE1

### Banks release ###

### Total Emissions ###
