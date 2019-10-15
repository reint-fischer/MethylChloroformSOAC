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

P_WMO2014_df=pd.read_excel('emissions_2014.xlsx')
P_WMO2018_df=pd.read_excel('agage_emissions.xlsx')
substance_df = pd.DataFrame({'CH3CCl3': [1/5, 133.4,'.3'], 'CFC-11': [1/52, 137.37,''], 'CFC-12': [1/100, 120.91,'.1']})

substance='CH3CCl3'#choose 'CH3CCl3', 'CFC-11' or 'CFC-12'
substanceunits = substance+' (Gg/yr)'

P_WMO2014=P_WMO2014_df[substanceunits] #select data from dataframe
P_WMO2014=P_WMO2014.to_numpy()/1000 #emissions in MT/year
P_WMO2018=P_WMO2018_df[substanceunits] #select data from dataframe
P_WMO2018=P_WMO2018.to_numpy() #emissions in MT/year
P_data=np.concatenate((P_WMO2014[:29],P_WMO2018[1:])) #create one emissions dataset from 1950 to 2016

#create constant P and time-array
P_constant=np.array([0.5]*18) #constant emissions in MT/year
#P_constant[5:18]=0 #turning emmisions of at 1977
time=np.arange(1972, 1972+len(P_constant), 1)


#inputvariables boxmodels (k,ke,P,C0,C0N,C0S,dt,MW)
k=substance_df.iloc[0][substance] #reaction constants: '1/5' or '1/52'
ke=0.5 # interhemispheric exchange constant
P=P_data #emissions data: choose 'P_constant' or 'P_data'
C0=20*10**-12 #start concentration onebox model (ppv)
C0N=30*10**-12 #NH start concentration twobox model (ppv)
C0S=10*10**-12 #SH start concentration twobox model (ppv)

MW=substance_df.iloc[1][substance] #Molar Weight: 'CH3CCl3: 133.4 gr/mole' or 'CFC-11: 137.37 gr/mole'
dt=1 #timestep (years)

#time array
timebar=np.insert(np.concatenate((P_WMO2014_df['time'].to_numpy()[:28],P_WMO2018_df['time'].to_numpy()[1:])), 0, 1949)



#Observations
O_df = pd.read_csv('AGAGE_CH3CCl3/global_mean_md.txt',header=14,delim_whitespace=True)

#BOTH HEMISPHERES
plt.figure(figsize=[15,10])
plt.plot(time, twoboxeulerfw(k,ke,P_constant,C0N,C0S,dt,MW)[0],label='NH')
plt.plot(time, twoboxeulerfw(k,ke,P_constant,C0N,C0S,dt,MW)[1],label='SH')
plt.ticklabel_format(axis='y', scilimits=(-12,-12))
plt.ylabel(substance+' concentration [ppt]')
plt.xlabel('year')
plt.legend()
plt.show()

#some plots   
plt.figure(figsize=[15,10])
plt.plot(time, twoboxeulerfw(1/2*k,ke,P_constant,C0N,C0S,dt,MW)[0], 'b',label='NH k = {0:.2f}'.format(1/2*k))
plt.plot(time, twoboxeulerfw(1/2*k,ke,P_constant,C0N,C0S,dt,MW)[1],'b',label='SH k = {0:.2f}'.format(1/2*k))
plt.plot(time, twoboxeulerfw(k,ke,P_constant,C0N,C0S,dt,MW)[0], color='black',label='NH k = {0:.2f}'.format(k))
plt.plot(time, twoboxeulerfw(k,ke,P_constant,C0N,C0S,dt,MW)[1], color='black',label='SH k = {0:.2f}'.format(k))
plt.plot(time, twoboxeulerfw(2*k,ke,P_constant,C0N,C0S,dt,MW)[0], 'r',label='NH k = {0:.2f}'.format(2*k))
plt.plot(time, twoboxeulerfw(2*k,ke,P_constant,C0N,C0S,dt,MW)[1], 'r',label='SH k = {0:.2f}'.format(2*k))
plt.plot(time, twoboxeulerfw(4*k,ke,P_constant,C0N,C0S,dt,MW)[0], 'c',label='NH k = {0:.2f}'.format(4*k))
plt.plot(time, twoboxeulerfw(4*k,ke,P_constant,C0N,C0S,dt,MW)[1], 'c',label='SH k = {0:.2f}'.format(4*k))
plt.ticklabel_format(axis='y', scilimits=(-12,-12))
plt.ylabel(substance+' concentration [ppt]')
plt.xlabel('year')
plt.legend()
plt.show()




#ERRORBARS:
Errormax=(P_WMO2018_df[substanceunits]+P_WMO2018_df['Uncertainties ' + substanceunits]).to_numpy()
Errormax=np.concatenate((P_WMO2014[:29],Errormax[1:]))
Errormin=(P_WMO2018_df[substanceunits]-P_WMO2018_df['Uncertainties ' + substanceunits]).to_numpy()
Errormin=np.concatenate((P_WMO2014[:29],Errormin[1:]))
Errormax=oneboxRK4(k,Errormax,C0,dt,MW)
Errormin=oneboxRK4(k,Errormin,C0,dt,MW)

ObsErrormax = O_df[substance]+O_df['---'+substance_df.iloc[2][substance]]
ObsErrormin = O_df[substance]-O_df['---'+substance_df.iloc[2][substance]]

#RK and observations comparison
plt.figure(figsize=[15,10])
plt.title('RK4 and observations comparison')
plt.plot(timebar, oneboxRK4(k,P,C0,dt,MW),label='RK4 model')
plt.fill_between(timebar, Errormax, Errormin, alpha=0.2)
plt.plot(O_df['time'],O_df[substance]/(10**9),label='AGAGE observations')
plt.fill_between(O_df['time'],ObsErrormax/(10**9),ObsErrormin/(10**9),alpha=0.4)
plt.ticklabel_format(axis='y', scilimits=(-9,-9))
plt.ylabel(substance+' concentration [ppb]')
plt.xlabel('year')
plt.legend()
plt.show()


#Euler and RK4 comparison
plt.figure(figsize=[15,10])
plt.title('Euler and RK4 comparison')
plt.plot(timebar, oneboxeulerfw(k,P,C0,dt,MW),label='Euler model')
plt.plot(timebar, oneboxRK4(k,P,C0,dt,MW),label='RK4 model')
plt.plot(O_df['time'],O_df[substance]/(10**9),label='AGAGE observations')
plt.ticklabel_format(axis='y', scilimits=(-9,-9))
plt.ylabel(substance+' concentration [ppb]')
plt.xlabel('year')
plt.legend()
plt.show()





