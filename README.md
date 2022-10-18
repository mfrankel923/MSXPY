# MSXPY
 **IN DEVELOPMENT** This library of functions and examples is currently under development </br>
 Set of functions and code to execute EPANET MSX models in Python, and conduct sensitivity analyses
 
 ### Overview
 
This library of functions enables users to execute water quality models within a water distribution system using EPANET MSX, through a wrapper with python. In addition, this repository contains a jupyter notebook and analygous python script to execute sensitivity analyses to determine the relative level of influence of each chemical parameter in a reaction scheme. 

The contents of this repository are as follows:
<br> 
-[EPANET_DLLs](https://github.com/mfrankel923/MSXPY/tree/main/EPANET_DLLs) contains the dynamic link libraries for epanet (version 2.0) and epanetmsx (version 1.1)
<br>
-[Function_Lbraries](https://github.com/mfrankel923/MSXPY/tree/main/Function_Libraries) which contains python wrappers for DLL functions, and additional functions for manipulation of EPANET MSX models within python
<br>
-[INP_and_MSX_Files](https://github.com/mfrankel923/MSXPY/tree/main/INP_and_MSX_Files) contains example epanet .inp and .msx files
<br>
-[Examples_and_Templates](https://github.com/mfrankel923/MSXPY/tree/main/Examples_and_Templates) contains Jupyter notebooks and scripts which demonstrate the functionality of this package, as well as provide templates to apply the functions in this package to any particular chemical reaction scheme
Note that the jupyter notebook [Documentation_Function_Uses_and_Examples.ipynb](https://github.com/mfrankel923/MSXPY/blob/main/Examples_and_Templates/Documentation_Function_Uses_and_Examples.ipynb) contains documentation and examples of all functions developed in this package.

### Getting Started

Download the files in this repository and ensure that the necessary package dependencies (listed below) are installed. Execute [Example1_Run_Model.ipynb](https://github.com/mfrankel923/MSXPY/blob/main/Examples_and_Templates/Example1_Run_Model.ipynb) for example of executing an epanet msx model. It is expected that the user has understanding of epanet, epanet msx, and running/editing python code.

### Dependencies

Utilization of this package requires installation of the following python packages:
<br>
-[WNTR](https://wntr.readthedocs.io/en/latest/overview.html)
<br>
-[Matplotlib](https://matplotlib.org/)
<br>
-[NumPy](https://numpy.org/)
<br>
-[pandas](https://pandas.pydata.org/)
<br>
-[SALib](https://salib.readthedocs.io/en/latest/)

### Additional Notes

The sensitivity analysis in this package utilizes a method called the Method of Morris, in which multiple model evaluations are contucted to determine the influence of a model parameter on a model output. The method is described in [Saltelli (2004)](http://www.andreasaltelli.eu/file/repository/SALTELLI_2004_Sensitivity_Analysis_in_Practice.pdf): 
The result of the Method of Morris is a metric Mu_star, which indicates the level of influence of a parameter on a function output, and sigma, which indicates the level of interaction between a paramater and all others. 


### Acknowledgments

This work was supported by the National Science Foundation under Grant 1953206. The authors acknowledge the Texas Advanced Computing Center (TACC) at The University of Texas at Austin for providing high performance computing resources that have contributed to the research results reported in this publication. The authors also acknowledge Samuel Brodfuehrer for consultations during the drafting of this manuscript.
<br> 
<br> 
The python wrapper of msx functions, "msx_toolbox.py" was developed by Junli Hao: https://github.com/junli-h/EPANET-MSX-Python-wrapper/blob/master/epanetmsxmodule.py
<br>
<br> 
The python wrapper of epanetfunctions, "epanet_toolbox.py" was developed by Gal Perelman, Gonçalo Grilo, and Michael Tryby: https://github.com/OpenWaterAnalytics/epanet-python/blob/dev/epanet-module/epamodule.py

### Contact Us

 Matthew Frankel - mfrankel@utexas.edu
 <br> 
 Lina Sela linasela@utexas.edu


