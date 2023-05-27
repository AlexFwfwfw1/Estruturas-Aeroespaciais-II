import Main
import Condicoes_Iniciais
import numpy as np
import Massa_E_Custo

from multiprocessing import Pool, cpu_count, shared_memory
from alive_progress import alive_bar 
from timeit import default_timer as timer

Simulation_Number = np.zeros((2))
shm = shared_memory.SharedMemory(create=True, size=Simulation_Number.nbytes)
Simulation_Name = shm.name

Dados_Precomputados = Condicoes_Iniciais.Matriz_K_Possbilities, Condicoes_Iniciais.Matriz_Theta_Possibilidades

N_Inical = 25

Laminado1 = N_Inical*np.ones(Condicoes_Iniciais.Formato_1, dtype=int)
Laminado2 = N_Inical*np.ones(Condicoes_Iniciais.Formato_1, dtype=int)
Laminado3 = N_Inical*np.ones(Condicoes_Iniciais.Formato_3, dtype=int)
Laminado_Inicial = np.append(np.append(Laminado1, Laminado2, axis=0), Laminado3, axis=0)

 
Generation_Birth = 20
#The bigger the population, the bigger the porbability of finding the global minimum
Maximum_Population = 750
Espessura_Divergence = 5

Estagnacao_Atingida = 2
Estagnacao_Max = 8

Espessura_Multipler = 0.05e-3

N_INICIAL = 10 #The bigger the N, bigger the divergence, bigger the probability of finidng the global solution

Threshhold = 0.5

Text_ = "Resulst_Evol_"

def Analise_Estagnacao(Estagnacao, Entrada, N, Slowness_Factor):
    Estagnacao.insert(0,Entrada)
    # print(Estagnacao)
    if len(Estagnacao) > Estagnacao_Max*Slowness_Factor:
        Estagnacao.pop(-1)
        Estagnacao = np.array(Estagnacao)
        if np.all(Estagnacao == Estagnacao[0]):
            
            existing_shm = shared_memory.SharedMemory(name=Simulation_Name)
            Simulation_Instance = np.ndarray((2,), dtype=np.int64, buffer=existing_shm.buf)
            
            
            print("Estagnacao atingida. Parando Simulacao Evolucionaria.")
            print(f"Um total de {Simulation_Instance[0]} Simulacoes Calculadas.\nUm Um total de {Simulation_Instance[1]} Pre-Simulacoes Calculadas.")
            return True, 1
        
    Counter = (Estagnacao == Estagnacao[0])
    if np.all(Counter[:Estagnacao_Atingida]):
        N -= 1
        if N <= 0: N = 1
        return False, N
            
    return False, N

def Print_Results(First_Place, Generation, Text, N):
    Laminado1, Laminado2, Laminado3 = np.split(2*First_Place[0], [Condicoes_Iniciais.Formato_1[0], Condicoes_Iniciais.Formato_1[0]*2])
    print(f"Generation: {Generation}\nBest Case Yet: ")
    print(Laminado1)
    print(Laminado2)
    print(Laminado3)
    print(f"Espessura: {round(First_Place[1]*Espessura_Multipler, 7)}, F: {First_Place[2]}, N: {N}")  
    
    with open(Text, "a") as Output_File:
        Output_File.write(f"\n\nGeneration: {Generation}\n\n")
        Output_File.write(np.array2string(Laminado1) + "\n\n")
        Output_File.write(np.array2string(Laminado2)+ "\n\n")
        Output_File.write(np.array2string(Laminado3)+ "\n")
        Output_File.write(f"\nEspessura: {round(First_Place[1]*Espessura_Multipler, 7)}, F: {First_Place[2]}, N: {N}")  
    
    
def Analisar(Laminado_Geral, Espessura):
    
    existing_shm = shared_memory.SharedMemory(name=Simulation_Name)
    Simulation_Instance = np.ndarray((2,), dtype=np.int64, buffer=existing_shm.buf)
    Simulation_Instance[0] += 1
    
    Espessura = Espessura*Espessura_Multipler
    
    Laminado1, Laminado2, Laminado3 = np.split(2*Laminado_Geral, [Condicoes_Iniciais.Formato_1[0], Condicoes_Iniciais.Formato_1[0]*2])
    return Main.Simulacao(Laminado1, Laminado2, Laminado3, Espessura, Dados_Precomputados)

def Minimo(Laminado_Geral, Espessura):
    existing_shm = shared_memory.SharedMemory(name=Simulation_Name)
    Simulation_Instance = np.ndarray((2,), dtype=np.int64, buffer=existing_shm.buf)
    Simulation_Instance[1] += 1
    
    Espessura = Espessura*Espessura_Multipler
    
    Laminado1, Laminado2, Laminado3 = np.split(2*Laminado_Geral, [Condicoes_Iniciais.Formato_1[0], Condicoes_Iniciais.Formato_1[0]*2])
    return Massa_E_Custo.Recalcular_Funcao_Minimo(Laminado1, Laminado2, Laminado3, Espessura)


def Create_Childs(Input):
    
    Parent, N = Input
    
    Childs = []
    for _ in range(Generation_Birth):
        #Create Random Variations on 
        Child_Laminado = np.copy(Parent[0]) - np.random.randint(-N,N+1, size=Laminado_Inicial.shape)
        #Cap to positive Vales
        Child_Laminado[Child_Laminado < 0] = 0
        
        #Create Random Variation on Espessura
        Child_Espessura = Parent[1] - np.random.randint(-Espessura_Divergence*N,Espessura_Divergence*N+1)
        if Child_Espessura < 0: Child_Espessura = 0 
        if not Analisar(Child_Laminado, Child_Espessura):
            Childs.append((Child_Laminado, Child_Espessura, Minimo(Child_Laminado, Child_Espessura)))
    return Childs

def Flatten_List(Childs, Survivors):
    Childs = [item for sublist in Childs for item in sublist]
    Survivors = [Survivors]
    Survivors.append(Childs)
    return [item for sublist in Survivors for item in sublist] 

def Remove_Duplicates(Survivors):
    
    Last_Visited = None
    for i in range(len(Survivors)):
        if Survivors[i][2] == Last_Visited:
            Survivors[i] = False
        else:
            Last_Visited = Survivors[i][2]
            
    for _ in range(Survivors.count(False)):
        Survivors.remove(False)


def Algoritmo_Otimizacao(Laminado_Geral, Espessura, Number):
    Text = "Results\\" + Text_ + str(Number) + ".txt"
    with open(Text, "w") as Output_File:
        Output_File.write("Simulation Algoritmo Evolucionario.")
        Output_File.write(f"Configuration: Generation_Birth = {Generation_Birth}\nMaximum_Population = {Maximum_Population}\n")
    
    Estagnacao,Survivors = [], []
    Generation = -1
    
    #Minimizar Camadas
    while not Analisar(Laminado_Geral, Espessura):
        print(Laminado_Geral)
        Laminado_Geral -= 1
    Laminado_Geral += 1
    
    #Select N
    N = N_INICIAL
    Survivors.append((Laminado_Geral, Espessura, Minimo(Laminado_Geral, Espessura)))
    
    with alive_bar() as bar:
        while True:
            Generation += 1
            with Pool(cpu_count()) as MultiCore:
                #Generate copies and apply a random decrese to each Parent.
                #Integrate N in Simulation
                
                Multi_Core_Input = [(a, N) for a in Survivors]
                Childs = MultiCore.map(Create_Childs, Multi_Core_Input)
                #Flatten Lists beacuse of wierd artifacts on list mechanics.
                Survivors = Flatten_List(Childs, Survivors)
                
            #Sort by Minimizing Function and 
            Survivors = sorted(Survivors, key=lambda x: x[2])
            while len(Survivors) > Maximum_Population:
                Survivors.pop()        
            Print_Results(Survivors[0], Generation, Text, N) 
            Stop, N = Analise_Estagnacao(Estagnacao,Survivors[0][2], N, 1)
            if Stop: break
            bar()
    Survivors = sorted(Survivors, key=lambda x: x[2])
    Remove_Duplicates(Survivors)
    return Survivors

def Algoritmo_Otim_Best(Best_Ones, Number):
    Text = "Results\\" + Text_ + "Best" + str(Number) + ".txt"
    with open(Text, "w") as Output_File:
        Output_File.write("Simulation Algoritmo Evolucionario. Best Selected")
        Output_File.write(f"Configuration: Generation_Birth = {Generation_Birth}\nMaximum_Population = {Maximum_Population}\n")
    
    Estagnacao,Survivors = [], Best_Ones
    Generation = -1
    
    #Select N
    N = 1
    
    with alive_bar(title = "Criando Espécies e Selecionando Melhores") as bar:
        while True:
            Generation += 1
            with Pool(cpu_count()) as MultiCore:
                #Generate copies and apply a random decrese to each Parent.
                #Integrate N in Simulation
                
                Multi_Core_Input = [(a, N) for a in Survivors]
                Childs = MultiCore.map(Create_Childs, Multi_Core_Input)
                #Flatten Lists beacuse of wierd artifacts on list mechanics.
                Survivors = Flatten_List(Childs, Survivors)
                
            #Sort by Minimizing Function and 
            Survivors = sorted(Survivors, key=lambda x: x[2])
            while len(Survivors) > Maximum_Population:
                Survivors.pop()        
            Print_Results(Survivors[0], Generation, Text, N) 
            Stop, N = Analise_Estagnacao(Estagnacao,Survivors[0][2], N, 3)
            if Stop: break
            bar()
            
    Remove_Duplicates(Survivors)
    return Survivors
            
def Cruzamento(Servivor1, Servivor2):
    M1, M2 = Servivor1[0], Servivor2[0] 
    Cash_1 = Cash_2 = np.zeros(Servivor1.shape)
    
    Probabilities = np.random.random(Servivor1.shape)
    Cash_1[Probabilities >= Threshhold] = 1
    Cash_1[Probabilities <  Threshhold] = 0
    Cash_2[Probabilities >= Threshhold] = 0
    Cash_2[Probabilities <  Threshhold] = 1
    return (Cash_1*M1 + Cash_2*M2).astype(int)

def Cruzar_Sobreviventes(Best_Survivors):
    Tamanho,Childs = len(Best_Survivors), Best_Survivors.copy()
    Tentativas,Quantidade_de_Filhos = 10, Tamanho*5
    with alive_bar(total = Quantidade_de_Filhos*Tentativas, title = "Cruzando Espécies") as bar:
        for _ in range(Quantidade_de_Filhos):
            Mom, Dad = np.random.randint(0, Tamanho-1),np.random.randint(0, Tamanho-1)
            for __ in range(Tentativas):
                #Create Random Variations on 
                Child_Laminado = Cruzamento(Best_Survivors[Mom][0],Best_Survivors[Dad][0]) 
                #Cap to positive Vales
                Child_Laminado[Child_Laminado < 0] = 0
                
                #Create Random Variation on Espessura
                Thr_Prob = np.random.random()
                Child_Espessura = Best_Survivors[Mom][1]*Thr_Prob + Best_Survivors[Dad][1]*(1-Thr_Prob)

                if Child_Espessura < 0: Child_Espessura = 0 
                if not Analisar(Child_Laminado, Child_Espessura):
                    Childs.append((Child_Laminado, Child_Espessura, Minimo(Child_Laminado, Child_Espessura)))
                bar()
        # print(Childs)
        return Childs

def Detect_Last_Result():
    i = 0
    while True:
        try:
            Text = "Results\\" + Text_ + str(i) + ".txt"
            print(Text)
            with open(Text, "r") as f:
                i += 1
        except FileNotFoundError:
            print(f"Files Detected: {i}")
            return i

Espessuras_Poss = [3**item for item in range(7)]

if __name__ == "__main__":
    start = timer()
    
    Tentativas = 2
    Results = []
    Offset = Detect_Last_Result()
    for i in range(len(Espessuras_Poss)):
        i_ = i + Offset
        temp = Algoritmo_Otimizacao(Laminado_Inicial, Espessuras_Poss[i] , i_)
        Results.append(temp)
    
    Optimized = [item for sublist in Results for item in sublist]
    for _ in range(Tentativas): 
        Optimized = sorted(Optimized, key=lambda x: x[2])
        Childs_Optimized = Cruzar_Sobreviventes(Optimized)
        Optimized = Algoritmo_Otim_Best(Childs_Optimized,_)
        
    end = timer()
    print(f"Time Elapsed: {round((end-start)*1000, 5)} ms")