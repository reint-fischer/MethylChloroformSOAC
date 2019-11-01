# -*- coding: utf-8 -*-
"""
Bottom up emissions

From AFEAS data of cumulative sales of CFC-11 products, compute bank sizes and emissions at all levels from production to installation to banks
Created on Thu Oct 24 15:00:20 2019

@author: reint fischer
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

AFEAS_df = pd.read_excel('Data/em_cfc_11.xls')

### Emission rates ###
rPnD = 0.015 #Production & Distribution
riRAC = 0.050 #Refrigeration and Air Conditioning Installation
riClosed = 0.300 #Closed Foams Installation
riOpen = 0.980 #Open Foams and Emissive Uses Installation
rRAC = 0.050 #Refrigeration and Air Conditioning Banks
rClosed = 0.080 #Closed Foams Banks
rOpen = 0.980 #Open Foams and Emissive Uses Banks

### Cumulative sales ###
RAC = np.copy(AFEAS_df['S_nonhermetic_cum'].to_numpy()+AFEAS_df['S_hermetic'].to_numpy())
Closed = np.copy(AFEAS_df['S_closed'].to_numpy())
Open = np.copy(AFEAS_df['S_open'].to_numpy())

### Production and Distribution Emissions ###
ERAC1 = [RAC[0]*rPnD]
EClosed1 = [Closed[0]*rPnD]
EOpen1 = [Open[0]*rPnD]
for i in range(len(RAC)-1):
    ERAC1 += [(RAC[i+1]-RAC[i])*rPnD]
    EClosed1 += [(Closed[i+1]-Closed[i])*rPnD]
    EOpen1 += [(Open[i+1]-Open[i])*rPnD]
    RAC[i] = RAC[i] - sum(ERAC1[:i+1])
    Closed[i] = Closed[i] - sum(EClosed1[:i+1])
    Open[i] = Open[i] - sum(EOpen1[:i+1])
RAC[-1] = RAC[-1] - sum(ERAC1)
Closed[-1] = Closed[-1] - sum(EClosed1)
Open[-1] = Open[-1] - sum(EOpen1)

### Installation ###
ERAC2 = [RAC[0]*riRAC]
EClosed2 = [Closed[0]*riClosed]
EOpen2 = [Open[0]*riOpen]
for i in range(len(RAC)-1):
    ERAC2 += [(RAC[i+1]-RAC[i])*riRAC]
    EClosed2 += [(Closed[i+1]-Closed[i])*riClosed]
    EOpen2 += [(Open[i+1]-Open[i])*riOpen]
    RAC[i] = RAC[i] - sum(ERAC2[:i+1])
    Closed[i] = Closed[i] - sum(EClosed2[:i+1])
    Open[i] = Open[i] - sum(EOpen2[:i+1])
RAC[-1] = RAC[-1] - sum(ERAC2)
Closed[-1] = Closed[-1] - sum(EClosed2)
Open[-1] = Open[-1] - sum(EOpen2)

### Banks release ###
ERAC3 = []
EClosed3 = []
EOpen3 = []
for i in range(len(RAC)):
    ERAC3 += [RAC[i]*rRAC]
    EClosed3 += [Closed[i]*rClosed]
    EOpen3 += [Open[i]*rOpen]
    if i<len(RAC)-1:
        RAC[i+1] = RAC[i+1] - sum(ERAC3[:i+1])
        Closed[i+1] = Closed[i+1] - sum(EClosed3[:i+1])
        Open[i+1] = Open[i+1] - sum(EOpen3[:i+1])
#    else:
#        RAC =np.append(RAC,RAC[i]-ERAC3[i])
#        Closed = np.append(Closed,Closed[i]-EClosed3[i])
#        Open = np.append(Open,Open[i]-EOpen3[i])
#%%
### Total Emissions ###
colors = [(0.1,0.6,0.1,0.3),(0.1,0.6,0.1,0.6),(0.1,0.6,0.1,0.95),(0.5,0.1,0.5,0.3),(0.5,0.1,0.5,0.6),(0.5,0.1,0.5,0.95),(0.9,0.5,0.02,0.3),(0.9,0.5,0.02,0.6),(0.9,0.5,0.02,0.95)]
labels = ['RAC production','RAC installation','RAC bank','Closed foam production','Closed foam installation','Closed foam bank','Open foam production','Open foam installation','Open foam bank']
f1 = plt.figure(1)
ax1 = plt.axes()
ax1.stackplot(AFEAS_df['year'],ERAC1,ERAC2,ERAC3,EClosed1,EClosed2,EClosed3,EOpen1,EOpen2,EOpen3,labels=labels,colors=colors)
plt.legend(loc='upper left')
plt.title('CFC-11 Emissions per sector')
plt.ylabel('Emissions [ktonnes/year]')

f2 = plt.figure(2)
ax2 = plt.axes()
ax2.stackplot(AFEAS_df['year'],RAC,Closed,Open,colors = colors[2::3],labels = labels[2::3])
plt.legend(loc='upper left')
plt.title('CFC-11 Banks per sector')
plt.ylabel('Bank size [ktonnes]')
plt.xlabel('Year')