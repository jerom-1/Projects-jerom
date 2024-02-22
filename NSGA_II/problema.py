from individuo import Individuo
import random

class Problema:
    
    def __init__(self,funciones,n_variables,rango_variables,expandir=True,rango_s=False):
        
        self.n_variables = n_variables
        self.rango_variables = rango_variables
        self.funciones = funciones
        self.expandir = expandir
        self.rango_variables=[]
        
        if rango_s:
            for _ in range(n_variables):
                self.rango_variables.append(rango_variables[0])
        else:
            self.rango_variables= rango_variables
            
    def generar_individuo(self):
        individuo=Individuo()
        individuo.genes=[random.uniform(*x) for x in self.rango_variables]
        return individuo
    
    def calcular_funciones(self,individuo):
        if self.expandir:
            individuo.funciones=[f(*individuo.genes) for f in self.funciones]
        else:
            individuo.funciones=[f(individuo.genes) for f in self.funciones]
            
            