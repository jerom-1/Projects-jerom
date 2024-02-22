import numpy as np
import time 
import random
from Auxiliares import *

def interchange(n,m,sol,a,b):
    vec = sol.copy()
    vec[a] = sol[b]
    vec[b] = sol[a] 
    if vec[a][1] == vec[b][1]:
        if vec[a][3] > vec[b][3]:
            return vec,float('inf')
    else:
        if factible(vec,n):
            return vec,makespan(vec,n,m)
        else:
            return vec,float('inf')

def insertion(n,m,sol,a,b):
    vec = sol.copy()
    el1 = vec.pop(b)
    vec.insert(a, el1)
    if vec[a][1] == vec[a+1][1]:
        if vec[a][3] > vec[a+1][3]:
            return vec,float('inf')
    else:
        if factible(vec,n):
            return vec, makespan(vec,n,m)
        else:
            return vec, float('inf')

def insertion_down(n,m,sol,a,b):
    vec = sol.copy()
    el1 = vec.pop(a)
    vec.insert(b, el1)
    if vec[a][1] == vec[a+1][1]:
        if vec[b][3] > vec[b+1][3]:
            return vec,float('inf')
    else:
        if factible(vec,n):
            return vec, makespan(vec,n,m)
        else:
            return vec, float('inf')
    
def interchange_BI(s,n,m,tMAX):

    f_s = makespan(s,n,m)
    it = 0
    stop = 0
    ti= time.time()
    while stop == 0:
        it += 1
        stop = 1 
        for i in range(0,n*m):
            for j in range(i+1,n*m):
                tt = time.time()
                if tt-ti>tMAX:
                    return s, f_s, tt-ti, it
                sp, f_sp = interchange(n,m,s,i,j)

                if f_sp < f_s:
                    s = sp
                    f_s = f_sp
                    stop = 0    
                
    t =time.time() - ti
    return s, f_s, t, it

def insertionUP_BI(s,n,m,tMAX):

    f_s = makespan(s,n,m)
    it = 0
    stop = 0
    ti= time.time()
    while stop == 0:
        it += 1
        stop = 1 
        for i in range(0,n*m):
            for j in range(i+1,n*m):
                tt = time.time()
                if tt-ti>tMAX:
                    return s, f_s, tt-ti, it
                sp, f_sp = insertion(n,m,s,i,j)

                if f_sp < f_s:
                    s = sp
                    f_s = f_sp
                    stop = 0    

    t =time.time() - ti
    return s, f_s, t, it

def insertion_down_BI(s,n,m,tMAX):

    f_s = makespan(s,n,m)
    it = 0
    stop = 0
    ti= time.time()
    while stop == 0:
        it += 1
        stop = 1 
        for i in range(0,n*m):
            for j in range(i+1,n*m):
                tt = time.time()
                if tt-ti>tMAX:
                    return s, f_s, tt-ti, it
                sp, f_sp = insertion_down(n,m,s,i,j)

                if f_sp < f_s:
                    s = sp
                    f_s = f_sp
                    stop = 0    

    t =time.time() - ti
    return s, f_s, t, it

def interchange_FI(s,n,m,tMAX):

    f_s = makespan(s,n,m)
    it = 0
    stop = 0
    ti= time.time()
    while stop == 0:
        it += 1
        stop = 1 
        for i in range(0,n*m):
            for j in range(i+1,n*m):
                tt = time.time()
                if tt-ti>tMAX:
                    return s, f_s, tt-ti, it
                
                sp, f_sp = interchange(n,m,s,i,j)

                if f_sp < f_s:
                    s = sp
                    f_s = f_sp
                    stop = 0    
                    break
            
            if stop == 0:
                break
            
    t =time.time() - ti
    return s, f_s, t, it


def insertionUP_FI(s,n,m,tMAX):

    f_s = makespan(s,n,m)
    it = 0
    stop = 0
    ti= time.time()
    while stop == 0:
        it += 1
        stop = 1 
        for i in range(0,n*m):
            for j in range(i+1,n*m):
                tt = time.time()
                if tt-ti>tMAX:
                    return s, f_s, tt-ti, it
                sp, f_sp = insertion(n,m,s,i,j)

                if f_sp < f_s:
                    s = sp
                    f_s = f_sp
                    stop = 0    
                    break
            
            if stop == 0:
                break
            
    t =time.time() - ti
    return s, f_s, t, it

def insertion_down_FI(s,n,m, tMAX):

    f_s = makespan(s,n,m)
    it = 0
    stop = 0
    ti= time.time()
    while stop == 0:
        it += 1
        stop = 1 
        for i in range(0,n*m):
            for j in range(i+1,n*m):
                tt = time.time()
                if tt-ti>tMAX:
                    return s, f_s, tt-ti, it
                
                sp, f_sp = insertion_down(n,m,s,i,j)

                if f_sp < f_s:
                    s = sp
                    f_s = f_sp
                    stop = 0    
                    break
            
            if stop == 0:
                break
            
    t =time.time() - ti
    return s, f_s, t, it




def VND(s,n,m,tMAX):
    
    j=1

    f_s = makespan(s,n,m)

    ti = time.time()
    it=0

    while j<=3:

        it +=1

        if j == 1:
            ta = time.time()
            if ta-ti > tMAX:
                return s, f_s, ta-ti, it
            sp, f_sp, t, it1 = interchange_BI(s,n,m, tMAX)
            it+=it1

        elif j == 2:
            ta = time.time()
            if ta-ti > tMAX:
                return s, f_s, ta-ti, it
            sp, f_sp, t, it2 = insertionUP_BI(s,n,m, tMAX)
        elif j==3:
            ta = time.time()
            if ta-ti > tMAX:
                return s, f_s, ta-ti, it
            sp, f_sp, t, it3 = insertionUP_FI(s,n,m, tMAX)
        
        if f_sp < f_s:
            s = sp
            f_s = f_sp
            j=1
        else:
            j = j + 1
        ta= time.time()
        if ta-ti > tMAX:
            return s, f_s, ta-ti, it

    return s, f_s, time.time()-ti, it

def interchange_R(s,n,m, tMAX):
    it = 0
    ti =  time.time()
    f_s = makespan(s,n,m)
    while it < 3:
        if time.time()-ti>tMAX:
            return s, f_s, time.time()-ti,it
        it+=1
        i = random.randint(1,n*m)
        j = random.randint(1,n*m)
        while j == i:
            i = random.randint(1,n*m)
            j = random.randint(1,n*m)
        if i > j: 
            a=i
            i=j
            j=a

        for k in range(i+1,j):
            if time.time()-ti>tMAX:
                return s, f_s, time.time()-ti,it

            sp, f_sp = interchange(n,m, s, i, k)

            if f_sp != float('inf'):
                s = sp
                f_s = f_sp
    return s, f_s, time.time()-ti,it

def MS_ELS_P(sols,n,m, tMAX, p):
    
    # tambien se puede usar VND
    it = 0
    ti = time.time()
    best = []
    f_b = float('inf')
    for sol in sols:
        s = sol[0]
        f_s=sol[1]
        if f_s < f_b:
            best  = s
            f_b  = f_s

        while time.time()-ti < tMAX:
            it+=1
            sp, f_sp, a,b  = interchange_R(s,n,m,tMAX)
            it+=b
            sp, f_sp, a,b  = interchange_BI(sp,n,m,tMAX)
            it+=b
            if f_sp < f_s:
                s = sp
                f_s = f_sp
                if f_sp < f_b:
                    best = sp
                    f_b = f_sp
            else:
                r = random.random()
                if r < p:
                    s = sp
                    f_s = f_sp    

    return best, f_b, time.time()-ti,it



def recocido(sols,n,m, tMAX, T0, Tf, L, rho):
    # tambien se puede usar VND
    it = 0
    ti = time.time()
    best = []
    f_b = float('inf')
    for sol in sols:
        s = sol[0]
        f_s=sol[1]
        if f_s < f_b:
            best  = s
            f_b  = f_s

    while time.time()-ti<tMAX:
        it = it +1
        T = T0
        while T > Tf and time.time()-ti < tMAX:
            for l in range(int(L)):
                sp, f_sp, a, b = interchange_R(s,n,m,tMAX)
                it=+b
                sp, f_sp, a, b  = interchange_BI(sp,n,m,tMAX)
                it+=b
                if f_sp < f_s:
                    s = sp
                    f_s = f_sp
                    if f_sp < f_b:
                        best = sp
                        f_b = f_sp
                else:
                    r = random.random()
                    if r < np.exp(-(f_sp-f_s)/T):
                        s = sp
                        f_s = f_sp

                if time.time()<tMAX: 
                    break
            T = T*rho
            L = L*1.2
    return best, f_b, time.time()-ti, it

                



