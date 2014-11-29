
########### Suma V 2.0-- de PARAPULPO. sum all 24 chanel from the LAGO Data.
########### Made for Chacaltaya's data until 2011.

import numpy as np
import os
import csv
import sys
from astropy.time import Time
import datetime

def Sidereal(value):#overall gps time ti sidereal time
  result= float()
  tunix = value +315964800 # gps time to unix time
  hour = Time(tunix, format='unix', location=('-68.131389', '-16.353333')) # defines object "hour" needed in astropy
  Side = str( hour.sidereal_time('mean') ) #trasform to sidereal time
  if Side[1]=='h':
    A = Side
    result = (float(A[0])*3600)+(float(A[2:4])*60)+(float(A[5:7]))
  if Side[2]=='h':
    A = Side
    result = (float(A[0:2])*3600)+(float(A[3:5])*60)+(float(A[6:8]))
  return int(result)

#build the day array separated in seconds

SiDAY=24*3600# the sidereal day is actually shorter but this will do the trick
#this is the array of every second in the sidereal day
linea=[0 for i in range(0,25)]
Arreglo=[[0 for i in range(0,25)] for i in range(0,SiDAY+1)]#builds a matriz of 25x86401
CHequeo=[0 for i in range(0,SiDAY)] #this will be the last row

#inicializing necesary variables
sum = 0
sum2 = 0
sum3 = 0
h = 1 #how many times has the same second appeared
canal = 1 #chanell of the data that will be sumated
i=0 #the second in the sidereal day array
TIM=int() #this is the second that is being sumated at the moment

#Define Path of the files that wold be analised
Path=str(sys.argv[1])
files=os.listdir(Path)
a=0

for fn in files:#goes from file to file
  if fn[0:3]!='CHA' or len(fn)!=27:#ignore ignorable files
    a=a+1
    print '# ', a, len(fn),'ignoring '+fn
    continue
  os.system('gunzip -dc '+Path+fn+'>'+Path+fn[0:24])#uncompress .gz files
  tiempo=datetime.datetime.now()
  mes=int(fn[9:11])
 # if mes < inf or mes > sup: #uncoment if month fileting needed.
 #    continue
  print '# ', fn , tiempo
  archiv = open(Path+fn[0:24])#opens each file
  for aline in archiv:#goes from line to line inside every file
    if len(aline)<65:#ignore incomplete lines
      continue
    row = aline.split() #split line in rows
    if row[0]=='#':
      continue
    if int(row[24])==TIM: #continues sumation if still on the same second
      h+=1
      for i in range(0,24):
         linea[i]+=float(row[i])
    else: #if pases to next second
      j = Sidereal(int(row[24]))#sidereal second that is being sumated
      for i in range(0,24): #prints completed second and starts next

         Arreglo[j][i]+=(float(linea[i]))/h #print each element of the sumated second
         linea[i]=float(row[i])
      Arreglo[j][24]+=1 #checking column
      
      h=1#restart counter
      
      TIM=int(row[24])#new second new TIM
  os.system('rm '+Path+fn[0:24])



for j in range(0,int(SiDAY)):
   if Arreglo[j][1]>0:
      list=[]
      for i in range(0,25):
          list.append(str("%.1f" %Arreglo[j][i]))
      
      print j, ' '.join(list) 

#with open("Sumatoria"+str(sys.argv[4])+".dat","a") as f:
#      f.write("# # here the result of the sideral sumation \n")
#      f.write("# # structure i, value \n")
#      for i in range(0,int(SiDAY)):
#          fila=[i+1,array[i],' ']
#          w = csv.writer(f,delimiter=' ')
#          w.writerow(fila)


hi=str(sys.argv[2])
os.system('touch /home/'+hi[0:2]+'/anunez/Sumatorias/'+hi+'/libre')
                      



