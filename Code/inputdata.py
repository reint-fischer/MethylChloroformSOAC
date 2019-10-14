# -*- coding: utf-8 -*-
"""
Input data handling for SOAC project

Created on Sat Oct  5 16:26:08 2019

@author: reint fischer
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from oneboxmodel import oneboxeulerfw, oneboxRK4
from twoboxmodel import twoboxeulerfw

P_df=pd.read_excel('emissions_2014.xlsx')
P_data=P_df[['CFC-11 (Gg/yr)']] #choose 'CH3CCl3 (Gg/yr)', 'CFC-11 (Gg/yr)' or 'CFC-12 (Gg/yr)'
P_data=P_data.to_numpy()/1000 #emissions in MT/year
P_constant=np.array([0.5]*18) #constant emissions in MT/year
P_constant[5:18]=0 #turning emmisions of at 1977

#inputdata

P=P_constant #emissions data: choose 'P_constant' or 'P_data'
k=1/5  # reaction constants: choose '1/5' or '1/52' (1/1, 1/2, 1/10)
k1=1
k2=1/2
k10=1/10
ke=0.5 # interhemispheric exchange constant
C0=20*10**-12 #start concentration onebox model (ppv)
C0N=30*10**-12 #NH start concentration twobox model (ppv)
C0S=10*10**-12 #SH start concentration twobox model (ppv)
startyear=1972 #choose '1950' or '1972'
MW=133.4 #Molar Weight: Choose 'CH3CCl3: 133.4 gr/mole' or 'CFC-11: 137.37 gr/mole'
time=np.arange(startyear, startyear+len(P), 1)
dt=1

#Observations
#t = np.arange(1994,2018,1) #define timerange of observations

O_df = pd.read_csv('AGAGE_CH3CCl3/global_mean_md.txt',header=14,delim_whitespace=True)

#some plots   
plt.figure(figsize=[10,5])
plt.plot(time, twoboxeulerfw(k,ke,P,C0N,C0S,dt,MW)[0], color='black')
plt.plot(time, twoboxeulerfw(k,ke,P,C0N,C0S,dt,MW)[1], color='black')
plt.plot(time, twoboxeulerfw(k1,ke,P,C0N,C0S,dt,MW)[0], color='blue')
plt.plot(time, twoboxeulerfw(k1,ke,P,C0N,C0S,dt,MW)[1], color='blue')
plt.plot(time, twoboxeulerfw(k2,ke,P,C0N,C0S,dt,MW)[0], color='red')
plt.plot(time, twoboxeulerfw(k2,ke,P,C0N,C0S,dt,MW)[1], color='red')
plt.plot(time, twoboxeulerfw(k10,ke,P,C0N,C0S,dt,MW)[0], color='orange')
plt.plot(time, twoboxeulerfw(k10,ke,P,C0N,C0S,dt,MW)[1], color='orange')

plt.ticklabel_format(axis='y', scilimits=(-12,-12))
plt.show()

#plt.figure(figsize=[10,5])
plt.title('Euler and RK4 comparison')

#plt.plot(time, oneboxeulerfw(k,P,C0,dt,MW))
#plt.plot(time, oneboxRK4(k,P,C0,dt,MW))
plt.plot(O_df['time'],O_df['CFC-11']/(10**9))
#plt.show()





