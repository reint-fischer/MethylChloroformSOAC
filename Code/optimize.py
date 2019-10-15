# -*- coding: utf-8 -*-
"""
Optimize oneboxmodel

Created on Mon Oct 14 11:33:08 2019

@author: reint fischer
"""

import numpy as np
import pandas as pd
from scipy import optimize
from oneboxmodel import oneboxRK4

P_df=pd.read_excel('emissions_2014.xlsx')
P_data=P_df[['CFC-11 (Gg/yr)']]
k=1/5
C0=20*10**-12
dt=1
MW=137.37

O_df = pd.read_csv('AGAGE_CH3CCl3/global_mean_md.txt',header=14,delim_whitespace=True)
#params, params_covariance = optimize.curve_fit(oneboxRK4, O_df['time'],O_df['CFC-11'], p0=[1, 0, 0.2])


