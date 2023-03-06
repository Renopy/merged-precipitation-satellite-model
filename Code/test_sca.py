
import numpy
import pandas as pd
import Reza
from math import *
import random 

Train_data = 'E:/Temperature/Data/Cal_Test/Temp_cal_1.xlsx'
Test_data = 'E:/Temperature/Data/Cal_Test/Temp_test_1.xlsx'
IT=1000

def List_with(Len,value):
    L=[]
    for i in range(Len):
        L.append(value)
    return L

def put_in_array(DB):
    X=[]
    Keys = pd.DataFrame.keys(DB)
    Obs = list(DB[Keys[0]])
    for i in range(1,len(Keys)):
        X.append(list(DB[Keys[i]]))
    List_1 = List_with(Len=len(Obs),value=1.0)
    X.append(List_1)
    X=numpy.array(X)
    return (X,Obs)

Input_Excel =  Train_data
Ex_train = pd.read_excel(Input_Excel)
Keys = pd.DataFrame.keys(Ex_train)
X_O_train = put_in_array(DB=Ex_train)
print(Keys)
X_train = X_O_train[0]
Obs_train = X_O_train[1]

Means=[]
STD = []
for i in range(1,len(Keys)):
    ave = numpy.mean(Ex_train[Keys[i]])
    std = numpy.std(Ex_train[Keys[i]])
    Means.append([ave])
    STD.append([std])

Means.append([0])
STD.append([1])
Means=numpy.array(Means)
STD=numpy.array(STD)

Input_Excel = Test_data
Ex_test = pd.read_excel(Input_Excel)
X_O_test = put_in_array(DB=Ex_test)

X_test = X_O_test[0]
Obs_test = X_O_test[1]

X_train = (X_train-Means)/STD
X_test = (X_test-Means)/STD

x=X_train
y=Obs_train

def fitness_function(Solution ):
    out=numpy.array(numpy.dot(Solution,x))
    SE=numpy.sum((y-out)**2)
    MSE=SE/len(y)
    RMSE= MSE**0.5
    #CSI = Reza.CSI(Obs=y, Product=out,threshold=0.1)
    return RMSE


import SCA_orginal


number_of_parameters= len(x)
LB=-2
UB=2

SearchAgents_number=1
P=SCA_orginal.SCA(fitness_function,LB,UB,number_of_parameters,SearchAgents_number,IT)

print(P,fitness_function(P))

x=X_test
y=Obs_test

out = numpy.array(numpy.dot(P,x))

r = Reza.correlation(out, y)
rmse=Reza.function_RMSE(Obs=y, Model=out)
nse=Reza.function_Ens(Model=out, Obs=y)
pod=Reza.POD(Obs=y, Product=out,threshold=0.1)
far=Reza.FAR(Obs=y, Product=out,threshold=0.1)
bias=Reza.BIAS(Obs=y, Product=out,threshold=0.1)
csi=Reza.CSI(Obs=y, Product=out,threshold=0.1)

print(["cor","rmse","nse","pod","far","bias","csi"])
print([ r,    rmse,  nse,  pod,  far,  bias,  csi])







