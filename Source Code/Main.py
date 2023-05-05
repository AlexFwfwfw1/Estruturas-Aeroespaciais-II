from Constantes import *

import Definicao_Laminado
import Propriadades_Seccao
import Carregamento
import Analise_Estrutural
import Afilamento
import Condicoes_Iniciais
import Massa_E_Custo

import numpy as np
from Configuration import NUMERO_DE_SECCOES
from timeit import default_timer as timer
import Debug

TORCAO_MAX = np.deg2rad(50)
DEFLECAO_MAX = np.deg2rad(50)
            
def Simulacao(Laminado1, Laminado2, Laminado3, Espessura_Tensor, Dados_Precomputados):
    
    Debug.Resetar_Debug()
    Peso_Cauda = 0
    
    Matriz_K_Possbilities, Matriz_Theta_Possibilidades = Dados_Precomputados
    
    #Calcular Matrizes e Propriadades Equivalentes
    Laminado_1 = Definicao_Laminado.Laminado_Class(Laminado1, Matriz_K_Possbilities, Matriz_Theta_Possibilidades, "Laminado_1")
    Laminado_2 = Definicao_Laminado.Laminado_Class(Laminado2, Matriz_K_Possbilities, Matriz_Theta_Possibilidades, "Laminado_2")
    Laminado_3 = Definicao_Laminado.Laminado_Class(Laminado3, Matriz_K_Possbilities, Matriz_Theta_Possibilidades, "Laminado_3")

    Laminados = (Laminado_1,Laminado_2,Laminado_3)
    print(Laminado_1.rho_Medio,Laminado_2.rho_Medio,Laminado_3.rho_Medio)
    Torcao, Deflecao = 0,0
    for Seccao_Z in np.linspace(COMPRIMENTO_FUSELAGEM,0,NUMERO_DE_SECCOES):
        # Propriadades da Seccao
        Seccao = Propriadades_Seccao.Definir_Propriadades(Seccao_Z, Laminados, Espessura_Tensor)
        
        
        # Carregamento
        Forcas, Momentos, Peso_Cauda = Carregamento.Obter_Forcas_e_Momentos(Seccao_Z, Seccao.Peso_Por_Metro, Peso_Cauda)

        #Forcas de Corte dado o Afilamento
        Forcas_Afilamento, Falha_Return = Afilamento.F_Afilamento(Seccao, Momentos, Forcas, Laminado_3)  
        if Falha_Return:
            return True
        
        #Analise_Estrutural Tensoes Diretas, Corte e Qs0 é feito em parelo de forma a poupar memoria e tempo de calculo
        Falha_Return, Taxa_Torcao, Taxa_Deflecao = Analise_Estrutural.Analise_Total(Seccao, Forcas, Momentos, Laminados, Forcas_Afilamento)
        if Falha_Return:
            return True
        
        if Seccao_Z == 0 or Seccao_Z == COMPRIMENTO_FUSELAGEM:
            Taxa_Torcao = Taxa_Torcao*0.5
            Taxa_Deflecao = Taxa_Deflecao*0.5
        Torcao += Taxa_Torcao
        Deflecao += Taxa_Deflecao
        
    Torcao, Deflecao = abs(Torcao*COMPRIMENTO_FUSELAGEM/NUMERO_DE_SECCOES), abs(Deflecao*COMPRIMENTO_FUSELAGEM/NUMERO_DE_SECCOES)
    # print(f"Torcao: {np.rad2deg(Torcao)} º, Deflecao: {np.rad2deg(Deflecao)} º, FS: ")
    if not Debug.DEBUG:
        if Torcao >= TORCAO_MAX:
            return True
        if Deflecao >= DEFLECAO_MAX:
            return True
    else:
        return Debug.Sort_By_FS(), TORCAO_MAX/Torcao, DEFLECAO_MAX/Deflecao
    print("Nao Falhou")
    return False
        
    

if __name__ == "__main__":
    
    Dados_Precomputados = Condicoes_Iniciais.Matriz_K_Possbilities,Condicoes_Iniciais.Matriz_Theta_Possibilidades

    Espessura_Tensor = Condicoes_Iniciais.Espessura_Tensor
    
    # Obter Laminado
    Laminado_1 = Condicoes_Iniciais.Laminado_Lista_1
    Laminado_2 = Condicoes_Iniciais.Laminado_Lista_2
    Laminado_3 = Condicoes_Iniciais.Laminado_Lista_3

    #F_Min = Massa_E_Custo.Recalcular_Funcao_Minimo(Laminado_1, Laminado_2, Laminado_3, Espessura_Tensor)
    start = timer()
    temp = Simulacao(Laminado_1, Laminado_2, Laminado_3, Espessura_Tensor, Dados_Precomputados)
    if Debug.DEBUG:
        Falha, Torcao, Deflecao = temp
        print(f"Ponto critico: {Falha[1]}, F.S : {Falha[0]} , Laminado: {Falha[2]}")
        print(f"Torcao F.S: {Torcao}, Deflecao F.S : {Deflecao} ")
    else:
        print(temp)
    end = timer()
    print(f"Time Elapsed: {round((end-start)*1000, 5)} ms")
    #print(F_Min)
