


import numpy
import pandas as pd
import Reza
from math import *
import random 

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

Input_Excel =  "E:/payan_name/AMSR2-TPW/Cal-test/cal_1.xlsx"
Ex_train = pd.read_excel(Input_Excel)
Keys = pd.DataFrame.keys(Ex_train)
X_O_train = put_in_array(DB=Ex_train)

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

Input_Excel = "E:/payan_name/AMSR2-TPW/Cal-test/+test_1.xlsx"
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
    CSI = Reza.CSI(Obs=y, Product=out)
    return RMSE-exp(CSI)

IT=1000
number_of_parameters= len(x)
lv=-2
uv=2
a=10

lb=numpy.array(List_with(Len=number_of_parameters,value=lv))
ub=numpy.array(List_with(Len=number_of_parameters,value=uv))

Loss_opt=10
MEM=[]
for k in range(10):
    solution =[]
    for i in range(number_of_parameters):
        ran= random.randint(lv*10000,uv*10000)/10000.0
        solution.append(ran)
    Loss = fitness_function(solution)
    if Loss<Loss_opt:
        memory= [solution ,Loss]
        Loss_opt=Loss
        MEM.append(solution)

MEM=numpy.array(MEM)
MEM = numpy.transpose(MEM)
for i in range(number_of_parameters):
    lb[i]= min(MEM[i])
    ub[i]= max(MEM[i])

print(memory)
solution = memory[0]
Loss = fitness_function(solution)
print([Loss])

def dic_same_as(List):
    dic={}
    for i in range(len(List)):
        dic[str(i)]=List[i]
    return dic
LOSS=[]
best = dic_same_as(solution)
for it in range(IT):
    print("in itteration" ,it)
    
    for i in range(number_of_parameters):
        for k in range(3):
            
            ran_1 = a-((a*it)/IT)
            ran_2 = 2*3.14*random.random()
            ran_3 = random.randint(-1*10000,1*10000)/10000.0
            ran_4 = random.random()

            if ran_4<=0.5:
                new = solution[i] + ran_1*sin(ran_2)*abs(ran_3*best[str(i)]-solution[i])
            else:
                new = solution[i] + ran_1*cos(ran_2)*abs(ran_3*best[str(i)]-solution[i])
            solution[i] = new
            new_Loss=fitness_function(solution)
            if new_Loss<Loss:
                Loss=new_Loss
                best = dic_same_as(solution)
                LOSS.append(Loss)
                print("Loss =",Loss,"\n"," and solution:",solution )
            
x=X_train
y=Obs_train

out = numpy.array(numpy.dot(best,x))

r = Reza.correlation(out, y)
rmse=Reza.function_RMSE(Obs=y, Model=out)
nse=Reza.function_Ens(Model=out, Obs=y)
pod=Reza.POD(Obs=y, Product=out)
far=Reza.FAR(Obs=y, Product=out)
bias=Reza.BIAS(Obs=y, Product=out)
csi=Reza.CSI(Obs=y, Product=out)

print(["cor","rmse","nse","pod","far","bias","csi"])
print([ r,    rmse,  nse,  pod,  far,  bias,  csi])





