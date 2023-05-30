# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 21:22:55 2023

@author: lzhang481
"""
"Noted that partial_corrX is tested,but not partial_corrXY"
import pandas as pd
import pingouin as pg
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
from colorspacious import cspace_converter
import matplotlib.pyplot as plt
# In[2]
temp=cm.get_cmap('seismic');
cmap_mat=temp(np.linspace(0,1,256+256+128))
I1=np.linspace(1,256,64).astype(int)
I2=np.linspace(256,256+128,128).astype(int)
I3=np.linspace(256+128,256+256+128,64).astype(int)
I=np.concatenate([I1,I2,I3])-1
colorPN=ListedColormap(cmap_mat[I,],name='colorPN')
plt.rcParams['font.family'] = 'Times New Roman'
# Set default font size and type
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'Times New Roman'

# Set font size and type for title
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.titlepad'] = 12

# Set font size and type for x and y labels
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.labelpad'] = 8
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
def partial_corrXY(
    data,
    x,
    y,
    covar,
    alternative="two-sided",
    method="pearson",
):
    ############In case there is object (factorized variables) in covariate, transfer into binary variables
    ############For example, if 'height' variables include 3 levels of: low, medium, high, this columns would be transfer
    ####in to three columns 'height_low','height_medium','height_high'
    gummyNeed=data[covar].select_dtypes(['object']).columns
    if len(gummyNeed)>0:
       covar = list(pd.get_dummies(data[covar], columns=gummyNeed).columns)
       data = pd.get_dummies(data, columns=gummyNeed)
       #print(covar)
   ############In case there is object (factorized variables) in covariate, transfer into binary variables
   ############For example, if 'height' variables include 3 levels of: low, medium, high, this columns would be transfer
   ####in to three columns 'height_low','height_medium','height_high'

       
    nan_r = np.full((len(x), len(y)), np.nan)
    nan_p = nan_r
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            if xi!=yj:
                temp=pg.partial_corr(data=data,x=xi,y=yj,covar=covar,alternative=alternative,method=method)
                nan_r[i,j]=temp.r
                nan_p[i,j]=temp['p-val']
            else:
                continue
    OutputR=pd.DataFrame(nan_r,index=x,columns=y);
    OutputP=pd.DataFrame(nan_p,index=x,columns=y);       
    return OutputR, OutputP

def partial_corrX(
    data,
    x,
    covar,
    alternative="two-sided",
    method="pearson",
):
    nan_r = np.full((len(x), len(x)), 0.0)
    nan_p =nan_r+1
   ############In case there is object (factorized variables) in covariate, transfer into binary variables
   ############For example, if 'height' variables include 3 levels of: low, medium, high, this columns would be transfer
   ####in to three columns 'height_low','height_medium','height_high'
    gummyNeed=data[covar].select_dtypes(['object']).columns
    if len(gummyNeed)>0:
       covar = list(pd.get_dummies(data[covar], columns=gummyNeed).columns)
       data = pd.get_dummies(data, columns=gummyNeed)
       #print(covar)
    ############In case there is object (factorized variables) in covariate, transfer into binary variables
    ############For example, if 'height' variables include 3 levels of: low, medium, high, this columns would be transfer
    ####in to three columns 'height_low','height_medium','height_high'
    #print(nan_p)
    for i, xi in enumerate(x):
        print(i)
        for j, xj in enumerate(x):
            if j > i:
              #print(xj)
                temp=pg.partial_corr(data=data,x=xi,y=xj,covar=covar,alternative=alternative,method=method)
                nan_r[i,j]=temp['r']
                nan_p[i,j]=temp['p-val']
                nan_r[j,i]=nan_r[i,j]
                nan_p[j,i]=nan_p[i,j]
            else:
                continue

    #print(nan_r)
    #print(nan_p)
    OutputR=pd.DataFrame(nan_r,index=x,columns=x)
    OutputP=pd.DataFrame(nan_p,index=x,columns=x)
    return OutputR, OutputP



def corrX(
    data,
    x,
    alternative="two-sided",
    method="pearson",
):
    nan_r = np.full((len(x), len(x)), 0.0)
    nan_p =nan_r+1
   ############In case there is object (factorized variables) in covariate, transfer into binary variables
   ############For example, if 'height' variables include 3 levels of: low, medium, high, this columns would be transfer

    for i, xi in enumerate(x):
        #print(xi)
        for j, xj in enumerate(x):
            if j > i:
              #print(xj)
                d1=data[xi].values
                d2=data[xj].values
                temp=pg.corr(x=d1,y=d2,alternative=alternative,method=method)
                nan_r[i,j]=temp['r']
                nan_p[i,j]=temp['p-val']
                nan_r[j,i]=nan_r[i,j]
                nan_p[j,i]=nan_p[i,j]
            else:
                continue

    #print(nan_r)
    #print(nan_p)
    OutputR=pd.DataFrame(nan_r,index=x,columns=x);
    OutputP=pd.DataFrame(nan_p,index=x,columns=x);       
    return OutputR, OutputP


