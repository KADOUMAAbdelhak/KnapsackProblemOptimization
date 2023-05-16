# -*- coding: utf-8 -*-
"""
Created on Fri May 20 09:31:42 2022

@author: acer
"""

# python implementation of Grey wolf optimization (GWO)
# minimizing rastrigin and sphere function
 
 
import random
import math    # cos() for Rastrigin
import copy    # array-copying convenience
import sys     # max float
from pdb import pm
import time 
import csv;
import numpy as np
 
#-------fitness functions---------
 
# rastrigin function
def fitness_(position,items_ord, s):
      value=0
      for t in range(int(s)):
          value+=position[t]*items_ord[t][0]
      return value
 




#Fonction Capacité
def Capacity(solution, items_ord, s,cap_sac):
        full=0   
        for t in range(int(s)):
           full+=solution[t]*items_ord[t][1]
        capacity=cap_sac-full
        return capacity
 
#Fonction Générer nbr_exmp
def rand_nbr_exp(item,items_ord, s,cap):
        nbr_exp=0
        nbr_exp_max= cap // items_ord[item][1]
        nbr_exp= random.randint(0,nbr_exp_max)
        return nbr_exp 

#Fonction Ajuster Solution
def Ajust_sol(solution,items_ord, s,cap_sac):
        tab_pourc=[0.0 for i in range(int(s))]
        som=abs(np.sum(solution))
        
        sol=[0 for i in range(int(s))]
        k=0
        
        while (k < int(s)):
            p=abs(solution[k])/som
            tab_pourc[k]=p
            k+=1
        
        tab_ind=[-1 for i in range(int(s))]
        tab_coche=[0 for i in range(int(s))]
        
        ind=0
        j=0
        while (j < int(s)):
           max_p=0
           for i in range(int(s)):
               if ((tab_pourc[i]>=max_p) and (tab_coche[i]!= -1)):
                   max_p=tab_pourc[i]
                   ind=i
           tab_ind[j]=ind
           tab_coche[ind]=-1
           j+=1
         
        k=0
        #print("Voici tab ind",tab_ind)
        
        while (k < int(s)):
            indice=tab_ind[k]
            cap= Capacity(sol, items_ord, s, cap_sac)
            nbr_exp_max= cap // items_ord[indice][1]
            nbr_exp= random.randint(nbr_exp_max-2,nbr_exp_max)
            if (nbr_exp<0):
                nbr_exp=0
            sol[indice]= nbr_exp
            k+=1    
         
        t=0
        while (t < int(s)):
            indice=tab_ind[t]
            cap=Capacity(sol, items_ord, s, cap_sac)
            if (cap >= items_ord[indice][1]):
                sol[indice]+=cap//items_ord[indice][1]
    
            t+=1
       
        return sol
    
# wolf class
class wolf:
  def __init__(self,s, items_ord, cap_sac):
    
    self.position = [0 for i in range(int(s))]

    for i in range(int(s)):
        cap=Capacity(self.position, items_ord, s,cap_sac) 
        x=rand_nbr_exp(i,items_ord, s,cap)
        
        if (cap >= items_ord[i][1]):
             self.position[i] = x
             
 
    self.fitness = fitness_(self.position,items_ord, s) # curr fitness
    
 
 
# grey wolf optimization (GWO)
def gwo( max_iter, n):
    
    rnd = random.Random(0)
    items_ord = []
    items=[]
    s= input("donne le nombre de items: ") 
    f=open("infos_3.csv")
    myReader=csv.reader(f)
    array= np.loadtxt(f,delimiter=";")
    for i in range(int(s)):
        items.insert(i, (int(array[i][0]),int(array[i][1]),i))
     
    
    items_ord=sorted(items,key=lambda item1: (item1 [0]/item1[1]) )  
    items_ord.reverse()

    cap_sac=int(input("Le poids de sac a dos: ") )
    
    # create n random wolves
    tps1=time.time()
    population = [ wolf(s,items_ord,cap_sac) for i in range(n)]
 
    # On the basis of fitness values of wolves
    # sort the population in asc order
    population = sorted(population, key = lambda temp: temp.fitness)
    population.reverse()
 
    # best 3 solutions will be called as
    # alpha, beta and gaama
    alpha_wolf, beta_wolf, gamma_wolf = copy.copy(population[: 3])
    #print("alpha_wolf.position=", alpha_wolf.position)
    
 
    # main loop of gwo
    Iter = 0
    while Iter < max_iter:
 
        # after every 10 iterations
        # print iteration number and best fitness value so far
       # if Iter % 10 == 0 and Iter > 1:
           # print("Iter = " + str(Iter) + " best fitness = " , alpha_wolf.fitness,"best sol=" ,alpha_wolf.position)
 
        # linearly decreased from 2 to 0
        a = 2*(1 - Iter/max_iter)
 
        # updating each population member with the help of best three members
        for i in range(n):
            
            A1, A2, A3 = a * (2 * random.randint(1,2)-1 ), a * (
              2 * random.randint(1,2) - 1), a * (2 * random.randint(1,2) - 1)
            C1, C2, C3 = 2 * random.randint(1,2), 2*random.randint(1,2), 2*random.randint(1,2)
            #print("A1, A2, A3 =", A1, A2, A3 )
 
            X1 = [0 for i in range(int(s))]
            X2 = [0 for i in range(int(s))]
            X3 = [0 for i in range(int(s))]
            Xnew = [0 for i in range(int(s))]
            for j in range(int(s)):
                X1[j] = abs(alpha_wolf.position[j] - A1 * abs(
                  C1 * alpha_wolf.position[j] - population[i].position[j]))
                X2[j] = abs( beta_wolf.position[j] - A2 * abs(
                  C2 *  beta_wolf.position[j] - population[i].position[j]))
                X3[j] = abs(gamma_wolf.position[j] - A3 * abs(
                  C3 * gamma_wolf.position[j] - population[i].position[j]))
                Xnew[j]+= X1[j] + X2[j] + X3[j]
             
            for j in range(int(s)):
                Xnew[j]=Xnew[j]//3
                
            #print("Xnew avant=", Xnew)
            Xnew=Ajust_sol(Xnew,items_ord, s,cap_sac)
            print("Xnew=", Xnew)
            # fitness calculation of new solution
            fnew = fitness_(Xnew,items_ord, s)
 
            # greedy selection
            if fnew > population[i].fitness:
                population[i].position = Xnew
                population[i].fitness = fnew
                 
        # On the basis of fitness values of wolves
        # sort the population in asc order
        population = sorted(population, key = lambda temp: temp.fitness)
        population.reverse()
 
        # best 3 solutions will be called as
        # alpha, beta and gaama
        alpha_wolf, beta_wolf, gamma_wolf = copy.copy(population[: 3])
         
        Iter+= 1
        tps2=time.time()
        tps=tps2-tps1
    # end-while
 
    # returning the best solution
    
    return alpha_wolf.position, alpha_wolf.fitness, tps
           
#----------------------------
 
 
# Execution

max_iter=2
n=70

best_sol=gwo(max_iter, n)

print("Meilleure solution =",best_sol[0])
print("valeur meilleure solution =",best_sol[1])
print("valeur meilleure solution =",best_sol[2])
 