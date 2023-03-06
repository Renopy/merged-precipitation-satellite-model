
import tifffile
import numpy 
import math
from math import *
import math


def sec(x):
    Sec=1/cos(x)
    return Sec


daynum=["",32,29,32,31,32,31,32,32,31,32,31,31]
MonthName=['Jan','Feb','March','April',"ΜΑΥ",'Jun','July','Aug','September','Octobr','November',"December"]

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


PWV = lambda V,dT89 , dT36 : 0.0186*V-28.7755*log10(dT89/dT36) + 0.0748

LL=tifffile.imread('Long,Lat.tiff')
long =LL[0]
lat = LL[1]

for year in range(2015,2016):
    yr=str(year)
    for Month in range(12,13):
        if Month<10:    moon="0"+str(Month)
        else:           moon=str(Month)
        for Day in range(24,daynum[Month]):

            if Day<10:      day="0"+str(Day)
            else:           day=str(Day)

            print(yr+"_"+moon+"_"+day,end="\r")

            fp = "AMSR2_BT_"+yr+"_"+moon+"_"+day+".tiff"
            Image = tifffile.imread(fp)
            Shape = numpy.shape(Image[0])
            Row = Shape[0]
            Column = Shape[1]
            PWV_Image = numpy.zeros(Shape,dtype=float)
            for i in range(Row):
                for j in range(Column):
                    if Image[0,i,j] > 0 :
                        BT_18h  = Image[0,i,j] 
                        BT_18v  = Image[1,i,j]
                        BT_23h  = Image[2,i,j] 
                        BT_23v  = Image[3,i,j]
                        BT_36h  = Image[4,i,j] 
                        BT_36v  = Image[5,i,j]
                        BT_89h  = Image[6,i,j] 
                        BT_89v  = Image[7,i,j]
                        θ  = Image[8,i,j]
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
                            pwv = -99
                        else:
                            try :
                                dT89=BT_89v-BT_89h
                                dT36=BT_36v-BT_36h
                                pwv = PWV(V , dT89 , dT36)
                            except :
                                pwv = -99
                                print("Check-->"+yr+"_"+moon+"_"+day ,"LL" ,long[i,j] , "," , lat[i,j])
                        
                    else : 
                        pwv = -999
                    PWV_Image[i,j]=pwv
            
            Opf = "AMSR2_PWV_"+yr + "_" + moon + "_"+ day + ".tiff"
            tifffile.imsave( Opf , PWV_Image)
