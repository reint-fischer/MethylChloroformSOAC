# -*- coding: utf-8 -*-
"""
Real emissions

Created on Sat Oct  5 16:26:08 2019

@author: reint fischer
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from oneboxmodel import oneboxeulerfw, oneboxRK4
from twoboxmodel import twoboxeulerfw
from inversemodel import inverseonebox

P_WMO2014_df=pd.read_excel('emissions_2014.xlsx')
P_WMO2018_df=pd.read_excel('agage_emissions.xlsx')
substance_df = pd.DataFrame({'CH3CCl3': [1/5, 133.4,'.3'], 'CFC-11': [1/52, 137.37,''], 'CFC-12': [1/100, 120.91,'.1']})

substance='CFC-11'#choose 'CH3CCl3', 'CFC-11' or 'CFC-12'
substanceunits = substance+' (Gg/yr)'

P_WMO2014=P_WMO2014_df[substanceunits] #select data from dataframe
P_WMO2014=P_WMO2014.to_numpy()/1000000 #emissions in MT/year
P_WMO2018=P_WMO2018_df[substanceunits] #select data from dataframe
P_WMO2018=P_WMO2018.to_numpy()/1000 #emissions in MT/year
P_data=np.concatenate((P_WMO2014[:29],P_WMO2018[1:])) #create one emissions dataset from 1950 to 2016


#inputvariables boxmodels (k,ke,P,C0,C0N,C0S,dt,MW)
k=substance_df.iloc[0][substance] #reaction constants: '1/5' or '1/52'
ke=0.5 # interhemispheric exchange constant
P=P_data #emissions data: choose 'P_constant' or 'P_data'
C0=0 #start concentration onebox model (ppv)
C0N=30*10**-12 #NH start concentration twobox model (ppv)
C0S=10*10**-12 #SH start concentration twobox model (ppv)
MW=substance_df.iloc[1][substance] #Molar Weight: 'CH3CCl3: 133.4 gr/mole' or 'CFC-11: 137.37 gr/mole'
dt=1 #timestep (years)

#time array
timebar=np.insert(np.concatenate((P_WMO2014_df['time'].to_numpy()[:28],P_WMO2018_df['time'].to_numpy()[1:])), 0, 1949)

#Observations
O_df = pd.read_csv('AGAGE_CH3CCl3/global_mean_md.txt',header=14,delim_whitespace=True)

#ERRORBARS:
Errormax=(P_WMO2018_df[substanceunits]+P_WMO2018_df['Uncertainties ' + substanceunits]).to_numpy()/1000
Errormax=np.concatenate((P_WMO2014[:29],Errormax[1:]))
Errormin=(P_WMO2018_df[substanceunits]-P_WMO2018_df['Uncertainties ' + substanceunits]).to_numpy()/1000
Errormin=np.concatenate((P_WMO2014[:29],Errormin[1:]))
Errormax=oneboxRK4(k,Errormax,C0,dt,MW)*1.06
Errormin=oneboxRK4(k,Errormin,C0,dt,MW)*1.06

ObsErrormax = O_df[substance]+O_df['---'+substance_df.iloc[2][substance]]
ObsErrormin = O_df[substance]-O_df['---'+substance_df.iloc[2][substance]]

#Inverse ERRORBARS
Invmax = inverseonebox(1/67,O_df[substance]/(10**12),dt/12,MW)
Invmin = inverseonebox(1/43,O_df[substance]/(10**12),dt/12,MW)


#RK and observations comparison
plt.figure(figsize=[15,10])
plt.title(substance+' RK4 and observations comparison')
plt.plot(timebar, oneboxRK4(k,P,C0,dt,MW)*1.06,label='RK4 model')
plt.fill_between(timebar, Errormax, Errormin, alpha=0.2,label='Uncertainty range')
plt.plot(O_df['time'],O_df[substance]/(10**12),label='AGAGE observations')
plt.fill_between(O_df['time'],ObsErrormax/(10**12),ObsErrormin/(10**12),alpha=0.4)
plt.ticklabel_format(axis='y', scilimits=(-12,-12))
plt.ylabel(substance+' concentration [ppt]')
plt.xlabel('year')
plt.legend()
plt.show()


#Euler and RK4 comparison
plt.figure(figsize=[15,10])
plt.title(substance+' Euler and RK4 comparison')
plt.plot(timebar, oneboxeulerfw(k,P,C0,dt,MW)*1.06,label='Euler model')
plt.plot(timebar, oneboxRK4(k,P,C0,dt,MW)*1.06,label='RK4 model')
plt.plot(O_df['time'],O_df[substance]/(10**12),label='AGAGE observations')
plt.ticklabel_format(axis='y', scilimits=(-12,-12))
plt.ylabel(substance+' concentration [ppt]')
plt.xlabel('year')
plt.legend()
plt.show()




P_monthly=inverseonebox(k,O_df[substance]/(10**12),dt/12,MW)

P_yearly=np.zeros(int(len(P_monthly)/12)+1)
P_ymax=np.zeros(int(len(P_monthly)/12)+1)
P_ymin=np.zeros(int(len(P_monthly)/12)+1)
for i in range(int(len(P_monthly)/12+1)):
    if i ==0:
        P_yearly[i]=(np.mean(P_monthly[0:5]))
        P_ymax[i]=(np.mean(Invmax[0:5]))
        P_ymin[i]=(np.mean(Invmin[0:5]))
    elif i ==39:
        P_yearly[i]=(np.mean(P_monthly[474:]))
        P_ymax[i]=(np.mean(Invmax[474:]))
        P_ymin[i]=(np.mean(Invmin[474:]))
    else:    
        P_yearly[i]=(np.mean(P_monthly[((i-1)*12+5):((i-1)*12+17)]))
        P_ymax[i]=(np.mean(Invmax[((i-1)*12+5):((i-1)*12+17)]))
        P_ymin[i]=(np.mean(Invmin[((i-1)*12+5):((i-1)*12+17)]))
    

#Emissions
plt.figure(figsize=[15,10])
plt.title(substance+' emissions')
plt.plot(timebar, P, label='WMO emissions')
#plt.plot(O_df['time'][:-1],inverseonebox(k,O_df[substance]/(10**12),dt/12,MW))
plt.plot(np.linspace(1978,2017,40),P_yearly,label='Inverse onebox model')
plt.fill_between(np.linspace(1978,2017,40),P_ymin,P_ymax,alpha=0.3,color='#ff7f0e',label='Lifetime uncertainties')
plt.ylabel(substance+' emissions [Mt/yr]')
plt.xlabel('year')
plt.legend()
plt.show()