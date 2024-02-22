import numpy as np
import time 
from Auxiliares import *
from vecindarios import *




def busqueda_local_best_improvement(sol, n, m, opc):
    mksol = makespan(sol,n,m)
    it = 0
    stop = 0
    ti= time.time()
    while stop == 0:
        tt=time.time() - ti
        if tt>300:
            break
        it += 1
        stop = 1

        for i in range(0,n*m):
            tt=time.time() - ti
            if tt>300:
                break
            for j in range(i+1,n*m):
                tt=time.time() - ti
                if tt>300:
                    break
                if opc == 1:
                    vec, mkvec = interchange(n,m,sol,i,j)
                elif opc == 2:
                    vec, mkvec = insertion(n,m,sol,i,j)
                elif opc ==3:
                    vec, mkvec = insertion_down(n,m,sol,i,j)
                if mkvec < mksol:
                    sol = vec
                    mksol= mkvec
                    stop = 0    
    t =time.time() - ti
    return sol, mksol, t, it




def busqueda_local_first_improvement(sol, n, m, opc):
    mksol = makespan(sol,n,m)
    it = 0
    stop = 0
    ti= time.time()
    while stop == 0:
        tt=time.time() - ti
        if tt>300:
            break
        
        it += 1
        stop = 1

        for i in range(0,n*m):
            tt=time.time() - ti
            if tt>300:
                break
            for j in range(i+1,n*m):
                tt=time.time() - ti
                if tt>300:
                    break
                if opc == 1:
                    vec, mkvec = interchange(n,m,sol,i,j)
                elif opc == 2:
                    vec, mkvec = insertion(n,m,sol,i,j)
                elif opc ==3:
                    vec, mkvec = insertion_down(n,m,sol,i,j)
                    
                if mkvec < mksol:
                    sol = vec
                    mksol= makespan(sol,n,m)
                    stop = 0 
                    break
            if stop == 0:
                break
    t=time.time() - ti
    return sol, mksol, t, it
