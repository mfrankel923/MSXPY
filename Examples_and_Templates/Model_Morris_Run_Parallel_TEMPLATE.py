# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 13:42:49 2022

@author: Matthew
"""


import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import wntr
import os

#CHANGE THIS VARIABLE BASED ON YOUR COMPUTER
main_folder=r'__________________'

sys.path.insert(0,main_folder+'\Function_Libraries')

#Import the packages that will be used in the subprosesses:

import epanet_toolkit as epa
import msx_toolkit as msx
import MSXPY_toolkit as mpy
import multiprocessing as mp
import pickle


#Import the processes that will be use in the main process only
if __name__=='__main__':
    from SALib.sample import morris as morris_s
    import time

#Set working directory
os.chdir(main_folder)


#Number of trajectories to run for the models
traj=_____

#Set the name of the pickle file
pickle_file=r'Examples_and_Templates\Pickle Files\_____.pkl'

#Set the seed so the morris trajectories are the same every time
seed=4

#Define constants and species to be varied in both models at the same time


#Choose the constants that we want to vary
constants_vary=[__________]
    
#Choose the species initial concentrations we want to vary   
#Dont vary H
species_vary=[____________]

#import bounds csv for the range on each parameter
#bounds_range=pd.read_csv('bounds.csv',header=None,index_col=0)

#Do the morris test for another model of interest- here it is Net1
    
#Close any models that might be open
epa.ENclose()
msx.MSXclose()


#open the inp file
inp_file=r'INP_and_MSX_Files/____________.inp'
epa.ENopen(inp_file,'report.rpt')
#open msx file
msx.MSXopen(r'INP_and_MSX_Files/_______.msx')  

#Number of days to run model
days=____

#0 for duration
epa.ENsettimeparam(0, int(days*24*3600))

#Solve the hydraulics of the model
msx.MSXsolveH()



#Define node where we want the initial concentrations.     

node='____'

    
if __name__=='__main__':
    #Get the values of the constants
    cons=mpy.GetConstants(constants_vary)  

    
    #Extract the initial concentrations of interest
    initial_con=mpy.GetInitialConcentration(node,species_vary)
        

    #append the rest of the initial concentrations
    i_cons=np.append(cons,initial_con)

    
    #Create a list of the variable names to be varied
    var_names=constants_vary.copy()

   
    var_names=var_names + species_vary
    
    #adjust the dimensions of i_cons so it is a d2 array
    i_cons=i_cons.reshape((-1,1))
    
    high_cons=np.zeros((len(i_cons),1))
    low_cons=np.zeros((len(i_cons),1))
    
   
    high_cons=1.25*i_cons
    low_cons=.8*i_cons
    
    bounds=np.hstack((low_cons,high_cons))
    
    #Create the problem dictionary for the SALib functions
    problem = {
        'num_vars': len(var_names),
        'names': var_names,
        'bounds': bounds
    }
    
    
    
    print('Generating Parameter Values')
    #Use the same parameter values as above- same seed and options
    param_values=morris_s.sample(problem,N=500,optimal_trajectories=traj,seed=seed)
    
    #Save the parameter values for later
    param_values_net1=param_values

#Get the base demands
base_demands=mpy.GetAllNodeDemands()  

#Get list of nodes
nodes=mpy.GetNodeNameList()

#Get list of links
links=mpy.GetLinkNameList()

   
def run_model(param_row):
    
    #Separate the values of the constants to the initial concentrations for ease of
    #manipulation later
       
    con_values=param_row[0:len(constants_vary)]
    species_values=param_row[len(constants_vary):]
   
           
    #Set the constant values in the model
    mpy.SetConstants(constants_vary,con_values)
    mpy.SetInitialConcentration(node,species_vary,species_values)
    
    #Solve the hydraulics of the model- If hydraulicspart of sensitivity analysis
    msx.MSXsolveH()   
  
    #Run the reaction model
    #Seprate by the t_start value
  
    my_results=mpy.MSXRunQual(by_species='no',t_start=days-1)
       
    
    return my_results



if __name__=='__main__':      
    
    
    #Get a list of all files in directory before the model evaluations
    files_before=os.listdir()
    
    #Get the number of available cores
    cores=int(np.round(mp.cpu_count()*.85,0))

    #Set start method to 'spawn' to avoid memory overload
    try:
        mp.set_start_method('forkserver')
    except:
        a=1
        
    t1=time.time()
    #Run the results using a map for parallelization
    pool=mp.Pool(processes=cores)
    
    print('Running Models')
    results_model=pool.map(run_model,param_values)
   
    pool.close()
    pool.join()
    t2=time.time()
    print(t2-t1)

    #Close epanet and msx models
    epa.ENclose()
    msx.MSXclose()
    #Get a list of all files in directory after model evaluations
    files_after=os.listdir()
    
    #Get the files that were created during model runs
    new_files=list(set(files_after).difference(files_before))
    
    #Remove binary files that were generated during model evaluations
    for file in new_files:
        os.remove(file)
    
    #assemble variables to be saved to pickle file into a dictionary
    to_pickle={}
    to_pickle['problem']=problem
    to_pickle['results']=results_model
    to_pickle['constants_vary']=constants_vary
    to_pickle['species_vary']=species_vary
    to_pickle['param_values']=param_values
    to_pickle['nodes']=nodes
    to_pickle['links']=links
    to_pickle['base_demands']=base_demands
    to_pickle['inp_file']=inp_file
        
    #Save Results as a pickle file
    #Save the simulation results as a pickle
    with open(pickle_file,'wb') as pfile:
        pickle.dump(to_pickle,pfile)
        

