from Constantes import *
import numpy as np

FS = 1.5 #com Fator de Segurança

def Tensoes_Eixos_Camada(Tensao_x, Tensao_y, Tensao_xy, Laminado):
    #Esta Matriz Tensao tem todas as 
    Matriz_Tensao_List = Laminado.List_Matriz_Stress
    # print(Matriz_Tensao_List)
    Array_Tensao = np.array([Tensao_x, Tensao_y, Tensao_xy])
    for Camada in Matriz_Tensao_List:
        #Obter Tensoes nos Eixos
        Matriz_Tensao,Material = Camada
        Tensao_Nos_Eixos = FS * np.matmul(Matriz_Tensao,Array_Tensao) 
        Tensao_1 ,Tensao_2, Tensao_12 = tuple(Tensao_Nos_Eixos) 
        
        #Criterio de Falha
        if Tsai_Hill(Tensao_1 ,Tensao_2, Tensao_12, Material) == 1 or Hoffman(Tensao_1 ,Tensao_2, Tensao_12, Material) == 1 or Tensao_Max(Tensao_1 ,Tensao_2, Tensao_12, Material) == 1 :
            return 1  #FALHOU!
    return 0

# #falta importar o ficheiro das tensões nos eixos do laminado

# # Módulos de Resistência   CFRP-HS |   CFRP-HM  |    GFRP
# Xt                  =      1500E6,      1000E6,    1000E6
# Xc                  =      1200E6,       850E6,     600E6
# Yt                  =        50E6,        40E6,      30E6
# Yc                  =       250E6,       200E6,     110E6
# S                   =        70E6,       120E6,      50E6

# Critérios NÃO INTERATIVOS
# Tensão Máxima (o i representa o material, de 0 a 2 consoante a tabela!)

def Tensao_Max(Tensao_1, Tensao_2, Tensao_12, Material):
    
    if Tensao_1 > 0:
        # Esforco_1 = "Tração longitudinal"
        if Tensao_1/Material.Xt >= 1:
            falho_1 = 1
        else : falho_1 = 0
    else: 
        # Esforco_1 = "Compressão longitudinal"
        if Tensao_1/Material.Yt <= -1:
            falho_1 = 1
        else : falho_1 = 0

    if Tensao_2 > 0:
        # Esforco_2 = "Tração transversal"
        if Tensao_2/Material.Xc >= 1:
            falho_2 = 1
        else : falho_2 = 0
    else: 
        # Esforco_2 = "Compressão transversal"
        if Tensao_2/Material.Yc <= -1:
            falho_2 = 1
        else : falho_2 = 0

    # Esforco_12 = "Corte"
    if abs(Tensao_12)/Material.S >=1:
        falho_12 = 1
    else: falho_12 = 0

    # Esforco = Esforco_1, Esforco_2, Esforco_12
    Tensao_maxima = max(falho_1, falho_2, falho_12)

    return Tensao_maxima


# Critérios INTERATIVOS

# Critério de Tsai-Hill
def Tsai_Hill(Tensao_1, Tensao_2, Tensao_12, Material):

    if Tensao_1 > 0: X = Material.Xt
    else: X = Material.Xc

    if Tensao_2 > 0: Y = Material.Yt
    else: Y = Material.Yc

    S = Material.S

    f = (Tensao_1/X)**2 + (Tensao_2/Y)**2 + (Tensao_12/S)**2 +(Tensao_1/X)*(Tensao_2/X)

    if f >= 1:
        falho_TH = 1
    else: falho_TH = 0

    return falho_TH

# Critério de Hoffman
def Hoffman(Tensao_1, Tensao_2, Tensao_12, Material):
    
    F1 = 1/Material.Xt - 1/Material.Xc
    F2 = 1/Material.Yt - 1/Material.Yc
    F11 = 1/(Material.Xt*Material.Xc)
    F22 = 1/(Material.Yt*Material.Yc)
    F33 = 1/Material.S**2
    F12 = -1/(2*Material.Xt*Material.Xc)

    f = F1 * Tensao_1 + F2 * Tensao_2 + F11 * Tensao_1**2 + F22 * Tensao_2**2 + F33 * Tensao_12**2 + 2 * F12 * Tensao_1 * Tensao_2

    if f >= 1:
        falho_Hoff = 1
    else: falho_Hoff = 0

    return falho_Hoff


# Indicação de falhos
#def Falhos(Tensao_maxima, Esforco ,falho_TH, falho_Hoff):
#    if Tensao_maxima[0] == 1 :  
#        print ("Falho por ", Esforco[0])
#    if Tensao_maxima[1] == 1 :
#        print ("Falho por ", Esforco[1])
#    if Tensao_maxima[2] == 1 :  
#        print ("Falho por ", Esforco[2])
#    if falho_TH == 1 :
#        print("Falho por Tsai-Hill")
#    if falho_Hoff == 1 : 
#        print("Falho por Hoffman")


