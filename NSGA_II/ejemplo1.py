from problema import Problema
from evolucion import Evolucion
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D



# def f1(x):
#     g=100*(1 +((x[2]-0.5)**2 - np.cos(20*np.pi*(x[2]-0.5))))
#     return 1/2*x[0]*x[1]*(1+g)
    
# def f2(x):
#     g=100*(1 +((x[2]-0.5)**2 - np.cos(20*np.pi*(x[2]-0.5))))
#     return 1/2*x[0]*(1-x[1])*(1+g)

# def f3(x):
#     g=100*(1 +((x[2]-0.5)**2 - np.cos(20*np.pi*(x[2]-0.5))))
#     return 1/2*(1-x[0])*(1+g)
    
    
def f1(x):
    return x[0] ** 2 +3*x[0]**2 -x[0]*x[1]

def f2(x):
    return np.sin(x[0]**2) + np.cos(x[1]**2)

def f3(x):
    return np.exp(-x[2]) 
    
problema = Problema(funciones=[f1, f2, f3],n_variables=3, rango_variables=[(-5, 5)], expandir=False,rango_s=True)
evo = Evolucion(problema, n_generaciones=500,n_individuos=150,n_participantes=2,param_cruce=2,param_mutacion=5)
func = [i.funciones for i in evo.evolucionar()]

func1 = [i[0] for i in func]
func2 = [i[1] for i in func]
func3 = [i[2] for i in func]


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(func1, func2, func3)


ax.set_xlabel('f1', fontsize=15)
ax.set_ylabel('f2', fontsize=15)
ax.set_zlabel('f3', fontsize=15)


plt.show()
