import Main
import Materiais

import numpy as np
import itertools

def Estudo_Paramétrico():
    
    #Estudo Paramétrico tem em conta certos possibilidades de ângulos.
    
    Angulos_Possiveis = (0,45,-45,90)
    i = len(Angulos_Possiveis)
    
    #Tem em conta materiais
    
    Materiais_Possiveis = (Materiais.MATERIAL_CFRP_HS, Materiais.MATERIAL_CFRP_HM, Materiais.MATERIAL_GFRP)
    j = len(Materiais_Possiveis)
    
    #Combinacoes tem de ser simetricas. Repete-se a ordem
    #Nao faz sentido estar a simular seccoes repetidas
    #Abstrai-se da ordem de camadas.
    
    #Cria-se uma tabela com todas as combinacoes e materiais possiveis representando o numero associado.
    #Limita-se o numero de camadas por n_max_i e por n_min_i
    
    
    #O universo das possibilidades encontra-se no dominio de N elevado a (i*j) <= n_max.
    #Sendo i, angulos possiveis, sendo j, materiais possiveis.
    
    
    def Obter_Combinacoes_de_N():
        Laminado_1 = {"N_Min": 3, "N_Max" : 10}
        Laminado_2 = Laminado_1
        Laminado_3 = {"N_Min": 4, "N_Max" : 8}
        
        
    def matrix_combinations(n):
     
        Matriz_A_List = []
        
        for Rows in range(i):
            for Columns in range(j):
                Possibilidade_A = np.zeros((i,j)) 
                Possibilidade_A[Rows,Columns] = 1
                Matriz_A_List.append(Possibilidade_A)

        K = itertools.product(tuple(Matriz_A_List), repeat=n)
        
        K = np.array(tuple(K))
        
        Somas = np.sum(K, axis=1)
        print(Somas)
        J = list(itertools.combinations(K,2))
        print(len(J))
        
        
    matrix_combinations(3)
    
Estudo_Paramétrico()