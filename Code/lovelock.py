# -*- coding: utf-8 -*-
"""
Lovelock model

Created on Tue Oct 15 16:47:47 2019

@author: Gebruiker
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from oneboxmodel import oneboxeulerfw, oneboxRK4
from twoboxmodel import twoboxeulerfw


substance_df = pd.DataFrame({'CH3CCl3': [1/5, 133.4,'.3'], 'CFC-11': [1/52, 137.37,''], 'CFC-12': [1/100, 120.91,'.1']})
substance='CH3CCl3'#choose 'CH3CCl3', 'CFC-11' or 'CFC-12'
substanceunits = substance+' (Gg/yr)'

#create constant P and time-array
P_constant=np.array([0.5]*5) #constant emissions in MT/year
P_stop =np.array([0.5]*18) #
P_stop[5:18]=0 #turning emmisions of at 1977
time=np.arange(1972, 1972+len(P_constant), 1)
timestop=np.arange(1972, 1972+len(P_stop), 1)

#inputvariables boxmodels (k,ke,P,C0,C0N,C0S,dt,MW)
k=substance_df.iloc[0][substance] #reaction constants: '1/5' or '1/52'
ke=0.5 # interhemispheric exchange constant
C0=20*10**-12 #start concentration onebox model (ppv)
C0N=30*10**-12 #NH start concentration twobox model (ppv)
C0S=10*10**-12 #SH start concentration twobox model (ppv)

MW=substance_df.iloc[1][substance] #Molar Weight: 'CH3CCl3: 133.4 gr/mole' or 'CFC-11: 137.37 gr/mole'
dt=1 #timestep (years)


plt.figure(figsize=[15,10])
plt.title(substance+' concentration: Euler and RK4 comparison', fontsize=20)
plt.plot(time, oneboxeulerfw(k,P_constant,C0,dt,MW),label='Euler', color='C1')
plt.plot(time, oneboxRK4(k,P_constant,C0,dt,MW),label='RK4', color='C0')
plt.ticklabel_format(axis='y', scilimits=(-12,-12))
plt.ylabel(substance+' concentration [ppt]', fontsize=20)
plt.xlabel('year', fontsize=20)
plt.tick_params(labelsize=15)
plt.grid(axis='y',alpha=.3)
plt.legend(fontsize=12)
plt.savefig('Figures/LoveLock_Concentration__Euler_and_RK4_comparison.png')
plt.show()

#BOTH HEMISPHERES
plt.figure(figsize=[15,10])
plt.title(substance+' concentration twobox model', fontsize=20)
plt.plot(time, twoboxeulerfw(k,ke,P_constant,C0N,C0S,dt,MW)[0],label='NH')
plt.plot(time, twoboxeulerfw(k,ke,P_constant,C0N,C0S,dt,MW)[1],label='SH')
plt.ticklabel_format(axis='y', scilimits=(-12,-12))
plt.ylabel(substance+' concentration [ppt]', fontsize=20)
plt.xlabel('year', fontsize=20)
plt.tick_params(labelsize=15)
plt.grid(axis='y',alpha=.3)
plt.legend(fontsize=12)
plt.savefig('Figures/Lovelock_concentration_twoboxmodel.png')
plt.show()

#some plots   
plt.figure(figsize=[15,10])
plt.title(substance+' concentration twobox model: varying lifetime', fontsize=20)
plt.plot(time, twoboxeulerfw(1/2*k,ke,P_constant,C0N,C0S,dt,MW)[0], 'b',label='NH k = {0:.2f}'.format(1/2*k))
plt.plot(time, twoboxeulerfw(1/2*k,ke,P_constant,C0N,C0S,dt,MW)[1],'b',label='SH k = {0:.2f}'.format(1/2*k))
plt.plot(time, twoboxeulerfw(k,ke,P_constant,C0N,C0S,dt,MW)[0], color='black',label='NH k = {0:.2f}'.format(k))
plt.plot(time, twoboxeulerfw(k,ke,P_constant,C0N,C0S,dt,MW)[1], color='black',label='SH k = {0:.2f}'.format(k))
plt.plot(time, twoboxeulerfw(2*k,ke,P_constant,C0N,C0S,dt,MW)[0], 'r',label='NH k = {0:.2f}'.format(2*k))
plt.plot(time, twoboxeulerfw(2*k,ke,P_constant,C0N,C0S,dt,MW)[1], 'r',label='SH k = {0:.2f}'.format(2*k))
plt.plot(time, twoboxeulerfw(4*k,ke,P_constant,C0N,C0S,dt,MW)[0], 'c',label='NH k = {0:.2f}'.format(4*k))
plt.plot(time, twoboxeulerfw(4*k,ke,P_constant,C0N,C0S,dt,MW)[1], 'c',label='SH k = {0:.2f}'.format(4*k))
plt.ticklabel_format(axis='y', scilimits=(-12,-12))
plt.ylabel(substance+' concentration [ppt]', fontsize=20)
plt.xlabel('year', fontsize=20)
plt.tick_params(labelsize=15)
plt.grid()
plt.legend(fontsize=12)
plt.savefig('Figures/Lovelock_concentration_twoboxmodel_varying_lifetime.png')
plt.show()

plt.figure(figsize=[15,10])
plt.title(substance+' concentration twobox model: Abrubt cease in emissions', fontsize=20)
plt.plot(timestop, twoboxeulerfw(k,ke,P_stop,C0N,C0S,dt,MW)[0],label='NH')
plt.plot(timestop, twoboxeulerfw(k,ke,P_stop,C0N,C0S,dt,MW)[1],label='SH')
plt.ticklabel_format(axis='y', scilimits=(-12,-12))
plt.ylabel(substance+' concentration [ppt]', fontsize=20)
plt.xlabel('year', fontsize=20)
plt.tick_params(labelsize=15)
plt.grid(axis='y',alpha=.3)
plt.legend(fontsize=12)
plt.savefig('Figures/Lovelock_concentration_twoboxmodel_ceased_emissions.png')
plt.show()