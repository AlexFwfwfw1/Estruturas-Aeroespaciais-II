from Constantes import *
import Analise_Estrutural
import Definicao_Laminado
import numpy as np

# Matriz [A]inversa (laminado)
#Matriz_A_Inversa = Definicao_Laminado.Obter_Laminado[0]
Lista = 1
n = 3

FS = 1.5 #com Fator de Segurança

def Tensoes_Eixos_Camada(Tensao_x, Tensao_y, Tensao_xy, Laminado):
    #Esta Matriz Tensao tem todas as 
    Matriz_Tensao = Laminado.Matriz_Stress
    Array_Tensao = np.array([Tensao_x, Tensao_y, Tensao_xy])
    for i in range(np.shape(Matriz_Tensao)[0]):
        for j in range(np.shape(Matriz_Tensao)[1]):
            #Obter Tensoes nos Eixos
            Tensao_Nos_Eixos = FS * np.matmul(Matriz_Tensao[i,j],Array_Tensao) 
            Tensao_1 ,Tensao_2, Tensao_12 = tuple(Tensao_Nos_Eixos) 
            #Criterio de Falha
            if Tsai_Hill(Tensao_1 ,Tensao_2, Tensao_12) == 1 or Hoffman(Tensao_1 ,Tensao_2, Tensao_12) == 1 or Tensao_Max(Tensao_1 ,Tensao_2, Tensao_12) == 1 :
                return 1  #FALHOU!
    return 0


# na função acima tem de se definir melhor a lista (l13), o número de camadas (l21) e a orientação em graus da camada (l14), material e angulo (l21)


#falta importar o ficheiro das tensões nos eixos do laminado

# Módulos de Resistência   CFRP-HS |   CFRP-HM  |    GFRP
Xt                  =      1500E6,      1000E6,    1000E6
Xc                  =      1200E6,       850E6,     600E6
Yt                  =        50E6,        40E6,      30E6
Yc                  =       250E6,       200E6,     110E6
S                   =        70E6,       120E6,      50E6

# Critérios NÃO INTERATIVOS
# Tensão Máxima (o i representa o material, de 0 a 2 consoante a tabela!)

##FALTA IMPLEMENTAR FATOR DE SEGURANÇA

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
    Tensao_maxima = max(falho_1, falho_2, falho_12)

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


