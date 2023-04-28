from Constantes import *
import numpy as np

from Configuration import FS, Debug #com Fator de Segurança

FS_Inv = 1/FS

def Tensoes_Eixos_Camada(Tensao_x, Tensao_y, Tensao_xy, Laminado):
    #Esta Matriz Tensao tem todas as 
    Matriz_Tensao_List = Laminado.List_Matriz_Stress
    # print(Matriz_Tensao_List)
    Array_Tensao = np.array([Tensao_x, Tensao_y, Tensao_xy])
    for Camada in Matriz_Tensao_List:
        #Obter Tensoes nos Eixos
        Matriz_Tensao,Material = Camada
        Tensao_Nos_Eixos = np.matmul(Matriz_Tensao,Array_Tensao) 
        Tensao_1 ,Tensao_2, Tensao_12 = tuple(Tensao_Nos_Eixos) 

        
        #Criterio de Falha
        if Debug:
            T = Tensao_Max(Tensao_1 ,Tensao_2, Tensao_12, Material)
            Ts =Tsai_Hill(Tensao_1 ,Tensao_2, Tensao_12, Material)
            Ho = Hoffman(Tensao_1 ,Tensao_2, Tensao_12, Material)
            Min = sorted([T,Ts, Ho],key=lambda x: x[0])[0]
            return Min
        elif Tsai_Hill(Tensao_1 ,Tensao_2, Tensao_12, Material) == 1 or Hoffman(Tensao_1 ,Tensao_2, Tensao_12, Material) == 1 or Tensao_Max(Tensao_1 ,Tensao_2, Tensao_12, Material) == 1 :
            return 1  #FALHOU!
    return 0


# Critérios NÃO INTERATIVOS

def Tensao_Max(Tensao_1, Tensao_2, Tensao_12, Material):
    Fs_1, Fs_2, Fs_3 = (10e100, "Tensao_X"), (10e100, "Tensao_Y"), (10e100, "Corte")
    if Debug:
        if Tensao_1 > 0:
            Fs_1 = (Material.Xt/Tensao_1, "Tensao_X")
        elif Tensao_1 < 0: 
            Fs_1 = (-Material.Xc/Tensao_1, "Compressao_X")
        if Tensao_2 > 0:
            Fs_2 = (Material.Yt/Tensao_2, "Tensao_Y") 
        elif Tensao_2 < 0: 
            Fs_2 = (-Material.Yc/Tensao_2, "Compressao_Y")
        if Tensao_12 != 0:
            Fs_3 = (abs(Material.S/Tensao_12), "Corte") 
        return sorted([Fs_1,Fs_2,Fs_3],key=lambda x: x[0])[0]
    else:
        if Tensao_1 > 0:
            if Tensao_1/Material.Xt >= FS_Inv: #Tração longitudinal
                return 1
        else: 
            if Tensao_1/Material.Xc <= -FS_Inv: #Compressão longitudinal
                return 1
        if Tensao_2 > 0:
            if Tensao_2/Material.Yt >= FS_Inv: #Tração transversal
                return 1
        else: 
            if Tensao_2/Material.Yc <= -FS_Inv: #Compressão transversal
                return 1
        if abs(Tensao_12)/Material.S >= FS_Inv:  #Corte
            return 1
        return 0



# Critérios INTERATIVOS

# Critério de Tsai-Hill
def Tsai_Hill(Tensao_1, Tensao_2, Tensao_12, Material):

    if Tensao_1 > 0: X = Material.Xt
    else: X = Material.Xc

    if Tensao_2 > 0: Y = Material.Yt
    else: Y = Material.Yc

    S = Material.S

    f = (Tensao_1/X)**2 + (Tensao_2/Y)**2 + (Tensao_12/S)**2 +(Tensao_1/X)*(Tensao_2/X)
    if Debug:
        return (1/f, "Tsai_Hill")

    if f >= FS_Inv:
        return 1
    return 0

# Critério de Hoffman
def Hoffman(Tensao_1, Tensao_2, Tensao_12, Material):
    
    F1 = 1/Material.Xt - 1/Material.Xc
    F2 = 1/Material.Yt - 1/Material.Yc
    F11 = 1/(Material.Xt*Material.Xc)
    F22 = 1/(Material.Yt*Material.Yc)
    F33 = 1/Material.S**2
    F12 = -1/(2*Material.Xt*Material.Xc)

    f = F1 * Tensao_1 + F2 * Tensao_2 + F11 * Tensao_1**2 + F22 * Tensao_2**2 + F33 * Tensao_12**2 + 2 * F12 * Tensao_1 * Tensao_2
    if Debug:
        return (1/abs(f), "Hoffman")

    if f >= FS_Inv:
        return 1
    return 0
