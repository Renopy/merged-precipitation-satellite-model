

import numpy
import h5py
import tifffile
import os 
import math
from math import *
from PIL import Image
import imageio
import Reza
from scipy.stats import ks_2samp


daynum=["",32,29,32,31,32,31,32,32,31,32,31,31]
MonthName=['Jan','Feb','March','April',"ΜΑΥ",'Jun','July','Aug','September','Octobr','November',"December"]

Gauge_info= Reza.Matread("Stations_long,lat.xlsx")
Numberg=len(Gauge_info)

Shape_G=numpy.shape(Gauge_info)
for r in range(Shape_G[0]):
    for c in range(Shape_G[1]):
        if c!=2:
            Gauge_info[r,c]=float(Gauge_info[r,c])
Nameg=[]
Xg=[]
Yg=[]
Zg=[]
for i in range(len(Gauge_info)):
    Nameg.append(Gauge_info[i,2])
    Yg.append(float(Gauge_info[i,1]))
    Xg.append(float(Gauge_info[i,0]))
    Zg.append(float(Gauge_info[i,4]))

CMORPH_param    =  {
    "left" : 44.0  ,
    "top"  : 40.25 ,
    "res"  : 0.25,
    "μ"    : 0.49,
    "σ"    : 2.28
    }

 
IMERG_param     =   {
    "left" : 44.1 ,
    "top"  : 39.80 ,
    "res"  : 0.1,
    "μ"    : 0.23,
    "σ"    : 1.16
     }

CHIRPS_param    =    {
    "left" : 44.0  ,
    "top" : 40.25 ,
    "res"   : 0.05,
    "μ"    : 0.86,
    "σ"    : 0.95
    }
PDIR_param      =   {
    "left"  : 44.0 ,
    "top"   : 39.84,
    "res"   : 0.04,
    "μ"    : 0.8,
    "σ"    : 2.52
    }
MERRA_T_param    =  {
    "left" : 44.0  ,
    "top"  : 40.25 ,
    "res_x"  : 0.625,
    "res_y" : 0.5,
    "μ"    : 15.71,
    "σ"    : 10.33
    }



PWV_param =  {
    'left' : 44,
    'top' :  40,
    'res' :  0.1,
    "μ"    : 5.98,
    "σ"    : 2.795
    }

LL=tifffile.imread('Long,Lat_Model[1].tiff')
long =LL[0]
lat = LL[1]
Shape=numpy.shape(LL[0])
Row = Shape[0]
Column = Shape[1]



def Neigh(Matrix,R,C):

    Neighbors=[]
    for iN in range(-1,2,1):
        for jN in range(-1,2,1):
            try:
                if float(Matrix[R+iN,C+jN])>=0.0:
                    Neighbors.append(Matrix[R+iN,C+jN])
            except:
                pass
    
    return Neighbors

def Nearest(Neighbors,o):
    N=len(Neighbors)
    O_N=[]
    for i in range(N):
        O_N.append(abs((Neighbors[i])-float(o)))
    imin=0
    Min=200
    result=0.0
    for i in range(N):
        if O_N[i]<Min:
            imin=i
            Min=O_N[i]
            result=Neighbors[i]
    if float(o)<0.0:
        print("observation<0:")
    return result
Obs = []
MODEL = [ ]


for year in range(2019,2016):
    yr=str(year)
    for Month in range(1,13):
        if Month<10:    moon="0"+str(Month)
        else:           moon=str(Month)
        for Day in range(1,daynum[Month]):

            Input= "E:\payan_name\Compelet-6 hr\Rain_Gauges_"+yr+"_Month"+str(Month)+"_Day"+str(Day)+".xlsx"
            E=Reza.Matread(Input)
            if Day<10:      day="0"+str(Day)
            else:           day=str(Day)
            fp = "Model_4\P_model_4_"+yr+"_"+moon+"_"+day+".tiff"
            Model = tifffile.imread(fp)
            
            CHIRPS_path  = "E:\payan_name\Compelet-6 hr\CHIRPS_"+str(year)+"_"+moon+"_"+day+".tif"
            CMORPH_path  = "E:\payan_name\Compelet-6 hr\CMORPH_"+str(year)+"_"+moon+"_"+day+".tif"
            IMERG_path   = "E:\payan_name\Compelet-6 hr\IMERG_"+str(year)+"_"+moon+"_"+day+".tif"
            PDIR_path    = "E:\payan_name\Compelet-6 hr\PDIR_1d"+str(year)+moon+day+".tif"
            MERRA_path  = "E:\payan_name\MERRA\MERRA_Temp"+"_"+day+"_"+moon+"_"+yr+".tif"

            PDIR    =Image.open(PDIR_path)
            PDIR    =numpy.array(PDIR)
            CHIRPS  =imageio.imread(CHIRPS_path)
            CHIRPS  =numpy.array(CHIRPS)
            CMORPH  =imageio.imread(CMORPH_path)
            CMORPH  =numpy.array(CMORPH)
            IMERG   =imageio.imread(IMERG_path)
            IMERG   =numpy.array(IMERG)
            MERRA   =imageio.imread(MERRA_path)
            MERRA   =numpy.array(MERRA)
            
            for g in range(len(E)):
                
                
                x=float(E[g,5])
                y=float(E[g,4])
                i=int(math.floor((y-PWV_param["top"])/(-PWV_param["res"])))
                j=int(math.floor((x-PWV_param["left"])/PWV_param["res"]))
                
                Pr_g =float( E[g,8])

                if Model[i,j]!=-999:

                    i_imerg=int(math.floor((y-IMERG_param["top"])/(-IMERG_param["res"])))
                    j_imerg=int(math.floor((x-IMERG_param["left"])/IMERG_param["res"]))

                    i_cmorph=int(math.floor((y-CMORPH_param["top"])/(-CMORPH_param["res"])))
                    j_cmorph=int(math.floor((x-CMORPH_param["left"])/CMORPH_param["res"]))

                    i_pdir=int(math.floor((y-PDIR_param["top"])/(-PDIR_param["res"])))
                    j_pdir=int(math.floor((x-PDIR_param["left"])/PDIR_param["res"]))

                    i_chirps=int(math.floor((y-CHIRPS_param["top"])/(-CHIRPS_param["res"])))
                    j_chirps=int(math.floor((x-CHIRPS_param["left"])/CHIRPS_param["res"]))

                    i_MERRA=int(math.floor((y-MERRA_T_param["top"])/(-MERRA_T_param["res_y"])))
                    j_MERRA=int(math.floor((x-MERRA_T_param["left"])/MERRA_T_param["res_x"]))


                    imerg = IMERG[i_imerg , j_imerg]
                    cmorph = CMORPH[i_cmorph,j_cmorph]
                    chirps = CHIRPS[i_chirps,j_chirps]
                    pdir = PDIR[i_pdir,j_pdir]

                    matrix = Model
                    Neighbors = Neigh(Model,i,j)
                    Sat = Nearest(Neighbors, Pr_g )
                    Obs.append(Pr_g)
                    MODEL.append(Sat)

cor = Reza.correlation(Obs,MODEL)
nse = Reza.function_Ens(MODEL,Obs)
rmse = Reza.function_RMSE(MODEL,Obs)
pod = Reza.POD(Obs,MODEL)
far = Reza.FAR(Obs,MODEL)
bias = Reza.BIAS(Obs,MODEL)
O = numpy.array(Obs)
M = numpy.array(MODEL)

Ks = ks_2samp(O,M)
print("cor = ",cor)
print("nse = ",nse)
print("rmse = ",rmse)
print("pod = ",pod)
print("far = ",far)
print("bias = ",bias)
print("Ks (D , p-value) " , Ks)






