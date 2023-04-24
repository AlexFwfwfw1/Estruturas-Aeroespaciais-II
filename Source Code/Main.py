from Constantes import *
import Definicao_Laminado
import Propriadades_Seccao
import Carregamento
import Analise_Estrutural

import Condicoes_Iniciais

import numpy as np

from timeit import default_timer as timer

NUMERO_DE_SECCOES = 20

Torcao_Max = np.deg2rad(0.5)
Deflecao_Max = np.deg2rad(0.5)
            
def Main(Laminado1, Laminado2, Laminado3, Espessura_Tensor):

    Laminados = (Laminado1,Laminado2,Laminado3)

    Torcao, Deflecao = 0,0

    for Seccao_Z in np.linspace(0,COMPRIMENTO_FUSELAGEM,NUMERO_DE_SECCOES):
        #print(f"Seccao = {Seccao_Z}")
        # Propriadades da Seccao
        Seccao = Propriadades_Seccao.Definir_Propriadades(Seccao_Z, Laminados, Espessura_Tensor)
        
        # Carregamento
        Forcas, Momentos = Carregamento.Obter_Forcas_e_Momentos(Seccao_Z)

        #Forcas de Corte dado o Afilamento
        # Forcas_SW = Afilamento.Obter_Forcas(Forcas, ... )  
        Forcas_SW = Forcas  #TEMPORARIO, ISTO ESTA ERRADo
        
        #Analise_Estrutural Tensoes Diretas, Corte e Qs0 é feito em parelo de forma a poupar memoria e tempo de calculo
        FS_Falha,Taxa_Torcao, Taxa_Deflecao = Analise_Estrutural.Analise_Total(Seccao, Forcas, Momentos, Laminados)
        if FS_Falha == 1:
            return 1
        
        Torcao, Deflecao += Taxa_Torcao, Taxa_Deflecao
    
    if Torcao >= Torcao_Max or Deflecao >= Deflecao_Max:
        return 1
    return 0
        
    
if __name__ == "__main__":

    Espessura_Tensor = Condicoes_Iniciais.Espessura_Tensor
    
    # Obter Laminado
    Laminado_1 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_1)
    Laminado_2 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_2)
    Laminado_3 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_3)


    start = timer()
    Main()
    end = timer()
    print(end-start)
