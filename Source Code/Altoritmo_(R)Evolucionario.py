import Main
import Condicoes_Iniciais
import numpy as np
import Massa_E_Custo

from multiprocessing import Pool, cpu_count
from alive_progress import alive_bar 

Dados_Precomputados = Condicoes_Iniciais.Matriz_K_Possbilities, Condicoes_Iniciais.Matriz_Theta_Possibilidades

N_Inical = 25

Laminado1 = N_Inical*np.ones(Condicoes_Iniciais.Formato_1, dtype=int)
Laminado2 = N_Inical*np.ones(Condicoes_Iniciais.Formato_1, dtype=int)
Laminado3 = N_Inical*np.ones(Condicoes_Iniciais.Formato_3, dtype=int)
Laminado_Inicial = np.append(np.append(Laminado1, Laminado2, axis=0), Laminado3, axis=0)

Calculated_Sim = 0
Generation_Birth = 15
#The bigger the population, the bigger the porbability of finding the global minimum
Maximum_Population = 200

Estagnacao_Atingida = 5
Estagnacao_Max = 20
Espessura = 0

Espessura_Multipler = 0.005

N = 3 #The bigger the N, bigger the divergence, bigger the probability of finidng the global solution

def Analise_Estagnacao(Estagnacao, Entrada):
    Estagnacao.append(Entrada)
    if len(Estagnacao) > Estagnacao_Max:
        Estagnacao.pop(0)
        Estagnacao = np.array(Estagnacao)
        if np.all(Estagnacao == Estagnacao[0]):
            print("Estagnacao atingida. Parando Simulacao Evolucionaria.")
            print(f"Um total de {Calculated_Sim} Simulacoes Calculadas.")
            return True
        
        Counter, Count = (Estagnacao == Estagnacao[0]), 0
        for i in Counter:
            if not i:
                return False
            Count += 1
            if Count > Estagnacao_Atingida:
                global N 
                N += 1 
            
    return False

def Print_Results(First_Place, Generation):
    Laminado1, Laminado2, Laminado3 = np.split(2*First_Place[0], [Condicoes_Iniciais.Formato_1[0], Condicoes_Iniciais.Formato_1[0]*2])
    print(f"Generation: {Generation}\nBest Case Yet: ")
    print(Laminado1)
    print(Laminado2)
    print(Laminado3)
    print(f"F: {First_Place[1]}")  
    
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
        Child_Laminado = np.copy(Parent[0]) - np.random.randint(-N,N+1, size=Laminado_Inicial.shape)
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
    Estagnacao = []
    Survivors = []
    Generation = -1
    
    #Minimizar Camadas
    while not Analisar(Laminado_Geral):
        print(Laminado_Geral)
        Laminado_Geral -= 1
          
    Laminado_Geral += 1
    Survivors.append((Laminado_Geral, Minimo(Laminado_Geral)))
    
    with alive_bar() as bar:
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
            Print_Results(Survivors[0], Generation) 
            if Analise_Estagnacao(Estagnacao,Survivors[0][1]):
                break
            bar()

if __name__ == "__main__":
    Algoritmo_Otimizacao(Laminado_Inicial)
