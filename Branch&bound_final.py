# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 23:47:15 2022

@author: HP VICTUS
"""

#from recordclass import recordclass
#from collections import deque
#import heapq

from pdb import pm
import time 
import csv;
import numpy as np
import matplotlib.pyplot as plt 

class Node:
    def __init__(self,sol,item,nbr_item,pmax):
        self.sol=sol
        self.item=item
        self.nbr_item=nbr_item
        self.pmax=pmax
        
"""class BenVol:
    def __init__(self):
        self.benifice=0
        self.volume=0  """      

def Eval(items_ord,Q1,s):
    
    e=0
    for t in range(int(s)):
        e+=Q1.sol[t]*items_ord[t][0]
    e=float(e)
    if (Q1.item != (int(s)-1)):
        e=e+((Q1.pmax /(items_ord[Q1.item+1][1]))*items_ord[Q1.item+1][0])
    return e

M=0       
items_ord = []
items=[]
 

NA=[]

f=open("infos_2.csv")
myReader=csv.reader(f)
array= np.loadtxt(f,delimiter=";")
s=len(array)
for i in range(int(s)):
 
     items.insert(i, (int(array[i][0]),int(array[i][1]),i))
     
items_ord=sorted(items,key=lambda item1: (item1 [0]/item1[1]) )  
items_ord.reverse()

pmax_temp=input("Le poids de sac a dos: ") 
solution=[0 for i in range(int(s))]

"""print(items)
print(items_ord)"""

sol2=[0 for i in range(int(s))]
Q1=Node(sol2,-1,0,int(pmax_temp))
Q2=Node(sol2,-1,0,int(pmax_temp))
NA.append(Q1)
tps1=time.time()
while(len(NA)!=0):
    Q1=Node(sol2,-1,0,int(pmax_temp))
    Q1=NA.pop(len(NA)-1)
  
    
    Q1.sol[Q1.item]=Q1.nbr_item
    print("Voici le noeud retiré")
    print(Q1.sol,Q1.item,Q1.nbr_item,Q1.pmax)
    
    indice=Q1.item+1
    
    print(indice)
    if(indice<int(s)):
      i=0
      max_item= Q1.pmax // items_ord[indice][1]
      print("nombre de fils")
      print(max_item)
      if (indice ==0) :
          while(i <= max_item):
            solu=Q1.sol
            solu[indice]=i
            Q2.sol=solu
            #print("Voici le poids disponible while")
            #print(Q1.pmax)
            #print(Q1.pmax)
            n=Q1.pmax-(i)*items_ord[indice][1]
            Q2.pmax= n
            print("Voici le poids noeud crée")
            print(Q2.pmax)
            Q2.item=indice
            Q2.nbr_item=i
            print(Q2.sol,Q2.item,Q2.nbr_item,Q2.pmax)
            print("Voici le noeud ajouté")
            print(Q2.sol,Q2.item,Q2.nbr_item,Q2.pmax)
            NA.append(Q2)
            Q2=Node(sol2,-1,0,int(pmax_temp))
            i+=1
         
      else :
           print("Evaluation du noeud égale à",Eval(items_ord,Q1,s))
           if (Eval(items_ord,Q1,s)>=float(M)):
            while(i <= max_item):
                
                 solu=Q1.sol
                 solu[indice]=i
                 Q2.sol=solu
                 #print("Voici le poids disponible while")
                 #print(Q1.pmax)
                 #print(Q1.pmax)
                 n=Q1.pmax-(i)*items_ord[indice][1]
                 Q2.pmax= n
                 print("Voici le poids noeud crée")
                 print(Q2.pmax)
                 Q2.item=indice
                 Q2.nbr_item=i
                 print(Q2.sol,Q2.item,Q2.nbr_item,Q2.pmax)
                 print("Voici le noeud ajouté")
                 print(Q2.sol,Q2.item,Q2.nbr_item,Q2.pmax)
                 NA.append(Q2)
                 Q2=Node(sol2,-1,0,int(pmax_temp))
                 i+=1
            
            
           
    else:
        M_tmp=0
        print("sssssssssssssssssss")
        for t in range(int(s)):
           M_tmp+=Q1.sol[t]*items_ord[t][0]
        if(M_tmp>M):
            M=M_tmp
            for t in range(int(s)):
              solution[t]=Q1.sol[t]
tps2=time.time()         





print("Le programme s'execute en un temps de :",tps2-tps1)
print("Profit total=",M)
print(solution)