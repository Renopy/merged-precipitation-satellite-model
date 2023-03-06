

import numpy
import tifffile

# Channel dimension should come first
left =44
top = 40
right =64
bottom = 25
res = 0.1
Row =int((top-bottom)/res)
Column =int((right-left)/res)

Shape = ( Row, Column  )
long = numpy.zeros( Shape , float)
lat = numpy.zeros( Shape , float)



for i in range(Row) :
    for j in range(Column):
        long[i,j] = j*res+left
        lat[i,j] = top - i*res
A = [ long , lat]
A =numpy.array(A , float)

tifffile.imsave('Long,Lat_Model[1].tiff', A)

txt = open( "long,lat.txt" , "w")
txt.write( "AMSR2 longitude and latitude Raster")
txt.write("\n Number of bands : 2")
txt.write("\n Row, Column :  60 , 80")
txt.write("\n Band 1 : Longitude ")
txt.write("\n Band 2 : Latitude ")
txt.write("\n Resolution : 0.25 Degree")
txt.write("\n Image type : tiff")
txt.write("\n data type : float")
txt.close
