import numpy

import xlsxwriter
from math import *

import pandas as pd
π=3.14159


def Float(List):
    L=[]
    for i in range(len(List)):
        L.append(float(List[i]))
    return L


def BIAS(Obs,Product,threshold):
    Product = Float(Product)
    Obs = Float(Obs)
    N=len(Obs)
    F=0.0
    H=0.0
    M=0.0
    Th=threshold
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

def CSI(Obs,Product,threshold):
    Product = Float(Product)
    Obs = Float(Obs)
    N=len(Obs)
    F=0.0
    H=0.0
    M=0.0
    Th=threshold
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

def FAR(Obs,Product,threshold):
    Product = Float(Product)
    Obs = Float(Obs)
    N=len(Obs)
    F=0.0
    H=0.0
    Th=threshold
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

def POD(Obs,Product,threshold):
    Product = Float(Product)
    Obs = Float(Obs)
    N=len(Product)
    H=0
    M=0
    Th=threshold
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

def ZPD(Obs,Product,threshold):
    Product = Float(Product)
    Obs = Float(Obs)
    N=len(Product)
    Z=0
    nunZ=0
    Th=threshold
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
    Model = Float(Model)
    Obs = Float(Obs)
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
    Model = Float(Model)
    Obs = Float(Obs)
    N=len(Model)
    se=0.0
    for k in range(N):
        se=se+(Model[k]-Obs[k])**2
        
    S=0.0
    for k in range(N):
        S=S+(Obs[k]-Mean(Obs))**2
    try:
        Ens=1-se/S
    except:
        Ens="Undefined"
    return Ens

def sumlist(List):
    List = Float(List)
    S=0.0
    for member in List :
        S=S+member
    return S
def Mean(List):
    List = Float(List)
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
    List =Float(List)
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
    X=Float(X)
    Y=Float(Y)
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


def Matrix(row,column,value):
    x=[]
    y=[]
    for i in range(row):
        x=[]
        for j in range(column):
            x.append(value)
        y.append(x)
    y=numpy.array(y)
    return y

def Matread(Address):
    wb = xlrd.open_workbook(Address) 
    sheet = wb.sheet_by_index(0)
    x=[]
    y=[]
    for i in range(sheet.nrows):
        x=[]
        for j in range(sheet.ncols):
            try:
                value=float(sheet.cell_value(i, j))
            except:
                value=sheet.cell_value(i, j)
            x.append(value)
        y.append(x)
    y=numpy.array(y)
    return y

def Matread_all_Sheets(Input):
    Ex= pd.ExcelFile(Input)
    shN=Ex.sheet_names
    A=[]
    for sh in shN :
        sheet=pd.read_excel(Input,sheet_name=sh)
        A.append(numpy.array(sheet))
    A=numpy.array(A)
    return A


def rotate270(matrix):

    a=numpy.shape(matrix)
    Rotate=Matrix(a[1],a[0],0.0)
    for i in range(a[0]):
        for j in range(a[1]):
            Rotate[a[1]-j-1,i]=matrix[i,j]
    return Rotate

def subset(matrix,StartRow,EndRow,StartCol,EndCol):
    a=numpy.shape(matrix)
    Subset=Matrix(EndRow-StartRow,EndCol-StartCol,0.0)
    for i in range(EndRow-StartRow):
        for j in range(EndCol-StartCol):
            Subset[i,j]=matrix[i+StartRow,j+StartCol]
    return Subset

def Read_ASCII(Address,row,column,field):
    f=open(Address,"r")
    T=[]
    j=0
    α=0
    for ii in f :
        α=α+1
        if α>5 and j<row  :
            g=list(ii)
            j=j+1
            i=0
            for Kol in range(column):
                z=''
                for ι in range(field):
                    z=z+(g[i+ι])
                try:
                    d=float(z)
                except:
                    d=0.0
                T.append(d)
                i=i+field
    raster=[]
    I=-1
    for i in range(row):
        A=[]
        for j in range(column):
            I=I+1
            b=float(T[I])
            if b<0.0:
                b=0
            A.append(b)
        raster.append(A)
    raster=numpy.array(raster)
    return raster

def RMSE(Obs,Model):
    N=len(Model)
    se=0.0
    for k in range(N):  se=se+(Model[k]-Obs[k])**2
    try:
        mse=se/N
        rmse=mse**0.5
    except: 
        rmse="Undefined"
    return  rmse

def Mat_Write(matrix,OutputFile):
    workbook = xlsxwriter.Workbook(OutputFile)
    worksheet = workbook.add_worksheet()
    Shape=numpy.shape(matrix)
    row=Shape[0]
    column=Shape[1]
    for i in range(row):
        for j in range(column):
            try:
                worksheet.write( i , j , float(matrix[i,j] ))
            except : 
                worksheet.write( i , j , matrix[i,j] )
    workbook.close()


def P_value_normal(z):
    A=0.0
    delta=0.000001
    x=0
    x2=abs(z)
    f1=exp(-x**2/2)/(2*π)**0.5
    while x<x2 :
        x=x+delta
        f2=exp(-x**2/2)/(2*π)**0.5
        A=A+(f1+f2)*delta/2
        f1=f2
    A+=0.5
    return A

def Kolomogrov_Smirnov_test(Obs,Expect,Thresholds_list):
    List = Thresholds_list
    f_o = numpy.zeros(len(List), dtype=int)
    f_e = numpy.zeros(len(List), dtype=int)
    N = len(Obs)
    for i in range(len(List)):
        for j in range(len(Obs)):
            o=Obs[j]
            e=Expect[j]
            if i == 0 :
                if o<List[i]:
                    f_o[i]+=1
                if e<List[i]:
                    f_e[i]+=1
            elif i==len(List)-1:
                if o>=List[i]:
                    f_o[i]+=1
                if e>=List[i]:
                    f_e[i]+=1
            else:
                if o>=List[i-1] and o<List[i] :
                    f_o[i]+=1
                if e>=List[i-1] and e<List[i]:
                    f_e[i]+=1
    Dc = [ ]
    Fe = 0.0
    Fo = 0.0
    for i in range(len(List)):
        Fe +=f_e[i]/N
        Fo +=f_o[i]/N
        Dc.append(abs(Fe-Fo))
    D = max(Dc)
    return D

def LOG(List):
    log_L= []
    for a in List:
        log_L.append(log(a))
    return log_L

def Gamma_dis_param(List):
    x= []
    for y in List:
        if y>0:
            x.append(y)
    ε=10**(-10)
    N= len(List)
    x = numpy.array(x)
    Ln_List = LOG(x)
    A = log(Mean(x))-Mean(Ln_List)
    α =( 1+ sqrt(1+0.75*A))/(4*A)
    β = Mean(x)/α
    p = (α,β)
    return p

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

def Kolomogrov_Smirnov_CDF_test(Obs,Expect):
    O_p = Gamma_dis_param(Obs)
    E_p = Gamma_dis_param(Expect)
    Γα_o = Gamma(O_p[0])
    Γα_e = Gamma(E_p[0])
    G_o = lambda y :( y**(O_p[0]-1)*exp(-y/O_p[1]) ) / ( O_p[1]**O_p[0] *Γα_o  )
    G_e = lambda y : (y**(E_p[0]-1)*exp(-y/E_p[1])) / ( E_p[1]**E_p[0] * Γα_e )
    D = [ ]
    for i in range(int(max(Obs+Except))):
        t = i*1.0
        FO = Integral( Range=(0.001,t) , f = G_o , dx = 0.01  )
        FE = Integral( Range=(0.001,t) , f = G_e , dx = 0.01  )
        D.append( abs(FE-FO))
    Dc = max(D)
    return Dc





def Gamma(a):
    fz = lambda y : y**(a-1)*exp(-y)
    g = Integral( (0.0001 , 25 ) , fz , 0.01)
    return g

def Kolomogrov_Smirnov_2sample(sample_1,sample_2,Thresholds_List):

    N = len(sample_1)
    f_1 = numpy.zeros( len(Thresholds_List)  ,dtype=int)
    f_2 = numpy.zeros( len(Thresholds_List)  ,dtype=int)
    for j in range(N):
        for i in range(len(Thresholds_List)):
        
            if i!=len(Thresholds_List)-1:
                if sample_1[j]>=Thresholds_List[i] and sample_1[j]<Thresholds_List[i+1]:
                    f_1[i]+=1
                if sample_2[j]>=Thresholds_List[i] and sample_2[j]<Thresholds_List[i+1]:
                    f_2[i]+=1
            else :
                if sample_1[j]>=Thresholds_List[i] :
                    f_1[i]+=1
                if sample_2[j]>=Thresholds_List[i] :
                    f_2[i]+=1
    F_1=0.0
    F_2=0.0
    D=[]
    for i in range(len(Thresholds_List)-1):
        t=Thresholds_List[i+1]
        F_1+= f_1[i]/N
        F_2+= f_2[i]/N
        D.append(abs(F_1-F_2))
    Dc = max(D)
    return Dc

def Transpose(X):
    Shape = numpy.shape(X)
    X=numpy.array(X)
    T = numpy.zeros((Shape[1],Shape[0]))
    for i in range(Shape[0]):
        for j in range(Shape[1]):
            value = X[i,j]
            T[j,i]=value
    return T

def Average_tTest(sample_1,sample_2):
    a=[Mean(sample_1),Mean(sample_2)]
    s=[Variance(sample_1),Variance(sample_2)]
    N= [len(sample_1),len(sample_2)]
    t = (a[1]-a[0])/sqrt( s[0]**2/N[0]+s[1]**2/N[1])
    Normal = lambda y : exp(-0.5*y**2)/sqrt(2*π)
    P_value = 2*Integral( Range = (0,abs(t)) , f=Normal , dx=0.01)
    return (t,P_value)


def Sigma(f,k):
    S=0.0
    for i in range(k[0],k[1]):
        S+=f(i)
    return S

