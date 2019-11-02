# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 13:37:53 2019

@author: janboukepronk

Here we create a combined dataset using AFEAS, UNEP and estimated Russian unreported emissions.
"""
import numpy as np
import pandas as pd



AFEAS_df = pd.read_excel('Data/em_cfc_11.xls') #Emissions from 1931 to 2003
UNEP_df = pd.read_excel('Data/UNEP_ODS_PROD_2010.xls',index_col=[0], parse_dates=True)/1000 #Emissions from 1986 to 2008

#Sectoral breakdown of UNEP_df cummulative emissions: RAc/Closed Cell/Open Cell = 0.1/0.5/0.4
UNEP_df['Total']=UNEP_df['nonA5']+UNEP_df['A5'] 
UNEP_df['Total_cum']=UNEP_df['Total'].cumsum()
UNEP_df['R/AC']=UNEP_df['Total']*0.1
UNEP_df['R/AC_cum']=UNEP_df['R/AC'].cumsum()
UNEP_df['Closed']=UNEP_df['Total']*0.5
UNEP_df['Closed_cum']=UNEP_df['Closed'].cumsum()
UNEP_df['Open']=UNEP_df['Total']*0.4
UNEP_df['Open_cum']=UNEP_df['Open'].cumsum()

# Sectoral breakdown and estimation of emissions using data from Russian McCulloch (2003). Linear increase from 0 to 43.7 Mt from 1968 to 1989.
Russian_P=np.linspace(0, 43700, num=21)/1000
Russian_RAc=np.cumsum(Russian_P*0.1)
Russian_Closed=np.cumsum(Russian_P*0.5)
Russian_Open=np.cumsum(Russian_P*0.4)
Russian_Production=pd.DataFrame(data={'R/AC_cum':Russian_RAc,'Closed_cum':Russian_Closed, 'Open_cum':Russian_Open,'year': np.arange(1968,1989,1) })

#combine cummulative datasets: From 1931 to 1989 AFEAS, from 1989 to 2009 UNEP. Adding Russian emmissions at 1968 to 1989.
AFEAS_RAc = AFEAS_df['S_nonhermetic_cum'].to_numpy()+AFEAS_df['S_hermetic'].to_numpy()
AFEAS_Closed = AFEAS_df['S_closed'].to_numpy()
AFEAS_Open = AFEAS_df['S_open'].to_numpy()

UNEP_RAc = UNEP_df['R/AC_cum'].to_numpy()
UNEP_Closed = UNEP_df['Closed_cum'].to_numpy()
UNEP_Open = UNEP_df['Open_cum'].to_numpy()

Combined_RAc = np.zeros(78)
Combined_Closed = np.zeros(78)
Combined_Open = np.zeros(78)

Combined_RAc[0:58] = AFEAS_RAc[0:58]
Combined_Closed[0:58] = AFEAS_Closed[0:58]
Combined_Open[0:58] = AFEAS_Open[0:58]

Combined_RAc[58:] = UNEP_RAc[3:]+ Combined_RAc[57]-UNEP_RAc[0]
Combined_Closed[58:] = UNEP_Closed[3:] + Combined_Closed[57]-UNEP_Closed[0]
Combined_Open[58:] = UNEP_Open[3:] + Combined_Open[57]-UNEP_Open[0]

Combined_RAc[37:58] = Combined_RAc[37:58]+ Russian_RAc
Combined_Closed[37:58] = Combined_Closed[37:58] + Russian_Closed
Combined_Open[37:58] = Combined_Open[37:58] + Russian_Open
Combined_RAc[58:] = Combined_RAc[58:] + [Russian_RAc[-1]]
Combined_Closed[58:] = Combined_Closed[58:] + [Russian_Closed[-1]]
Combined_Open[58:] = Combined_Open[58:] + [Russian_Open[-1]]


Combined_df=pd.DataFrame(data={'R/AC_cum': Combined_RAc, 'Closed_cum': Combined_Closed, 'Open_cum': Combined_Open, 'year': np.arange(1931,2009,1)})

#Save combined cummulative emissions
Combined_df.to_excel('Data/Combined_Cummulative_Production.xls')

## Increased closed-cell foam Production  ##





