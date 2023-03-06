
import tifffile
import Reza
import numpy
import sys
import math
from PIL import Image
import imageio
from math import *
import pandas as pd
from scipy import stats
import de 
α_ks = 0.05
def MBE(obs,model):
    
    n = len(obs)
    mbe = numpy.mean(obs-model)
    return mbe

def Sigma(f,k):
    S=0.0
    for i in range(k[0],k[1]):
        S+=f(i)
    return S
def floatable(x):
    try:
        a=float(x)
        return True
    except:
        return False

class Gamma():
    def distribution(List):
        mean= numpy.average(List)
        Ln_List = log(List)
        mean_Ln = numpy.average(Ln_List)
        Ln_mean = log(mean)
        A  = Ln_mean - mean_Ln
        alpha = ((1)/(4*A))*(1+SQRT(1+1.33*A))
        beta = A/mean
        return [alpha , beta]


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

def Z(x , m , s):
    z = (x-m)/s
    return z



"""----- Harmony Search ----- """

"""    [ Bias        PWV     IMERG    CMORPH     MERAA   CHIRPS    PDIR] """
#1 C = [0.1945,    0.1531,   1.8080,    0.0 ,     0.0 ,    0.0,     0.0 ]
#2 C = [0.0994,    0.2223,   1.3252,   0.5193,    0.0,     0.0,     0.0 ]
#3 C=  [-0.0762,   0.5412,   1.5761,   0.5946,  -0.3755,   0.0,     0.0 ]
#4 C = [0.0065,	   0.2020,	1.2518,    0.5506,	-0.2519	,  0.1896,	0.3375]
#5 C = [0.2092,    0.0,    1.1046,    0.5725,   -0.1918,   0.7804, 0.2952]

"""-------- Sine Cosine Algorithm  ------- """
#1 C = [0.62368669 ,    0.22810318,     1.66181322 ,    0.0 ,            0.0 ,          0.0,            0.0         ]
#2 C = [0.66024048,	    0.22287468,	    1.50424732,	    0.11485804,      0.0 ,          0.0 ,           0.0         ]
#3 C = [0.17021334,     0.47994397,     1.81898485,     0.05681694,	    -0.60861773,    0.0,	        0.0         ] 
#4 C = [0.264153167,    0.425798951,    1.49193684,     0.226190323,	-0.042675087,	0.001098879,	0.531084253 ]
#5 C = [0.649529464,	0	,           1.63544114,     0.04028987,	    -0.330233329,	0.594586671,	0.000376484]

""""------- Path Finder Algorithm  ------- """
#1 C= [0.64411, 0.23762,	1.81879,	0.00000,	0.00000,	0.00000,	0.00000]
#2 C= [0.66375,	0.26412,    1.65266,	0.30750	,   0.00000	,   0.00000,	0.00000]
#3 C= [0.43300,	0.38271,	1.59972,	0.17101,	-0.41323,	0.00000,	0.00000]
#4 C= [0.43293,	0.42648,	1.40645,	0.22677,	-0.41694,	0.42534,	0.22620]
#5 C= [0.58138,	0.00000,    1.42024,	0.15594,	-0.28672,	0.49709,	0.34205]
C = [0.1945,    0.1531,   1.8080,    0.0 ,     0.0 ,    0.0,     0.0 ]


MERGE = lambda pwv, Ts , imerg ,cmorph , chirps , pdir : C[0]+C[1]*Z(pwv,0.82442664,0.884275046)+C[2]*Z(imerg,IMERG_param["μ"],IMERG_param["σ"])+C[3]*Z(cmorph,CMORPH_param["μ"],CMORPH_param["σ"])+C[4]*Z(Ts,MERRA_param["μ"],MERRA_param["σ"])+C[5]*Z(chirps,CHIRPS_param["μ"],CHIRPS_param["σ"])+C[6]*Z(pdir,PDIR_param["μ"],PDIR_param["σ"])

def BIAS(Obs,Product) :
    N=len(Obs)
    F=0.0
    H=0.0
    M=0.0
    Th=1
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
    Th=1
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
    Th=1
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
    Th=1
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

def ZPD(Obs,Product):
    N=len(Product)
    Z=0
    nunZ=0
    Th=1
    for i in range(N):
        O=float(Obs[i])
        P=float(Product[i])
        if O<Th and P<Th :  Z=Z+1
        if O<Th and P>=Th : nunZ=nunZ+1
    try:
        zpd=float(Z)/float(Z+nunZ)
    except:
        zpd="Undefined"
    return zpd

def function_RMSE(Obs,Model):
    N=len(Model)
    se=0.0
    mse = numpy.mean((Obs-Model)**2)
    rmse = mse**0.5

    return rmse

def function_Ens(Model,Obs):
    nse = 1 - ( numpy.sum((Model-Obs)**2) / numpy.sum((Obs-numpy.mean(Obs ))**2 ))
    return nse

def sumlist(List):
    S=0.0
    for member in List :
        S=S+member
    return S
def Mean(List):
    S=0.0
    for member in List :
        S=S+member
    N=len(List)
    try:
        mean=S/float(N)
    except:
        mean="undefined"
    return mean
def Variance(List):
    S=0.0
    for member in List :
        S=S+member
    N=len(List)
    try:
        mean=S/float(N)
        D=0.0
        for i in range(len(List)) :
            D=D+(List[i]-mean)**2
        V=D/float(N)
    except:
        V="undefined"
    return V
def correlation(X,Y):
    try:
        xave=Mean(X)
        yave=Mean(Y)
        var_x=Variance(X)
        var_y=Variance(Y)
        sx=var_x**0.5
        sy=var_y**0.5
        n=len(X)
        r=0
        cov=0.0
        e=0.0000000000001
        if var_x*var_y==0.0:
            c="Undefined"
        else:
            for i in range(n-r):
                cov=cov+(((X[i]-xave)*(Y[i+r]-yave)))/float(n-r)
            c=cov/(var_x*var_y)**0.5
    except:
        c="Undefined"
    return c

def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "|"*x, "."*(size-x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()

def Seasonal_func(pwv,Ts,imerg,cmorph , chirps , pdir, season):
    if season==1:
        Cof = [ 0.3237 ,    -0.2168     , 1.5461 ,     1.3766      ,0.61134369 , -0.3596 , 0.4694    ]
    if season==2:
        Cof = [0.1129    , -0.18541159,  1.0956    ,  0.6406    ,  0.7715    , -0.0357 ,   0.2693   ]
    if season==3:
        Cof = [0.53279494, -0.1904    ,  1.1127    ,  0.1392    ,  0.5023    , 0.0521   ,-0.19204192091893957]
    if season==4:
        Cof = [0.78217254, -0.2656    ,  1.698     ,  0.6848    ,  0.93814408,
        0.09468546,0.2401096]
    
    P_model = float(Cof[0]*Z(pwv,0.82442664,0.884275046)+Cof[1]*Z(Ts,MERRA_param["μ"],MERRA_param["σ"])
        +Cof[2]*Z(imerg,IMERG_param["μ"],IMERG_param["σ"]) 
        +Cof[3]*Z(cmorph,CMORPH_param["μ"],CMORPH_param["σ"])
        +Cof[4]*Z(chirps,CHIRPS_param["μ"],CHIRPS_param["σ"])
        +Cof[5]*Z(pdir,PDIR_param["μ"],PDIR_param["σ"])
        +Cof[6])
    return P_model

    



daynum=["",32,29,32,31,32,31,32,32,31,32,31,31]

MonthName=['Jan','Feb','March','April',"ΜΑΥ",'Jun','July','Aug','September','Octobr','November',"December"]

Station_PWV = []
Station_P   = []

Complete=[ ["P" ,    "pwv" ,    "Ts",  
            "V" ,   "IMERG" ,   "CMORPH" , 
            "CHIRPS" , "PDIR" , "BT89v", 
            "BT36v",    "BT23v", "BT18v" , 
            "Logterm",'BT_89h' , 'BT_36h' ,
            'BT_23h', 'BT_18h',"day","month","year"] ]

for i in range(81):
    Station_PWV.append([])
    Station_P.append([])

Climate_Obs=[]
Climate_Model=[]
for i in range(8):
    Climate_Obs.append([])
    Climate_Model.append([])

Season_PWV = [ [ ] , [ ] , [ ] , [ ] ]
Season_P   = [ [ ] , [ ] , [ ] , [ ] ]
G = pd.read_excel("E:\payan_name\Compelet-6 hr\X,Y.xlsx")
period = "test"
MODEL=[]
OBS = []
iran_pr=[["mean_pr","Day",'Month','year']]

S_Pr_c =[]
for i in range(4):
    S_Pr_c.append({"0-5" :0, "5-10" :0, "10-15":0 , "15-20":0 , ">20":0})


A = {
    "North":0,
    "Other":0
    }


North = ["Ramsar" ,
"Bandar-E-Anzali"
"Jirandeh",
"Masuleh",
"Talesh",
"Rudsar",
"Bandar-E-Gaz",
"Gorgan" ]

for Month in range(1,13):
    Season = int(Month/3.1)
    for year in range(2019,2021):
        yr = str(year)
        print(MonthName[Month-1], " ", year)
        
        for Day in range(1,daynum[Month]):
        
            vec_pr=[]
            if Month<10:    moon="0"+str(Month)
            else:           moon=str(Month)
            if Day<10:      day="0"+str(Day)
            else:           day=str(Day)
            
            path_TPW = "E:\payan_name\AMSR2-TPW\AMSR2_TPW_"+yr+"_"+moon+"_"+day+".xlsx"
            path_Pre = "E:\payan_name\Compelet-6 hr\Rain_Gauges_"+yr+"_Month"+str(Month)+"_Day"+str(Day)+".xlsx"

            AMSR2_TPW = pd.read_excel(path_TPW)
            Rain_gauge= pd.read_excel(path_Pre)

            Shape =  numpy.shape(AMSR2_TPW)
            row = Shape[0]
            col = Shape[1]
            CHIRPS_path  = "E:\payan_name\Compelet-6 hr\CHIRPS_"+str(year)+"_"+moon+"_"+day+".tif"

            CMORPH_path  = "E:\payan_name\Compelet-6 hr\CMORPH_"+str(year)+"_"+moon+"_"+day+".tif"

            IMERG_path   = "E:\payan_name\Compelet-6 hr\IMERG_"+str(year)+"_"+moon+"_"+day+".tif"

            PDIR_path    = "E:\payan_name\Compelet-6 hr\PDIR_1d"+str(year)+moon+day+".tif"

            PDIR    =Image.open(PDIR_path)
            PDIR    =numpy.array(PDIR)
            CHIRPS  =tifffile.imread(CHIRPS_path)
            CHIRPS  =numpy.array(CHIRPS)
            CMORPH  =tifffile.imread(CMORPH_path)
            CMORPH  =numpy.array(CMORPH)
            IMERG   =tifffile.imread(IMERG_path)
            IMERG   =numpy.array(IMERG)
            
            for i in range(row):
                print(AMSR2_TPW["V"][i])
                if str(AMSR2_TPW["V"][i]) != 'nan':

                    x=float(AMSR2_TPW["Long"][i])
                    y=float(AMSR2_TPW["Lat"][i])

                    i_imerg=int(math.floor((y-IMERG_param["top"])/(-IMERG_param["res"])))
                    j_imerg=int(math.floor((x-IMERG_param["left"])/IMERG_param["res"]))

                    i_cmorph=int(math.floor((y-CMORPH_param["top"])/(-CMORPH_param["res"])))
                    j_cmorph=int(math.floor((x-CMORPH_param["left"])/CMORPH_param["res"]))

                    i_pdir=int(math.floor((y-PDIR_param["top"])/(-PDIR_param["res"])))
                    j_pdir=int(math.floor((x-PDIR_param["left"])/PDIR_param["res"]))

                    i_chirps=int(math.floor((y-CHIRPS_param["top"])/(-CHIRPS_param["res"])))
                    j_chirps=int(math.floor((x-CHIRPS_param["left"])/CHIRPS_param["res"]))

                    if IMERG[i_imerg,j_imerg]<1000 and IMERG[i_imerg,j_imerg]>-1000  and CHIRPS[i_chirps,j_chirps]>-500 :
                        Name = AMSR2_TPW["NAME"][i]
                        for gauge in range(len(Rain_gauge)):
                            if Rain_gauge["Name"][gauge] == Name :

                                edm = int(G[Name][2])
                                Ts  = float(AMSR2_TPW["Ts"][i])
                                V   = float(AMSR2_TPW["V"][i])
                                pwv = float(AMSR2_TPW["PWV"][i])
                                P   = float(Rain_gauge["Rain"][gauge])
                                BT_89v=float(AMSR2_TPW["BT 89 v"][i])
                                BT_36v=float(AMSR2_TPW["BT 36 v"][i])
                                BT_23v=float(AMSR2_TPW["BT 23 v"][i])
                                BT_18v=float(AMSR2_TPW["BT 18 v"][i])

                                BT_89h=float(AMSR2_TPW["BT 89 h"][i])
                                BT_36h=float(AMSR2_TPW["BT 36 h"][i])
                                BT_23h=float(AMSR2_TPW["BT 23 h"][i])
                                BT_18h=float(AMSR2_TPW["BT 18 h"][i])
                                logterm = float(AMSR2_TPW["log10(dT89/dT36)"][i])
                                Complete.append([ P  , pwv , Ts  , V , IMERG[i_imerg,j_imerg] , 
                                CMORPH[i_cmorph,j_cmorph] , CHIRPS[i_chirps,j_chirps] , PDIR[i_pdir,j_pdir] ,
                                BT_89v , BT_36v ,BT_23v, BT_18v ,logterm ,BT_89h , BT_36h ,BT_23h, BT_18h,
                                Day,Month,year ])
                                # Merg = MERGE(pwv, Ts , IMERG[i_imerg,j_imerg],CMORPH[i_cmorph,j_cmorph] , CHIRPS[i_chirps,j_chirps] , PDIR[i_pdir,j_pdir] )
                                vec_pr.append(P)
                                Merg =  IMERG[i_imerg,j_imerg] 
                                #Merg = Seasonal_func( pwv , Ts , IMERG[i_imerg,j_imerg] , CMORPH[i_cmorph,j_cmorph] , CHIRPS[i_chirps,j_chirps] , PDIR[i_pdir,j_pdir] ,int((Month-1)/3)+1)
                                if Merg<0: Merg=0.0
                                MODEL.append(Merg)
                                OBS.append(P)
                                if Merg  <0 : Merg = 0
                                Station_P[i].append(P)
                                Station_PWV[i].append(Merg )

                                season= int((Month-1)/3)
                                Season_P[season].append(P)
                                Season_PWV[season].append(Merg)

                                Climate_Obs[edm-1].append(P)
                                Climate_Model[edm-1].append(Merg)
                                
                                # if P>0.1:
                                #     if Name in North :
                                #         A["North"]+=1
                                #     else :
                                #         A["Other"]+=1                          
                                # if P>0 and P<=5:
                                #     S_Pr_c[Season]["0-5"] +=1
                                # elif P>5 and P<=10:
                                #     S_Pr_c[Season]["5-10"] +=1
                                # elif P>10 and P<=15:
                                #     S_Pr_c[Season]["10-15"] +=1
                                # elif P>15 and P<=20:
                                #     S_Pr_c[Season]["15-20"] +=1
                                # elif P>20 :
                                #     S_Pr_c[Season][">20"] +=1


            # if len(vec_pr)!=0:
            #     mean_pr= sum(vec_pr)/len(vec_pr)
            #     iran_pr.append([mean_pr,Day,Month,year])


thl=[0,5,10,15,20,1000]
Output_by_stations = [ 
    [ "NAME" , "RMSE" , "ρ" , "NSE" , "POD" , "FAR" , "BIAS","CSI","Dc" , "D" , "p_value" , 'MBE' ,'kge'] 
    ]
print(A)
# for i in range(4):
#     print(S_Pr_c[i])

for st in range(row):
    
    c    = correlation(Station_P[st],Station_PWV[st])

    rmse = function_RMSE(Station_P[st],Station_PWV[st])

    nse  = function_Ens(Station_PWV[st],Station_P[st])

    pod  = POD(Station_P[st],Station_PWV[st])

    far  = FAR(Station_P[st],Station_PWV[st])

    bias = BIAS(Station_P[st],Station_PWV[st])

    csi = CSI(Station_P[st],Station_PWV[st])
    
    kge = de.kge.calc_kge(Station_P[st],Station_PWV[st])
    
    mbe = MBE(Station_P[st],Station_PWV[st])

    DKs = Reza.Kolomogrov_Smirnov_2sample(Station_P[st],Station_PWV[st],thl)
    n = len(Station_P[st])
    D = sqrt(-log(α_ks/2)*0.5)*(sqrt(2/n))
    t_p = Reza.Average_tTest(Station_P[st],Station_PWV[st])
    p_value = t_p[1]

    Output_by_stations.append([ AMSR2_TPW["NAME"][st] , rmse , c , nse , pod , far ,bias,csi  , DKs , D  , p_value])

Seasons =[ "Winter" , "Spring" , "Summer" , "Atumn"] 

Output_by_season = [ 
    [ "Season" , "RMSE" , "ρ" , "NSE" , "POD" , "FAR" , "BIAS","CSI","Dc","D","p_value"  , 'mbe' ,'kge'] 
    ]

for s in range(4):
    c    = correlation(Season_P[s],Season_PWV[s])

    rmse = function_RMSE(Season_P[s],Season_PWV[s])

    nse  = function_Ens(Season_PWV[s],Season_P[s])

    pod  = POD(Season_P[s],Season_PWV[s])

    far  = FAR(Season_P[s],Season_PWV[s])

    bias = BIAS(Season_P[s],Season_PWV[s])

    csi = CSI(Season_P[s],Season_PWV[s])
    
    mbe  = MBE(Season_P[s],Season_PWV[s])
    kge = de.kge.calc_kge(Station_P[st],Station_PWV[st])
    
    DKs = Reza.Kolomogrov_Smirnov_2sample(Season_P[s],Season_PWV[s],thl)
    n=len(Season_P[s])
    D = sqrt(-log(α_ks/2)*0.5)*(sqrt(2/n))
    pks=1-2*exp(-n*DKs**2)
    t_p = Reza.Average_tTest(Season_P[s],Season_PWV[s])
    p_value = t_p[1]
    dk=stats.ks_2samp(Season_P[s],Season_PWV[s])
    Output_by_season.append( [  Seasons[s] , rmse , c , nse , pod , far ,bias,csi,DKs,D, pks , mbe, kge] )
import Reza


c    = correlation(OBS,MODEL)

rmse = function_RMSE(OBS,MODEL)

nse  = function_Ens(MODEL,OBS)

pod  = Reza.POD(OBS,MODEL)

far  = Reza.FAR(OBS,MODEL)

bias = BIAS(OBS,MODEL)

csi = CSI(OBS,MODEL)

kge = de.kge.calc_kge(OBS,MODEL)

mbe = MBE(OBS,MODEL)

DKs = Reza.Kolomogrov_Smirnov_2sample(OBS, MODEL, thl)
n=len(OBS)
D = sqrt(-log(α_ks/2)*0.5)*(sqrt(2/n))
pks=1-2*exp(-n*DKs**2)
t_p = Reza.Average_tTest(OBS,MODEL)
p_value = t_p[1]
dk=stats.ks_2samp(OBS,MODEL)

Output_by_season.append( [  "Complete" , rmse , c , nse , pod , far ,bias , csi, DKs,D,pks  , mbe,kge] )

Edm_name = ["A1.1","A1.2","A2","A3","A4","A5","A6","A7"]
Output_by_climate=[ ["Climate" , "RMSE" , "ρ" , "NSE" , "POD" , "FAR" , "BIAS","CSI","Dc","D","p_value",'mbe' ,'kge' ]]

for i in range(8):

    c    = correlation(Climate_Obs[i],Climate_Model[i])

    rmse = function_RMSE(Climate_Obs[i],Climate_Model[i])

    nse  = function_Ens(Climate_Model[i],Climate_Obs[i])

    pod  = POD(Climate_Obs[i],Climate_Model[i])

    far  = FAR(Climate_Obs[i],Climate_Model[i])

    bias = BIAS(Climate_Obs[i],Climate_Model[i])

    csi = CSI(Climate_Obs[i],Climate_Model[i])
    
    kge = de.kge.calc_kge(Climate_Obs[i],Climate_Model[i])
    
    mbe = MBE(Climate_Obs[i],Climate_Model[i])

    DKs = Reza.Kolomogrov_Smirnov_2sample(Climate_Obs[i],Climate_Model[i], thl)

    t_p = Reza.Average_tTest(Climate_Obs[i],Climate_Model[i])
    p_value = t_p[1]
    n=len(Climate_Obs[i])
    D = sqrt(-log(α_ks/2)*0.5)*(sqrt(2/n))
    Output_by_climate.append( [  Edm_name[i] , rmse , c , nse , pod , far ,bias , csi, DKs, D  , p_value,mbe,kge] )


Output_by_stations = numpy.array(Output_by_stations)
Reza.Mat_Write(Output_by_stations, "E:\payan_name\AMSR2-TPW\Cal-test\Out_Station.xlsx")

Output_by_climate = numpy.array(Output_by_climate)
Reza.Mat_Write(Output_by_climate, "E:\payan_name\AMSR2-TPW\Cal-test\Out_Climate.xlsx")

Complete=numpy.array(Complete)
iran_pr = numpy.array(iran_pr)
Reza.Mat_Write( Complete , "E:\payan_name\AMSR2-TPW\Cal-test\P,PWV_"+"2014-2018"+"_period_pwv,imerg,cmorph.xlsx")

Output_by_season = numpy.array(Output_by_season)
Reza.Mat_Write(Output_by_season, "E:\payan_name\AMSR2-TPW\Cal-test\Out_season.xlsx")



