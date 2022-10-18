# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 16:43:20 2022

@author: Matthew
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import wntr
import os

#CHANGE THIS VARIABLE BASED ON YOUR COMPUTER
main_folder=r'C:\Users\frank\Documents\Box Sync\working files\Leap-hi\Epanet-MSX\MSXpy\MSXPY'

pwd=os.getcwd()
pwd=pwd[0:-23]
sys.path.insert(0,main_folder+'\Function_Libraries')
sys.path.insert(0,main_folder+'\INP_and_MSX_Files')

import MSXPY_toolkit as mpy
import epanet_toolkit as epa
import msx_toolkit as msx

#Close any files that were already open
epa.ENclose()
msx.MSXclose()

#open the inp file
os.chdir(main_folder)

inp_file = r'INP_and_MSX_Files/Net1.inp'
epa.ENopen(inp_file,'report.rpt')
#open msx file
msx.MSXopen(r'INP_and_MSX_Files/bacteria_net1.msx')
#msx.MSXopen('example_net1.msx')

#Import wntr model to be used later for plot
wn = wntr.network.WaterNetworkModel(inp_file)


#Number of days to run model
days=12

#0 for duration
epa.ENsettimeparam(0, int(days*24*3600))
#epa.ENsettimeparam(0, 51300)

#Solve the hydraulics of the model
msx.MSXsolveH()   

#Run the reaction model
print('Running Sim')
my_results=mpy.MSXRunQual(by_species='yes',t_start=days-1)
print('Ending Sim')

epa.ENclose()
msx.MSXclose()
os.remove('report.rpt')


# by_step=1

# if by_step!=1:
#     print('running')
#     #Run the reaction model
#     my_results=mpy.MSXRunQual(by_species='no')
#     print('finished')
    
#     #Get the list of links
#     links=mpy.GetLinkNameList()
    
#     #for i in range(len(links)):
#         #print(links[i])
#         #print(my_results['link'][links[i]]['Xa'].loc[1500])
#         #print(my_results['link'][links[i]]['MUB'].loc[2340])


# if by_step==1:
#     t_left=1
#     msx.MSXinit(0)
#       #Create loop to run model
#     while (t_left>0):
#         #Solve the quality for that timestep
#         [t,t_left]=msx.MSXstep()
        
        


        

# e_type='node'
# e_id='1'

# plt.figure()
# plt.plot(my_results[e_type][e_id]['AGE'],my_results[e_type][e_id]['Hb'],marker='o',ls='')
# plt.xlabel('Age (hours)')
# plt.ylabel('TTHM ug/l Hb')

# plt.figure()
# plt.plot(my_results[e_type][e_id]['AGE'],my_results[e_type][e_id]['Cb'],marker='o',ls='')
# plt.xlabel('Age (hours)')
# plt.ylabel('Chlorine mg/l Cb')

# plt.figure()
# plt.plot(my_results[e_type][e_id]['AGE'],my_results[e_type][e_id]['Nb'],marker='o',ls='')
# plt.xlabel('Age (hours)')
# plt.ylabel('NOM mg/l Nb')

# plt.figure()
# plt.plot(my_results[e_type][e_id]['AGE'],my_results[e_type][e_id]['Sb'],marker='o',ls='')
# plt.xlabel('Age (hours)')
# plt.ylabel('BDOC mg/l Sb')

# plt.figure()
# plt.plot(my_results['link'][e_id]['AGE'],my_results[e_type][e_id]['Xb'],marker='o',ls='')
# plt.xlabel('Age (hours)')
# plt.ylabel('Biomass mg/l Xb')

