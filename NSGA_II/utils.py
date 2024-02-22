import random
from poblacion import Poblacion


class NSGA2:
    
    def __init__(self,problema,n_individuos,n_participantes, param_cruce,param_mutacion):
        
        self.problema=problema
        self.n_individuos=n_individuos
        self.n_participantes=n_participantes
        self.param_cruce=param_cruce
        self.param_mutacion=param_mutacion
    
    def crear_poblacion_inicial(self):
        # Crea una población inicial de individuos
        poblacion=Poblacion()
        for _ in range(self.n_individuos):
            individuo=self.problema.generar_individuo()
            self.problema.calcular_funciones(individuo)
            poblacion.append(individuo)
        return poblacion
    
    def nondominated_sort(self,poblacion):
        # Algoritmo de NSGA-II para hacer la clasificación por dominancia
        poblacion.frentes=[[]] #inicializo los frentes
        
        for individuo in poblacion: 
            individuo.veces_dominado=0 # Número de veces que el individuo es dominado
            individuo.conjunto_dominado=[] # Conjunto de individuos que el individuo domina
            
            for otro in poblacion:
                if individuo.dominancia(otro): # Si el individuo domina al otro
                    individuo.conjunto_dominado.append(otro)
                elif otro.dominancia(individuo): # Si el otro domina al individuo
                    individuo.veces_dominado+=1
            if individuo.veces_dominado==0:
                # Si el individuo no es dominado por ningún otro, entonces pertenece al frente 0
                individuo.rango=0
                poblacion.frentes[0].append(individuo)
        
        i=0
        while len(poblacion.frentes[i])>0:
            Q=[]
            # Ciclo para sacar los demás frentes
            for individuo in poblacion.frentes[i]:
                for otro in individuo.conjunto_dominado:
                    otro.veces_dominado-= 1
                    if otro.veces_dominado==0:
                        otro.rango=i+1
                        Q.append(otro)
            i+=1
            poblacion.frentes.append(Q)
            
    def calcular_crowding_distance(self,frente):
        # Calcula la distancia crowding entre los individuos de un frente
        if len(frente)>0:
            n_soluciones=len(frente)
            for individuo in frente:
                individuo.crowding_distance=0 #Inicializa las distancias en 0
            
            # Para cada función objetivo evaluada 
            for m in range(len(frente[0].funciones)):
                
                frente.sort(key=lambda individuo: individuo.funciones[m]) #Oeganiza en orden ascendente de magnitud
                
                # El primero y el ultimo en "infinito" para asegurar que no se eliminan
                frente[0].crowding_distance=10**9 
                frente[n_soluciones - 1].crowding_distance = 10 ** 9
                
                # los valores de la funion objetivo m en el frente dado
                m_vals=[individuo.funciones[m] for individuo in frente]
                
                # Magnitud de la funcion para normalizar las distancias
                escala=max(m_vals)-min(m_vals)
                
                if escala==0: 
                    escala=1
                
                # Se calcula la distancia como la diferencia entre los vecinos, normalizada
                # y se añade a la distancia total del frente dado
                for i in range(1,n_soluciones-1):
                    frente[i].crowding_distance+=(frente[i+1].funciones[m]-frente[i-1].funciones[m])/escala
                    
                    
    def crowding_operator(self,individuo,otro):
        # Si tenemos una solución de un frente menor(mejor) entonces la preferimos, o si pertenecen al mismo frente entonces preferimos aquella 
        # con la mayor distancia (región menos densa).
        if (individuo.rango < otro.rango) or ((individuo.rango==otro.rango) and (individuo.crowding_distance > otro.crowding_distance)):
            return 1
        else:
            return -1
        
    def crear_hijos(self,poblacion):
        hijos=[]
        
        # La poblacion total debe ser de tamaño 2N
        while len(hijos) < len(poblacion):
            
            #obtengo los mejores padres
            
            padre1=self.__competencia(poblacion)
            padre2=padre1
            while padre1 == padre2:
                padre2=self.__competencia(poblacion)
            
            # Reproducción mediante los dos padres
            hijo1,hijo2=self.__cruzar(padre1,padre2)
            
            # Mutación de los hijos
            self.__mutar(hijo1)
            self.__mutar(hijo2)
            
            # Obtener el valor de los hijos en las funciones para su posterior crowding distance
            self.problema.calcular_funciones(hijo1)
            self.problema.calcular_funciones(hijo2)
            
            hijos.append(hijo1)
            hijos.append(hijo2)
            
        return hijos
    
    # Implementa el operador de cruza SBX (Simulated Binary Crossover)
    def __cruzar(self, individuo1,individuo2):
        hijo1=self.problema.generar_individuo()
        hijo2=self.problema.generar_individuo()
        
        # Numero genes= Numero variables, cosas que se modifican
        n_genes=len(hijo1.genes)
        
        genes_ind=range(n_genes)
        
        for i in genes_ind:
            
            # Equilibrar la diversidad y la convergencia 
            beta=self.__get_beta()
            
            x1=(individuo1.genes[i]+individuo2.genes[i])/2
            
            x2=abs((individuo1.genes[i]-individuo2.genes[i])/2)
            
            # recombinación de ADN
            
            hijo1.genes[i]=x1+beta*x2
            hijo2.genes[i]=x1-beta*x2
            
        return hijo1,hijo2
    
    
    
    # Si el valor de u es menor o igual a 0.5, entonces la expresión generará
    # un valor de beta cercano a 1, lo que significa que los nuevos hijos se 
    # generarán cerca de los padres. Si el valor de u es mayor que 0.5, 
    # entonces la expresión generará un valor de beta cercano a 0, lo que 
    # significa que los nuevos hijos se generarán lejos de los padres
    
    
    def __get_beta(self):
        u=random.random()
        
        if u<=0.5:
            return (2*u)**(1/(self.param_cruce+1))
        return (2*(1-u))**(-1/(self.param_cruce+1))
    
    
    
    def __mutar(self, hijo):
        
        n_genes = len(hijo.genes)
        
        
        for gen in range(n_genes):
            
            # Obtener un número aleatorio y un valor delta aleatorio
            u, delta = self.__get_delta()
            
            # Si el número aleatorio es menor que 0,5, mutar el gen en función de su distancia al límite inferior
            if u < 0.5:
                hijo.genes[gen] += delta * (hijo.genes[gen] - self.problema.rango_variables[gen][0])
            # De lo contrario, mutar el gen en función de su distancia al límite superior
            else:
                hijo.genes[gen] += delta * (self.problema.rango_variables[gen][1] - hijo.genes[gen])
            
            # Comprobar si el gen mutado está fuera de los límites, y corregirlo si es necesario
            if hijo.genes[gen] < self.problema.rango_variables[gen][0]:
                hijo.genes[gen] = self.problema.rango_variables[gen][0]
            elif hijo.genes[gen] > self.problema.rango_variables[gen][1]:
                hijo.genes[gen] = self.problema.rango_variables[gen][1]

    def __get_delta(self):
        u = random.random()
        
        if u<0.5:
            return u,(2*u)**(1/(self.param_mutacion +1)) - 1
        return u,1-(2*(1-u))**(1/(self.param_mutacion+1))
    
    # Binary Tournament Selection (selección por torneo binario)
    def __competencia(self, poblacion):
        # Seleccionar un par aleatorio de la población para la competencia
        participantes = random.sample(poblacion.poblacion, self.n_participantes)
        
        # Inicializar la mejor solución a "None"
        best = None
        
        # Iterar a través de cada participante
        for participante in participantes:
            # Si la mejor solución es "None" o el participante es mejor que la mejor solución actual, actualice la mejor solución
            if best is None or (self.crowding_operator(participante, best) == 1):
                best = participante
        
        # Devolver la mejor solución encontrada en la competencia
        return best

    