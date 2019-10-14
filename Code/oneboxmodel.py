# -*- coding: utf-8 -*-
"""
One box model for Methyl Chloroform SOAC project

Created on Sat Oct  5 12:15:10 2019

@author: Reint Fischer
"""
import numpy as np

def oneboxeulerfw(k,P,C0,dt,MW):
    Mair = 1.81*10**(20) #mol of air in the entire atmosphere
    P = P*10**(12) #Megatonnes to grams
    PM = P/MW #moles/year from grams/year
    Pv = PM/Mair #volume fraction/year
    C = np.zeros(len(P)) #define length of abundance timeseries with length of emission data
    C[0] = C0 #Set initial abundance
    for n in range(len(P)-1): #Calculate abundances for next time step until t = n-1
        C[n+1] = C[n]+(Pv[n]-k*C[n])*dt #Euler fw method : previous abundance + (Emission rate - destruction rate)*timestep
    return C

def oneboxRK4(k,P,C0,dt,MW):
    Mair = 1.81*10**(20) #mol of air in the entire atmosphere
    P = P*10**(12) #Megatonnes to grams
    PM = P/MW #moles/year from grams/year
    Pv = PM/Mair #volume fraction/year
    C = np.zeros(len(P)) #define length of abundance timeseries with length of emission data
    C[0] = C0 #Set initial abundance
    for n in range(len(P)-1): #Calculate abundances for next time step until t = n-1
        k1 = (Pv[n]-k*C[n])*dt
        k2 = ((Pv[n]+Pv[n+1])/2-k*(C[n]+k1/2))*dt
        k3 = ((Pv[n]+Pv[n+1])/2-k*(C[n]+k2/2))*dt
        k4 = (Pv[n+1]-k*(C[n]+k3))*dt
        C[n+1] = C[n]+1/6*(k1+2*k2+2*k3+k4)
    return C
