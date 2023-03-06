# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 12:02:39 2022

@author: reza
"""


import pyhomogeneity as hg
import numpy
import pandas as pd 
from math import *
import  scipy.stats as sci
import scipy

'''data prepration '''

# Out = [ ['name'  , 'year' , 'month' , 'day' , 'X'  , 'Y' , 'rrr'] ] 
# for year in range(2014,2021):
    
#     yr = str(year)
#     for month in range(1,13):
#         # if month <10 : MM = '0'+str(month)
#         # else: MM = str(month)
#         print(year , month)
#         for day in range(1,32):
#             # if day < 10 : DD = '0'+str(day)
#             # else: DD = str(day)
#             try:
#                 fp = "E:\payan_name\Compelet-6 hr\Rain_Gauges_"+yr+"_Month"+str(month)+"_Day"+str(day)+".xlsx"
#                 Ex = pd.read_excel(fp)
#                 for i in range(len(Ex)):
#                     name = Ex['Name'][i]
#                     rain = Ex['Rain'][i]
#                     X = Ex['long'][i]
#                     Y = Ex['lat'][i]
#                     data = [ name , year , month , day , X ,Y , rain ] 
#                     Out.append(data)
#             except:
#                 pass

# Out = pd.DataFrame(Out)
# of = 'E:\payan_name\AMSR2-TPW\Cal-test\obs_data.xlsx'
# Out.to_excel(of)

#_________________________________________________________________


def vonneuman(data):
    data = numpy.array(data)
    n = len(data)
    mean =numpy.mean(data)
    yi =data[0:n-1]
    yj = data[1:n]
    
    
    suc_dif = numpy.sum( (yi-yj)**2)
    var =numpy.sum(    (  data-mean)**2)
    N = suc_dif/var
    
    return  N


''' hmomogenity test  '''


fp = 'E:/payan_name/AMSR2-TPW/Cal-test/test_resampled_data.xlsx'


Ex = pd.read_excel(fp)
Ex = Ex[Ex['year'] < 2021]

names = list(Ex[ 'name'])
names = list(dict.fromkeys(names))
test_result = [ [ 'name' , 'p-value' , 'Null-hyp']]

def chi(X,DF):
    mean = numpy.mean(X)
    std  = numpy.std(X)
    Z = (X-mean) / std
    X2 = numpy.sum(Z)
    
for name in names :
    Ex_st = Ex[Ex['name'] == name]
    data = numpy.array(Ex_st['rrr'])
    shape = data.shape
    n= shape[0]
    
    X2 =Chi(data)
                              
    r=[]
    for season in range(1,5):
        Ex_season = Ex_st[Ex_st['season'] == season]
        data = list(Ex_season['rrr'])
        r.append( hg.pettitt_test(data , 0.05)[2])
    
    r= sum(r)/4
    
    # r= hg.buishand_u_test(data ,0.05 )
    null= ''
    if r > 0.05 :
        null = 'Rejected'
    else :
        print(r,season)
        null = 'Accepted'
    test_result.append( [ name , r , null ])

test_result = numpy.array(test_result)
test_result = pd.DataFrame(test_result)
test_result.to_excel('E:\payan_name\AMSR2-TPW\Cal-test\obs_homo_test.xlsx')

    
    
    
    


