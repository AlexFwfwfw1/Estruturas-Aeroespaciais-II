from Constantes import *

import Definicao_Laminado
import Propriadades_Seccao
import Carregamento
import Analise_Estrutural
import Afilamento
import Condicoes_Iniciais
import Massa_E_Custo
import Torcao_Deflecao

import numpy as np
from Configuration import NUMERO_DE_SECCOES, Plotting
from timeit import default_timer as timer
import Debug

import Plotting_Lib

TORCAO_MAX = 0.5
DEFLECAO_MAX = 0.5

Paco_Z = COMPRIMENTO_FUSELAGEM/NUMERO_DE_SECCOES 
            
def Simulacao(Laminado1, Laminado2, Laminado3, Espessura_Tensor, Dados_Precomputados):
    
    Debug.Resetar_Debug()
    Peso_Cauda = []
    Peso_Por_Metro = 0
    
    Matriz_K_Possbilities, Matriz_Theta_Possibilidades = Dados_Precomputados
    
    #Calcular Matrizes e Propriadades Equivalentes
    Laminado_1 = Definicao_Laminado.Laminado_Class(Laminado1, Matriz_K_Possbilities, Matriz_Theta_Possibilidades, "Laminado_1")
    Laminado_2 = Definicao_Laminado.Laminado_Class(Laminado2, Matriz_K_Possbilities, Matriz_Theta_Possibilidades, "Laminado_2")
    Laminado_3 = Definicao_Laminado.Laminado_Class(Laminado3, Matriz_K_Possbilities, Matriz_Theta_Possibilidades, "Laminado_3")

    if Laminado_1.Cancelar == True or Laminado_2.Cancelar == True or Laminado_3.Cancelar == True :
        return True
    Laminados = (Laminado_1,Laminado_2,Laminado_3)
    
    Torcao, Deflecao = [],[]
    Seccoes_Z_List = np.linspace(COMPRIMENTO_FUSELAGEM,0,NUMERO_DE_SECCOES)
    for Seccao_Z in Seccoes_Z_List:
        # Propriadades da Seccao
        Seccao = Propriadades_Seccao.Definir_Propriadades(Seccao_Z, Laminados, Espessura_Tensor)
        
        # Carregamento
        Forcas, Momentos = Carregamento.Obter_Forcas_e_Momentos(Seccao_Z, Peso_Por_Metro, Peso_Cauda)

        #Forcas de Corte dado o Afilamento
        Forcas_Afilamento, Falha_Return = Afilamento.F_Afilamento(Seccao, Momentos, Forcas, Laminado_3, Seccao_Z)  
        if Falha_Return:
            return True
        
        #Analise_Estrutural Tensoes Diretas, Corte e Qs0 é feito em parelo de forma a poupar memoria e tempo de calculo
        Falha_Return, Taxa_Torcao, Taxa_Deflecao = Analise_Estrutural.Analise_Total(Seccao, Forcas, Momentos, Laminados, Forcas_Afilamento, Seccao_Z)
        if Falha_Return:
            return True
        Torcao.append(Taxa_Torcao)
        Deflecao.append(Taxa_Deflecao)
    Theta_Z, Theta_X, Delta_Y = Torcao_Deflecao.Deformacao_E_Torcao(Torcao, Deflecao, Paco_Z)
    if Plotting:
        Plotting_Lib.Plot()
    
    print(f"Torcao: {Theta_Z} graus, Deflecao: {Theta_X} graus, Deflecao_Metro: {Delta_Y} metros")#,  Deflecao_Msx: {Deflecao_abs} metros")
    if not Debug.DEBUG:
        if abs(Theta_Z) >= TORCAO_MAX:
            return True
        if abs(Theta_X) >= DEFLECAO_MAX:
            return True
    else:
        return Debug.Sort_By_FS(), TORCAO_MAX/Theta_Z, DEFLECAO_MAX/Theta_X
    #print("Nao Falhou")
    return False
        
    

if __name__ == "__main__":
    Debug.DEBUG = True
    Dados_Precomputados = Condicoes_Iniciais.Matriz_K_Possbilities,Condicoes_Iniciais.Matriz_Theta_Possibilidades

    Espessura_Tensor = Condicoes_Iniciais.Espessura_Tensor
    
    # Obter Laminado
    Laminado_1 = Condicoes_Iniciais.Laminado_Lista_1
    Laminado_2 = Condicoes_Iniciais.Laminado_Lista_2
    Laminado_3 = Condicoes_Iniciais.Laminado_Lista_3

    #F_Min = Massa_E_Custo.Recalcular_Funcao_Minimo(Laminado_1, Laminado_2, Laminado_3, Espessura_Tensor)
    start = timer()
    temp = Simulacao(Laminado_1, Laminado_2, Laminado_3, Espessura_Tensor, Dados_Precomputados)
    F_min = Massa_E_Custo.Recalcular_Funcao_Minimo(Laminado_1, Laminado_2, Laminado_3, Espessura_Tensor)
    if Debug.DEBUG:
        Falha, Torcao, Deflecao = temp
        print(f"Ponto critico: {Falha[1]}, F.S : {Falha[0]} , Laminado: {Falha[2]}")
        print(f"Torcao F.S: {Torcao}, Deflecao F.S : {Deflecao}, F_min: {F_min} ")
    else:
        print(temp)
    end = timer()
    print(f"Time Elapsed: {round((end-start)*1000, 5)} ms")
    #print(F_Min)
