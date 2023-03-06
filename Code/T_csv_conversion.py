import os
import pandas as pd
import numpy

Folder='T_csv/'
entries = os.listdir(Folder)

X= pd.read_csv(Folder+entries[1])
X=numpy.array(X)
print(X[0])