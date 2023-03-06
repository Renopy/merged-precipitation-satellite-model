

import Harmony_Search_Majol_main as HS

HS.Harmony_search(
input_name='E:/payan_name/AMSR2-TPW/Cal-test/calibration_1.xlsx',
model_type="a*x+b",
method="Standard",
loss_type="RMSE-exp(CSI)",
Maximum_HMS=5,
HMCR=0.8,
PAR=0.7,
pitch=0.1,
it_1=20,
it_2=100,
it_3=20,
Initial_Search_limit=(-2,2)
)




def HS(  loss_function , number_of_parametrs , HMCR , PAR  , iteration ) : 
    
    
    



# import Reza
# import numpy
# from math import *
# import pandas as pd

# G = pd.read_excel("Cal-test\Observation.xlsx")
# List = list(G["Observation"])
# X = Reza.Float(List)

# α , β = Reza.Gamma_dis_param(X)
# print("α ,β = " , α ,β)
# Γα=Reza.Gamma(α)
# e=exp(1)
# gz = lambda x : ( 1/ (β**α *Γα ) )*x**(α-1)*e**(-x/β)
# P=0.3
# dz=0.01
# z=0.001
# p=0.0
# while p<P:
#     z=z+dz
#     p= p+Reza.Integral(Range=(z-dz,z), f=gz, dx=dz)
# print(z)

# import numpy
# import pandas as pd 
# import Reza
# Input="cal-test\+test_4.xlsx"
# ex = pd.read_excel(Input)
# E=numpy.array(ex)
# Keys =list(pd.DataFrame.keys(ex))
# Shape = numpy.shape(ex)
# X= [Keys]
# for i in range(Shape[0]):
#     ray=0
#     for k in Keys:
#         if ex[k][i]<1000 and ex[k][i]>-1000:
#             ray+=1
#     if ray==len(Keys): 
#         X.append(E[i])
# X=numpy.array(X)
# Reza.Mat_Write(X,Input)


