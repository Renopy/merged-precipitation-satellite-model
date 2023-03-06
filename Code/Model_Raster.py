
import numpy
import h5py
import tifffile
import os 
import math
from math import *
from PIL import Image
import imageio


daynum=["",32,29,32,31,32,31,32,32,31,32,31,31]
MonthName=['Jan','Feb','March','April',"ΜΑΥ",'Jun','July','Aug','September','Octobr','November',"December"]

LL=tifffile.imread('Long,Lat_Model[1].tiff')
long =LL[0]
lat = LL[1]
Shape=numpy.shape(LL[0])
Row = Shape[0]
Column = Shape[1]


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
    "res"  : 0.1,
    "μ"    : 0.2962461902977852,
    "σ"    : 1.573247121755517
     }

CHIRPS_param    =    {
    "left" : 44.0  ,
    "top" : 40.25 ,
    "res"   : 0.05,
    "μ"    : 0.86,
    "σ"    : 4.566859118593261
    }
PDIR_param      =   {
    "left"  : 43.96 ,
    "top"   : 39.76,
    "res"   : 0.04,
    "μ"    : 0.8973076416804204,
    "σ"    :  3.0678025262247117
    }

CMORPH_param    =  {
    "left" : 44.0  ,
    "top"  : 40.25 ,
    "res"  : 0.25,
    "μ"    : 0.492772146900091,
    "σ"    : 2.552500992781016
    }

PWV_param =  {
    'left' : 44,
    'top' :  40,
    'res' :  0.25,
    "μ"    : 0.824426,
    "σ"    : 0.884275
    }


def Z(x , m , s):
    z = (x-m)/s
    return z

Cof = [ -0.36673385,  1.72356812,  0.2191    ,  0.91650231,  0.263685 , 0.10714297876296655 ]

Model_fx = lambda pwv, Ts , imerg ,cmorph , chirps , pdir : -0.36673385*Ts+1.72356812*imerg+0.2191*cmorph+0.91650231*chirps+0.263685*pdir+0.10714297876296655
#0.40237241*Z(pwv,PWV_param["μ"],PWV_param["σ"])-0.31028275*Z(Ts,MERRA_T_param["μ"],MERRA_T_param["σ"])+1.3496*Z(imerg,IMERG_param["μ"],IMERG_param["σ"]) +0.4054*Z(cmorph,CMORPH_param["μ"],CMORPH_param["σ"])+0.8116*Z(chirps,CHIRPS_param["μ"],CHIRPS_param["σ"])+0.2459*Z(pdir,PDIR_param["μ"],PDIR_param["σ"])+0.094

for year in range(2015,2016):
    yr=str(year)
    for Month in range(1,13):
        if Month<10:    moon="0"+str(Month)
        else:           moon=str(Month)

        Model_raster = numpy.zeros(Shape,dtype=float)

        for Day in range(1,daynum[Month]):

            if Day<10:      day="0"+str(Day)
            else:           day=str(Day)

            print(yr+"_"+moon+"_"+day,end="\r")

            fp = "AMSR2_PWV_"+yr+"_"+moon+"_"+day+".tiff"

            PWV = tifffile.imread(fp)

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
            
            for i in range(Row):
                for j in range(Column):
                    x=float(long[i,j])
                    y=float(lat[i,j])

                    i_pwv = int(math.floor((y-PWV_param["top"])/(-PWV_param["res"])))
                    j_pwv = int(math.floor((x-PWV_param["left"])/PWV_param["res"]))
                    
                    pwv =PWV[i_pwv,j_pwv]
                    if pwv>-98 or True :
                        try :
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
                            
                            
                            imerg = IMERG[i_imerg,j_imerg]
                            cmorph = CMORPH[i_cmorph,j_cmorph]
                            chirps = CHIRPS[i_chirps,j_chirps]
                            pdir = PDIR[i_pdir,j_pdir]
                            Ts = MERRA[i_MERRA,j_MERRA]


                            P_model = Model_fx(pwv, Ts , imerg ,cmorph , chirps , pdir)
                            if P_model<0 :
                                P_model =0 
                            Model_raster[i,j]=P_model
                        except:
                            Model_raster[i,j]= -999

                    else :
                        Model_raster[i,j]= -999
            
            Output_path = "E:\payan_name\AMSR2-TPW\Model_5\P_model_5_"+str(year)+"_"+moon+"_"+day+".tiff"
            tifffile.imsave( Output_path , Model_raster)

            metadata =  "E:\payan_name\AMSR2-TPW\Model_5\P_model_5_"+str(year)+"_"+moon+"_"+day+".mtd.txt"
            txt_file = open (metadata , 'w')
            txt= "#-----------Precipitation Model 4-----------#\n"
            txt0= "\n Used variable :  PWV ,Ts,  IMERG ,CMORPH "
            txt1="\n#----------- Bands Information -----------#\n"
            txt2="\n Band 1 : Precipitation mm/day"  
            txt3="\n#----------- Geometric Information -----------#\n"
            txt4="\n left=44 E"+ "\n right=64 E "+ "\n top=40 N"+ "\n bottom=25 N" + "\n Resolution=0.25 "
            txt5="\n#----------- Data Information -----------#\n"
            txt6="\n Image Format : Tiff" +"\n Image Shape : "
            txt7= str(Row)
            txt8="x"
            txt9=str(Column)
            txt10="\n Data digital type : Float" + "\n No value : -999" 
            txt_file = open(metadata,"w")
            txt_file.write(txt)
            txt_file.write(txt0)
            txt_file.write( yr)
            txt_file.write("_")
            txt_file.write( moon )
            txt_file.write("_")
            txt_file.write(day)
            txt_file.write(txt1)
            txt_file.write(txt2)
            txt_file.write(txt3)
            txt_file.write(txt4)
            txt_file.write(txt5)
            txt_file.write(txt6)
            txt_file.write(txt7)
            txt_file.write(txt8)
            txt_file.write(txt9)
            txt_file.write(txt10)
            txt_file.close()


