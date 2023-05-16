# -*- coding: utf-8 -*-
"""
Created on Thu May 12 14:48:18 2022

@author: HP VICTUS
"""

import random
import math
import copy
import time 
import csv;
import numpy as np


n = 20
w_max = 130000

cross_rate = 0.99
g_num = 500


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
    
#creer sol aléatoire
def rand_sol(production):
    sol=[0 for i in range(dim)]
    for i in range(dim):
        cap=Capacity(sol, production, dim,w_max) 
        x=rand_nbr_exp(i,production, dim,cap)
        if (cap >= production[i][1]):
            sol[i] = x
    return sol

def Ajust_sol(solution):
       
        sol=[solution[i] for i in range(dim)]
        t=0
        while (t < dim):
            cap=Capacity(solution, production, dim, w_max)
            if (cap >= production[t][1]):
                sol[t]+=cap//production[t][1]
    
            t+=1
       
        return sol





items=[]

f=open("infos.csv")
myReader=csv.reader(f)
array= np.loadtxt(f,delimiter=";")
s=len(array)
for i in range(int(s)):
     items.insert(i, (int(array[i][0]),int(array[i][1]),i))
     
    
production=sorted(items,key=lambda item1: (item1 [0]/item1[1]) )  
production.reverse()




dim = len(production)


def f(g):
    weight = sum([production[j][1] * g[j] for j in range(dim)])
    if weight <= w_max:
        return sum([production[j][0] * g[j] for j in range(dim)]), weight
    else:
        return 1, weight
    
    
    
def select(score):
    total = sum(score)
    threshold = random.random() * total
    sum_s = 0
    for i, s in enumerate(score):
        sum_s += s
        if sum_s > threshold:
            return i
        
def find_elite(score, weight=None):
    if not weight is None and len(list(set(score))) == 1:
        min_weight = 1e+6
        min_index = None
        for i, w in enumerate(weight):
            if min_weight > w:
                min_weight = w
                min_index = i
        return min_index
    else:
        max_score = -1
        max_index = None
        for i, val in enumerate(score):
            if max_score < val:
                max_score = val
                max_index = i
        return max_index


def cross(parent1, parent2):
    length = len(parent1)
    r1 = int(math.floor(random.random() * length))
    r2 = r1 + int(math.floor(random.random() * (length - r1)))

    child = copy.deepcopy(parent1)
    child[r1:r2] = parent2[r1:r2]

    return child

def mutate(geen):
    for i in range(n):
        for l in range(dim):
            if random.random() > cross_rate:
                geen[i][l] = 1 - geen[i][l]
                if geen [i][l] < 0 :
                    geen [i][l] = 0

    return geen


#Génération population initial:
    
tps1=time.time()
geen=[[] for i in range(n)]
for l in range(n):
    geen[l]=  Ajust_sol(rand_sol(production))
#geen = [[random.randint(0, 11) for i in range(dim)] for l in range(n)]

for stage in range(g_num):
    #ÉVALUATION
    score = []
    weight = []
    for g in geen:
        s, w = f(g)
        score.append(s)
        weight.append(w)

    #LA SÉLECTION DE LA ROULETTE
    elite_index = find_elite(score, weight)
    if stage % 100 == 0:
        #print("Generation: {}".format(stage))
        print(f(geen[elite_index]), geen[elite_index])

    #CROISEMENT À DEUX POINTS
    next_geen = [geen[elite_index]]
    while len(next_geen) < n:
        selected_index1 = select(score)
        selected_index2 = select(score)
        while selected_index1 == selected_index2:
            selected_index2 = select(score)
        next_geen.append(cross(geen[selected_index1], geen[selected_index2]))

    #MUTATION (EVITER SOLUTION OPTIMUM LOCALE)
    geen = mutate(next_geen)

tps2=time.time()
print("Le programme s'execute en un temps de :",tps2-tps1)