from Constantes import *
import Definicao_Laminado
import Propriadades_Seccao
import Carregamento
import Analise_Estrutural
import Tensores

import Condicoes_Iniciais

import numpy as np

from timeit import default_timer as timer

NUMERO_DE_SECCOES = 20
            
def Simulacao(Laminado_1,Laminado_2,Laminado_3,Espessura_Tensor):


    Laminados = (Laminado_1,Laminado_2,Laminado_3)

    for Seccao_Z in np.linspace(0,COMPRIMENTO_FUSELAGEM,NUMERO_DE_SECCOES):
        #print(f"Seccao = {Seccao_Z}")
        # Propriadades da Seccao
        Seccao = Propriadades_Seccao.Definir_Propriadades(Seccao_Z, Laminados, Espessura_Tensor)
        
        # Carregamento
        Forcas, Momentos = Carregamento.Obter_Forcas_e_Momentos(Seccao_Z)

        #Forcas de Corte dado o Afilamento
        # Forcas_SW = Tensores.F_Afilamento(????)  
        
        
        #Analise_Estrutural Tensoes Diretas, Corte e Qs0 é feito em parelo de forma a poupar memoria e tempo de calculo
        FS_Falha = Analise_Estrutural.Analise_Total(Seccao, Forcas, Momentos)
        
    print(f"{NUMERO_DE_SECCOES} seccoes analisadas." )
    
    
    
#Condicoes Iniciais
Espessura_Tensor = Condicoes_Iniciais.Espessura_Tensor

# Obter Laminado
Laminado_1 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_1)
Laminado_2 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_2)
Laminado_3 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_3)

if __name__ == "__main__":
    start = timer()
    Simulacao(Laminado_1, Laminado_2, Laminado_3, Espessura_Tensor)
    end = timer()
    print(end-start)