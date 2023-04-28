import Main
import Materiais
import Definicao_Laminado

import numpy as np
import itertools

import Massa_E_Custo

from multiprocessing import Pool, cpu_count, freeze_support, shared_memory
from multiprocessing.managers import SharedMemoryManager
from alive_progress import alive_bar

from tqdm import tqdm


Laminado_1_Limits = {"N_Min": 46, "N_Max": 528588584555555588            }
Laminado_2_Limits = Laminado_1_Limits
Laminado_3_Limits = {"N_Min": 20, "N_Max": 25}
Espessura_B_Limits = {"b_min": 0, "b_max": 0.1, "divisions": 10}

FAZER_IMPAR = False

Multiprocessing = True
Print_Possibilies = False


# Estudo Paramétrico tem em conta certos possibilidades de ângulos.

Angulos_Possiveis = (0, 45, -45, 90)
i_Angulos_Possiveis = len(Angulos_Possiveis)

# Tem em conta materiais

Materiais_Possiveis = Materiais.Materials_List

j_Materiais_Possiveis = len(Materiais_Possiveis)

Espessuras_B_Possiveis = np.linspace(
        Espessura_B_Limits["b_min"],
        Espessura_B_Limits["b_max"],
        Espessura_B_Limits["divisions"],
    )

Matriz_K_Possbilities,Matriz_Theta_Possibilidades = Definicao_Laminado.Obter_Matriz_K_Possibilities(Angulos_Possiveis, Materiais_Possiveis)
Dados_Precomputados = (Matriz_K_Possbilities,Matriz_Theta_Possibilidades)
def laminado_simetrico(n, i, j):

    Matriz_A_List = []

    for Rows in range(i):
        for Columns in range(j):
            Possibilidade_A = np.zeros((i, j))
            Possibilidade_A[Rows, Columns] = 1
            Matriz_A_List.append(Possibilidade_A)

    # Combinacoes tem de ser simetricas. Repete-se a ordem
    # Nao faz sentido estar a simular seccoes repetidas, logo podemos abstrair da ordem de camadas.

    # Cria-se uma tabela com todas as combinacoes e materiais possiveis representando o numero associado.
    # Limita-se o numero de camadas por n_max_i e por n_min_i

    # O universo das possibilidades encontra-se no dominio de N elevado a (i*j) <= n_max.
    # Sendo i, angulos possiveis, sendo j, materiais possiveis.

    # O loop acima cria uma lista de matrizes diferentes com o elemento 1 a "passar" por todas as casas da matriz.
    # Isto é util porque é possivel pegar nessa lista para ser os eixos de uma tabela multi-dimensional (pensem em 2D por agora).
    # Os elementos dessa tabela serao a soma dos eixos desse mesmo elemento.
    # Ao fazer isso, essa tabela tera todas as combinacoes possiveis de matriz ixj de soma N.
    # Para teres todas as combinacoes para um N = 2, a tabela sera bi-dimensional
    # E os dois eixos serao a lista de matrizes "Matriz_A_List"
    # Os elementos dessa tabela sera a soma dos eixos correspondentes. É esse o proposito da linha de codigo abaixo.
    # Esta ideia generaliza-se para qualquer N. Para N = 5, a matriz tera de ter 5 dimensoes em que cada elemento tera
    # de somar 5 matrizes, 1 proveniente de cada eixo.

    Tabela_nD = itertools.combinations_with_replacement(tuple(Matriz_A_List), n)

    # Criar uma tabela de dimensoes N com os eixos Matriz_A_List. É recomendavel usar funcoes externas para isto
    # Devido a performance. Iterar no proprio python é extremamente ineficiente para numeros altos como é este caso.

    # No entanto, existem imensos items repetidos dado os exios serem simetricos. Entao é
    # usado combinacoes com subsitituicao que o matematicamente equivalente a so fazer
    # o triangulo superior com a diagonal da tabela. É possivel descobrir isso se fizerem as combinacoes a mao xd.

    Tabela_nD = np.array(tuple(Tabela_nD))
    # Agora convertemos essa matriz ((i*j)^n)xIxJxN em uma matriz numpy para podermos manipular a vontade e manter performance.

    Combinacoes_Soma_N = np.sum(Tabela_nD, axis=1)

    # Pegamos em cada elemento de n matrizes e somamos todas.
    # Conseguimos agora todas as combinacoes possiveis de matrizes ixj de soma N

    Combinacoes_Soma_N_Unica = np.unique(Combinacoes_Soma_N, axis=0)

    # O comando acima serve para eliminar elementos repetidos.
    # É mais eficaz fazer esta filtragem depois da soma dado que podem haver listas distintas com somas iguais.
    # No entanto, estou a verificar que nunca existem elementos repetidos inesperadamente. Pode-se retirar.

    # Com isto podemos multiplicar por dois para obter o laminado simetrico.
    Combinacoes_Soma_N_Unica_Simetrica = Combinacoes_Soma_N_Unica * 2
    # print(np.shape(Combinacoes_Soma_N))
    return Combinacoes_Soma_N_Unica_Simetrica


def laminado_simetrico_impar(combinacoes, i, j):
    # Este algoritmo utiliza a propriadade de impar = 2*par + 1

    Matriz_A_List = []

    for Rows in range(i):
        for Columns in range(j):
            Possibilidade_A = np.zeros((i, j))
            Possibilidade_A[Rows, Columns] = 1
            Matriz_A_List.append(Possibilidade_A)

    combinacoes = tuple(combinacoes)

    Tabela_nD = itertools.product(tuple(Matriz_A_List), combinacoes)
    Tabela_nD = np.array(tuple(Tabela_nD))
    Combinacoes_Soma_N = np.sum(Tabela_nD, axis=1)
    Combinacoes_Soma_N_Unica = np.unique(Combinacoes_Soma_N, axis=0)

    return Combinacoes_Soma_N_Unica


def Obter_Combinacoes():

    # LAMINADO 1 E 2. Tem as mesmas possibilidades.
    Combinacoes_N_Par = None
    Combinacoes_Laminado_1_2 = np.zeros((0, i_Angulos_Possiveis, j_Materiais_Possiveis))
    for n in range(Laminado_1_Limits["N_Min"], Laminado_1_Limits["N_Max"]):
        if n % 2 == 0:
            Combinacoes_N_Par = laminado_simetrico(
                int(n / 2), i_Angulos_Possiveis, j_Materiais_Possiveis
            )

            Size = len(Combinacoes_N_Par)
            Combinacoes_Laminado_1_2 = np.append(
                Combinacoes_Laminado_1_2, Combinacoes_N_Par, axis=0
            )
            if Print_Possibilies:
                print(f"Calculated N = {n}, Size = {Size}, Laminado : 1")
        elif FAZER_IMPAR:
            if n == 1:
                temp = laminado_simetrico(1, i_Angulos_Possiveis, j_Materiais_Possiveis)*0.5
                Combinacoes_N_Impar = temp.astype(int)
            else:
                Combinacoes_N_Impar = laminado_simetrico_impar(Combinacoes_N_Par, i_Angulos_Possiveis, j_Materiais_Possiveis)
                
        
            Size = len(Combinacoes_N_Impar)
            Combinacoes_Laminado_1_2 = np.append(
                Combinacoes_Laminado_1_2, Combinacoes_N_Impar, axis=0
            )
            if Print_Possibilies:
                print(f"Calculated N = {n}, Size = {Size}, Laminado : 1")
        

    # Agora é necessario obter todas as combinacoes possiveis entre os dois laminados.

    Combinacoes_Laminado_1_2 = tuple(Combinacoes_Laminado_1_2)

    # LAMINADO 3
    # Aqui os angulos possiveis é apenas 1. O a zero graus.
    Combinacoes_Laminado_3 = np.zeros((0, 1, j_Materiais_Possiveis))
    for n in range(Laminado_3_Limits["N_Min"], Laminado_3_Limits["N_Max"]):

        if n % 2 == 0:
            Combinacoes_N_Par = laminado_simetrico(int(n / 2), 1, j_Materiais_Possiveis)

            Size = len(Combinacoes_N_Par)
            Combinacoes_Laminado_3 = np.append(
                Combinacoes_Laminado_3, Combinacoes_N_Par, axis=0
            )
            if Print_Possibilies:
                print(f"Calculated N = {n}, Size = {Size}, Laminado : 3")
        elif FAZER_IMPAR:
            if n == 1:
                temp = laminado_simetrico(1, 1, j_Materiais_Possiveis)*0.5
                Combinacoes_N_Impar = temp.astype(int)
            else:
                Combinacoes_N_Impar = laminado_simetrico_impar(
                    Combinacoes_N_Par, 1, j_Materiais_Possiveis
                )

            Size = len(Combinacoes_N_Impar)
            Combinacoes_Laminado_3 = np.append(
                Combinacoes_Laminado_3, Combinacoes_N_Impar, axis=0
            )
            if Print_Possibilies:
                print(f"Calculated N = {n}, Size = {Size}, Laminado : 3")

    Combinacoes_Laminado_3 = tuple(Combinacoes_Laminado_3)
    return (
        Combinacoes_Laminado_1_2,
        Combinacoes_Laminado_1_2,
        Combinacoes_Laminado_3,
    )

    
Laminado1_Lista, Laminado2_Lista, Laminado3_Lista = Obter_Combinacoes()

Possibilities_Number = (
    len(Laminado1_Lista)
    * len(Laminado2_Lista)
    * len(Laminado3_Lista)
    * Espessura_B_Limits["divisions"]
)

(
    Massa_1,
    Massa_2,
    Massa_3,
    Custo_1,
    Custo_2,
    Custo_3,
) = Massa_E_Custo.Precalcular_Funcao_Minimo(Laminado1_Lista, Laminado2_Lista, Laminado3_Lista)



def temp_f(bm):
    
    Espessura, Lam_3, Shared_Memory = bm
    if Multiprocessing:
        existing_shm = shared_memory.ShareableList(name=Shared_Memory)
        Min = existing_shm[0]
        print(Min)
        
    Sim_Started = 0
    Combinacao_Minimo = None
    for Lam_1 in range(len(Laminado1_Lista)):
        for Lam_2 in range(len(Laminado2_Lista)):
            
            Funcao_Minimizacao = Massa_E_Custo.Massa(
                Massa_1[Lam_1],
                Massa_2[Lam_2],
                Massa_3[Lam_3],
                Custo_1[Lam_1],
                Custo_2[Lam_2],
                Custo_3[Lam_3],
                Espessura,
            )
            
            if Funcao_Minimizacao < Min:
                Sim_Started += 1
                Falha = Main.Simulacao(Laminado1_Lista[Lam_1], Laminado2_Lista[Lam_2], Laminado3_Lista[Lam_3], Espessura, Dados_Precomputados)
                if Falha == 0:
                    Min = Funcao_Minimizacao
                    Combinacao_Minimo = Laminado1_Lista[Lam_1], Laminado2_Lista[Lam_2], Laminado3_Lista[Lam_3], Espessura
        
    if Multiprocessing:
        existing_shm[0] = float(Min)
    return Min, Combinacao_Minimo, Sim_Started 
                 

if __name__ == "__main__":
    
    Gap_Number = len(Laminado3_Lista)* Espessura_B_Limits["divisions"]
    Total = len(Laminado1_Lista)*len(Laminado2_Lista)
    
    Core_List_Arguments = []
        
    for Espessura in Espessuras_B_Possiveis:
        for Lam_3 in range(len(Laminado3_Lista)):
            Core_List_Arguments.append((Espessura, Lam_3))
            
    if Multiprocessing:
        freeze_support()
        with SharedMemoryManager() as smm:
            Minimo = smm.ShareableList([10e100])
            Name = Minimo.shm.name
            print(Name)
            
            Core_List_Arguments = []
            for Espessura in Espessuras_B_Possiveis:
                for Lam_3 in range(len(Laminado3_Lista)):
                    Core_List_Arguments.append((Espessura, Lam_3, Name))
       
    
            Results = []
            with Pool(processes=cpu_count()) as Multi_Core_Process:
                for result in tqdm(Multi_Core_Process.imap(func=temp_f, iterable=Core_List_Arguments),colour="blue",unit = " Simulacoes", dynamic_ncols = True,unit_scale = Total, total= Gap_Number, desc = "Estudo Paramétrico"):
                    Results.append(result)
    else:
        Results = []
        with alive_bar(total = Total*Gap_Number) as bar:
            for Core in Core_List_Arguments:
                Results.append(temp_f(Core))
                bar(Total)
                
    Best_Simulation = sorted(Results,key=lambda x: x[0])[0]
    Lam1_R,Lam2_R,Lam3_R, Espessura = Best_Simulation[1]
    Sim_Started = sum([pair[2] for pair in Results])
        
    print("Estudo Paramétrico: Simulacao Completa.")
    print(f"Mass/Cost Function: {Best_Simulation[0]}")
    
    print(f"Laminado 1: ")
    print(Lam1_R)
    print(f"Laminado 2: ")
    print(Lam2_R)
    print(f"Laminado 3: ")
    print(Lam3_R)
    print(f"Espessura B: {Espessura}")
    
    print(f"Ammount of Simulations Calculated: {Sim_Started} from {Total*Gap_Number} Combinations")

    