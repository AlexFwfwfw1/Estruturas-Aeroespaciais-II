import Main
import Condicoes_Iniciais
import numpy as np
import Massa_E_Custo
import sys

Dados_Precomputados = Condicoes_Iniciais.Matriz_K_Possbilities, Condicoes_Iniciais.Matriz_Theta_Possibilidades

N_Inical = 25

Laminado1 = N_Inical*np.ones(Condicoes_Iniciais.Formato_1, dtype=int)
Laminado2 = N_Inical*np.ones(Condicoes_Iniciais.Formato_1, dtype=int)
Laminado3 = N_Inical*np.ones(Condicoes_Iniciais.Formato_3, dtype=int)
Laminado_Inicial = np.append(np.append(Laminado1, Laminado2, axis=0), Laminado3, axis=0)

Calculated_Sim = 0

def Analisar(Laminado_Geral, Espessura):
    print(Laminado_Geral)
    global Calculated_Sim
    Calculated_Sim += 1
    
    Laminado1, Laminado2, Laminado3 = np.split(2*Laminado_Geral, [Condicoes_Iniciais.Formato_1[0], Condicoes_Iniciais.Formato_1[0]*2])
    return Main.Simulacao(Laminado1, Laminado2, Laminado3, Espessura, Dados_Precomputados)

def Minimo(Laminado_Geral, Espessura):
    global Calculated_Sim
    Calculated_Sim += 1
    
    Laminado1, Laminado2, Laminado3 = np.split(2*Laminado_Geral, [Condicoes_Iniciais.Formato_1[0], Condicoes_Iniciais.Formato_1[0]*2])
    return Massa_E_Custo.Recalcular_Funcao_Minimo(Laminado1, Laminado2, Laminado3, Espessura)

                    
  
def Compensar(Laminado_Geral, Espessura, Coordenada):
    Temp_Min, Temp_Laminado = 10e100, None
    with np.nditer(Laminado_Geral, op_flags=['readwrite'], flags=['multi_index']) as it:
        for Simulacao in it:
            if it.multi_index != Coordenada and Simulacao[...] > 0 :
                Simulacao[...] -= 1
                Laminado_Geral[Coordenada] += 1
                F_Min = Minimo(Laminado_Geral, Espessura)
                if F_Min < Temp_Min and not Analisar(Laminado_Geral, Espessura):
                    Temp_Min = F_Min
                    Temp_Laminado = Laminado_Geral
                Simulacao[...] += 1
                Laminado_Geral[Coordenada] -= 1
    
    return Temp_Laminado

def Algoritmo_Otimizacao(Laminado_Geral, Espessura):
    Hash = []
    
                        

# Compensar(Laminado_Inicial, 0, (0,0))
Algoritmo_Otimizacao(Laminado_Inicial, 0)
