import Main
import Condicoes_Iniciais
import numpy as np
import Massa_E_Custo
import sys
sys.setrecursionlimit(100000000)

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
    
def Verificar_Falha(Laminado_Geral, Espessura):
    Hash = []
    
    with np.nditer(Laminado_Geral, op_flags=['readwrite'], flags=['multi_index']) as it:
        for Simulacao in it:
            if Simulacao[...] > 0 :
                Simulacao[...] -= 1
                if Analisar(Laminado_Geral, Espessura):
                    Algoritmo_Otimizacao(Compensar(Laminado_Geral, Espessura, it.multi_index))
                else:
                    Hash.append((Laminado_Geral, Minimo(Laminado_Geral, Espessura)))
                Simulacao[...] += 1
                
    for Angle in range(len(Laminado_Geral)):
        if not np.all(Laminado_Geral[Angle] == 0) :
            Laminado_Geral[Laminado_Geral < 0] = 0
            Laminado_Geral[Angle] -= 1
            
            if Analisar(Laminado_Geral, Espessura):
                Algoritmo_Otimizacao(Compensar(Laminado_Geral, Espessura))
            else:
                Hash.append((Laminado_Geral, Minimo(Laminado_Geral, Espessura)))
            Laminado_Geral[Angle] += 1
            
    for Column in range(np.shape(Laminado_Geral)[1]):
        if not np.all(Laminado_Geral[:,Column] == 0) :
            Laminado_Geral[Laminado_Geral < 0] = 0
            Laminado_Geral[:,Column] -= 1
            
            if Analisar(Laminado_Geral, Espessura):
                Algoritmo_Otimizacao(Compensar(Laminado_Geral, Espessura))
            else: 
                Hash.append((Laminado_Geral, Minimo(Laminado_Geral, Espessura)))
            Laminado_Geral[:,Column] += 1
    return sorted(Hash, key=lambda x: x[1])[0][0]

def Algoritmo_Otimizacao(Laminado_Geral, Espessura):
    if not Analisar(Laminado_Geral, Espessura):
        Laminado_Geral -= 1
        Laminado_Geral[Laminado_Geral < 0] = 0
        return Algoritmo_Otimizacao(Laminado_Geral, Espessura)
    else:
        Laminado_Copia = Laminado_Geral + 1
        Laminado_Compensado = Verificar_Falha(Laminado_Copia, Espessura)
        print(Laminado_Compensado)
        raise
        return Algoritmo_Otimizacao(Laminado_Compensado, Espessura)
        
                        

# Compensar(Laminado_Inicial, 0, (0,0))
Algoritmo_Otimizacao(Laminado_Inicial, 0)
