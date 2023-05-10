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

 
Generation_Birth = 25
#The bigger the population, the bigger the porbability of finding the global minimum
Maximum_Population = 1000

Estagnacao_Atingida = 25
Estagnacao_Max = 5

Espessura_Multipler = 0.05e-3
Calculated_Sim = 0

N = 1 #The bigger the N, bigger the divergence, bigger the probability of finidng the global solution
N_Espessura = 10

Threshhold = 0.5

Text_ = "Resulst_Evol_"

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

def Print_Results(First_Place, Generation, Text):
    Laminado1, Laminado2, Laminado3 = np.split(2*First_Place[0], [Condicoes_Iniciais.Formato_1[0], Condicoes_Iniciais.Formato_1[0]*2])
    print(f"Generation: {Generation}\nBest Case Yet: ")
    print(Laminado1)
    print(Laminado2)
    print(Laminado3)
    print(f"Espessura: {round(First_Place[1]*Espessura_Multipler, 7)}, F: {First_Place[2]}")  
    
    with open(Text, "a") as Output_File:
        Output_File.write(f"\n\nGeneration: {Generation}\n\n")
        Output_File.write(np.array2string(Laminado1) + "\n\n")
        Output_File.write(np.array2string(Laminado2)+ "\n\n")
        Output_File.write(np.array2string(Laminado3)+ "\n")
        Output_File.write(f"\nEspessura: {round(First_Place[1]*Espessura_Multipler, 7)}, F: {First_Place[2]}")  
    
def Analisar(Laminado_Geral, Espessura):
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
        Output_File.write(f"Configuration: Generation_Birth = {Generation_Birth}\nMaximum_Population = {Maximum_Population}\nN = {N}\n")
    
    Estagnacao,Survivors = [], []
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
            Print_Results(Survivors[0], Generation, Text) 
            if Analise_Estagnacao(Estagnacao,Survivors[0][2]):
                break
            bar()
            
    Remove_Duplicates(Survivors)
    return Survivors

def Algoritmo_Otim_Best(Best_Ones, Number):
    Text = "Results\\" + Text_ + "Best" + str(Number) + ".txt"
    with open(Text, "w") as Output_File:
        Output_File.write("Simulation Algoritmo Evolucionario. Best Selected")
        Output_File.write(f"Configuration: Generation_Birth = {Generation_Birth}\nMaximum_Population = {Maximum_Population}\nN = {N}\n")
    
    Estagnacao,Survivors = [], Best_Ones
    Generation = -1
    
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
            Print_Results(Survivors[0], Generation, Text) 
            if Analise_Estagnacao(Estagnacao,Survivors[0][2]):
                break
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
    Tentativas = 100
    Childs = []
    Tamanho = len(Best_Survivors)
    for i in range(0, int(Tamanho/2), 2):
        for _ in range(Tentativas):
            #Create Random Variations on 
            if i >= Tamanho - 1:
                continue
            Child_Laminado = Cruzamento(Best_Survivors[i][0],Best_Survivors[i+1][0]) 
            #Cap to positive Vales
            Child_Laminado[Child_Laminado < 0] = 0
            
            #Create Random Variation on Espessura
            Thr_Prob = np.random.random()
            Child_Espessura = Best_Survivors[i][1]*Thr_Prob + Best_Survivors[i+1][1]*(1-Thr_Prob)

            if Child_Espessura < 0: Child_Espessura = 0 
            if not Analisar(Child_Laminado, Child_Espessura):
                Childs.append((Child_Laminado, Child_Espessura, Minimo(Child_Laminado, Child_Espessura)))
    print(Childs)
    return Childs

Espessuras_Poss = (200,500)

if __name__ == "__main__":
    Tentativas = 3
    Results = []
    for i in range(len(Espessuras_Poss)):
        temp = Algoritmo_Otimizacao(Laminado_Inicial, Espessuras_Poss[i] , i)
        Results.append(temp)
    
    Optimized = [item for sublist in Results for item in sublist]
    for _ in range(Tentativas): 
        Childs_Optimized = Cruzar_Sobreviventes(Optimized, _)
        Optimized = Algoritmo_Otim_Best(Childs_Optimized)
    
    
    