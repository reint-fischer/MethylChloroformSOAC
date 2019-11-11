# MethylChloroform Box models
For the SOAC course Jan Bouke Pronk and Reint Fischer will create Box
Models of the chemical activity of Methyl Chloroform to study the expected behaviour of ozone-depleting substances.

The repository includes three maps: (1) Code, (2) Presentation and (3) TaskDescription.

1) Code: 

This map contains all python (.py) files. The complete list:
  
    1 bottomup                              :   The bottom-up model. Produces plots of CFC-11 emissions and banksize from 1931 to 2008. 
  
    2 bottomup_emissionrange                :   Bottom-up model for different CFC-11 bank sensitivities. Produces plots of emissions from 1931 to 2018. Plots are compared with plot from 'inversemodel.py'
  
    3 globalproduction_cfc11_dataframe      :   Produces CFC-11 Combined_Cummulative_Production.xls using production data from AFEAS, UNEP and unreported Russian Emissions
  
    4 inversemodel                          :   Models emissions from observed concentrations (Euler forward numerical scheme) 
  
    5 lovelock                              :   Produces plots of different substances using oneboxmodel.py and twoboxmodel.py to evaluate model performance. 
  
    6 oneboxmodel                           :   Models substance concentration using one box using RK4 and Euler forward numerical schemes. 
  
    7 realemissions                         :   Produces plots of substance concentration and emissions from real emission data. oneboxmodel.py, twoboxmodel.py and inversemodel used as numerical model. 
  
    8 twoboxmodel                           :   Models substance concentration using two boxes and Euler forward numerical schemes.

  
  Code contains two submaps: (1.1) Data and (1.2) Figures:
  
  1.1) Data: 
  
  This map contains all data used in the python files: The Complete list:
      
      1 agage_emissions                   :   1978-2016 emisssion data of the following substances: CH3CCl3, CFC-11 and CFC-12.
      
      2 Combined_Cummulative_Production   :   Output from 'globalproduction_cfc11_dataframe.py'. Cummulative CFC-11 production data from 1931 to 2008.
      
      3 em_cfc_11                         :   AFEAS CFC-11 production data from 1931 to 2003.
      
      4 emissions_2014                    :   AGAGE CH3CCl3, CFC-11 and CFC-12 emission data from 1951 to 2013
      
      5 global_mean_md                    :   Global CFC-11 AGAGE observations from 1978 to 2018.
      
      6 UNEP_ODS_PROD_2010                :   UNEP production data from 1986 to 2008. 
      
      7 Yearly_Emissions_InverseModel     :   Output file from 'inversemodel.py' calculates emissions from 1978 to 2018.
      
  1.2) Figures:
 
  Here all figures produced by all python (.py) files are stored:     
        
      1 Bottemup_banksize
      2 Bottemup_emissions
      3 Bottemup_emissions_range_bank_sensitivity
      4 Concentration_Euler_and_RK4_comparison
      5 Concentration_RK4_and_observations_comparison
      6 Emissions_Inverse_model_comparison
      7 Emissions_AFEAS_WMO_inverse_and_bottemup
      8 Increased_Closed_Cell_Foam_Production
      9 LoveLock_Concentration_Euler_and_RK4_comparison
      10  Lovelock_concentration_twoboxmodel
      11  Lovelock_concentration_twoboxmodel_ceased_emissions
      12  Lovelock_concentration_twoboxmodel_varying_lifetime
      13  LoveLock_logConcentration_Euler_and_RK4_comparison
      14  Lovelock_logconcentration_twoboxmodel
      15  Lovelock_logconcentration_twoboxmodel_ceased_emissions
      16  Lovelock_logconcentration_twoboxmodel_varying_lifetime
      17  Lovelock_original
      
  
2) Presentation: Contains PDF PowerPoint(.pptx) file of CFC-11 detective study

3) TaskDescription:
This map contains all original datafiles, literature, and taskdescription.

   
      
  
      

