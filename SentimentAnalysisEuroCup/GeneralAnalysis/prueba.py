import pandas as pd


def analisis_formageneral():
    
    df=pd.read_csv('playersbrian31.csv').astype(str)
    grande=pd.DataFrame()
    df = df.drop(index=0)
    nombres = ['Fecha','Jugador', 'Inmigrante', 'Gol', 'Resultado']
    for i in range(1, len(df.columns)-1, 3):
        # Obtener las 3 columnas actuales
        cols = pd.concat([df.iloc[:,0],df.iloc[:, i:i+3],df.iloc[:, -1]],axis=1)
        # Cambiamos los nombres de las columnas del dataframe
        cols.set_axis(nombres, axis=1, inplace=True)
        grande = pd.concat([grande, cols], axis=0, ignore_index=True)
        # Hacer lo que necesites con las 3 columnas
        #print(cols)
    print(grande)
    grande.to_csv('finalplayersf.csv')
        
def main():
    analisis_formageneral()
    
if __name__ == '__main__':
    main()