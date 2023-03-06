import h5py
import numpy
import xlsxwriter
import Reza
import sys
import time
import pandas as pd
# AMSR2 Brightness Temperature

def Dis(X1,Y1,X2,Y2):
    d=((X1-X2)**2+(Y1-Y2)**2)**0.5
    return d

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
import os
Folder = 'New Folder/'
entries = os.listdir(Folder)
II = 0
Num=0

for Input in entries:
    II=II+1
    if II>Num :

        fp=Folder+Input
        INP=list(Input)
        yr=INP[7]+INP[8]+INP[9]+INP[10]
        moon=INP[11]+INP[12]
        day=INP[13]+INP[14]
        print(yr+" "+MonthName[int(moon)-1]," ", day)
        try:
            
            h5 = h5py.File(fp, 'r+')

            Lat = numpy.array(h5['Latitude of Observation Point for 89B'])
            Long= numpy.array(h5['Longitude of Observation Point for 89B'])

            Gauge= pd.read_excel("Stations_long,lat.xlsx")
            Numberg=len(Gauge)
            

            Output=[["Name" , "BT 18 H" , "BT 18 V" , "BT 23 H" ,"BT 23 V" , "BT 36 H" , "BT 36 V" , "BT 89 H" , "BT 89 V" , "θ" ,"long"  , "lat"]]
            Shape=numpy.shape(Lat)
            Row=Shape[0]
            Column=Shape[1]
            
            for g in progressbar(range(Numberg) ,"Computing: ", 40):
                Name=Gauge["Name"][g]
                X=float(Gauge["long"][g])
                Y=float(Gauge["lat"][g])

                ##################################

                D = Dis(X1=X, Y1=Y , X2=Long, Y2=Lat)
                MinValue = numpy.amin(D)
                Index = numpy.where(D == numpy.amin(D))
                I = Index[0][0]
                J = int(Index[1][0]/2.00)

                ####################################
                
                if MinValue<=0.177 :

                    BT_89h=numpy.array(h5["Brightness Temperature (res06,89.0GHz,H)"])
                    BT_89v=numpy.array(h5["Brightness Temperature (res06,89.0GHz,V)"])

                    BT_23h=numpy.array(h5["Brightness Temperature (res06,23.8GHz,H)"])
                    BT_23v=numpy.array(h5["Brightness Temperature (res06,23.8GHz,V)"])

                    BT_18h=numpy.array(h5["Brightness Temperature (res06,18.7GHz,H)"])
                    BT_18v=numpy.array(h5["Brightness Temperature (res06,18.7GHz,V)"])

                    BT_36h=numpy.array(h5["Brightness Temperature (res06,36.5GHz,H)"])
                    BT_36v=numpy.array(h5["Brightness Temperature (res06,36.5GHz,V)"])

                    incidence= numpy.array(h5[ "Earth Incidence" ])

                    Output.append([ Name , BT_18h[I,J] , BT_18v[I,J] , BT_23h[I,J] , BT_23v[I,J] , BT_36h[I,J] , BT_36v[I,J] , BT_89h[I,J] , BT_89v[I,J] , incidence[I,J] , X , Y])
                else :
                    Output.append([ Name , "noValue" ,    "noValue" ,   "noValue" ,   "noValue" ,   "noValue" ,   "noValue" ,   "noValue" ,   "noValue" ,    "noValue" , X, Y])
        except : 
            print(yr,moon,day)
        Output=numpy.array(Output)
        Reza.Mat_Write(Output , "AMSR2_BT_"+yr+"_"+moon+"_"+day+".xlsx")



