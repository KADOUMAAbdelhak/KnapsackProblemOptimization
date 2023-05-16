# -*- coding: utf-8 -*-
"""
Created on Fri May  6 03:13:37 2022

@author: acer
"""

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
        
        
def Objfun(solution, items_ord, s):
       value=0
       for t in range(int(s)):
          value+=solution[t]*items_ord[t][0]
       return value
   
def Capacity(solution, items_ord, s,cap_sac):
        full=0   
        for t in range(int(s)):
           full+=solution[t]*items_ord[t][1]
        capacity=cap_sac-full
        return capacity

def Voisin( solution,k, i ,j , cap_sac,s):
        solu=[solution[k] for k in range(int(s))]


        
        nb=0
       
        while (k>=items_ord[j][1]):
            
            nb+=1
            solu[j]= nb
            k-=items_ord[j][1]
            
        #print("voici solu apres nb",solu)
        return solu


def nouv_voisinage(solution,i,items_ord,cap_sac,s):
        solu=[solution[o] for o in range(int(s))]
        if (solution[i]!=0):
          solu[i] = solution[i]-1
        else:
          solu[i]=0
        return solu

def min_poids(items_ord,cap_sac,s):
    min=cap_sac
    for i in range (int(s)):
        if (items_ord[i][1]<min):
            min=items_ord[i][1]
    return min


def Heuristic( items_ord, cap_sac,s):
  resultat=[0 for k in range(int(s))]
        
  M=0       

  NA=[]

  pmax_temp=cap_sac 

  sol2=[0 for i in range(int(s))]
  Q1=Node(sol2,-1,0,int(pmax_temp))
  Q2=Node(sol2,-1,0,int(pmax_temp))
  NA.append(Q1)

  while(len(NA)!=0):
    Q1=Node(sol2,-1,0,int(pmax_temp))
    Q1=NA.pop(len(NA)-1)
  
    
    Q1.sol[Q1.item]=Q1.nbr_item
    
    indice=Q1.item+1
    
    print(indice)
    if(indice<int(s)):
            
            max_item= Q1.pmax // items_ord[indice][1]
            solu=Q1.sol
            solu[indice]=max_item
            Q2.sol=solu
            
            n=Q1.pmax-max_item*items_ord[indice][1]
            Q2.pmax= n
            Q2.item=indice
            Q2.nbr_item=max_item
            NA.append(Q2)
            Q2=Node(sol2,-1,0,int(pmax_temp))
            
           
    else:
            for t in range(int(s)):
              M+=Q2.sol[t]*items_ord[t][0]
              resultat[t]=Q2.sol[t]
  return resultat





items_ord = []
items=[]
nom=input("le nom du fichier")
nom+=".csv"
f=open(nom)

myReader=csv.reader(f)
array= np.loadtxt(f,delimiter=";")
s=len(array)
solution=[0 for i in range(int(s))]
for i in range(int(s)):
 
     items.insert(i, (int(array[i][0]),int(array[i][1]),i))
     
items_ord=sorted(items,key=lambda item1: (item1 [0]/item1[1]) )  
items_ord.reverse()

cap_sac=int(input("Le poids de sac a dos: ") )
#Solution initiale
sol_init=Heuristic(items_ord, cap_sac, s)
#sol_init=[0 for i in range(int(s))]
#sol_init[0]=14
#sol_init[5]=1
tps1=time.time()
# meilleure solution 
best_sol=sol_init

curr_sol=sol_init
It_max= 100
It_max_nochange=10
It=0
It_nochange=0
#liste tabou initialement et taille liste
T = []
tl=10
count_tabu=0


print("capacity de sol initiale:",Capacity(sol_init, items_ord, s, cap_sac))
#La boucle while
while( (It <= It_max) and (It_nochange<It_max_nochange)):
    It+=1
    
    val_max=0
    
    #Définir le voisinage et y trouver la meilleure solution
    j=1
    sol_voi=[0 for i in range(int(s))]
    if (Capacity(curr_sol, items_ord, s, cap_sac)< min_poids(items_ord, cap_sac, s) ):
     #print("if test nouv voisinage")   
     
     for i in range(int(s)):
       
          curr_sol= nouv_voisinage(curr_sol,i,items_ord,cap_sac,s) 
          #print("curr_sol nouveau voisinage=", curr_sol)
     while(j < int(s)):
           
           k=Capacity(curr_sol, items_ord, s, cap_sac)
           sol1=Voisin( curr_sol,k, i ,j , cap_sac,s)
           so=sol1
           if(Objfun(so, items_ord, s)>val_max ):
             val_max=Objfun(so, items_ord, s)
             sol_voi=so
        #print("solution voisin choisie", sol_voi)
           j+=1
    else:
        j=0
        while(j < int(s)):
          
           k=Capacity(curr_sol, items_ord, s, cap_sac)
           sol1=Voisin( curr_sol,k, i ,j , cap_sac,s)
        
           #print("sol1=", sol1)
        
        
           so=sol1
        #print("Voici sol1", sol1)
           if(Objfun(so, items_ord, s)>val_max ):
             val_max=Objfun(so, items_ord, s)
             sol_voi=so
        #print("solution voisin choisie", sol_voi)
           j+=1
    if not(sol_voi in T):#Est ce que cette solution n'est pas dans la liste tabou 
        count_tabu+=1
    
        if (Objfun(best_sol, items_ord, s)<Objfun(sol_voi, items_ord, s)):#et améliore la meilleure solution actuelle
            best_sol=sol_voi #alors mettre  jnkmb,,m,nkjkm,njnbjnk,b,kbjnb,kjjnjb,k,n,bk bbbbbbbb b à jour la nouvelle meilleure solution
    
    if (best_sol==sol_voi):#si la meilleure solution n'a pas changé   
        It_nochange+=1
    else: #elle a changé
        It_nochange=0
    
    curr_sol=sol_voi
    
    
    if(count_tabu == tl):#si longueur de la liste tabou est atteinte 
       del T[0]
       count_tabu-=1
    T.append(curr_sol)
tps2=time.time()         
print("Le programme s'execute en un temps de :",tps2-tps1)    
print("Voici la meilleure solution obtenue:", best_sol)
print("Le bénéfice de cette solution est:",Objfun(best_sol, items_ord, s))
