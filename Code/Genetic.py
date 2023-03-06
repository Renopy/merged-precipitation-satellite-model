

import pygad
import numpy
import pandas as pd
import Reza
from math import *

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

def fitness_function(Solution , Solution_idx  ):
    out=numpy.array(numpy.dot(Solution,x))
    SE=numpy.sum((y-out)**2)
    MSE=SE/len(y)
    RMSE= MSE**0.5
    CSI = Reza.CSI(Obs=y, Product=out)
    return -RMSE+exp(CSI)


num_generations = 100
num_parents_mating =4

sol_per_pop = 8
num_genes = len(X_train)

init_range_low = -2
init_range_high = 5

parent_selection_type = "sss"
keep_parents = 1

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 20

ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes)
ga_instance.run()


solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("solution_idx : " ,solution_idx)
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=-solution_fitness))


x=X_test
y=Obs_test

out = numpy.array(numpy.dot(solution,x))

r = Reza.correlation(out, y)
rmse=Reza.function_RMSE(Obs=y, Model=out)
nse=Reza.function_Ens(Model=out, Obs=y)
pod=Reza.POD(Obs=y, Product=out)
far=Reza.FAR(Obs=y, Product=out)
bias=Reza.BIAS(Obs=y, Product=out)
csi=Reza.CSI(Obs=y, Product=out)

print(["cor","rmse","nse","pod","far","bias","csi"])
print([ r,    rmse,  nse,  pod,  far,  bias,  csi])




