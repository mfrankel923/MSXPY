# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 16:13:24 2022

@author: Matthew
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
from SALib.sample import morris as morris_s
from SALib.analyze import morris as morris_a
import pandas as pd
import wntr
import mf_msx_toolkit as mf

pickle_file_model='example_morris.pkl'

species='Xb'


#import model results from pickle file
with open(pickle_file_model,'rb') as pfile:
    model_pickle=pickle.load(pfile)

results_model=model_pickle['results']
nodes=model_pickle['nodes']
links=model_pickle['links']
problem=model_pickle['problem']
param_values_model=model_pickle['param_values']
inp_file=model_pickle['inp_file']

morris_results, age= mf.MorrisWallEvaluate(model_pickle,species)
    
plt.figure()
plt.plot(age['node']['32'],morris_results['mu_star']['node']['32']['Kd'],ls='',marker='o')

plt.figure()
plt.plot(age['link']['122'],morris_results['mu_star']['link']['122'],ls='',marker='o')

#At an aggregate level, which parameters are influential?


links.remove('10')
links.remove('9')
parameters=problem['names']
mu_star_link_df=pd.DataFrame(columns=parameters,index=links)
sigma_link_df=pd.DataFrame(columns=parameters,index=links)


for i in range(len(links)):
    mu_star_df=morris_results['mu_star']['link'][links[i]]
    sigma_df=morris_results['sigma']['link'][links[i]]
    
    link_mu_star_row=[]
    link_sigma_row=[]
    
    for k in range(len(parameters)):
        link_mu_star_row.append(mu_star_df[parameters[k]].mean())
        link_sigma_row.append(sigma_df[parameters[k]].mean())
    
    mu_star_link_df.loc[links[i],:]=link_mu_star_row
    sigma_link_df.loc[links[i],:]=link_sigma_row
    
    
fig,ax= plt.subplots()
ax.boxplot(mu_star_link_df)
ax.set_xticklabels(parameters,rotation=45)
ax.set_ylabel('mu_star')
plt.title('Distribution of mean mu_star values for each link | Species: '+species)

plt.figure()
mu_star_plot=mu_star_link_df.mean().to_numpy()
sigma_plot=sigma_link_df.mean().to_numpy()
plt.plot(mu_star_plot,sigma_plot,marker='o',ls='')
for i in range(len(parameters)):
    plt.text(mu_star_plot[i],sigma_plot[i],parameters[i])#,rotation=-45)
plt.xlabel('Mu_star')
plt.ylabel('Sigma')
plt.title('Overall Mean values among each link | Species: '+species)

#Map of overall Influence

#Import network to wntr
wn = wntr.network.WaterNetworkModel(inp_file)


#Choose a parameter
parameter='Kb'
plot_var=mu_star_link_df[parameter]

wntr.graphics.plot_network(wn,link_attribute=plot_var)
plt.title('Mu_star for parameter: '+parameter +' based on species: '+species )