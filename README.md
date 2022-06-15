# MSXPY
 **IN DEVELOPMENT** This library of functions and examples is currently under development </br>
 Set of functions and code to execute EPANET MSX models in Python, and conduct sensitivity analyses
 
This library of functions enables users to execute water quality models within a water distribution system using EPANET MSX, through a wrapper with python. In addition, this repository contains a jupyter notebook and analygous python script to execute sensitivity analyses to determine the relative level of influence of each chemical parameter in a reaction scheme. 

The sensitivity analysis in this package utilizes a method called the Method of Morris, in which multiple model evaluations are contucted to determine the influence of a model parameter on a model output. The method is described in Saltelli(2004): http://www.andreasaltelli.eu/file/repository/SALTELLI_2004_Sensitivity_Analysis_in_Practice.pdf
The result of the Method of Morris is a metric Mu_star, which indicates the level of influence of a parameter on a function output, and sigma, which indicates the level of interaction between a paramater and all others. 


Utilization of this package requires installation of the following python packages:
-WNTR
-Matplotlib
-Numpy
-Pandas
-SALib
