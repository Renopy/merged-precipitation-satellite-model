# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 10:01:48 2021

@author: reza
"""

import numpy 
import pandas as pd 
import math
from math import *
import random
# import PFA
import Reza
import keras_model
import xlsxwriter

import tensorflow as tf

def Save(W_ , address, Dim):
    
    workbook = xlsxwriter.Workbook(address)
    i_=0
    if Dim==3:
        for w_ in W_ :
            i_+=1
            Sh = numpy.shape(w_)
            worksheet = workbook.add_worksheet(str(i_))
            for J_ in range(Sh[1]):
                worksheet.write(0 ,J_ , "C"+str(J_))
            for I_ in range(Sh[0]):
                for J_ in range(Sh[1]):
                    worksheet.write(I_+1 ,J_ , float(w_[I_,J_]))
    if Dim==2:
        for w_ in W_ :
            i_+=1
            Sh = numpy.shape(w_)
            worksheet = workbook.add_worksheet(str(i_))
            for J_ in range(Sh[0]):
                
                worksheet.write(0 ,J_ , "C"+str(J_) )
                try:
                    worksheet.write(1 ,J_ , float(w_[J_]))
                except:
                    worksheet.write(1 ,J_ ,w_[J_] )
    if Dim==1:
        worksheet = workbook.add_worksheet("sheet")
        for J_ in range(len(W_)):
            worksheet.write(1 ,J_ , float(W_[J_]))
            try:
                worksheet.write(1 ,J_ , float(W_[J_]))
            except:
                worksheet.write(1 ,J_ ,W_[J_] )
    workbook.close()

def order(Ex , Keys):
    Output =[ ]
    for k in Keys :
        List = list(Ex[k])
        
        Output.append(List)
    Order = numpy.transpose(Output)
    return Order

def fitness_function(Solution):
    bias = Solution[-1]
    
    out=numpy.array(numpy.dot(    Solution[0:-1]  , numpy.transpose( x_train)) ) +bias
    #r = numpy.corrcoef( obs_train , out )[0,1]
    #nse  = 1 - ( numpy.sum((out-obs_train)**2) / numpy.sum((obs_train-numpy.mean(obs_train ))**2 ))
    rmse = numpy.mean((out-obs_train)**2)**0.5
    #SE=numpy.sum((y-out)**2)
    #MSE=SE/len(y)
    #RMSE= MSE**0.5
    # Th = 1
    
    # csi = Reza.CSI(Obs=obs_train , Product=out ,threshold=Th)
    return rmse

def evaluation_criteria(Obs , Model  , interval=None) :
    nse  = 1 - ( numpy.sum((Model-Obs)**2) / numpy.sum((Obs-numpy.mean(Obs ))**2 ))
    rmse = numpy.mean((Obs-Model)**2)**0.5
    mbe  = numpy.mean( Model - Obs)
    mae = numpy.mean( numpy.absolute( Model - Obs))
    pbias =  100*numpy.sum(Model-Obs)/numpy.sum(Obs) 
    kge ,r, alpha ,beta = he.evaluator(he.kge, Model, Obs)
    pod = POD(Obs , Model)
    far = FAR(Obs , Model)
    bias = BIAS(Obs , Model)
    csi = CSI(Obs , Model)
    spearman = sci.spearmanr(Obs , Model)[0]
    Dc , D  = Kolomogrov_smirnov(Obs , Model , interval)
    return   { 'correlation' : r[0]  , 'NSE' : nse ,
              "RMSE" : rmse ,"MAE" : mae, 'MBE'  : mbe , 
              'PBIAS' : pbias,
              'KGE' : kge[0]  ,'spearman':spearman, 'POD' : pod , 'FAR' : far , 'BIAS': bias  , 'CSI' : csi , 'KS' : Dc/D}  

def CSI(Obs,Product,threshold):
    Product = Float(Product)
    Obs = Float(Obs)
    N=len(Obs)
    F=0.0
    H=0.0
    M=0.0
    Th=threshold
    for i in range(N):
        O=float(Obs[i])
        P=float(Product[i])
        if O>=Th and P>=Th :  H=H+1
        if O<Th and P>=Th :   F=F+1
        if O>=Th and P<Th :   M=M+1
    try:
        csi=(H)/(H+M+F)
    except:
        csi="Undefined"
    return csi

def feed_forward(X,W,B):
    number_of_layers = len(W)
    Xa=X
    for i in range(number_of_layers):
        h = numpy.dot(Xa,numpy.array(W[i]))+B[i]
        if i!= number_of_layers-1:
             # Xa = numpy.tanh(h)
             Xa = numpy.maximum(h,0)
        else :
            Xa = h
    M =[]
    for i in range(len(Xa)):
        M.append(Xa[i,0] ) #+B[-1][0]
    return M

       
def my_loss(model,obs):
    ecsi = exp(CSI(obs,model,0.1))
    L = (tf.square(obs-model))**0.5 - ecsi
    return tf.reduce_mean(L, axis=-1)  

type = 'ANN'

model_name = 'ANN_1_new'

saving ='yes'
  

if type ==  'ANN':
    number_of_layers = 10
    n_neo_between = (40,50)
    size_batch = 500
    n_epoch = 50
    act_func = 'relu'
    LOSS = my_loss
    ord_keys =[  'PWV' ,   'IMERG' ]          

      
if type ==  'MLR':
    ord_keys =[  'TPW' ,   'IMERG'  ]          
    IT = 3000
    IT2 = 12000


train_file ='H:/payan_name/AMSR2-TPW/Cal-test/calibration_4.xlsx'
Test_file = 'H:/payan_name/AMSR2-TPW/Cal-test/test_resampled_data.xlsx'
result_path = 'H:/ANN_output/'+model_name+'.xlsx'

# Excel = { }
# Excel['train']= pd.read_excel(train_file)
# Excel['test']= pd.read_excel(Test_file )


Keys = pd.DataFrame.keys(Excel['train'] )
shape = ( len(Keys) , len(Excel['train']) )

Train={ }
Train_data = Excel['train'].values
# Train["X"] = Train_data[:,1:shape[0]]

Train["X"] = order( Excel['train'] , ord_keys)
Train["O"] =  numpy.array(Excel['train']['rrr'])


Test = {}
Test_data = Excel['test'].values
Test["X"] = order( Excel['test'] , ord_keys)
Test["O"] = numpy.array(Excel['test']['rrr'])


Train["mean"]=numpy.zeros(len(ord_keys))
Train["std"]=numpy.zeros(len(ord_keys))
Train["max"]=numpy.zeros(len(ord_keys))
Train["min"]=numpy.zeros(len(ord_keys))
for i in range(len(ord_keys)):
    Train["mean"][i]=numpy.mean(Train["X"][:,i]) 
    Train["std"][i]=numpy.std(Train["X"][:,i])
    Train["max"][i]=numpy.max(Train["X"][:,i]) 
    Train["min"][i]=numpy.min(Train["X"][:,i]) 

Train["X"] = (Train["X"] - Train["mean"]) / Train["std"]
Test["X"] = (Test["X"] - Train["mean"]) /  Train["std"]


x_train  = Train["X"]
obs_train = Train["O"]




num_of_param = len(x_train[0])+1


if type== "MLR" : 
    
    solution  , Loss  = PFA.PFA_fit(  fitness_function  , num_of_param   , IT  , IT2 , 1,2 )

    bias = solution[-1]
    
    Model= numpy.array(numpy.dot(    solution[0:-1]  , numpy.transpose( Test["X"])) ) +bias
    for i in range(len(Model)):
        Model[i] = max(Model[i] , 0 )
        
    Obs = Test["O"]
    result = evaluation_criteria(Obs , Model )
    print(result)
    
    Loss =pd.DataFrame(numpy.array(Loss))
    Loss.to_excel('E:\Precipitaion Climates\Data\Cal_Test/result/result_'+'Convergin_curve_'+model_name+'.xlsx')
    
    ans = pd.DataFrame(numpy.array( [ ord_keys , solution , Train["mean"] ,Train["std"]] )) 
    ans.to_excel('E:\Precipitaion Climates\Data\Cal_Test/result/result_'+'solution_'+model_name+'.xlsx')

elif type == 'ANN':
        
    result , Model , predicted , W  , bias = keras_model.ANN(Train_x = Train["X"]  , Train_obs =Train["O"]  ,
                 Test_x = Test["X"] , Test_obs = Test["O"] 
                 ,n_layer=number_of_layers , n_neorons=n_neo_between, batch=size_batch , epoch=n_epoch ,
                 loss_func=LOSS ,  ki ="random_uniform" , act=act_func  )
    w_out_path = 'E:\Precipitaion Climates\Data\Cal_Test/result/W_'+model_name+'.xlsx'
    
    Save(W_ =W , address = w_out_path, Dim=3)
    
    b_out_path = 'E:\Precipitaion Climates\Data\Cal_Test/result/Bias_'+model_name+'.xlsx'
    Save(W_ =bias, address =b_out_path , Dim=2)
    print(result)

if type=='ANN' and saving=='yes':
    Ex = Excel['train']
    geo_train =feed_forward(Train['X'] ,W,bias)
    geo_train = numpy.array(geo_train)  
    try:
        del(Ex[model_name])
    except:
        pass
    Keys = pd.DataFrame.keys( Ex)
    Ex.insert(len(Keys),model_name,geo_train,True)
    Ex.to_excel(Train_file)    
        
    
    Ex = Excel['test']
    geo_test =feed_forward(Test['X'] ,W,bias)
    geo_test = numpy.array(geo_test)  
    try:
        del(Ex[model_name])
    except:
        pass
    Keys = pd.DataFrame.keys( Ex)
    Ex.insert(len(Keys),model_name,geo_test,True)
    Ex.to_excel(Test_file)





# R = [result]
# for st in names: 
#     print(st)
#     Input_Excel = 'E:\Precipitaion Climates\Data\Cal_Test\stations/Complete_Test_'+st+'.xlsx'
#     Excel['test']= pd.read_excel(Input_Excel)
#     Ex = Excel['test']
#     Test = {}
#     Test_data = Excel['test'].values
        
#     Keys = pd.DataFrame.keys( Excel['test'])
    
#     shape = ( len(Keys) , len( Excel['test'] ))
             
#     Test["X"] =  order( Excel['test'] , ord_keys)
    
#     Test["O"] = numpy.array(Excel['test']['rrr24'])
    
#     Test["X"] = (Test["X"] - Train["mean"]) / Train["std"]
    
#     if type == 'MLR':
#         Model=numpy.array(numpy.dot( solution[0:-1]  , numpy.transpose( Test["X"])) ) +bias
#         for i in range(len(Model)):
#             Model[i] = max(Model[i] , 0 )
#     elif type=='ANN':
#         Model = feed_forward(X=  Test["X"]  ,W = W ,B=bias)
        
#     Obs = Test["O"]
#     result = evaluation_criteria(Obs , Model )
#     result["station"] = st
#     R.append(result )
    
#     if type=='ANN' and saving=='yes':

#         geo_test =feed_forward(Test['X'] ,W,bias)
#         geo_test = numpy.array(geo_test)
#         try:
#             del(Ex[model_name])
#         except:
#             pass
#         Keys = pd.DataFrame.keys( Excel['test'])
#         Ex.insert(len(Keys),model_name,geo_test,True)
#         Ex.to_excel(Input_Excel)

# R =pd.DataFrame(R)

# R.to_excel(result_path)
      

      
      
