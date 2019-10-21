# -*- coding: utf-8 -*-
"""
Reverse model

Created on Mon Oct 21 14:03:44 2019

@author: reintfischer
"""

import numpy as np

def inverseonebox(k,C,dt,MW):
    C = C/1.06
    Pv = np.zeros(int(len(C)-1))
    for i in range(len(Pv)):
        Pv[i] = (C[i+1]-C[i])/dt+k*C[i]
    Mair = 1.81*10**(20) #mol of air in the entire atmosphere
    PM = Pv*Mair #volume fraction/year
    P = PM*MW #moles/year from grams/year
    P = P/10**(12) #Megatonnes to grams
    return P
    
    

