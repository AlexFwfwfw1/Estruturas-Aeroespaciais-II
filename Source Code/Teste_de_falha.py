from Constantes import *
import Analise_Estrutural
import Definicao_Laminado
import numpy as np

# Matriz [A]inversa (laminado)
Matriz_A_Inversa = Definicao_Laminado.Obter_Laminado[0]
Lista = 1
n = 3

def Tensoes_Eixos_Laminado (Tensao_x, Tensao_y, Tensao_xy):
    
    for Camada in Lista :
        Theta = np.rad2deg()
        Matriz_Theta = np.matrix([
        [np.cos(Theta)**2,               np.sin(Theta)**2,          2*np.sin(Theta)*np.cos(Theta)],
        [np.sin(Theta)**2,               np.cos(Theta)**2,          -2*np.sin(Theta)*np.cos(Theta)],
        [-np.sin(Theta)*np.cos(Theta),   np.sin(Theta)*np.cos(Theta),  np.cos(Theta)-np.sin(Theta)]
        ])

        Matriz_A_Inversa_t = Matriz_A_Inversa * n * ESPESSURA_CAMADA   
        Matriz_K_Barra = Definicao_Laminado.Obter_Matriz_K_Barra
        Matriz_Tensoes_Laminado = np.matrix([
        [Tensao_x],
        [Tensao_y],
        [Tensao_xy]
        ])

        Matriz_Theta_K_Barra = np.dot(Matriz_Theta, Matriz_K_Barra)
        Matriz_K_Barra_A_Inversa_t = np.dot(Matriz_A_Inversa_t, Matriz_Tensoes_Laminado)
        Matriz_Tensoes_Camada = np.dot(Matriz_Theta_K_Barra, Matriz_K_Barra_A_Inversa_t)

        return Matriz_Tensoes_Camada


# na função acima tem de se definir melhor a lista (l13), o número de camadas (l21) e a orientação em graus da camada (l14)


#falta importar o ficheiro das tensões nos eixos do laminado

# Módulos de Resistência   CFRP-HS |   CFRP-HM  |    GFRP
Xt                  =      1500E6,      1000E6,    1000E6
Xc                  =      1200E6,       850E6,     600E6
Yt                  =        50E6,        40E6,      30E6
Yc                  =       250E6,       200E6,     110E6
S                   =        70E6,       120E6,      50E6

# Critérios NÃO INTERATIVOS
# Tensão Máxima (o i representa o material, de 0 a 2 consoante a tabela!)

def Tensao_Max(Tensao_1, Tensao_2, Tensao_12, i):
    
    if Tensao_1 > 0:
        # Esforco_1 = "Tração longitudinal"
        if Tensao_1/Xt[i] >= 1:
            falho_1 = 1
        else : falho_1 = 0
    else: 
        # Esforco_1 = "Compressão longitudinal"
        if Tensao_1/Yt[i] <= -1:
            falho_1 = 1
        else : falho_1 = 0

    if Tensao_2 > 0:
        # Esforco_2 = "Tração transversal"
        if Tensao_2/Xc[i] >= 1:
            falho_2 = 1
        else : falho_2 = 0
    else: 
        # Esforco_2 = "Compressão transversal"
        if Tensao_2/Yc[i] <= -1:
            falho_2 = 1
        else : falho_2 = 0

    if Tensao_12 != 0 :
        # Esforco_12 = "Corte"
        if abs(Tensao_12)/S[i] >=1:
            falho_12 = 1
        else: falho_12 = 0

    # Esforco = Esforco_1, Esforco_2, Esforco_12
    Tensao_maxima = falho_1, falho_2, falho_12

    return Tensao_maxima


# Critérios INTERATIVOS

# Critério de Tsai-Hill
def Tsai_Hill(Tensao_1, Tensao_2, Tensao_12, i):

    if Tensao_1 > 0: X = Xt[i]
    else: X = Xc[i]

    if Tensao_2 > 0: Y = Yt[i]
    else: Y = Yc[i]

    S = S[i]

    f = (Tensao_1/X)**2 + (Tensao_2/Y)**2 + (Tensao_12/S)**2 +(Tensao_1/X)*(Tensao_2/X)

    if f >= 1:
        falho_TH = 1
    else: falho_TH = 0

    return falho_TH

# Critério de Hoffman
def Hoffman(Tensao_1, Tensao_2, Tensao_12, i):
    
    F1 = 1/Xt[i] - 1/Xc[i]
    F2 = 1/Yt[i] - 1/Yc[i]
    F11 = 1/(Xt[i]*Xc[i])
    F22 = 1/(Yt[i]*Yc[i])
    F33 = 1/S[i]**2
    F12 = -1/(2*Xt[i]*Xc[i])

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


