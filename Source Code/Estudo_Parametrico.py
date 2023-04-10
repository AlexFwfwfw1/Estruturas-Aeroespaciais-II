import Main
import Materiais

import numpy as np
import itertools

Laminado_1_Limits = {"N_Min": 2, "N_Max" : 10}
Laminado_2_Limits = Laminado_1_Limits
Laminado_3_Limits = {"N_Min": 4, "N_Max" : 8}
Espessura_B_Limits = {"b_min" : 0.001, "b_max" : 0.01, "divisions" : 10}

FATOR_SEGURANCA_FALHA = 1.5
FATOR_SEGURANCA_DEFLEXAO = 1.0

def Estudo_Paramétrico():
    
    #Estudo Paramétrico tem em conta certos possibilidades de ângulos.
    
    Angulos_Possiveis = (0,45,-45,90)
    i_Angulos_Possiveis = len(Angulos_Possiveis)
    
    #Tem em conta materiais
    
    Materiais_Possiveis = (Materiais.MATERIAL_CFRP_HS, Materiais.MATERIAL_CFRP_HM, Materiais.MATERIAL_GFRP)
    j_Materiais_Possiveis = len(Materiais_Possiveis)
    
    Espessuras_B_Possiveis = np.linspace(Espessura_B_Limits["b_min"], Espessura_B_Limits["b_max"], Espessura_B_Limits["divisions"])
    
    #Combinacoes tem de ser simetricas. Repete-se a ordem
    #Nao faz sentido estar a simular seccoes repetidas, logo podemos abstrair da ordem de camadas.
    
    #Cria-se uma tabela com todas as combinacoes e materiais possiveis representando o numero associado.
    #Limita-se o numero de camadas por n_max_i e por n_min_i
    
    #O universo das possibilidades encontra-se no dominio de N elevado a (i*j) <= n_max.
    #Sendo i, angulos possiveis, sendo j, materiais possiveis.
    
    
    def laminado_simetrico(n, i, j):
     
        Matriz_A_List = []
        
        for Rows in range(i):
            for Columns in range(j):
                Possibilidade_A = np.zeros((i,j)) 
                Possibilidade_A[Rows,Columns] = 1
                Matriz_A_List.append(Possibilidade_A)
                
        # O loop acima cria uma lista de matrizes diferentes com o elemento 1 a "passar" por todas as casas da matriz.
        # Isto é util porque é possivel pegar nessa lista para ser os eixos de uma tabela multi-dimensional (pensem em 2D por agora).
        # Os elementos dessa tabela serao a soma dos eixos desse mesmo elemento.
        # Ao fazer isso, essa tabela tera todas as combinacoes possiveis de matriz ixj de soma N.
        # Para teres todas as combinacoes para um N = 2, a tabela sera bi-dimensional
        # E os dois eixos serao a lista de matrizes "Matriz_A_List"
        # Os elementos dessa tabela sera a soma dos eixos correspondentes. É esse o proposito da linha de codigo abaixo.
        # Esta ideia generaliza-se para qualquer N. Para N = 5, a matriz tera de ter 5 dimensoes em que cada elemento tera
        # de somar 5 matrizes, 1 proveniente de cada eixo.

        Tabela_nD = itertools.combinations_with_replacement(tuple(Matriz_A_List),n)
    
        #Criar uma tabela de dimensoes N com os eixos Matriz_A_List. É recomendavel usar funcoes externas para isto
        # Devido a performance. Iterar no proprio python é extremamente ineficiente para numeros altos como é este caso.
        
        #No entanto, existem imensos items repetidos dado os exios serem simetricos. Entao é 
        #usado combinacoes com subsitituicao que o matematicamente equivalente a so fazer
        #o triangulo superior com a diagonal da tabela. É possivel descobrir isso se fizerem as combinacoes a mao xd.
        
        Tabela_nD = np.array(tuple(Tabela_nD))
        #Agora convertemos essa matriz ((i*j)^n)xIxJxN em uma matriz numpy para podermos manipular a vontade e manter performance.
        
        Combinacoes_Soma_N = np.sum(Tabela_nD, axis=1)
        
        #Pegamos em cada elemento de n matrizes e somamos todas.
        # Conseguimos agora todas as combinacoes possiveis de matrizes ixj de soma N 
        
        Combinacoes_Soma_N_Unica = np.unique(Combinacoes_Soma_N, axis=0)
        
        # O comando acima serve para eliminar elementos repetidos. 
        # É mais eficaz fazer esta filtragem depois da soma dado que podem haver listas distintas com somas iguais.
        # No entanto, estou a verificar que nunca existem elementos repetidos inesperadamente. Pode-se retirar. 
        
        # Com isto podemos multiplicar por dois para obter o laminado simetrico.
        Combinacoes_Soma_N_Unica_Simetrica = Combinacoes_Soma_N_Unica*2
        return Combinacoes_Soma_N_Unica_Simetrica
    
    def laminado_simetrico_impar(n):
        #Se alguem souber fazer isto. Que me diga.
        return
    
    def Obter_Combinacoes():
        
        ## LAMINADO 1 E 2. Tem as mesmas possibilidades.
        
        Combinacoes_Laminado_1_2 = np.zeros((1,i_Angulos_Possiveis, j_Materiais_Possiveis))
        for n in range(Laminado_1_Limits["N_Min"],Laminado_1_Limits["N_Max"]):
            if n % 2 == 0: 
                Combinacoes_N = laminado_simetrico( int(n/2) , i_Angulos_Possiveis , j_Materiais_Possiveis)
                
                Size = len(Combinacoes_N)
                Combinacoes_Laminado_1_2 = np.append(Combinacoes_Laminado_1_2, Combinacoes_N, axis = 0)
                
                print(f"Calculated N = {n}, Size = {Size}, Laminado : 1")
        
        #Agora é necessario obter todas as combinacoes possiveis entre os dois laminados.

        Combinacoes_Laminado_1_2 = tuple(Combinacoes_Laminado_1_2)
        
        ## LAMINADO 3
        
        Combinacoes_Laminado_3 = np.zeros((1, 1 , j_Materiais_Possiveis))  #Aqui os angulos possiveis é apenas 1. O a zero graus.
        for n in range(Laminado_3_Limits["N_Min"],Laminado_3_Limits["N_Max"]):
            if n % 2 == 0: 
                Combinacoes_N = laminado_simetrico( int(n/2) , 1 , j_Materiais_Possiveis)
                
                Size = len(Combinacoes_N)
                Combinacoes_Laminado_3 = np.append(Combinacoes_Laminado_3, Combinacoes_N, axis = 0)
                
                print(f"Calculated N = {n}, Size = {Size}, Laminado : 3")
        
        Combinacoes_Laminado_3 = tuple(Combinacoes_Laminado_3)
        
        Combinacoes_Total = itertools.product(Combinacoes_Laminado_1_2, Combinacoes_Laminado_1_2, Combinacoes_Laminado_3)
        
        return Combinacoes_Total
    
    Combinacoes = Obter_Combinacoes()
    Combinacao_Minimo = 0
    with open("Output.txt","w") as file:
        Minimo = 10E100
        for Simulacao in Combinacoes:
            Funcao_Minimizacao = Main.Pre_Simulacao(Simulacao)
            if Funcao_Minimizacao < Minimo:
                Falha, Deflexao = Main.Simulacao(Simulacao)
                if Falha > FATOR_SEGURANCA_FALHA and Deflexao > FATOR_SEGURANCA_DEFLEXAO:
                    Minimo = Funcao_Minimizacao
                    file.write(Simulacao, Falha, Deflexao)
                    Combinacao_Minimo = Simulacao
            else:
                continue
        
    print("Minimo Encontrado")
    print(Combinacao_Minimo)
    
Estudo_Paramétrico()