

"""------ PathFinderAlg ------"""

import numpy
import pandas as pd
import Reza
from math import *
import random 




def PFA(Train_data , Test_data, IT, IT2  , Th , alpha , beta 
         ):

    
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
    X_train = (X_train-Means)/STD
    if Test_data != None :
        Input_Excel = Test_data
        Ex_test = pd.read_excel(Input_Excel)
        X_O_test = put_in_array(DB=Ex_test)
    
        X_test = X_O_test[0]
        Obs_test = X_O_test[1]
    
    
        X_test = (X_test-Means)/STD
    
    x=X_train
    y=Obs_train
        
        
    def fitness_function(Solution ):
        out=numpy.array(numpy.dot(Solution,x))
        rmse = numpy.mean((out-y)**2)**0.5
        
        #SE=numpy.sum((y-out)**2)
        #MSE=SE/len(y)
        #RMSE= MSE**0.5
        #CSI = Reza.CSI(Obs=y, Product=out,threshold=Th)
        
        return rmse

    num_of_param = len(x)
    sol = numpy.zeros(num_of_param)
    def random_arr(shape,dim,a=0,b=1):
        Arr=numpy.zeros(shape)
        if dim==2:
            for i in range(shape[0]):
                for j in range(shape[1]):
                    Arr[i,j] = random.randint(a*10000, b*10000)/10000
        if dim==1:
            for j in range(shape):
                Arr[j] = random.randint(a*10000, b*10000)/10000
        return Arr
    best_sol= random_arr(num_of_param,1)
    best_fit = fitness_function(sol)
    print(sol)
    
    
    Dict = {}
    Loss={}
    mem=0
    for it in range(IT) :
        sol = random_arr(shape=num_of_param, dim=1)
        fitness = fitness_function(sol)
        if fitness<best_fit :
            mem+=1
            best_fit=fitness
            best_sol=sol
            Dict[str(mem)]=sol
            Loss[str(mem)]=fitness
            print("Solution :",sol)
            print("fitness = ",fitness)
    num_of_mem = len(Dict)
    
    
    best_sol=Dict[str(num_of_mem)]
    best_fit=fitness_function(Dict[str(num_of_mem)])
    
    print(Dict)
    
    
    position={}
    print("---Path finder---")
    
    position["0"]=Dict[str(num_of_mem-1)]
    position["1"]=Dict[str(num_of_mem)]
    
    
    mem=num_of_mem
    
    for it in range(1,IT2):
        print(it,"of",IT2)
        for mem in range(2,num_of_mem+1):
            
            r1=numpy.random.uniform(0, 1, num_of_param)
            r2=numpy.random.uniform(0, 1, num_of_param)
            u1=numpy.random.uniform(-1, 1, num_of_param)
            u2=numpy.random.uniform(-1, 1, num_of_param)
            R1=alpha*r1
            R2=beta*r2
            D=abs(Dict[str(mem)]-Dict[str(mem-1)])
            dif = Dict[str(mem)]-Dict[str(mem-1)]
            r3=numpy.random.uniform(0, 1, num_of_param)
    
            A=u2*exp(-2*it/IT2)
            position[str(it+1)] =  position[str(it)] + 2*r3*(position[str(it)]-position[str(it-1)])+A
            epsilon = (1-it/IT2)*u1*D
            sol = Dict[str(mem)]
            dpos= position[str(it+1)]-sol
            sol =  sol+R1*dif+R2*dpos+epsilon
            fitness=fitness_function(sol)
            if fitness<Loss[str(mem)]:
                Dict[str(mem)] = sol
                Loss[str(mem)] = fitness
            if fitness<best_fit:
                best_sol = sol
                best_fit = fitness
                print("Solution :",sol)
                print("fitness = ",fitness)
            position[str(it)] = best_sol
        position[str(it+1)] = best_sol
    
    P = best_sol
    if Test_data!=None:
        x=X_test
        y=Obs_test
        
        
        print(P)
        out = numpy.array(numpy.dot(P,x))
        Th = 0.1
        r = Reza.correlation(out, y)
        rmse = numpy.mean((out-y)**2)**0.5
        nse= 1 - ( numpy.sum((out-y)**2) /
                numpy.sum((y-numpy.mean(y ))**2 ))
        # pod=Reza.POD(Obs=y, Product=out,threshold=Th)
        # far=Reza.FAR(Obs=y, Product=out,threshold=Th)
        # bias=Reza.BIAS(Obs=y, Product=out,threshold=Th)
        # csi=Reza.CSI(Obs=y, Product=out,threshold=Th)
    
        print("MODEL")
        
        print("cor=" ,  r ,
              "rmse=",  rmse,
              "nse=" ,  nse)
            #   "pod=" ,  pod,
            #   "far=" ,  far,
            #   "bias=",  bias,
            #   "csi=" ,  csi)
        
    return P

W= PFA(Train_data= 'E:/Temperature/Data/Cal_Test/Temp_cal_1.xlsx'
    , Test_data= 'E:/Temperature/Data/Cal_Test/Temp_test_1.xlsx'
    , IT=100
    , IT2=200  , Th=0.1
    , alpha=1 , beta=2 )

print(W)

stations = ["nowshahr", 'omidiyeh (aghajari)', 'orumieh',
            'parsabad', 'quchan', 'rasht', 
            'sabzevar','safiabad', 'sanandaj', 
            'shahrekord', 'tabriz','Ahar',
             'ardebil', 'babolsar', 'baft', 
             'bam','bandar abbas', 'bandare anzali',
             'bandare dayyer','bandare lengeh', 'birjand', 
            'bojnurd', 'bushehr','bushehr',
             'Dogonbadan', 'fasa', 'mianeh', 
             'nehbandan','maravehtappeh', 'ilam',
             'kermanshah','gorgan' , 'isfahan', 
             'kerman', 'yazd' , 'kashan' , 
             'qazvin' ,'tehran(mehrabad)'  , 'zanjan']

             



