

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


M=0       
items_ord = []
items=[]

NA=[]

f=open("infos.csv")
myReader=csv.reader(f)
array= np.loadtxt(f,delimiter=";")
s=len(array)
solution=[0 for i in range(int(s))]
for i in range(int(s)):
 
     items.insert(i, (int(array[i][0]),int(array[i][1]),i))

    
items_ord=sorted(items,key=lambda item1: (item1 [0]) )  
items_ord.reverse()

pmax_temp=input("Le poids de sac a dos: ") 


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
            
            max_item= Q1.pmax // items_ord[indice][1]
            print("max_objets =",max_item)
        
            solu=Q1.sol
            solu[indice]=max_item
            Q2.sol=solu
            #print("Voici le poids disponible while")
            #print(Q1.pmax)
            #print(Q1.pmax)
            n=Q1.pmax-max_item*items_ord[indice][1]
            Q2.pmax= n
            print("Voici le poids noeud crée")
            print(Q2.pmax)
            Q2.item=indice
            Q2.nbr_item=max_item
            print(Q2.sol,Q2.item,Q2.nbr_item,Q2.pmax)
            print("Voici le noeud ajouté")
            print(Q2.sol,Q2.item,Q2.nbr_item,Q2.pmax)
            NA.append(Q2)
            Q2=Node(sol2,-1,0,int(pmax_temp))
            i+=1
        
            
           
    else:
            for t in range(int(s)):
              M+=Q2.sol[t]*items_ord[t][0]
              solution[t]=Q2.sol[t]
tps2=time.time()         
print("Le programme s'execute en un temps de :",tps2-tps1)
print('profit total =' ,M)
print(solution)
