from Constantes import *
import numpy as np

from Configuration import FS #com Fator de Segurança
import Debug

FS_Inv = 1/FS

def Tensoes_Eixos_Camada(Tensao_x, Tensao_y, Tensao_xy, Laminado):
    #Esta Matriz Tensao tem todas as 
    Matriz_Tensao_List = Laminado.List_Matriz_Stress
    Laminado_Name = Laminado.Name
    # print(Matriz_Tensao_List)
    Array_Tensao = np.array([Tensao_x, Tensao_y, Tensao_xy])
    for Camada in Matriz_Tensao_List:
        #Obter Tensoes nos Eixos
        Matriz_Tensao,Material = Camada
        Tensao_Nos_Eixos = np.matmul(Matriz_Tensao,Array_Tensao) 
        Tensao_1 ,Tensao_2, Tensao_12 = tuple(Tensao_Nos_Eixos) 

        
        #Criterio de Falha
        if Debug.DEBUG:
            T = Tensao_Max(Tensao_1 ,Tensao_2, Tensao_12, Material, Laminado_Name)
            #Ts = Tsai_Hill(Tensao_1 ,Tensao_2, Tensao_12, Material, Laminado_Name)
            #Ho = Hoffman(Tensao_1 ,Tensao_2, Tensao_12, Material, Laminado_Name)
        else:
            T = Tensao_Max(Tensao_1 ,Tensao_2, Tensao_12, Material, Laminado_Name)
            #Ts = Tsai_Hill(Tensao_1 ,Tensao_2, Tensao_12, Material, Laminado_Name)
            #Ho = Hoffman(Tensao_1 ,Tensao_2, Tensao_12, Material, Laminado_Name)
            if T:
                return True  #FALHOU!
    return False


# Critérios NÃO INTERATIVOS

def Tensao_Max(Tensao_1, Tensao_2, Tensao_12, Material, Laminado_Name):
    
    if Tensao_1 > 0:
        Fs = abs(Material.Xt/Tensao_1)
        if Debug.DEBUG:
            Fs_Point = (Fs, "Tensao_X",Laminado_Name)
            Debug.Adiocionar_Ponto(Fs_Point)
        elif Fs <= FS:
            return True
    if Tensao_1 < 0: 
        Fs = abs(Material.Xc/Tensao_1)
        if Debug.DEBUG:
            Fs_Point = (Fs, "Compressao_X",Laminado_Name)
            Debug.Adiocionar_Ponto(Fs_Point)
        elif Fs <= FS:
            return True
    if Tensao_2 > 0:
        Fs = abs(Material.Yt/Tensao_2)
        if Debug.DEBUG:
            Fs_Point = (Fs, "Tensao_Y",Laminado_Name)
            Debug.Adiocionar_Ponto(Fs_Point)
        elif Fs <= FS:
            return True
    if Tensao_2 < 0: 
        Fs = abs(Material.Yc/Tensao_2)
        if Debug.DEBUG:
            Fs_Point = (Fs, "Compressao_Y",Laminado_Name)
            Debug.Adiocionar_Ponto(Fs_Point)
        elif Fs <= FS:
            return True
    if Tensao_1 != 0:
        Fs = abs(Material.S/Tensao_12)
        if Debug.DEBUG:
            Fs_Point = (Fs, "Corte",Laminado_Name)
            Debug.Adiocionar_Ponto(Fs_Point)
        elif Fs <= FS:
            return True
    
    return False



# Critérios INTERATIVOS

# Critério de Tsai-Hill
def Tsai_Hill(Tensao_1, Tensao_2, Tensao_12, Material,Laminado_Name):

    if Tensao_1 > 0: X = Material.Xt
    else: X = Material.Xc

    if Tensao_2 > 0: Y = Material.Yt
    else: Y = Material.Yc

    S = Material.S

    f = (Tensao_1/X)**2 + (Tensao_2/Y)**2 + (Tensao_12/S)**2 - (Tensao_1/X)*(Tensao_2/X)
    if Debug.DEBUG:
        Debug.Adiocionar_Ponto((1/abs(f), "Tsai_Hill",Laminado_Name))

    if f >= FS_Inv:
        return True
    return False

# Critério de Hoffman
def Hoffman(Tensao_1, Tensao_2, Tensao_12, Material,Laminado_Name):
    
    F1 = 1/Material.Xt - 1/Material.Xc
    F2 = 1/Material.Yt - 1/Material.Yc
    F11 = 1/(Material.Xt*Material.Xc)
    F22 = 1/(Material.Yt*Material.Yc)
    F33 = 1/Material.S**2
    F12 = -1/(2*Material.Xt*Material.Xc)

    f = F1 * Tensao_1 + F2 * Tensao_2 + F11 * Tensao_1**2 + F22 * Tensao_2**2 + F33 * Tensao_12**2 + 2 * F12 * Tensao_1 * Tensao_2
    if Debug.DEBUG:
        Debug.Adiocionar_Ponto((1/abs(f), "Hoffman",Laminado_Name))

    if f >= FS_Inv:
        return True
    return False
