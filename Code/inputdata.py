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
P_data=P_df[['CH3CCl3 (Gg/yr)']] #choose 'CH3CCl3 (Gg/yr)', 'CFC-11 (Gg/yr)' or 'CFC-12 (Gg/yr)'
P_data=P_data.to_numpy()/1000 #emissions in MT/year
P_constant=np.array([0.5]*18) #constant emissions in MT/year
#P_constant[5:18]=0 #turning emmisions of at 1977

#inputdata
P=P_data #emissions data: choose 'P_constant' or 'P_data'
k=1/5  # reaction constants: choose '1/5' or '1/52'
ke=0.5 # interhemispheric exchange constant
C0=20*10**-12 #start concentration onebox model (ppv)
C0N=30*10**-12 #NH start concentration twobox model (ppv)
C0S=10*10**-12 #SH start concentration twobox model (ppv)
startyear=1950 #choose '1950' or '1972'
MW=133.4 #Molar Weight: Choose 'CH3CCl3: 133.4 gr/mole' or 'CFC-11: 137.37 gr/mole'
time=np.arange(startyear, startyear+len(P), 1)
dt=1


#some plots   
plt.figure(figsize=[10,5])
plt.plot(time, twoboxeulerfw(k,ke,P,C0N,C0S,dt,MW)[0])
plt.plot(time, twoboxeulerfw(k,ke,P,C0N,C0S,dt,MW)[1])
plt.show()

plt.figure(figsize=[10,5])
plt.plot(time, oneboxeulerfw(k,P,C0,dt,MW))
plt.plot(time, oneboxRK4(k,P,C0,dt,MW))
plt.show()



