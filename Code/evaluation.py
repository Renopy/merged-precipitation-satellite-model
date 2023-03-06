# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 13:57:11 2022

@author: reza
"""


import pandas as pd
import numpy
from math import *
import hydroeval as he
import scipy.stats as sci
π=3.14159


def Integral( Range, f , dx):
    x = Range
    X=x[0]
    f0 = f(X)
    S=0.0
    while X<x[1]:
        X = X+dx
        f1 = f(X)
        S = S+(f0+f1)*dx/2
        f0=f1
    return S

def Average_tTest(sample_1,sample_2):
    a= [numpy.mean(sample_1),numpy.mean(sample_2)]
    s= [numpy.var(sample_1),numpy.var(sample_2)]
    N= [len(sample_1),len(sample_2)]
    t = (a[1]-a[0])/sqrt( s[0]**2/N[0]+s[1]**2/N[1])
    Normal = lambda y : exp(-0.5*y**2)/sqrt(2*π)
    P_value = 2*Integral( Range = (0,abs(t)) , f=Normal , dx=0.01)
    return  t, P_value


def KGE(Obs,Model):
    r = numpy.corrcoef( Obs , Model )[0,1]
    alpha = numpy.std(Model)/numpy.std(Obs)
    beta = numpy.mean(Model)/numpy.mean(Obs)
    kge= 1- sqrt((1-r)**2 + (1-alpha)**2 +(1-beta)**2)
    return kge      

def Kolomogrov_smirnov(data_1 , data_2 , intervals):
    data_1 = numpy.array(data_1)
    data_2 = numpy.array(data_2)

    m= len(data_1)
    n = len(data_2)
    alpha = 0.05
    D = sqrt(-0.5 * log(0.5*alpha)) * sqrt((m+n)/(m*n))

    cdf_1 = CDF(data_1 , intervals)
    cdf_2  = CDF(data_2 , intervals)
    cdf_1  =  numpy.array(cdf_1)
    cdf_2  =  numpy.array(cdf_2)
    dif = cdf_1-cdf_2
    absol = numpy.absolute(dif)
    Dc = numpy.max(absol )
    
    return Dc , D

def Frequency(data , intervals):
        data = numpy.array(data)
        N = len(data)
        freq = []
        nc = 0 
        for i in range(len(intervals)-1):
            qu_1 = data[ data >= intervals[i] ]
            qu_2 = qu_1[qu_1 < intervals[i+1] ]
            n = len(qu_2)/N
            
            freq.append(n)
        return freq
    
def CDF(data , intervals):
    data = numpy.array(data)
    N = len(data)
    cdf = []
    nc = 0 
    for i in range(len(intervals)-1):
        qu_1 = data[ data >= intervals[i] ]
        qu_2 = qu_1[qu_1 < intervals[i+1] ]
        n = len(qu_2)
        nc+=n
        cdf.append(nc/N)
    return cdf
    
    
    
def BIAS(Obs,Product) :
    N=len(Obs)
    F=0.0
    H=0.0
    M=0.0
    Th=0.1
    for i in range(N):
        O=float(Obs[i])
        P=float(Product[i])
        if O>=Th and P>=Th :  H=H+1
        if O<Th and P>=Th :   F=F+1
        if O>=Th and P<Th :   M=M+1
    try:
        bias=(H+F)/(H+M)
    except:
        bias="Undefined"
    return bias

def CSI(Obs,Product):
    N=len(Obs)
    F=0.0
    H=0.0
    M=0.0
    Th=0.1
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

def FAR(Obs,Product):
    N=len(Obs)
    F=0.0
    H=0.0
    Th=0.1
    for i in range(N):
        O=float(Obs[i])
        P=float(Product[i])
        if O>=Th and P>=Th :  H=H+1
        if O<Th and P>=Th :   F=F+1
    try:
        far=(F)/(F+H)
    except:
        far="Undefined"
    return far


def POD(Obs,Product):
    N=len(Product)
    H=0
    M=0
    Th=0.1
    for i in range(N):
        O=float(Obs[i])
        P=float(Product[i])
        if O>=Th and P>=Th :  H=H+1
        if O>=Th and P<Th  :  M=M+1
    try:
        pod=float(H)/float(H+M)
    except:
        pod="Undefined"
    return pod


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
    t , p   = Average_tTest(Obs , Model)
    
    return   {'correlation' : r[0]  , 'NSE' : nse ,
              "RMSE" : rmse , "MAE" : mae, 'MBE'  : mbe , 
              'PBIAS' : pbias,'KGE' : kge[0]  , 'spearman':spearman,
              'POD' : pod , 'FAR' : far , 'BIAS': bias  , 
              'CSI' : csi , 'KS' : Dc/D ,'P_value(t-test)' :  p 
               }  

fp = 'H:/Paper3/Data/test_main.xlsx'
Ex = pd.read_excel(fp)
directory = 'H:/Paper3/Data/result/'

observation_key = 'rrr'
complete = []
interval =  [ 0, 5 , 10  , 15 , 20 , 1000]



for product_name in [ 'P_merged_ANN_1' ] :
    
    evaluation_category = ['name']
    obs = numpy.array(Ex[observation_key]) 
    Product = numpy.array(Ex[product_name])
    
    result = evaluation_criteria(obs , Product  , interval)
    print(product_name)
    print( result)
    result['Model'] = product_name
    complete.append(result)
    
    for cat in evaluation_category:
        Category = list(Ex[ cat])
        uniques = list(dict.fromkeys(Category))
        
        output = [ ]
        for item in uniques:
            ex= Ex[Ex[cat] == item ]
            model = numpy.array(ex[product_name])
            obs = numpy.array(ex[observation_key])
            
            result = evaluation_criteria(obs , model ,interval)
            result['item'] = item
            output.append(result)
        output = pd.DataFrame(output)
        
        of = directory + product_name + '_' + cat + '.xlsx'
        output.to_excel(of)

# complete = pd.DataFrame(complete)
# of = directory +'_complete.xlsx' 
# complete.to_excel(of)


    
