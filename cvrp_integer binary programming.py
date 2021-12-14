# -*- coding: utf-8 -*-
import numpy as np
import xlrd

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


distance = excel2m("distance.xls")
demand = excel2m("demand.xls")


n = 8  # numbre of clients
M = 4  # number of vehicles
N = [i for i in range(1, n+1)]
V = [0] + N
A = [(i, j) for i in V for j in V if i != j]
c = {(i, j): distance[i,j] for i, j in A}
Q = 15
q = {i: demand[0,i-1] for i in N}

from gurobipy import Model, GRB, quicksum
mdl = Model('CVRP')

x = mdl.addVars(A, vtype=GRB.BINARY) 
u = mdl.addVars(N, vtype=GRB.CONTINUOUS)

mdl.modelSense = GRB.MINIMIZE
mdl.setObjective(quicksum(x[i, j]*c[i, j] for i, j in A))

mdl.addConstrs(quicksum(x[i, j] for j in V if j != i) == 1 for i in N)
mdl.addConstrs(quicksum(x[i, j] for i in V if i != j) == 1 for j in N)
mdl.addConstrs(quicksum(x[i, j] for j in N) <= M for i in [0])
mdl.addConstrs(quicksum(x[i, j] for i in N) <= M for j in [0])
mdl.addConstrs((x[i, j] == 1) >> (u[i]+q[j] == u[j]) for i, j in A if i != 0 and j != 0)
mdl.addConstrs(u[i] >= q[i] for i in N)
mdl.addConstrs(u[i] <= Q for i in N)

mdl.Params.MIPGap = 0.1
mdl.Params.TimeLimit = 30
mdl.optimize()


print("Obj:", mdl.objVal)
for v in mdl.getVars():
    print('Var', v.varName, '=', v.x)


















