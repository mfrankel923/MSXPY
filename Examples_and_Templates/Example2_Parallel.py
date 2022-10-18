# -*- coding: utf-8 -*-
"""
Created on Tue May 31 11:36:13 2022

@author: Matthew
"""

import time
import multiprocessing as mp
import numpy as np



#Function to be run in parallel
def my_sleep(x):
    print('Hello!')
    time.sleep(1)
    y=x+1
    z=y+1
    # text='The process ID is: '+ str(os.getpid())
    # f=open('file'+str(os.getpid())+'.txt','w')
    # f.write(text)
    # f.close()
    
    return x, y, z

#EVERYTHING YOU DON"T WANT TO BE REPLECATED IN THE SUB-PROCESSES
#NEEDS TO BE GUARDED BY THE if __name__=='__main__': BLOCK!!


if __name__=='__main__':
    

    #n is the number of function evaluations we want to use
    n=7
    
    t1=time.time()
    #Run model in serial
    for _ in range(n):
        x=my_sleep(1)
    t2=time.time()
    print('Serial Time:')
    print(t2-t1)
    
    
    #Get the number of cores to be used in paarallel
    cores=int(np.round(mp.cpu_count()*.85,0))
    
    #Generate input parameter values
    x=np.arange(n)
    t1=time.time()
    #Create multiprocessing pool
    pool=mp.Pool(processes=cores)
    
    #Execute function with input parameters
    y=pool.map(my_sleep,x)
    
    #Close the processors that were used to run the sub-processes
    pool.close()
    pool.join()
    t2=time.time()
    print('Parallel Time:')
    print(t2-t1)
