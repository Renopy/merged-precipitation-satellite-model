from tensorflow.keras.metrics import RootMeanSquaredError 

import keras 
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow import keras

import pandas as pd
import numpy

def ANN(Train_x , Train_obs ,
        Test_x , Test_obs  ,
        n_layer , n_neorons, 
        batch=256 , epoch=100 ,
        loss_func='mse' ,  ki ="GlorotNormal" , act="tanh" ):
    
    "random_uniform"
    "GlorotNormal"
    
    import random
    n1= n_neorons[0]
    n2 = n_neorons[1]
    n_of_neurons = random.randint(n1,n2)

    Model=Sequential()
    
    Shape_inp = numpy.shape(Train_x)
    Model.add(Dense(units=n_of_neurons, input_dim=Shape_inp[1], kernel_initializer=ki
                    , activation=act))
    for i in range(n_layer):
        n_of_neurons =random.randint(n1,n2)
        
        Model.add(Dense(units=n_of_neurons,kernel_initializer=ki, activation=act))
    
    Model.add(Dense(units=1,kernel_initializer=ki))
    
    Model.compile(optimizer="adam",loss= loss_func ,metrics=[RootMeanSquaredError()])
    
    Model.fit(Train_x,Train_obs,batch_size=batch,epochs=epoch)
    
    
    reshape = len(Test_obs)
    modelprediction = Model.predict(Test_x)
    
    W =[]
    Bias=[]
    for layer in Model.layers:
        weights = layer.get_weights()
        W.append(weights[0])
        Bias.append(weights[1])

    
    modelprediction = modelprediction.reshape(reshape)
    
    corr = numpy.corrcoef(modelprediction , Test_obs)[0,1]
    
    nse  = 1 - ( numpy.sum((modelprediction-Test_obs)**2) /
                numpy.sum((Test_obs-numpy.mean(Test_obs ))**2 ))
    
    rmse = numpy.mean((Test_obs-modelprediction)**2)**0.5
    mbe  = numpy.mean( Test_obs - modelprediction)
    print(  'Correlation = ' , corr )
    return {'corelation': corr , 'NSE':nse  , 'RMSE' : rmse , 'MBE' : mbe} , Model , modelprediction ,W  ,Bias       


# def order(Ex , Keys):
#     Output =[ ]
#     for k in Keys :
#         List = list(Ex[k])
        
#         Output.append(List)
#     Order = numpy.transpose(Output)
#     return Order


# ord_keys =['DEM' , 'Slope', 'Aspect_cat']

# Train_file ='E:\Precipitaion Climates\Data\Cal_Test\stations/Complete_Cal.xlsx'
# Test_file = 'E:\Precipitaion Climates\Data\Cal_Test\stations/Complete_Test.xlsx'
# Excel = { }
# Excel['train']= pd.read_excel(Train_file)
# Excel['test']= pd.read_excel(Test_file)

# Keys = pd.DataFrame.keys(Excel['train'])
# shape = ( len(Keys) , len(Excel['train']) )

# Train={ }
# Train_data = Excel['train'].values
# # Train["X"] = Train_data[:,1:shape[0]]
# Train["X"] = order( Excel['train'] , ord_keys)
# Train["O"] = Train_data[:,0]

# Test = {}
# Test_data = Excel['test'].values
# Test["X"] = order( Excel['test'] , ord_keys)
# Test["O"] = Test_data[:,0]


# Train["mean"]=numpy.zeros(len(ord_keys))
# Train["std"]=numpy.zeros(len(ord_keys))
# Train["max"]=numpy.zeros(len(ord_keys))
# Train["min"]=numpy.zeros(len(ord_keys))
# for i in range(len(ord_keys)):
#     Train["mean"][i]=numpy.mean(Train["X"][:,i]) 
#     Train["std"][i]=numpy.std(Train["X"][:,i])
#     Train["max"][i]=numpy.max(Train["X"][:,i]) 
#     Train["min"][i]=numpy.min(Train["X"][:,i]) 

# Train["X"] = (Train["X"] - Train["mean"]) / Train["std"]
# Test["X"] = (Test["X"] - Train["mean"]) /  Train["std"]

# result , Model , predicted , W  , bias = ANN(Train_x = Train["X"]  , Train_obs =Train["O"]  ,
#              Test_x = Test["X"] , Test_obs = Test["O"] 
#              ,n_layer=5 , n_neorons=(20,30), batch=128 , epoch=150 ,
#              loss_func="mse" ,  ki ="random_uniform" , act="tanh"  )

# print(result)
# from math import *

# def feed_forward(X,W,B):
#     number_of_layers = len(W)
#     Xa=X
#     for i in range(number_of_layers):
#         print(numpy.shape(W[i]))
#         h = numpy.dot(Xa,numpy.array(W[i]))+B[i]
#         if i!= number_of_layers-1:
#              Xa = numpy.tanh(h)
#         else :
#             Xa = h
#     M =[]
#     for i in range(len(Xa)):
#         M.append(Xa[i,0] ) #+B[-1][0]
#     return M

# Model =  feed_forward(X=  Test["X"]  ,W = W ,B=bias )
# Obs = Test['O']
# numpy.corrcoef(Model , Obs)[0,1]
