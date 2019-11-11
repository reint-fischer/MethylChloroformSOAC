# -*- coding: utf-8 -*-
"""
Reverse model

Created on Mon Oct 21 14:03:44 2019

@author: reintfischer
"""

import numpy as np

def inverseonebox(k,C,dt,MW):           # Input in 1/year, ppv, years and g/mol respectively
    C = C/1.06                          # Boundary layer compensation
    Pv = np.zeros(int(len(C)-1))        # Empty emission array
    for i in range(len(Pv)):
        Pv[i] = (C[i+1]-C[i])/dt+k*C[i] # rewritten Euler forward one-box model
    Mair = 1.81*10**(20)                # mol of air in the entire atmosphere
    PM = Pv*Mair                        # volume fraction/year to moles/year
    P = PM*MW                           # moles/year to grams/year
    P = P/10**(12)                      # Megatonnes from grams
    return P                            # Megatonnes/year


    
    

