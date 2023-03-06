

import numpy
import h5py
import tifffile
import os 
import math
from math import *
def Dis(X1,Y1,X2,Y2):
    d=((X1-X2)**2+(Y1-Y2)**2)**0.5
    return d


def sec(x):
    Sec=1/cos(x)
    return Sec

daynum=["",32,29,32,31,32,31,32,32,31,32,31,31]
MonthName=["",'Jan','Feb','March','April'," May",'Jun','July','Aug','September','Octobr','November',"December"]

Folder = 'New folder/'
entries = os.listdir(Folder)

long_lat = tifffile.imread('Long,Lat.tiff')
long = long_lat[0]
lat = long_lat[1]
Shape=numpy.shape(long)
row = Shape[0]
column = Shape[1]
number = 0
start_number = 0
for Input in entries:
    number+=1
    fp=Folder+Input
    INP=list(Input)
    yr=INP[7]+INP[8]+INP[9]+INP[10]
    moon=INP[11]+INP[12]
    day=INP[13]+INP[14]
    h5 = h5py.File(fp, 'r+')
    Month = int(moon)
    if number>=start_number:

        
        AMSR2 = {
            "long" : numpy.array(h5['Longitude of Observation Point for 89B']),
            "lat"  : numpy.array(h5['Latitude of Observation Point for 89B'])
        }

        BT_89h=numpy.array(h5["Brightness Temperature (res06,89.0GHz,H)"])
        BT_89v=numpy.array(h5["Brightness Temperature (res06,89.0GHz,V)"])

        BT_23h=numpy.array(h5["Brightness Temperature (res06,23.8GHz,H)"])
        BT_23v=numpy.array(h5["Brightness Temperature (res06,23.8GHz,V)"])

        BT_18h=numpy.array(h5["Brightness Temperature (res06,18.7GHz,H)"])
        BT_18v=numpy.array(h5["Brightness Temperature (res06,18.7GHz,V)"])

        BT_36h=numpy.array(h5["Brightness Temperature (res06,36.5GHz,H)"])
        BT_36v=numpy.array(h5["Brightness Temperature (res06,36.5GHz,V)"])

        incidence= numpy.array(h5[ "Earth Incidence" ])
        Image = numpy.zeros( ( 9 ,row , column) , dtype=float)

        for i in range(row):
            for j in range(column):
                x=long[i,j]
                y=lat[i,j]
                #___________________________

                D = Dis(X1=x, Y1=y , X2=AMSR2["long"] , Y2=AMSR2["lat"])
                MinValue = numpy.amin(D)
                Index = numpy.where(D == numpy.amin(D))
                I = Index[0][0]
                J = int(Index[1][0]/2.00)

                #___________________________
                
                if MinValue<=0.177 : 
                    Image[0,i,j] = BT_18h[I,J]
                    Image[1,i,j] = BT_18v[I,J]
                    Image[2,i,j] = BT_23h[I,J]
                    Image[3,i,j] = BT_23v[I,J]
                    Image[4,i,j] = BT_36h[I,J]
                    Image[5,i,j] = BT_36v[I,J]
                    Image[6,i,j] = BT_89h[I,J]
                    Image[7,i,j] = BT_89v[I,J]
                    Image[8,i,j] = incidence[I,J]
                else : 
                    Image[0,i,j] = -99
                    Image[1,i,j] = -99
                    Image[2,i,j] = -99
                    Image[3,i,j] = -99
                    Image[4,i,j] = -99
                    Image[5,i,j] = -99
                    Image[6,i,j] = -99
                    Image[7,i,j] = -99
                    Image[8,i,j] = -99
        
        Opf = "AMSR2_BT_"+yr + "_" + moon + "_"+ day + ".tiff"
        tifffile.imsave( Opf , Image)

        metadata = "AMSR2_BT_"+yr + "_" + moon + "_"+ day + ".mtd.txt"

        txt= "#-----------AMSR2 BrightnessTemprature Ascending path-----------#\n"
        txt0= "\n Processing Date :" 
        txt1="\n#----------- Bands Information -----------#\n"
        txt2="\n Band 1 : 18 GHz horizontal" + "\n Band 2 : 18 GHz vertical" +"\n Band 3 : 23 GHz horizontal" + "\n Band 4 : 23 GHz vertical" 
        txt3="\n Band 5 : 36 GHz horizontal" + "\n Band 6 : 36 GHz vertical" +"\n Band 7 : 89 GHz horizontal" + "\n Band 8 : 89 GHz vertical"
        txt4="\n Band 9 : incidence angle"   
        txt5="\n#----------- Geometric Information -----------#\n"
        txt6="\n left=44 E"+ "\n right=64 E "+ "\n top=40 N"+ "\n bottom=25 N" + "\n Resolution=0.25 "
        txt7="\n#----------- Data Information -----------#\n"
        txt8="\n Image Format : Tiff" +"\n Image Shape : 60x80" + "\n Data digital type : Float" + "\n No value : -99" 
        mm= str(MonthName[Month])
        txt_file = open(metadata,"w")
        txt_file.write(txt)
        txt_file.write(txt0)
        txt_file.write( yr)
        txt_file.write("_")
        txt_file.write( mm )
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
        
        txt_file.close()

