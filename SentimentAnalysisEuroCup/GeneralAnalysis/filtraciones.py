import pandas as pd
import os
from jugadoresspacy import analizar
from analize_tweets import analizarglobal

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

def filtrar():
    
    jugadores = pd.read_csv('finalplayers.csv')

    # Inmigrante, gol,gana
    igg = jugadores.loc[(jugadores['inmigrante'] == 1) & (jugadores['gol'] == 1) & (jugadores['resultado'] == 'GANO')]

    # Inmigrante,no gol,no gana
    ingng = jugadores.loc[(jugadores['inmigrante'] == 1) & (jugadores['gol'] == 0) & (jugadores['resultado'] == 'PERDIO')]
    
    # no inmigrante, hace Gol, gana
    nigg = jugadores.loc[(jugadores['inmigrante'] == 0) & (jugadores['gol'] == 1) & (jugadores['resultado'] == 'GANO')]
    
    # no inmigrante, no gol, no gana
    ningng = jugadores.loc[(jugadores['inmigrante'] == 0) & (jugadores['gol'] == 0) & (jugadores['resultado'] == 'PERDIO')]

    os.mkdir("resultados_filtracion")
    resultadosigg = analizar(igg)
    resultadosigg.to_csv('resultados_filtracion/inmigrantes_gol_gana.csv')
    resultadosingng = analizar(ingng)
    resultadosingng.to_csv('resultados_filtracion/inmigrantes_nogol_nogana.csv')
    resultadosnigg = analizar(nigg)
    resultadosnigg.to_csv('resultados_filtracion/noinmigrantes_gol_gana.csv')
    resultadosningng = analizar(ningng)
    resultadosningng.to_csv('resultados_filtracion/noinmigrantes_nogol_nogana.csv')
    
    # Un archivo para cada jugador con la fecha, si gano, si hizo gol, si es inmigrante.


def main():
   filtrar()
   #analizarglobal()


if __name__ == '__main__':
    main()