# -*- coding: utf-8 -*-
"""
Bottom up emissions

Created on Thu Oct 24 15:00:20 2019

@author: reint fischer
"""

import numpy as np
import pandas as pd

AFEAS_df = pd.read_excel('em_cfc_11')

### Emission rates ###
rPnD = 0.015
riRAC = 0.100
riClosed = 0.300
riOpen = 0.980
rRAC = 0.040
rClosed = 0.100
rOpen = 0.700

### Budgets ###
RAC = AFEAS_df['S_rnonhermetic']+AFEAS_df['S_rhermetic']
Closed = AFEAS_df['S_closed']
Open = AFEAS_df['S_open']

### Production and Distribution ###
PRAC1 = RAC*rPnD
PCLO1 = Closed*rPnD
POPE1 = Open*rPnD

RAC = RAC - PRAC1
Closed = Closed - PCLO1
Open = Open - POPE1

### Installation ###


### Banks release ###

### Total Emissions ###
