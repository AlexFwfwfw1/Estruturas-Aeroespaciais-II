from Constantes import *
import Definicao_Laminado
import Propriadades_Seccao
import Carregamento
import Analise_Estrutural

import Condicoes_Iniciais

import numpy as np
from alive_progress import alive_bar

from timeit import default_timer as timer

NUMERO_DE_SECCOES = 20
            
def Main():

    Espessura_Tensor = Condicoes_Iniciais.Espessura_Tensor
    
    # Obter Laminado
    Laminado_1 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_1)
    Laminado_2 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_2)
    Laminado_3 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_3)

    Laminados = (Laminado_1,Laminado_2,Laminado_3)
    with alive_bar(total=NUMERO_DE_SECCOES) as bar:
        for Seccao_Z in np.linspace(0,COMPRIMENTO_FUSELAGEM,NUMERO_DE_SECCOES):
            #print(f"Seccao = {Seccao_Z}")
            # Propriadades da Seccao
            Segundo_Momentos_De_Area, Centroide, Geometria_Media, Coordenadas_X, Coordenadas_Y, Espessuras, Elasticidades = Propriadades_Seccao.Definir_Propriadades(
                Seccao_Z, Laminados, Espessura_Tensor)
            
            # Carregamento
            Forcas, Momentos = Carregamento.Obter_Forcas_e_Momentos(Seccao_Z)

            #Forcas de Corte dado o Afilamento
            # Forcas_SW = Afilamento.Obter_Forcas(Forcas, ... )  
            Forcas_SW = Forcas  #TEMPORARIO, ISTO ESTA ERRADo
            
            #Tensoes Diretas
            Tensoes_Diretas = Analise_Estrutural.Tensao_Direta(Geometria_Media, Centroide, Segundo_Momentos_De_Area, Momentos, Elasticidades)
            
            #Tensoes De Corte
            Tensoes_Corte = Analise_Estrutural.Tensao_de_Corte(Geometria_Media, Centroide, Segundo_Momentos_De_Area, Forcas_SW, Elasticidades, Espessuras, Coordenadas_Y, Coordenadas_X)
            
            bar()
    
    print(f"{NUMERO_DE_SECCOES} seccoes analisadas." )
    
if __name__ == "__main__":
    start = timer()
    Main()
    end = timer()
    print(end-start)