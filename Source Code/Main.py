from Constantes import *

import Definicao_Laminado
import Propriadades_Seccao
import Carregamento
import Analise_Estrutural
import Afilamento
import Condicoes_Iniciais

import numpy as np
from Configuration import NUMERO_DE_SECCOES, Debug
from timeit import default_timer as timer

TORCAO_MAX = np.deg2rad(0.5)
DEFLECAO_MAX = np.deg2rad(0.5)
            
def Simulacao(Laminado1, Laminado2, Laminado3, Espessura_Tensor, Dados_Precomputados):
    
    if Debug:
        Metodo_Min = []
    
    Matriz_K_Possbilities, Matriz_Theta_Possibilidades = Dados_Precomputados
    
    #Calcular Matrizes e Propriadades Equivalentes
    Laminado_1 = Definicao_Laminado.Laminado_Class(Laminado1, Matriz_K_Possbilities, Matriz_Theta_Possibilidades)
    Laminado_2 = Definicao_Laminado.Laminado_Class(Laminado2, Matriz_K_Possbilities, Matriz_Theta_Possibilidades)
    Laminado_3 = Definicao_Laminado.Laminado_Class(Laminado3, Matriz_K_Possbilities, Matriz_Theta_Possibilidades)

    Laminados = (Laminado_1,Laminado_2,Laminado_3)

    Torcao, Deflecao = 0,0

    for Seccao_Z in np.linspace(0,COMPRIMENTO_FUSELAGEM,NUMERO_DE_SECCOES):
        # Propriadades da Seccao
        Seccao = Propriadades_Seccao.Definir_Propriadades(Seccao_Z, Laminados, Espessura_Tensor)
        
        # Carregamento
        Forcas, Momentos = Carregamento.Obter_Forcas_e_Momentos(Seccao_Z)

        #Forcas de Corte dado o Afilamento
        Forcas_Afilamento = Afilamento.F_Afilamento(Seccao, Momentos, Forcas)  
        
        #Analise_Estrutural Tensoes Diretas, Corte e Qs0 é feito em parelo de forma a poupar memoria e tempo de calculo
        Fs_Falha, Taxa_Torcao, Taxa_Deflecao = Analise_Estrutural.Analise_Total(Seccao, Forcas, Momentos, Laminados, Forcas_Afilamento)
        if Debug:
            Metodo_Min.append(Fs_Falha) 
        elif Fs_Falha == 1:
            return 1, "Rotura"
        
        if Seccao_Z == 0 or Seccao_Z == COMPRIMENTO_FUSELAGEM:
            Torcao /= 2
            Deflecao /= 2
        Torcao += Taxa_Torcao
        Deflecao += Taxa_Deflecao
    
    if Torcao >= TORCAO_MAX:
        return 1, "Torcao"
    if Deflecao >= DEFLECAO_MAX:
        return 1, "Deflecao"
    
    if Debug:
        return sorted(Metodo_Min,key=lambda x: x[0])[0], TORCAO_MAX/Torcao, DEFLECAO_MAX/Deflecao
    return 0
        
    

if __name__ == "__main__":
    
    Dados_Precomputados = Condicoes_Iniciais.Matriz_K_Possbilities,Condicoes_Iniciais.Matriz_Theta_Possibilidades

    Espessura_Tensor = Condicoes_Iniciais.Espessura_Tensor
    
    # Obter Laminado
    Laminado_1 = Condicoes_Iniciais.Laminado_Lista_1
    Laminado_2 = Condicoes_Iniciais.Laminado_Lista_2
    Laminado_3 = Condicoes_Iniciais.Laminado_Lista_3

    start = timer()
    Falha, Torcao, Deflecao = Simulacao(Laminado_1, Laminado_2, Laminado_3, Espessura_Tensor, Dados_Precomputados)
    print(f"Ponto critico: {Falha[1]}, F.S : {Falha[0]} ")
    print(f"Torcao F.S: {Torcao}, Deflecao F.S : {Deflecao} ")
    end = timer()
    print(f"Time Elapsed: {round((end-start)*1000, 5)} ms")
