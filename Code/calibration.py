

import Reza
import math
import numpy
import xlsxwriter
from math import *
import pandas as pd
Input_path  = "Cal-test\cal_pwv.xlsx"
Excell=pd.read_excel(Input_path)

N=len(Excell)
method = "Orginal"
# method = "Orginal"
def MSE(M,obs):
    L=0.0
    Li=[]
    for i in range(len(M)):
        Li.append((M[i]-obs[i])**2)
        L = L+ (M[i]-obs[i])**2
    L=L/float(len(M))
    return L
Keys=list(pd.DataFrame.keys(Excell))
variables=Keys

number_of_variables=len(Keys)
print(number_of_variables)
Var=[]

for v in variables:
    Var.append(Reza.Float(list(Excell[v])))

One = []
for k in range(len(Var[0])):
    One .append(1.00)
Var.append(One)
Var=numpy.array(Var,dtype=float)

Obs=Var[0]

A= numpy.zeros ( (number_of_variables,number_of_variables) , dtype = float)

for i in range(number_of_variables):
    for j in range(number_of_variables):
        A[i,j]= sum(Var[i+1]*Var[j+1] )



A=numpy.array(A,dtype=float)
A=numpy.reshape(A , (number_of_variables,number_of_variables))

print("A=",A)
B=[]
for i in range(1,number_of_variables):
    B.append(sum(Var[0]*Var[i]))
B.append(sum(Var[0]))
B = numpy.array(B)

A_Inv=numpy.linalg.inv(A)
Cof=numpy.dot(A_Inv,B)

print("Cof=",list(Cof))

P_names=[]
for i in range(1,number_of_variables):
    P_names.append(variables[i])
P_names.append("bias")
print(P_names)


# Sensivity 
Model = [ ]
bias = Cof[-1]

for i in range(len(Var[0])):
    fx=0
    for j in range(len(Cof)-1):
        value=  float(Var[j+1][i])
        fx = fx +  Cof[j]*value
    fx = fx+ bias
    Model.append(fx)

loss = sqrt(MSE(Model,Obs))
print(loss , "loss")



OutputFile = Input_path+"_Parameter.xlsx"
workbook2 = xlsxwriter.Workbook(OutputFile)
worksheet2 = workbook2.add_worksheet("Parameter")


worksheet2.write( 1 , 0 , "Cof" )

for i in range(len(variables)-1):
    worksheet2.write( 0 , i+1 , P_names[i] )
    worksheet2.write( 1 , i+1 , Cof[i] )

worksheet2.write( 1 , len(variables) , Cof[-1] )


workbook2.close()

