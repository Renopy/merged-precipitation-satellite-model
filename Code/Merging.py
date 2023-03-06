import numpy
import Reza
import math
from math import *

from random import random
import xlsxwriter
import pandas as pd

method = "Standard"
# method = "Orginal"
Type = "linear"
Cof=[-0.19184615,  1.1046    ,  0.5725    ,  0.7804    ,  0.2952 ,0.2092   ]
Input_path = "cal-test\+test_5.xlsx"
Means= [ 15.85287714786201, 0.2962461902977852, 0.492772146900091, 0.9676023936574198, 0.8973076416804204]
stdv= [ 10.18351587392609, 1.573247121755517, 2.552500992781016, 4.566859118593261, 3.0678025262247117]


def MSE(M,obs):
    L=0.0
    Li=[]
    for i in range(len(M)):
        Li.append((M[i]-obs[i])**2)
        L = L+ (M[i]-obs[i])**2
    L=L/float(len(M))
    return L

def functions(Model , Obs):
    r = Reza.correlation(Obs,Model)
    rmse = Reza.function_RMSE(Obs,Model)
    nse = Reza.function_Ens(Model,Obs)

    pod = Reza.POD(Obs,Model)
    far = Reza.FAR(Obs, Model)
    bias= Reza.BIAS(Obs,Model)
    return [r , rmse , nse , pod , far ,bias]



def Model_fx(Predictors,a,b):
    M=[ ]
    for i in range(len(Predictors[0])):
        fx=0
        for j in range(len(Predictors)):
            fx = fx +  a[j]*log(abs(b[j]*Predictors[j][i])+1)
        fx= fx- Sensivity

        if fx < 0.1 :
            M.append(0)
        else :
            M.append(fx)
    return M

Input = pd.read_excel(Input_path)
Keys = list(pd.DataFrame.keys(Input))


Obs = list(Input[Keys[0]])
Obs = Reza.Float(Obs)

variables = Keys
variables.pop(0)
print(variables)



Predictors = [ ]
for pre in variables:
    Predictors.append(Reza.Float(list(Input[pre])))


if Type == "linear":
    Model=[]
    bias=Cof[-1]
    for i in range(len(Obs)):
        fx=0
        for j in range(len(Cof)-1):
            if method == "Standard" :
                value=  (float(Predictors[j][i])- Means[j])/stdv[j]
            if method == "Orginal":
                value=  float(Predictors[j][i])
            fx = fx +  Cof[j]*value
        fx = fx+ bias
        if fx<0:
            Model.append(0)
        if fx>=0:
            Model.append(fx)

if Type == "nonlinear":
    Predictors= numpy.array(Predictors)
    P = []
    for i in range(len(Predictors)):
        L = numpy.array(Predictors[i])
        P.append( 
            list(
                ( (L)- Means[i]) /stdv[i] ) 
                ) 
    Model = Model_fx(P,a,b)


loss = sqrt(MSE(Model,Obs))
print("loss = " ,loss)

X= [ Obs , Model]
X= numpy.array(X)
X=numpy.transpose(X)
Reza.Mat_Write( X ,Input_path+"_"+Type+"_"+"Obs,Merg.xlsx")

List_criteria = [  "r" , "rmse" , "nse" , "pod" , "far" ,"bias", "predictors"]
List_out = functions(Model, Obs) 
List_out.append("Model")
result = [ List_criteria ]

for j in range(len(Predictors)):
    
    Lo = functions(Predictors[j],Obs)
    Lo.append(variables[j])
    result.append(Lo)
result.append(List_out)
result=numpy.array(result)
result=numpy.transpose(result)
Reza.Mat_Write(result,Input_path+"_"+Type+"_"+"Result_Merg.xlsx")

