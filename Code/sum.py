import numpy
import tifffile

s="csi"

Folder = "E:\مقاله\GIS\Tiffs/"

imerg =tifffile.imread(  Folder+ 'imerg_'+s+'_s.tif')

cmorph =tifffile.imread(Folder+'cmorph_'+s+'_s.tif')

chirps  =tifffile.imread(Folder+'chirps_'+s+'_s.tif')

pdir =tifffile.imread(Folder+'pdir_'+s+'_s.tif')

m1 = tifffile.imread(Folder+'m1_'+s+'_s.tif')
m2 =tifffile.imread(Folder+'m2_'+s+'_s.tif')
m3= tifffile.imread(Folder+'m3_'+s+'_s.tif')
m4 =tifffile.imread(Folder+'m4_'+s+'_s.tif')
m5 =tifffile.imread(Folder+'m5_'+s+'_s.tif')

a1 =tifffile.imread(Folder+'a1_'+s+'_s.tif')
a2 =tifffile.imread(Folder+'a2_'+s+'_s.tif')
a3 =tifffile.imread(Folder+'a3_'+s+'_s.tif')
a4 =tifffile.imread(Folder+'a4_'+s+'_s.tif')
a5 =tifffile.imread(Folder+'a5_'+s+'_s.tif')


ZERO = imerg*0

#M5=tifffile.imread("D:\CSI\M5.tif")

# SCA = []
# PFA = []
# for i in range(5):
#     j=i+1
#     ras =  tifffile.imread("D:\R\Tiff\csi_m"+str(j)+"_sca.tif")
#     SCA.append(ras)
#     ras =  tifffile.imread("D:\R\Tiff\csi_m"+str(j)+"_pfa.tif")
#     PFA.append(ras)
# ras_shape=numpy.array(ras)

# v = [[ imerg ,  cmorph, pdir    ],
#      [ chirps,  M1,     M2      ],
#      [  M3,     M4,     M5      ], 
#      [SCA[0],   SCA[1], SCA[2]  ], 
#      [SCA[3],   SCA[4], PFA[0]  ],
#      [PFA[1],   PFA[2], PFA[3]  ], 
#      [PFA[4]                    ]  ]



v=[
  [  imerg  ,   cmorph , chirps],
  [  pdir    ,   m1  ,     m2  ],
  [  m3 ,        m4  ,     m5  ],
  [ a1 ,         a2 ,      a3  ],
  [ a4,          a5 ,      ZERO]   ]



background_value =0
print(background_value)

for row in  v:
    for img in row : 
        Shape = numpy.shape(img)
        print(Shape)

lag= 50 
row = len(v)*Shape[0]+(len(v)-1)*lag
col = 3*Shape[1]+2*lag

Arr = numpy.zeros(shape=(row,col),dtype=float)+background_value


for ii in range(len(v)):
    for jj in range(len(v[ii])):
        for i in range(Shape[0]):
            for j in range(Shape[1]):
                Arr[i+(Shape[0]+lag)*ii,j+(Shape[1]+lag)*jj]=v[ii][jj][i,j]

for i in range(row):
    for j in range(col):
        if (Arr[i,j]<=-1000) or ( i>=Shape[0] and i<=Shape[0]+lag) or (j>=Shape[1] and j<=Shape[1]+lag): 
            Arr[i,j]=background_value
print(numpy.min(Arr))        
        
OutputFile= 'E:/مقاله/GIS/Map/'+s+'.tif'
tifffile.imwrite(OutputFile,Arr)








