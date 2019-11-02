# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 22:47:26 2019

@author: janbo
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#load emmision data from WMO, AFEAS, Combined Cummulative Production, and Inverse emissions
P_WMO2014_df=pd.read_excel('Data/emissions_2014.xlsx')
P_WMO2018_df=pd.read_excel('Data/agage_emissions.xlsx')
Comb_Em_df = pd.read_excel('Data/Combined_Cummulative_Production.xls',index_col=[0], parse_dates=True)
AFEAS_df = pd.read_excel('Data/em_cfc_11.xls')
Inv_em_df = pd.read_excel('Data/Yearly_Emissions_InverseModel.xls')*1000

#create combined WMO dataset
P_WMO2014=P_WMO2014_df['CFC-11 (Gg/yr)'] #select data from dataframe
P_WMO2014=P_WMO2014.to_numpy()/1000000 #emissions in MT/year
P_WMO2018=P_WMO2018_df['CFC-11 (Gg/yr)'] #select data from dataframe
P_WMO2018=P_WMO2018.to_numpy()/1000 #emissions in MT/year
P_WMO_data=np.concatenate((P_WMO2014[:29],P_WMO2018[1:])) #create one emissions dataset from 1950 to 2016

##### Extend dataset untill 2018 assuming no sales ############
zeros=pd.DataFrame(np.zeros((10, 4)), columns=Comb_Em_df.columns)
Comb_Em_df=pd.DataFrame(np.concatenate((Comb_Em_df, zeros)), columns=Comb_Em_df.columns)
Comb_Em_df['year'][78:88]=np.arange(2009,2019,1)
Comb_Em_df['R/AC_cum'][78:88]=Comb_Em_df['R/AC_cum'][77]
Comb_Em_df['Closed_cum'][78:88]=Comb_Em_df['Closed_cum'][77]
Comb_Em_df['Open_cum'][78:88]=Comb_Em_df['Open_cum'][77]


#choose bank emission scenario 

def bottumup(rRAC, rClosed, rOpen, Extra):

    ### Emission rates ###
    rPnD = 0.015 #Production & Distribution
    riRAC = 0.050 #Refrigeration and Air Conditioning Installation
    riClosed = 0.300 #Closed Foams Installation
    riOpen = 0.980 #Open Foams and Emissive Uses Installation
    rRAC = rRAC #Refrigeration and Air Conditioning Banks
    rClosed = rClosed #Closed Foams Banks
    rOpen = rOpen #Open Foams and Emissive Uses Banks
    
    
    ### Cumulative sales ###
    RAC = np.copy(Comb_Em_df['R/AC_cum'].to_numpy())
    Closed = np.copy(Comb_Em_df['Closed_cum'].to_numpy())
    Open = np.copy(Comb_Em_df['Open_cum'].to_numpy())
    
    if Extra==True:
        Closed[71:] = Closed[71:]+np.cumsum([35]*len(Closed[71:]))
        Closed[79:] = Closed[79:]+np.cumsum([35]*len(Closed[79:]))
    
    
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
            
    emissions = np.asarray(ERAC1) + np.asarray(ERAC2) + np.asarray(ERAC3) + np.asarray(EClosed1) + np.asarray(EClosed2) + np.asarray(EClosed3) + np.asarray(EOpen1) + np.asarray(EOpen2) + np.asarray(EOpen3)
    
    return emissions
    
#%%

#PICK From RANGE:
#rRAC = 0.02 -- 0.10 #Refrigeration and Air Conditioning Banks
#rClosed = 0.04 -- 0.10 #Closed Foams Banks
#rOpen = 0.70 -- 0.98 #Open Foams and Emissive Uses Banks



path1=bottumup(0.05, 0.08, 0.98, False)
path2=bottumup(0.1, 0.1, 0.98, False)
path3=bottumup(0.02, 0.04, 0.7, False)

extra_foam=bottumup(0.05, 0.08, 0.98, True)






#time array
timebar=np.insert(np.concatenate((P_WMO2014_df['time'].to_numpy()[:28],P_WMO2018_df['time'].to_numpy()[1:])), 0, 1949)


#Emissions
plt.figure(figsize=[15,10])
plt.title('Bottom-up CFC-11 emissions range: Bank sensitivity', fontsize=20)
plt.plot(Comb_Em_df['year'],path1, label='Sensitivity - most likely', color='C2')
plt.plot(Comb_Em_df['year'],path2, label='Sensitivity - High', color='C3')
plt.plot(Comb_Em_df['year'],path3, label='Sensitivity - Low', color='C0')
plt.plot(np.linspace(1978,2017,40),Inv_em_df['P_yearly'],label='Inverse onebox model', color='C1')
plt.fill_between(np.linspace(1978,2017,40),Inv_em_df['P_ymin'],Inv_em_df['P_ymax'],alpha=0.3,color='C1',label='Lifetime uncertainties')
plt.ylabel('CFC-11 emissions [Mt/yr]', fontsize=15)
plt.xlabel('year', fontsize=15)
plt.tick_params(labelsize=15)
plt.grid(axis='y',alpha=.3)
plt.legend(fontsize=12)
#plt.savefig('Figures/Bottemup_emissions_range_bank_sensitivity.png')
plt.show()

#Emission comparison WMO, AFEAS, bottomup, Inverse
plt.figure(figsize=[15,10])
plt.title('Bottom-up CFC-11 emissions: Bottem-up vs Top-down', fontsize=20)
plt.plot(timebar, P_WMO_data*1000, label='Top-down: WMO emissions')
plt.plot(np.linspace(1978,2017,40),Inv_em_df['P_yearly'],label='Top-down: Inverse onebox model', color='C1')
plt.plot(Comb_Em_df['year'],path1, label='Bottem-up: most likely', color='C2')
plt.plot(AFEAS_df['year'], AFEAS_df['R_annual'], label='Bottem-up: AFEAS', color='C3')
plt.fill_between(np.linspace(1978,2017,40),Inv_em_df['P_ymin'],Inv_em_df['P_ymax'],alpha=0.3,color='C1',label='Lifetime uncertainties')
plt.ylabel('CFC-11 emissions [Mt/yr]', fontsize=15)
plt.xlabel('year', fontsize=15)
plt.tick_params(labelsize=15)
plt.grid(axis='y',alpha=.3)
plt.legend(fontsize=12)
#plt.savefig('Figures/Emissions_AFEAS_WMO_inverse_and_bottemup.png')
plt.show()

#create barplot of extra emissions
extra_f=np.asarray([35]*15)
extra_f[8:]=extra_f[8:]+35


plt.figure(figsize=[15,10])
plt.title('Increased Closed-Cell Foam Production', fontsize=20)
plt.plot(Comb_Em_df['year'],extra_foam, label='Bottem-up: most likely', color='C2')
plt.plot(np.linspace(1978,2017,40),Inv_em_df['P_yearly'],label='Inverse onebox model', color='C1')
plt.fill_between(np.linspace(1978,2017,40),Inv_em_df['P_ymin'],Inv_em_df['P_ymax'],alpha=0.3,color='C1',label='Lifetime uncertainties')
plt.bar(np.linspace(2002,2017,15), extra_f , width=1,alpha=0.3,color='C3',label='Extra Production Closed Foam')
plt.ylabel('CFC-11 emissions [Mt/yr]', fontsize=15)
plt.xlabel('year', fontsize=15)
plt.tick_params(labelsize=15)
plt.grid(axis='y',alpha=.3)
plt.legend(fontsize=12)
plt.savefig('Figures/Increased_Closed_Cell_Foam_Production.png')
plt.show()



