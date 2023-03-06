



import Reza
import numpy
import random
from math import *
import math
import sys
import xlsxwriter


input_name = "calibration_5.xlsx"
Input = Reza.Matread(input_name)

method = "Standard"
# method = "Orginal"

it_1 = 10000
it_2 = 20
it_3 = 100
it_4 = 20
it_5 = 50
Maximum_HMS = 7
HMCR = 0.3
PAR  = 0.2
δ    = 0.1

infinity = 99999999999999999999


def _Model_F(V,Coef):
    Modeled = numpy.zeros(len(V[0]))
    for jj in range(len(V)) :
        Modeled= Modeled + numpy.array(V[jj])*Coef[jj]
    Modeled = Modeled + Coef[-1]
    return list(Modeled)
def Sort_F(Harmony_Memory,size)   :   
    Sorted=[]
    for i in range(size):
        Sorted.append(Harmony_Memory[len(Harmony_Memory)-i-1])
    return Sorted

def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" %
                   (prefix, "|"*x, "."*(size-x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()

def False_Alaram_Average(Obs,Model):
    List_of_false_alarm = []
    Th=0.1
    for i in range(len(Obs)):
        if Obs[i]<=Th and Model[i]>Th:
            List_of_false_alarm.append(Model[i])
    if len(List_of_false_alarm) == 0 :
        FAA = infinity
    else : 
        FAA = sum(List_of_false_alarm)/(len(List_of_false_alarm))
    return FAA

infinity = 99999999999999999999

Input = list(Input)
variables = list(Input[0])
variables.pop(0)
Input.pop(0)
Input_tr = numpy.transpose(Input)

Obs = list(Input_tr[0])
Obs = Reza.Float(Obs)

Predictors = [ ]
for pre in range(1,len(variables)+1):
    Predictors.append(Reza.Float(list(Input_tr[pre])))

Means=[]
stdv=[]
a=[]

for i in range(len(Predictors)):
    μ=sum(Predictors[i])/len(Predictors[i])
    σ=numpy.std(Predictors[i])
    Means.append(μ)
    stdv.append(σ)
    if method == "Standard" :
        Predictors[i]=(numpy.array(Predictors[i])-μ)/σ


Cof= list(numpy.zeros(len(Predictors)+1))
Predictors=numpy.array(Predictors)

print("Means=" , Means)
print("stdv=" , stdv)

Loss_opt=1000
Loss_list= [ ]
Memory = []
print('HM creation')
for k in range(it_1):
    print(k,end="\r")
    for i in range(len(Cof)): 
        Cof[i]= random.randint(-2, 2)*random.random()
    Model = _Model_F(V= Predictors , Coef= Cof)
   # Li= (numpy.array(Model)-numpy.array(Obs))**2
    # loss= (sum(list(Li))/float(len(Li)))**0.5
    try:
        Li= (numpy.array(Model)-numpy.array(Obs))**2
        loss = (sum(list(Li))/float(len(Li)))**0.5-exp(Reza.CSI(Obs,Model))
    except:
        loss = infinity
    if loss < Loss_opt:
        print("loss :"  , loss )
        print(Cof)
        Loss_opt = loss
        Memory.append( list(Cof) )
        Loss_list.append(loss)

Memory = Sort_F(Memory, size=Maximum_HMS)
Memory_2 = []
print("\n---------Harmony Memory Considration Rule---------\n")

for I in range(len(Memory)):
    Cof = Memory[I]
    print("I = " , I)
    for it in range(it_2):
        ran_1 = random.random()
        if ran_1 > HMCR :
            for i in range(len(Cof)):
                for itt in range(it_3):
                    short_term_memory = Cof[i]
                    Cof[i] = random.random()*random.randint(-2,2)
                    Model = _Model_F( V= Predictors , Coef= Cof)
                    # Li= (numpy.array(Model)-numpy.array(Obs))**2
                    # loss= (sum(list(Li))/float(len(Li)))**0.5
                    try:
                        Li= (numpy.array(Model)-numpy.array(Obs))**2
                        loss = (sum(list(Li))/float(len(Li)))**0.5-exp(Reza.CSI(Obs,Model))
                    except:
                        loss = infinity

                    if loss < Loss_opt:
                        print("loss :"  , loss )
                        print(Cof)
                        Loss_opt = loss
                        Memory_2.append( list(Cof) )
                        Loss_list.append(loss)
                    if loss >= Loss_opt:
                        Cof[i] = short_term_memory

if len(Memory_2)< Maximum_HMS :
    Memory_2 = Sort_F(Memory_2,size=len(Memory_2))
else :
    Memory_2 = Sort_F(Memory_2,size=Maximum_HMS)

Memory = Memory_2+Memory
Memory_2 = []

print("\n-------Harmony Memory Pitch Adjustment Rule---------\n")

for I in range(len(Memory)):
    Cof = Memory[I]
    print( "I = " , I )
    for it in range(it_4):
        for i in range(len(Cof)):
            ran_2 = random.random()
            if ran_2 > PAR :
                for itt in range(it_5):
                    short_term_memory = Cof[i]
                    Cof[i] = Cof[i] + random.random()*random.choice([-1,1])*δ
                    Model = _Model_F(V= Predictors , Coef= Cof)
                    # Li= (numpy.array(Model)-numpy.array(Obs))**2
                    # loss= (sum(list(Li))/float(len(Li)))**0.5
                    try:
                        Li= (numpy.array(Model)-numpy.array(Obs))**2
                        loss = (sum(list(Li))/float(len(Li)))**0.5-exp(Reza.CSI(Obs,Model))
                    except:
                        loss = infinity
                    if loss < Loss_opt:
                        print("loss :"  , loss )
                        print(Cof)
                        Loss_opt = loss
                        Memory_2.append( list(Cof) )
                        Loss_list.append(loss)
                    if loss >= Loss_opt:
                        Cof[i] = short_term_memory
    



if len(Memory_2)< Maximum_HMS :
    Memory_2 = Sort_F(Memory_2,size=len(Memory_2))
else :
    Memory_2 = Sort_F(Memory_2,size=Maximum_HMS)

Memory = Memory_2


print( "Cof = " , Memory[0])

txt_file = open(input_name+"HS.txt" , "w")
txt_file.write("Cof=")
txt_file.write(str(Memory[0]))
txt_file.write("\nMeans=")
txt_file.write(str(Means))
txt_file.write("\nstdv=")
txt_file.write(str(stdv))
txt_file.close()

import xlsxwriter

workbook = xlsxwriter.Workbook(input_name+"loss_list.xlsx")
worksheet = workbook.add_worksheet()
for i in range(len(Loss_list)):
    worksheet.write( i , 0, Loss_list[i])
workbook.close()


