# -*- coding: utf-8 -*-
"""
One box model for Methyl Chloroform SOAC project

Created on Sat Oct  5 12:15:10 2019

@author: Reint Fischer
"""
import numpy as np

def oneboxeulerfw(k,P,C0,dt,MW):
    Mair = 1.81*10**(20) #mol of air
    P = P*10**(12) #Megatonnes to grams
    PM = P/MW #moles/year
    Pv = PM/Mair
    C = np.zeros(len(P))
    C[0] = C0
    for n in range(len(P)-1):
        C[n+1] = C[n]+(Pv[n]-k*C[n])*dt
    return C

mwmc = 133.40 #g/mol