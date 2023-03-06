
import numpy
import Reza
import math
from math import *
import sys
import os
from random import random
import imageio
import tifffile
import pandas as pd
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


daynum=["",32,29,32,31,32,31,32,32,31,32,31,31]
MonthName=['Jan','Feb','March','April',"ΜΑΥ",'Jun','July','Aug','September','Octobr','November',"December"]

def sec(x):
    Sec=1/cos(x)
    return Sec



PWV = lambda V,dT89 , dT36 : -0.007601991*V-8.769553773*log10(dT89/dT36) -0.939231339
# [1] 0.32+0.1*Ts+0.08*V-26.78*log10(dT89/dT36)
# [3] 0.0365*V+0.0092*V**2-5.58*10**(-6)*V**3-1.103*10**(-6)*V**4+0.3406
# [4] -0.0518*BT89v + 0.00127*BT89v**2- 3.5529*10**(-6)*BT89v**3

Gauge= pd.read_excel("Stations_long,lat.xlsx")
Keys = pd.DataFrame.keys(Gauge)
Numberg=len(Gauge)

Shape_G=numpy.shape(Gauge)


ω = 0.05 
ε_osh_18 = 0.771
ε_osh_23 = 0.781
ε_osv_18 = 0.994
ε_osv_23 = 0.975

ε_wv_18 = 0.630
ε_wv_23 = 0.685

ε_wh_18 = 0.336
ε_wh_23 = 0.421

αv_18 = 0.0034 
αv_23 = 0.0104

αo_18 = 0.0103 
αo_23 = 0.0131

δ  = 0.96


# Surface Temp MERRA

X1=44.00
X2=64.00
Y1=40.00
Y2=25.00
ax=0.625
ay = -0.5
#___________________________

for year in range(2014,2021):
    yr=str(year)
    for Month in range(1,13):
        print(MonthName[Month-1], " ", year)
        for Day in progressbar(range(1,daynum[Month]),"Computing: ", 40):
            
            if Month<10:    moon="0"+str(Month)
            else:           moon=str(Month)
            if Day<10:      day="0"+str(Day)
            else:           day=str(Day)

            Input= "AMSR2_BT_"+yr+"_"+moon+"_"+day+".xlsx"

            E=pd.read_excel(Input)

            O = [[ "NAME", "Long" , "Lat" , "PWV" , "Ts" , "V" , 
                "BT 89 v", "BT 36 v" ,"BT 23 v", "BT 18 v" , "log10(dT89/dT36)" , " H ",
                "BT 89 h", "BT 36 h" ,"BT 23 h", "BT 18 h"]]

            for i in range(0,len(E)):
                if E["BT 18 V"][i] != "noValue":

                    BT_18h = float(E["BT 18 H"][i]) 
                    BT_18v = float(E["BT 18 V"][i]) 

                    BT_23h = float(E["BT 23 H"][i]) 
                    BT_23v = float(E["BT 23 V"][i]) 

                    BT_36h = float(E["BT 36 H"][i]) 
                    BT_36v = float(E["BT 36 V"][i]) 

                    BT_89h = float(E["BT 89 H"][i]) 
                    BT_89v = float(E["BT 89 V"][i]) 

                    θ = float(E["θ"][i]) 
                    IF=False
                    β0= 0.88

                    it = 0
                    try :
                        while IF is False :
                            it+=1
                            β=β0
                            MAWVI=(BT_23v-BT_23h)/(BT_18v-BT_18h)
                            #print(β)
                            V = (log(MAWVI/β)*cos(θ)+αo_23-αo_18)/(αv_18-αv_23)

                            Ao_18=αo_18
                            Av_18=αv_18*V

                            Ao_23 = αo_23
                            Av_23 = αv_23*V

                            τ_18 = sec(θ)*(Ao_18+Av_18)
                            τ_23 = sec(θ)*(Ao_23+Av_23)

                            ta_18 = exp(-τ_18)
                            ta_23 = exp(-τ_23)

                            Fh = BT_23h/BT_18h
                            P  = BT_18h/BT_18v

                            Ap = ta_18*(P*ε_wv_18-ε_wh_18)
                            Af = ta_18*Fh*ε_wh_18-ta_23*ε_wh_23
                            Bp = (1-ta_18)*(1-P)*δ
                            Bf = ((1-ta_23)-Fh*(1-ta_18))*δ
                            Cp = ta_18*(1-ω)*(1-P)
                            Cf = (1-ω)*(ta_23-ta_18*Fh)
                            Dp = ta_18*(ε_osh_18-1+ω)-P*(ε_osv_18-1+ω)
                            Df = ta_23*(ε_osh_23-1+ω)-ta_18*Fh*(ε_osh_18-1+ω)

                            tc = ( Ap*(Bf+Cf)-Bp*(Af+Cf)+Cp*(Bf-Af))/(Dp*(Af-Bf)+Df*(Bp-Ap))

                            εl_h_18 = ε_osh_18*tc+(1-ω)*(1-tc)
                            εl_v_18 = ε_osv_18*tc+(1-ω)*(1-tc)

                            εl_h_23 = ε_osh_23*tc+(1-ω)*(1-tc)
                            εl_v_23 = ε_osv_23*tc+(1-ω)*(1-tc)

                            fw = (Bp+ta_18*(εl_h_18-P*(εl_v_18)))/(ta_18*( P*(ε_wv_18-εl_v_18)+(εl_h_18-ε_wh_18)))

                            εs_h_18 = fw*ε_wh_18+(1-fw)*εl_h_18
                            εs_v_18 = fw*ε_wv_18+(1-fw)*εl_v_18

                            εs_h_23 = fw*ε_wh_23+(1-fw)*εl_h_23
                            εs_v_23 = fw*ε_wv_23+(1-fw)*εl_v_23

                            β = (εs_v_23-εs_h_23)/(εs_v_18-εs_h_18)
                            Δ = abs(β-β0)
                            β0= β
                            if Δ<=0.001 :
                                IF = True
                            if it==2000 :
                                V = "No_value"  
                                IF = True

                    except:
                        V = "No_value" 
                    
                    if V == "No_value" :
                        pwv = "No_value"
                    else:
                        try :
                            dT89=BT_89v-BT_89h
                            dT36=BT_36v-BT_36h
                            pwv = PWV(V , dT89 , dT36)
                        except :
                            pwv = "No_value"
                            print("Check-->"+yr+"_"+moon+"_"+day ,"LL" ,long[i,j] , "," , lat[i,j])  
                    Temp = tifffile.imread("E:\payan_name\MERRA\MERRA_Temp"+"_"+day+"_"+moon+"_"+yr+".tiff")
                    Temp=numpy.array(Temp)

                    c=int(math.floor((float(E["long"][i])-X1)/ax))
                    r=int(math.floor((float(E["lat"][i])-Y1)/ay))

                    Ts=Temp[r,c]
                    H=Gauge["H"][i]
                    
                    dT23=BT_23v-BT_23h
                    dT18=BT_18v-BT_18h
 

                    O.append([ E["Name"][i], E["long"][i] , E["lat"][i] , pwv, Ts , V ,  BT_89v ,BT_36v,BT_23v,BT_18v , log10(dT89/dT36)  , H,  BT_89h ,BT_36h,BT_23h,BT_18h ])
                else:
                    O.append([ E["Name"][i], E["long"][i] , E["lat"][i] , "noValue" , "noValue" , "noValue" ,  "noValue" ,  "noValue" , "noValue",   "noValue" ,   "noValue" ,   "noValue", "noValue",   "noValue" ,   "noValue" ,   "noValue"  ])
            O = numpy.array(O)
            Output = "AMSR2_TPW_"+yr+"_"+moon+"_"+day+".xlsx"
            Reza.Mat_Write(O,Output)




