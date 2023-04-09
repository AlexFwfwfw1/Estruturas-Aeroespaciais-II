from Constantes import *



# Módulos de Resistência   CFRP-HS | CFRP-HM | GFRP
Xt                  =      1500,      1000,    1000
Xc                  =      1200,       850,     600
Yt                  =        50,        40,      30
Yc                  =       250,       200,     110
S                   =        70,       120,      50

# Critérios NÃO INTERATIVOS
# Tensão Máxima (o i representa o material, de 0 a 2 consoante a tabela!)

def Tensao_Max(Tensao_1, Tensao_2, Tensao_12, i):
    
    if Tensao_1 > 0:
        Esforco_1 = "Tração longitudinal"
        if Tensao_1/Xt[i] >= 1:
            falho_1 = 1
        else : falho_1 = 0
    else: 
        Esforco_1 = "Compressão longitudinal"
        if Tensao_1/Yt[i] <= -1:
            falho_1 = 1
        else : falho_1 = 0

    if Tensao_2 > 0:
        Esforco_2 = "Tração transversal"
        if Tensao_2/Xc[i] >= 1:
            falho_2 = 1
        else : falho_2 = 0
    else: 
        Esforco_2 = "Compressão transversal"
        if Tensao_2/Yc[i] <= -1:
            falho_2 = 1
        else : falho_2 = 0

    if Tensao_12 != 0 :
        Esforco_12 = "Corte"
        if abs(Tensao_12)/S[i] >=1:
            falho_12 = 1
        else: falho_12 = 0

    Esforco = Esforco_1, Esforco_2, Esforco_12
    Tensao_maxima = falho_1, falho_2, falho_12

    return Tensao_maxima, Esforco

# Extensão Máxima (o i representa o material, de 0 a 2 consoante a tabela!)
# é preciso fazer?????



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

#Critério de extensões de Tsai-Wu ----> preciso fazer??


# Indicação de falhos
def Falhos(Tensao_maxima, Esforco ,falho_TH, falho_Hoff):

    if Tensao_maxima[0] == 1 :  
        print ("Falho por ", Esforco[0])
    
    if Tensao_maxima[1] == 1 :
        print ("Falho por ", Esforco[1])

    if Tensao_maxima[2] == 1 :  
        print ("Falho por ", Esforco[2])

    if falho_TH == 1 :
        print("Falho por Tsai-Hill")

    if falho_Hoff == 1 : 
        print("Falho por Hoffman")



    






