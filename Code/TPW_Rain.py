

import Reza
import numpy
import sys
import math


def BIAS(Obs,Product):
    N=len(Obs)
    F=0.0
    H=0.0
    M=0.0
    for i in range(N):
        O=float(Obs[i])
        P=float(Product[i])
        if O>=1 and P>=1 :  H=H+1
        if O<1 and P>=1 :   F=F+1
        if O>=1 and P<1 :   M=M+1
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
    for i in range(N):
        O=float(Obs[i])
        P=float(Product[i])
        if O>=1 and P>=1 :  H=H+1
        if O<1 and P>=1 :   F=F+1
        if O>=1 and P<1 :   M=M+1
    try:
        csi=(H)/(H+M+F)
    except:
        csi="Undefined"
    return csi

def FAR(Obs,Product):
    N=len(Obs)
    F=0.0
    H=0.0
    for i in range(N):
        O=float(Obs[i])
        P=float(Product[i])
        if O>=1 and P>=1 :  H=H+1
        if O<1 and P>=1 :   F=F+1
    try:
        far=(F)/(F+H)
    except:
        far="Undefined"
    return far


def POD(Obs,Product):
    N=len(Product)
    H=0
    M=0
    Threshold=[1,1]
    for i in range(N):
        O=float(Obs[i])
        P=float(Product[i])
        if O>=Threshold[0] and P>=Threshold[1] :  H=H+1
        if O>=Threshold[0] and P<Threshold[1]  :  M=M+1
    try:
        pod=float(H)/float(H+M)
    except:
        pod="Undefined"
    return pod

def ZPD(Obs,Product):
    N=len(Product)
    Z=0
    nunZ=0
    for i in range(N):
        O=float(Obs[i])
        P=float(Product[i])
        if O<1 and P<1 :  Z=Z+1
        if O<1 and P>=1 :   nunZ=nunZ+1
    try:
        zpd=float(Z)/float(Z+nunZ)
    except:
        zpd="Undefined"
    return zpd

def function_RMSE(Obs,Model):
    N=len(Model)
    se=0.0
    for k in range(N):
        se=se+(Model[k]-Obs[k])**2
    try:
        mse=se/N
        rmse=mse**0.5
    except:
        rmse="Undefined"
    return rmse

def function_Ens(Model,Obs):
    N=len(Model)
    se=0.0
    for k in range(N):
        se=se+(Model[k]-Obs[k])**2
    S=0.0
    μ=Mean(Obs)
    for k in range(N):
        S=S+(Obs[k]-μ)**2
    try:
        Ens=1-se/S
    except:
        Ens="Undefined"
    return Ens

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


daynum=["",32,29,32,31,32,31,32,32,31,32,31,31]
MonthName=['Jan','Feb','March','April',"ΜΑΥ",'Jun','July','Aug','September','Octobr','November',"December"]
year = 2014
yr   = str(year)
P=["P"]
V=["V"]
Logterm=["logterm"]
Ts=["Ts"]
TPW=["TPW"]
Station_TPW=[]
Station_P=[]

for i in range(81):
    Station_TPW.append([])
    Station_P.append([])

for Month in range(1,3):
    for Day in progressbar(range(1,daynum[Month]),"Computing: ", 40):
        if Month<10:    moon="0"+str(Month)
        else:           moon=str(Month)
        if Day<10:      day="0"+str(Day)
        else:           day=str(Day)
        path_TPW = "AMSR2_TPW_"+yr+"_"+moon+"_"+day+".xlsx"
        path_Pre = "gauge\Rain_Gauges_"+yr+"_Month"+str(Month)+"_Day"+str(Day)+".xlsx"

        AMSR2_TPW = Reza.Matread(path_TPW)
        Rain_gauge= Reza.Matread(path_Pre)

        Shape =  numpy.shape(AMSR2_TPW)
        row = Shape[0]
        col = Shape[1]

        for i in range(1,row):
            if AMSR2_TPW[i,3]!="noValue":
                Ts.append(float(AMSR2_TPW[i,4]))
                V.append(float(AMSR2_TPW[i,5]))
                Logterm.append(float(AMSR2_TPW[i,6]))
                TPW.append(float(AMSR2_TPW[i,3]))
                P.append(float(Rain_gauge[i-1,8]))
        for st in range(0,row-1):
            if AMSR2_TPW[st+1,3]!="noValue":
                Station_TPW[st].append(float(AMSR2_TPW[st+1,3])**2)
                Station_P[st].append(float(Rain_gauge[st,8]))

Output_by_stations=[[ "NAME" , "RMSE" , "ρ" , "NSE" ]]

for st in range(row-1):

    c    = correlation(Station_P[st],Station_TPW[st])

    rmse = function_RMSE(Station_P[st],Station_TPW[st])

    nse  = function_Ens(Station_P[st],Station_TPW[st])

    Output_by_stations.append([ AMSR2_TPW[st+1,0] , rmse , c , nse])

Output_by_stations = numpy.array(Output_by_stations)

Reza.Mat_Write(Output_by_stations, "Out.xlsx")
X=[TPW , P ]
X=numpy.array(X)
X=numpy.transpose(X)
Reza.Mat_Write(X, "PWV,P.xlsx")
Y=[P,Ts,V,Logterm]
Y=numpy.array(Y)
Y=numpy.transpose(Y)
Reza.Mat_Write(Y, "Ts,V,Logterm.xlsx")



