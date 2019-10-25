# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:23:55 2019

@author: janbo
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

em_cfc_11=pd.read_excel('em_cfc_11.xls')


plt.figure(figsize=[15,10])
plt.title('production & release global annual')
plt.plot(em_cfc_11['year'],em_cfc_11['P_annual'])
plt.plot(em_cfc_11['year'],em_cfc_11['R_annual'])
plt.show()


plt.figure(figsize=[15,10])
plt.title('production, released & unreleased global total')
plt.plot(em_cfc_11['year'],em_cfc_11['P_total'])
plt.plot(em_cfc_11['year'],em_cfc_11['R_total'])
plt.plot(em_cfc_11['year'],em_cfc_11['U_total'])
plt.show()

plt.figure(figsize=[15,10])
plt.title('Sales, Released & Unreleased nonhermetic_cum')
plt.plot(em_cfc_11['year'],em_cfc_11['S_nonhermetic_cum'])
plt.plot(em_cfc_11['year'],em_cfc_11['R_nonhermetic_cum'])
plt.plot(em_cfc_11['year'],em_cfc_11['U_nonhermetic_cum'])
plt.show()

plt.figure(figsize=[15,10])
plt.title('Sales, Released & Unreleased Blowing Agents Closed Cell Foam')
plt.plot(em_cfc_11['year'],em_cfc_11['S_closed'])
plt.plot(em_cfc_11['year'],em_cfc_11['R_closed'])
plt.plot(em_cfc_11['year'],em_cfc_11['U_closed'])
plt.show()

plt.figure(figsize=[15,10])
plt.title('Sales, Released & Unreleased Open Cell Foam, Aerosols & Others')
plt.plot(em_cfc_11['year'],em_cfc_11['S_open'])
plt.plot(em_cfc_11['year'],em_cfc_11['R_open'])
plt.plot(em_cfc_11['year'],em_cfc_11['U_open'])
plt.show()