### Documentation

*Documentation_Function_Uses_and_Examples.ipynb* contains a list of all functions developed for MSXPY, including function inputs/outputs, and usage examples. 

### Getting Started - Examples
*Example1_Run_Model_Example.ipynb* contains an initial example demonstrating importing an epanet model and msx file, executing a model simulation, and extracting model results
<br>
<br>
*Example2_Parallel.py* contains an example showing how to use python's multiprocessing module. This example does not utilize epanet models, but the multiprocessing framework is implemented in subsequent scripts which require model evaluations.

### Executing a Sensitivity Analysis

The implementation of the Method of Morris requires two main steps: (1) model evaluations and (2) analysis. In the python scripts included, the evaluation and analysis portions are split into seperate notebooks/scripts. The model evaluation portion saves all model results to a pickle file, which is then read by the analysis script. The advantage of this approach is that evaluating the models can take considerable time, so saving results to a pickle file enables the user to re-use previous model simulations.

Depending on the phase of the species in the MSX model, either a batch reactor model, or the full hydraulic model, is necessary. The batch reactor is appropriate if all species in the reaction scheme are present in the bulk phase only. The Model analysis (running multiple simulations in a hydraulic network) is required if there are species present in the wall phase.

**If All Species are in the Bulk Phase**

1. Execute model evaluations using either *Batch_Morris_Run.ipynb* or *Batch_Morris_Run_Parallel.py*. If using your own reaction scheme, use *Batch_Morris_Run_Parallel_TEMPLATE.py* and fill in the blanks in the template according to your model/reaction scheme. If you used *Batch_Morris_Run_Parallel_TEMPLATE.py*, note that your simulation results will be saved as a pickle file. 
2. Evaluate metrics of sensitivity based on Morris Method using *Batch_Morris_Analyze.ipynb*. If you crated a new pickle file with model results, change the location and file name of the variable <code>pickle_file_beaker</code> within Batch_Morris_Analyze.ipynb.

Note: The "Batch_Morris_Run.ipynb" and "Batch_Morris_Run_Parallel.py" produce the same results. The jupyter notebook (.ipynb file) is present to demonstrate the process of executing model evaluations. However, due to incompatabilities between the multiprocessing python module and jupyter notebook, the model evaluations are executed in serial. For faster computation time, use "Batch_Morris_Run_Parallel.py" which uses the multiprocessing module to evaluate epanetmsx models in parallel.

**If Any Species are in the Wall Phase**
1. Execute model evaluations using *Model_Morris_Run_Parallel.py*. If using your own reaction scheme, use *Model_Morris_Run_Parallel_TEMPLATE.py* and fill in the blanks in the template according to your model/reaction scheme. If you used *Model_Morris_Run_Parallel_TEMPLATE.py*, note that your simulation results will be saved as a pickle file. 
2. Evaluate metrics of sensitivity based on Morris Method using *Model_Morris_Analyze.ipynb*. If you crated a new pickle file with model results, change the location and file name of the variable <code>pickle_file_model</code> within Model_Morris_Analyze.ipynb.
