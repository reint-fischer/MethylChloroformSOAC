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

cummulatief_df = pd.read_excel('Data/Cummulative_emissions.xls')
cum_df=cummulatief_df






### Emission rates ###
rPnD = 0.015 #Production & Distribution
riRAC = 0.050 #Refrigeration and Air Conditioning Installation
riClosed = 0.300 #Closed Foams Installation
riOpen = 0.980 #Open Foams and Emissive Uses Installation
rRAC = 0.050 #Refrigeration and Air Conditioning Banks
rClosed = 0.080 #Closed Foams Banks
rOpen = 0.980 #Open Foams and Emissive Uses Banks

### Cumulative sales ###
RAC = np.copy(cum_df['R/AC_cum'].to_numpy())
Closed = np.copy(cum_df['Closed_cum'].to_numpy())
Open = np.copy(cum_df['Open_cum'].to_numpy())

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
#%%
### Total Emissions ###
colors = [(0.1,0.6,0.1,0.3),(0.1,0.6,0.1,0.6),(0.1,0.6,0.1,0.95),(0.5,0.1,0.5,0.3),(0.5,0.1,0.5,0.6),(0.5,0.1,0.5,0.95),(0.9,0.5,0.02,0.3),(0.9,0.5,0.02,0.6),(0.9,0.5,0.02,0.95)]
labels = ['R/AC production','R/AC installation','R/AC bank','Closed foam production','Closed foam installation','Closed foam bank','Open foam production','Open foam installation','Open foam bank']
f1 = plt.figure(1,figsize=[15,10])
ax1 = plt.axes()
ax1.stackplot(cum_df['year'],ERAC1,ERAC2,ERAC3,EClosed1,EClosed2,EClosed3,EOpen1,EOpen2,EOpen3,labels=labels,colors=colors)
plt.legend(loc='upper left')
plt.title('CFC-11 bottem-up Emissions per sector', fontsize=20)
plt.ylabel('Emissions [ktonnes/year]', fontsize=20)
plt.xlabel('Year', fontsize=20)
plt.tick_params(labelsize=15)
plt.legend(fontsize=12)
plt.grid(axis='y',alpha=.3)
plt.savefig('Figures/Bottemup_emissions.png')
plt.show()

f2 = plt.figure(2,figsize=[15,10])
ax2 = plt.axes()
ax2.stackplot(cum_df['year'],RAC,Closed,Open,colors = colors[2::3],labels = labels[2::3])
plt.legend(loc='upper left')
plt.title('CFC-11 bottem-up Banks per sector', fontsize=20)
plt.ylabel('Bank size [ktonnes]', fontsize=20)
plt.xlabel('Year', fontsize=20)
plt.tick_params(labelsize=15)
plt.legend(fontsize=12)
plt.grid(axis='y',alpha=.3)
plt.savefig('Figures/Bottemup_banksize.png')
plt.show()