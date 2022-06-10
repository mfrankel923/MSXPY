# -*- coding: utf-8 -*-
"""
Created on Wed May 25 10:25:48 2022

@author: Matthew
"""

#%% Import Packages

#Import the packages that will be used in the subprosesses:
import numpy as np
import epanet_toolkit as epa
import msx_toolkit as msx
import pandas as pd
import mf_msx_toolkit as mf
import multiprocessing as mp
import pickle
import os

#Import the processes that will be use in the main process only
if __name__=='__main__':
    from SALib.sample import morris as morris_s
    import time

#%% Select initial variables

# pickle_file is the name of the pickle file with the saved simulation results

# seed is the random seed for reproducability of the input parameter values

# days is the duration of the simulation, in units of days

# inp_file is the name of the EPANET .inp file

# msx_file is the name of the EPANET MSX .msx file

# traj is the number of trajectories to utilize for the Method of Morris

# constants_vary is a list containing the names of the constants to be included
# in the sensitivity analysis. The constants must appear in the "Constants" 
# block of the .msx file

# species_vary is a list containing the names of the species to be included in 
#the sensitivity analysis, for which the initial concentration is varied. The 
#species must appear in the "Species" block of the .msx file

# node is the node in the Epanet model from which the initial concentrations 
#should be extracted to be used as the base value for the method of morris 
#sensitivity analysis.

# bounds_csv is the name of the csv file containing the upper and lower bound 
#of each parameter



#Number of trajectories to run for the models
traj=3

#Set the name of the pickle file
pickle_file='beaker_morris.pkl'

#Set the seed so the morris trajectories are the same every time
seed=4

#Define constants and species to be varied in both models at the same time

#Choose the constants that we want to vary
constants_vary=['k1','k2','k3','k4','k6','k7','k8','k9','k10','k12','k13',
                'k14','k11CO3','k11OCL','k11OH','kDOC1','kDOC2','AC1','AC2','AC3']
    
#Choose the species initial concentrations we want to vary   
#Dont vary H
species_vary=['DOC1','DOC2','TOTNH','TOTCO']

#import bounds csv for the range on each parameter
bounds_range=pd.read_csv('bounds.csv',header=None,index_col=0)

inp_file='beaker.inp'

msx_file='Beaker-NH2CL_JV_TOC.msx'

#Number of days to run beaker model
days=3


#%% Import and run hydraulic simulaiton

#Close any files that were already open
epa.ENclose()
msx.MSXclose()

#open the inp file
epa.ENopen(inp_file,'report.rpt')

#open msx file
msx.MSXopen(msx_file)


#Set the duration of the model evaluation
epa.ENsettimeparam(0, days*24*3600)

#Solve the hydraulics of the model
msx.MSXsolveH()
    

#%% Set up the problem dictionary


#In this block, the "problem" dictionary, as required by the SALIB package, 
#is created. Because TOC, S1, and S2 are model parameters which do not appear
# in the MSX file, the <code>var_names</code> variable is manipulated to 
#include the TOC, S1, and S2 variables. This is not necesary if all of the 
#model parameters exist in the msx file.


#The node that we want the initial concentrations form
node='1'

#The if statment is included so that this section of code only executes in the 
#main process and not in any of the subprocesses
if __name__=='__main__':
    
    #Define constants_vary and species_vary as global variables because they are
    #used in the parallel function but it is a bit messy to have them in the 
    #function arguments
    
    #Get the values of the constants
    cons=mf.GetConstants(constants_vary)
        
    #Extract the initial concentrations of interest
    initial_con=mf.GetInitialConcentration(node,species_vary)
        
    #Adjust the TOC, s1, and s2 values outside of the model
    #Initial TOC value
    TOC=1.5
    #Initial S1 Value
    s1=.016
    s2=.57
        
    #Append the values of the initial constants of interest to the initial
    #Because TOC, s1 and s2 are outside the model itself append those ones seperately
    i_cons=np.append(cons,[TOC,s1,s2])
    #append the rest of the initial concentrations
    i_cons=np.append(i_cons,initial_con[2:])
    
    #Create a list of the variable names to be varied
    var_names=constants_vary.copy()

    var_names.append('TOC')
    var_names.append('S1')
    var_names.append('S2')
    var_names=var_names + species_vary[2:]
    
    #adjust the dimensions of i_cons so it is a d2 array
    i_cons=i_cons.reshape((-1,1))
    
    high_cons=np.zeros((len(i_cons),1))
    low_cons=np.zeros((len(i_cons),1))
    
    for i in range(len(i_cons)):
        high_cons[i]=(1+bounds_range.loc[var_names[i],1]/100)*i_cons[i]
        low_cons[i]=(1-bounds_range.loc[var_names[i],1]/100)*i_cons[i]
        
    bounds=np.hstack((low_cons,high_cons))
    
    #Create the problem dictionary for the SALib functions
    problem = {
        'num_vars': len(var_names),
        'names': var_names,
        'bounds': bounds
    }

#%% Function to execute model evaluations

#Define the function to be used in the parallel process
def beaker_sa(param_row):
    node='1'
    #Separate the values of the constants to the initial concentrations for ease of
    #manipulation later
    con_values=param_row[0:len(constants_vary)]
    species_values=param_row[len(constants_vary):]
    

    # #Convert from the S1 and S2 values to DOC1 and DOC2 Concentrations
    #S1 to DOC1
    #These lines of code are specific to the monochloramine reaction and should
    #be deleted for use in other reactions
    species_values[1]=np.multiply(species_values[1],species_values[0])/12000
    #S2 to DOC2
    species_values[2]=np.multiply(species_values[2],species_values[0])/12000

    #Set the initial species values in the model
    #Leave out the first column of species_values because that is 
    #the direct TOC conecntration which does not end up directly in
    #the MSX model
    mf.SetInitialConcentration(node,species_vary,species_values[1:])

    #Set the constant values in the model
    mf.SetConstants(constants_vary,con_values)

    #run the model
    my_results=mf.MSXRunQual(links=[],by_species='no')       
    
    return my_results 


#%% Run models using parallelization


#Only run the parallelization and the rest of the analysis in the main process
if __name__=='__main__':
        
    
    #Get a list of all files in directory before the model evaluations
    files_before=os.listdir()
    
    #Create a variable of the names of variables used in sensitivty analysis
    var_names=problem['names']
    
    #Generate parameter values
    print('Running Morris with ' +str(traj)+ ' trajectories')
    param_values=morris_s.sample(problem,N=1000,optimal_trajectories=traj,seed=seed)
    
    #Save the parameter values for later
    param_values_beaker=param_values
    
    #Find the number of rows in param_values (the number of simulations to be run)
    [r,c]=param_values.shape 
    
    #Get the number of available cores
    cores=int(np.round(mp.cpu_count()*.85,0))
    
    print('Running Models')
    t1=time.time()
    #Run the results using a map for parallelization
    try:
        mp.set_start_method('forkserver')
    except:
        a=1+1
    pool=mp.Pool(processes=cores)
    results=pool.map(beaker_sa,param_values)
    pool.close()
    pool.join()
    t2=time.time()
    print(t2-t1)
    #Run the results using a map for parallelization
    #results=list(map(beaker_sa,param_values[0:2,:]))
    
    
    
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
    to_pickle['results']=results
    to_pickle['constants_vary']=constants_vary
    to_pickle['species_vary']=species_vary
    to_pickle['param_values']=param_values
    
    #Save Results as a pickle file
    #Save the simulation results as a pickle
    with open(pickle_file,'wb') as pfile:
        pickle.dump(to_pickle,pfile)
        
    print('Complete')
    
