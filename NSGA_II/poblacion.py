class Poblacion:
    def __init__(self):
        self.poblacion=[]   
        self.frentes=[]   
    
    def __len__(self):
        return len(self.poblacion)   
    
    def __iter__(self):
        # Devuelve un iterador para la población
        return self.poblacion.__iter__()   
    
    def extend(self,hijos):
        
        # Crea Q
        self.poblacion.extend(hijos)  
        
    def append(self,hijos):
        # Inserta Q en R 
        self.poblacion.append(hijos)   
