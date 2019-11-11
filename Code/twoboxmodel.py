# -*- coding: utf-8 -*-
"""
Two box model for Methyl Chloroform SOAC project

Created on Sat Oct  5 16:23:42 2019

@author: reint fischer
"""
import numpy as np

def twoboxeulerfw(k,ke,P,C0N,C0S,dt,MW): # input in 1/year, 1/year, Mtonnes/year, ppv, ppv, years and g/moles respectively
    Mnh = 1.81*10**(20)/2                # mol of air in NH
    P = P*10**(12)                       # Megatonnes to grams
    PM = P/MW                            # moles/year from grams/year
    Pv = PM/Mnh                          # volume fraction/year in the NH
    CN = np.zeros(len(P))                # define length of abundance timeseries with length of emission data
    CS = np.zeros(len(P))                # define length of abundance timeseries with length of emission data
    CN[0] = C0N                          # Set initial NH abundance
    CS[0] = C0S                          # Set initial SH abundance
    for n in range(len(P)-1):            # Calculate abundances for next time step until t = n-1
        CN[n+1] = CN[n]+(Pv[n]-k*CN[n]-ke*CN[n]+ke*CS[n])*dt # Euler fw method for NH: Emission - destruction - loss to SH + gain from SH
        CS[n+1] = CS[n]+(-k*CS[n]+ke*CN[n]-ke*CS[n])*dt      # Euler fw method for SH: - destruction + gain from NH - loss to NH
    return CN,CS                         # return abundance timeseries in ppv