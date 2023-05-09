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

 
Generation_Birth = 20
#The bigger the population, the bigger the porbability of finding the global minimum
Maximum_Population = 100

Estagnacao_Atingida = 25
Estagnacao_Max = 100

Espessura_Multipler = 0.05e-3
Calculated_Sim = 0

N = 1 #The bigger the N, bigger the divergence, bigger the probability of finidng the global solution
N_Espessura = 5

def Analise_Estagnacao(Estagnacao, Entrada):
    global N 
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
                N = 1
                return False
            Count += 1
            if Count > Estagnacao_Atingida: 
                N += 1 
                return False
            
    return False

def Print_Results(First_Place, Generation):
    Laminado1, Laminado2, Laminado3 = np.split(2*First_Place[0], [Condicoes_Iniciais.Formato_1[0], Condicoes_Iniciais.Formato_1[0]*2])
    print(f"Generation: {Generation}\nBest Case Yet: ")
    print(Laminado1)
    print(Laminado2)
    print(Laminado3)
    print(f"Espessura: {round(First_Place[1]*Espessura_Multipler, 7)}, F: {First_Place[2]}")  
    
def Analisar(Laminado_Geral, Espessura):
    #print(Laminado_Geral)
    global Calculated_Sim
    Calculated_Sim += 1
    
    Espessura = Espessura*Espessura_Multipler
    
    Laminado1, Laminado2, Laminado3 = np.split(2*Laminado_Geral, [Condicoes_Iniciais.Formato_1[0], Condicoes_Iniciais.Formato_1[0]*2])
    return Main.Simulacao(Laminado1, Laminado2, Laminado3, Espessura, Dados_Precomputados)

def Minimo(Laminado_Geral, Espessura):
    global Calculated_Sim
    Calculated_Sim += 1
    
    Espessura = Espessura*Espessura_Multipler
    
    Laminado1, Laminado2, Laminado3 = np.split(2*Laminado_Geral, [Condicoes_Iniciais.Formato_1[0], Condicoes_Iniciais.Formato_1[0]*2])
    return Massa_E_Custo.Recalcular_Funcao_Minimo(Laminado1, Laminado2, Laminado3, Espessura)

def Create_Childs(Parent):
    
    Childs = []
    for _ in range(Generation_Birth):
        #Create Random Variations on 
        Child_Laminado = np.copy(Parent[0]) - np.random.randint(-N,N+1, size=Laminado_Inicial.shape)
        #Cap to positive Vales
        Child_Laminado[Child_Laminado < 0] = 0
        
        #Create Random Variation on Espessura
        Child_Espessura = Parent[1] - np.random.randint(-N_Espessura,N_Espessura+1)
        if Child_Espessura < 0: Child_Espessura = 0 
        if not Analisar(Child_Laminado, Child_Espessura):
            Childs.append((Child_Laminado, Child_Espessura, Minimo(Child_Laminado, Child_Espessura)))
    return Childs

def Flatten_List(Childs, Survivors):
    Childs = [item for sublist in Childs for item in sublist]
    Survivors = [Survivors]
    Survivors.append(Childs)
    return [item for sublist in Survivors for item in sublist] 

def Algoritmo_Otimizacao(Laminado_Geral, Espessura):
    Estagnacao = []
    Survivors = []
    Generation = -1
    
    #Minimizar Camadas
    while not Analisar(Laminado_Geral, Espessura):
        print(Laminado_Geral)
        Laminado_Geral -= 1
          
    Laminado_Geral += 1
    Survivors.append((Laminado_Geral, Espessura, Minimo(Laminado_Geral, Espessura)))
    
    with alive_bar() as bar:
        while True:
            Generation += 1
            with Pool(cpu_count()) as MultiCore:
                #Generate 20 copies and apply a random decrese to each Parent.
                Childs = MultiCore.map(Create_Childs, Survivors)
                #Flatten Lists beacuse of wierd artifacts on list mechanics.
                Survivors = Flatten_List(Childs, Survivors)
                
            #Sort by Minimizing Function and 
            Survivors = sorted(Survivors, key=lambda x: x[2])
            while len(Survivors) > Maximum_Population:
                Survivors.pop()        
            Print_Results(Survivors[0], Generation) 
            if Analise_Estagnacao(Estagnacao,Survivors[0][2]):
                break
            bar()

if __name__ == "__main__":
    Algoritmo_Otimizacao(Laminado_Inicial, 100)
    Calculated_Sim = 0