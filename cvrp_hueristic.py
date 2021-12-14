# -*- coding: utf-8 -*-
import numpy as np
import xlrd
import pandas as pd

def excel2m(path):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0] 
    nrows = table.nrows
    ncols = table.ncols
    datamatrix = np.zeros((nrows, ncols))
    for x in range(ncols):
        cols = table.col_values(x)
        cols1 = np.matrix(cols)
        datamatrix[:, x] = cols1
    return datamatrix

distance = pd.DataFrame(excel2m("distance.xls"))
demand = pd.DataFrame(excel2m("demand.xls"))
D = 15

def f(v,x):
    a = distance.iloc[[x]]
    a_drop = a.drop([x]+v,axis=1)
    if a_drop.empty == False:
        minvalue = min(a_drop.iloc[0])
        idx = a.values.tolist()[0].index(minvalue)
        return idx
    
NV = 4 #number of vehicles
lst=[0]
rst=[0]*NV

for j in range(NV):
    c = 0
    for i in range(9): 
        idx = f(lst,lst[i])
        if isinstance(idx,int):
            c += demand.iloc[0,idx-1]
            if c  < D:              
                lst.append(idx) 
            else:
                break 
        else:
            break  
    rst[j] = [i for i in lst]
#    print(lst)

rst_final = [0]*NV
rst_final[0] = rst[0]
for i in range(1,NV):
    rst_final[i] = [j for j in rst[i] if j not in rst[i-1]]
rst_final[0].remove(0)
for i in range(NV):
    print('vehicle{}:'.format(i+1),rst_final[i])
