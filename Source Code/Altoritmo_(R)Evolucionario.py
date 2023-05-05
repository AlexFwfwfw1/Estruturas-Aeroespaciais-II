import Main
import Condicoes_Iniciais
import numpy as np
import Massa_E_Custo
import sys

from multiprocessing import Pool, cpu_count

Dados_Precomputados = Condicoes_Iniciais.Matriz_K_Possbilities, Condicoes_Iniciais.Matriz_Theta_Possibilidades

N_Inical = 25

Laminado1 = N_Inical*np.ones(Condicoes_Iniciais.Formato_1, dtype=int)
Laminado2 = N_Inical*np.ones(Condicoes_Iniciais.Formato_1, dtype=int)
Laminado3 = N_Inical*np.ones(Condicoes_Iniciais.Formato_3, dtype=int)
Laminado_Inicial = np.append(np.append(Laminado1, Laminado2, axis=0), Laminado3, axis=0)

Calculated_Sim = 0
Generation_Birth = 10
#The bigger the population, the bigger the porbability of finding the global minimum
Maximum_Population = 200

Espessura = 0

def Analisar(Laminado_Geral):
    #print(Laminado_Geral)
    global Calculated_Sim
    Calculated_Sim += 1
    
    Laminado1, Laminado2, Laminado3 = np.split(2*Laminado_Geral, [Condicoes_Iniciais.Formato_1[0], Condicoes_Iniciais.Formato_1[0]*2])
    return Main.Simulacao(Laminado1, Laminado2, Laminado3, Espessura, Dados_Precomputados)

def Minimo(Laminado_Geral):
    global Calculated_Sim
    Calculated_Sim += 1
    
    Laminado1, Laminado2, Laminado3 = np.split(2*Laminado_Geral, [Condicoes_Iniciais.Formato_1[0], Condicoes_Iniciais.Formato_1[0]*2])
    return Massa_E_Custo.Recalcular_Funcao_Minimo(Laminado1, Laminado2, Laminado3, Espessura)

def Create_Childs(Parent):
    
    Childs = []
    for _ in range(Generation_Birth):
        Child_Laminado = np.copy(Parent[0]) - np.random.randint(-1,2, size=Laminado_Inicial.shape)
        #Cap to positive Vales
        Child_Laminado[Child_Laminado < 0] = 0
        if not Analisar(Child_Laminado):
            Childs.append((Child_Laminado, Minimo(Child_Laminado)))
    return Childs

def Flatten_List(Childs, Survivors):
    Childs = [item for sublist in Childs for item in sublist]
    Survivors = [Survivors]
    Survivors.append(Childs)
    return [item for sublist in Survivors for item in sublist]
 

def Algoritmo_Otimizacao(Laminado_Geral):
    Survivors = []
    Generation = 0
    #Minimizar Camadas
    while not Analisar(Laminado_Geral):
        Laminado_Geral -= 1
    Laminado_Geral += 1
    Survivors.append((Laminado_Geral, Minimo(Laminado_Geral)))
    while True:
        Generation += 1
        with Pool(cpu_count()) as MultiCore:
            #Generate 20 copies and apply a random decrese to each Parent.
            Childs = MultiCore.map(Create_Childs, Survivors)
            #Flatten Lists beacuse of wierd artifacts on list mechanics.
            Survivors = Flatten_List(Childs, Survivors)
            
        #Sort by Minimizing Function and 
        Survivors = sorted(Survivors, key=lambda x: x[1])
        while len(Survivors) > Maximum_Population:
            Survivors.pop()                    
        print(f"Generation: {Generation}")
        print(f"Best Case Yet: {Survivors[0][0]} with f: {Survivors[0][1]}")   
     
# Compensar(Laminado_Inicial, 0, (0,0))

if __name__ == "__main__":
    Algoritmo_Otimizacao(Laminado_Inicial)
