from poblacion import Poblacion
from utils import NSGA2
from tqdm import tqdm


class Evolucion:
    
    def __init__(self,problema,n_generaciones,n_individuos,n_participantes,param_cruce,param_mutacion):
        self.utils=NSGA2(problema,n_individuos,n_participantes,param_cruce,param_mutacion)
        
        self.poblacion=None
        self.n_generaciones=n_generaciones
        self.generacion_terminada=[]
        self.n_individuos=n_individuos
        
    def evolucionar(self):
        # Crear población inicial
        self.poblacion = self.utils.crear_poblacion_inicial()
        
        # Clasificar la población en frentes de no dominancia
        self.utils.nondominated_sort(self.poblacion)
        
        # Calcular la distancia crowding para cada individuo en cada frente de no dominancia
        for frente in self.poblacion.frentes:
            
            self.utils.calcular_crowding_distance(frente)
            
        # Crear hijos a partir de la población actual
        hijos = self.utils.crear_hijos(self.poblacion)
        poblacion_retornada = None
        

        # Iterar a través de las generaciones
        for i in tqdm(range(self.n_generaciones)):
            
            # Agregar los hijos a la población actual
            self.poblacion.extend(hijos)
            # Clasificar la nueva población en frentes de no dominancia
            self.utils.nondominated_sort(self.poblacion)
            # Crear una nueva población vacía
            nueva_poblacion = Poblacion()
            frente_i = 0
            # Agregar individuos de los frentes de no dominancia a la nueva población hasta que se alcance el tamaño deseado (2N)
            # solo toma los frentes necesarios, ya que los frentes ya estan sorteados
            
            # ciclo de recorte de obsoletos
            while len(nueva_poblacion) + len(self.poblacion.frentes[frente_i]) <= self.n_individuos:
                # Calcular la distancia crowding para cada individuo en el frente actual
                self.utils.calcular_crowding_distance(self.poblacion.frentes[frente_i])
                # Agregar todos los individuos del frente actual a la nueva población
                nueva_poblacion.extend(self.poblacion.frentes[frente_i])
                # Pasar al siguiente frente de Pareto
                frente_i += 1
                
        
            self.utils.calcular_crowding_distance(self.poblacion.frentes[frente_i])
            
            
            # Ordenar el último frente de Pareto en orden decreciente de distancia crowding y agregar los mejores individuos a la nueva población
            
            self.poblacion.frentes[frente_i].sort(key=lambda individuo: individuo.crowding_distance, reverse=True)
            
            #Asegurarse de que el tamaño sea el correcto
            nueva_poblacion.extend(self.poblacion.frentes[frente_i][0:self.n_individuos - len(nueva_poblacion)])
            
            # Actualizar la población actual con la nueva población
            self.poblacion = nueva_poblacion
            # Clasificar la población actual en frentes de Pareto
            self.utils.nondominated_sort(self.poblacion)
            # Calcular la distancia crowding para cada individuo en cada frente de Pareto
            for frente in self.poblacion.frentes:
                self.utils.calcular_crowding_distance(frente)
            # Crear hijos a partir de la población actual para la próxima generación
            hijos = self.utils.crear_hijos(self.poblacion)
        
        return self.poblacion.frentes[0]

            
