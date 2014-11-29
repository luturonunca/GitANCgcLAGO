import numpy as np
import csv
import os
import sys
import time
import chalib

T=0
altura=0


def oruga(A,w):#A es la ventana y w el ancho de esta
      for i in range(0, w):
                  A[i]= A[i+1]

def promedio(A,w):
      c=0
      for i in range(0,w+1):
           c=c+A[i]
      return c

def restart_line():
  sys.stdout.write('\r')
  sys.stdout.flush()


##################### Argumentos  ######################################################
########################################################################################

Argl = sys.argv
L=len(sys.argv)
for i in range(1, L):
  if Argl[i]=='-f':#si no es locat poner el PATH entero
    faux=Argl[i+1]
    #le = int(len(faux)-4)
    #fn=faux[0:le]
    fn=faux
    print fn

  if Argl[i]=='-y': #punto en el eje y en el cual la ventana hara e recorrido

    altura=float(Argl[i+1])
 

  if Argl[i]=='-t': #Ancho de la ventana en el eje x 
    T=int(Argl[i+1])


  if Argl[i]=='-c':#aqui para especificar el canal a promediar

        chanel=int(Argl[i+1])

  if Argl[i]=='-s':#aqui para el nombre del achivo de salida
    
    ArchivoDeSalida=Argl[i+1]+".dat"
   
  if Argl[i]=='-?':#imprime el help

    print  "\n \nANC autor: arturonunez25@gmail.com \nPara la colaboracion LAGO-Venezuela-Colombia \nEste codigo hace Moving Window Average de un archivo de salida de crktools \nanalizado y  con las estructura x,y,par_id, densidad.\nY las opciones son \n \n-f                  nombre del archivo de datos que se analiza. de tener \n                    la terminacion de .sec.bz2 \n-y                  cordenada Y en la que la ventana hara el recorrido\n-t                  ancho de la ventana\n-s                  nombre del archivo de salida, el .dat sale automatico\n \n"
    sys.exit()



################################################################################
################################################################################


if T==0:
 print "ERROR1:hace falta especificar el Ancho de la ventana opcion -t!!!!!!"
 sys.exit()
#elif altura==0:
# print "ERROR2:hace falta especificar el la altura del recorrido de la ventana opicon -y!!!!!!"
# sys.exit()

A=[0 for i in range(0,T+1)]# esta es la ventana
MW=[]
X=[]
data=[]
aux=0
contador=0



with open(ArchivoDeSalida,"a") as f:
     f.write("# # aqui el archivo de salida del moving window average \n ")
     f.write("# # las columnas son x, promedio, densidad , \n")



qbfile = open(fn,"r")


for aline in qbfile:
  row  = aline.split()
  if row[0]== '#' or float(row[25])==0.0:
    continue
  if row[2]!=altura:
    continue
  contador=+1
  oruga(A,T)   
  A[T]=float(row[chanel])#/float(row[25])
  P= promedio(A,T)
  prom=P/T
  x=float(row[0])
  densidad=float(row[2])
          #estos son los valores ahora hay que imprimirlos
  fila=[x,prom,densidad]
  if (contador/100)==1:
    restart_line()
    aux=+1
    contador=-100
    sys.stdout.write('------------------'+"van "+(aux*100)+" impresas")
    sys.stdout.flush()
  with open(ArchivoDeSalida,"a") as f:
               w = csv.writer(f,delimiter=' ')
               w.writerow(fila)
           
                  
        
    












