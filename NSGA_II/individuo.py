class Individuo(object):
    def __init__(self):
        self.rango = None
        self.crowding_distance=None
        self.veces_dominado=None
        self.conjunto_dominado=None
        self.genes=None
        self.funciones=None
        
    def __eq__(self,otro):
        if isinstance(self,otro.__class__):
            return self.genes==otro.genes
        return False
    
    def dominancia(self,otro):
        conjuncion=True
        disyuncion=False
        
        for coor1,coor2 in zip(self.funciones,otro.funciones):
            conjuncion=conjuncion and coor1<=coor2
            disyuncion=disyuncion or coor1<coor2
        return (conjuncion and disyuncion)
            
            