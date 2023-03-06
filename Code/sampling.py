# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 00:07:16 2022

@author: reza
"""
import pandas as pd 
import numpy
from math import * 
import tifffile as tff
import math


MERRA_param = {
    "name" : "MERRA_",
    "μ"    : 15.85287714786201,
    "σ"    : 10.18351587392609,
    "res_x": 0.625, 
    "res_y": 0.5
    } 
 
IMERG_param     =   {
    "left" : 44.1 ,
    "top"  : 39.80 ,
    "res_x"  : 0.1,
    'res_y' : -0.1,
    "μ"    : 0.2962461902977852,
    "σ"    : 1.573247121755517
     }

CHIRPS_param    =    {
    "left" : 44.0  ,
    "top" : 40.25 ,
    "res_x"  : 0.05,
    'res_y' : -0.05,
    "μ"    : 0.86,
    "σ"    : 4.566859118593261
    }
PDIR_param      =   {
    "left"  : 43.96 ,
    "top"   : 39.76,
    "res_x"  : 0.04,
    'res_y' : -0.04,
    "μ"    : 0.8973076416804204,
    "σ"    :  3.0678025262247117
    }

CMORPH_param    =  {
    "left" : 44.0  ,
    "top"  : 40.25 ,
    "res_x"  : 0.25,
    'res_y' : -0.25,
    "μ"    : 0.492772146900091,
    "σ"    : 2.552500992781016
    }

def Z(x , m , s):
    z = (x-m)/s
    return z

def find_pixel(image_dict,_X,_Y):
    left = image_dict["left"]
    top = image_dict["top"]
    res_x = image_dict["res_x"]
    res_y = image_dict["res_y"]
    c=int(math.floor((_X-left)/res_x))
    r=int(math.floor((_Y-top)/res_y))
    return r,c

def evaluation_criteria(Obs , Model ) :
    r = numpy.corrcoef( Obs , Model )[0,1]
    nse  = 1 - ( numpy.sum((Model-Obs)**2) / numpy.sum((Obs-numpy.mean(Obs ))**2 ))
    rmse = numpy.mean((Obs-Model)**2)**0.5
    mbe  = numpy.mean( Obs - Model)
    
    return   { 'correlation' : r  , 'NSE' : nse , "RMSE" : rmse , 'MBE'  : mbe }


G = pd.read_excel("E:\payan_name\Compelet-6 hr\X,Y.xlsx")

fp  = 'E:\payan_name\AMSR2-TPW\Cal-test\obs_test.xlsx'
Ex = pd.read_excel(fp)
Ex = Ex[Ex['year'] > 2018]


T = [ ]
TPW = []
IMERG_l = []
CMORPH_l = [ ]
CHIRPS_l = []
PDIR_l = [ ]

M1_l = []
M2_l = []
M3_l = []
M4_l = []
M5_l = []

Cof = [
[0.1945,    0.1531,   1.8080,    0.0 ,     0.0 ,    0.0,     0.0 ],
[0.0994,    0.2223,   1.3252,   0.5193,    0.0,     0.0,     0.0 ],
[-0.0762,   0.5412,   1.5761,   0.5946,   -0.3755,   0.0,     0.0 ],
[0.0065,  	0.2020,   1.2518,	0.5506,	  -0.2519,	0.1896,	0.3375],
[0.2092,    0.0,      1.1046,    0.5725,  -0.1918,   0.7804, 0.2952]
]


Cof  = numpy.array(Cof)
MERGE = lambda C , pwv, Ts , imerg ,cmorph , chirps , pdir  : C[0]+C[1]*Z(pwv,0.82442664,0.884275046)+C[2]*Z(imerg,IMERG_param["μ"],IMERG_param["σ"])+C[3]*Z(cmorph,CMORPH_param["μ"],CMORPH_param["σ"])+C[4]*Z(Ts,MERRA_param["μ"],MERRA_param["σ"])+C[5]*Z(chirps,CHIRPS_param["μ"],CHIRPS_param["σ"])+C[6]*Z(pdir,PDIR_param["μ"],PDIR_param["σ"])
SEASON=[]
EDM = [ ]

N= len(Ex)
for i in range(28432 ,  N):
    print(i , 'of' ,N )
    name = Ex['name'][i]
    year = Ex['year'][i]
    month = Ex['month'][i]
    day = Ex['day'][i]
    yr = str(year)
    if month<10:    moon="0"+str(month)
    else:           moon=str(month)
    if day<10:      dd="0"+str(day)
    else:           dd=str(day)
    X =  Ex['X'][i]
    Y = Ex['Y'][i]
    
    
    fp_tpw = "E:\payan_name\AMSR2-TPW\AMSR2_TPW_"+yr+"_"+moon+"_"+dd+".xlsx"
    Ex_tpw = pd.read_excel(fp_tpw)
    
    season = int(month/3.1)+1
    
    
    edm = G[name][2]
    
    
    for j in range(len(Ex_tpw)):
        if Ex_tpw["NAME"][j]  == name:
            tpw = Ex_tpw['PWV'][j]
            Ts = Ex_tpw['Ts'][j]
    
   
    
    CHIRPS_path  = "E:\payan_name\Compelet-6 hr\CHIRPS_"+str(year)+"_"+moon+"_"+dd+".tif"
    
    CMORPH_path  = "E:\payan_name\Compelet-6 hr\CMORPH_"+str(year)+"_"+moon+"_"+dd+".tif"
    
    IMERG_path   =  "E:\Dataset\IMERG\Daily\IMERG_"+str(year)+"_"+moon+"_"+dd+".tif"
    
    
    try:
        PDIR_path    = "E:\payan_name\Compelet-6 hr\PDIR_1d"+str(year)+moon+dd+".tif"
        
        PDIR   =tff.imread(PDIR_path)
        r,c = find_pixel(PDIR_param,X,Y)
        pdir  = PDIR[r,c]
    except:
        pdir = 'noValue'
    
    
    CHIRPS  =tff.imread(CHIRPS_path)
    r,c = find_pixel(CHIRPS_param,X,Y)
    chirps = CHIRPS[r,c]
    
    CMORPH  =tff.imread(CMORPH_path)
    r,c = find_pixel(CMORPH_param,X,Y)
    cmorph = CMORPH[r,c]
    
    IMERG   =tff.imread(IMERG_path)
    
    r,c = find_pixel(IMERG_param,X,Y)
    imerg = IMERG[r,c]
    if imerg<0.0001 :imerg =0
    
    PDIR_l.append(pdir)
    IMERG_l.append(imerg)
    CMORPH_l.append(cmorph)
    CHIRPS_l.append(chirps)
    T.append(Ts)
    TPW.append(tpw)
    
    
    EDM.append(edm)
    SEASON.append(season)
    
    
    try:
        M1  = MERGE(Cof[0],tpw, Ts , imerg ,cmorph , chirps , pdir )
        M2  = MERGE(Cof[1],tpw, Ts , imerg ,cmorph , chirps , pdir )
        M3  = MERGE(Cof[2],tpw, Ts , imerg ,cmorph , chirps , pdir )
        M4  = MERGE(Cof[3],tpw, Ts , imerg ,cmorph , chirps , pdir )
        M5 = MERGE(Cof[4],tpw, Ts , imerg ,cmorph , chirps , pdir )
    except :
        M1 = 'noValue'
        M2 = 'noValue'
        M3 = 'noValue'
        M4 = 'noValue'
        M5 = 'noValue'
    
    M1_l.append(M1)
    M2_l.append(M2)
    M3_l.append(M3)
    M4_l.append(M4)
    M5_l.append(M5)

Keys = list(pd.DataFrame.keys(Ex))

Ex.insert(len(Keys),'IMERG',  IMERG_l ,True)
Ex.insert(len(Keys)+1,'CMORPH',  CMORPH_l ,True)
Ex.insert(len(Keys)+2,'CHIRPS',  CHIRPS_l ,True)
Ex.insert(len(Keys)+3,'PDIR',  PDIR_l ,True)
Ex.insert(len(Keys)+4,'TPW',  TPW ,True)
Ex.insert(len(Keys)+5,'T',  T ,True)
Ex.insert(len(Keys)+6,'M1',  M1_l ,True)
Ex.insert(len(Keys)+7,'M2',  M2_l ,True)
Ex.insert(len(Keys)+8,'M3',  M3_l ,True)
Ex.insert(len(Keys)+9,'M4',  M4_l ,True)
Ex.insert(len(Keys)+9,'M5',  M5_l ,True)
Ex.insert(len(Keys)+6,'season',  SEASON ,True)
Ex.insert(len(Keys)+7,'EDM',  EDM ,True)


of = 'E:/payan_name/AMSR2-TPW/Cal-test/test_resampled_data.xlsx'
Ex.to_excel(of)

# def order(Ex , Keys):
#     Output =[ ]
#     for k in Keys :
#         List = [k]
#         List+= list(Ex[k])
#         Output.append(List)
#     Order = numpy.transpose(Output)
#     return Order

# fp  = {
#        'input'   : 'E:/payan_name/AMSR2-TPW/Cal-test/test_resampled_data.xlsx',
#        'output'  : 'E:/payan_name/AMSR2-TPW/Cal-test/test_5.xlsx',
#        'keys'    : [ 'rrr' , 'IMERG' , 'CMORPH'  , 'T' ,'CHIRPS' , 'PDIR' ]
#        } 
       

# Ex = pd.read_excel(fp['input'])

# Query = order(Ex , fp['keys'])
# Query = pd.DataFrame(Query)
# Query.to_excel(fp['output'])

