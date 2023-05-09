from Constantes import *
import Teste_de_falha

from Configuration import Falha

import Debug

#Dimensoes da cauda na raiz e na ponta

w_raiz = 1.5
w_ponta = 1.5*(1-0.7)
h_raiz = 0.9
h_ponta = 0.9*(1-0.5)

def F_Afilamento(Propriadades_Seccao, Momentos, Forcas, Laminado_3):

    I_xx, I_yy, Ixy = Propriadades_Seccao.Segundo_Momentos_De_Area
    Ex_1,Ex_2,Ex_3 = Propriadades_Seccao.Elasticidades
    T1,T2,A3 = Propriadades_Seccao.Espessuras

    Momento_X, Momento_Y = Momentos
    Forca_SX, Forca_SY = Forcas

    Constante_A_Direta = (Momento_Y / I_yy)
    Constante_B_Direta = (Momento_X / I_xx)

    X1,X2,X3,X4 = Propriadades_Seccao.Coordenadas_X
    Y1,Y2,Y3,Y4 = Propriadades_Seccao.Coordenadas_Y

    A_tensores_i = 4*A3

    #Posicao dos tensores na raiz e na ponta
    x_raiz_3 = x_raiz_4 = -(w_raiz - T1)/2
    x_raiz_2 = x_raiz_1 = (w_raiz - T1)/2
    y_raiz_3 = y_raiz_2 = -(h_raiz - T2/2)
    y_raiz_4 = y_raiz_1 = 0

    x_ponta_3 = x_ponta_4 = -(w_ponta- T1)/2
    x_ponta_2 = x_ponta_1 = (w_ponta-T1)/2
    y_ponta_3 = y_ponta_2 = -(h_ponta - T2/2)
    y_ponta_4 = y_ponta_1 = 0

    #Deltas
    delta_x_3 = x_ponta_3 - x_raiz_3
    delta_y_3 = y_ponta_3 - y_raiz_3

    delta_x_2 = x_ponta_2 - x_raiz_2
    delta_y_2 = y_ponta_2 - y_raiz_2
    
    delta_x_4 = x_ponta_4 - x_raiz_4
    delta_y_4 = y_ponta_4 - y_raiz_4
    
    delta_x_1 = x_ponta_1 - x_raiz_1
    delta_y_1 = y_ponta_1 - y_raiz_1
    
    delta_z = COMPRIMENTO_FUSELAGEM

    #Tensores diretas em cada tensor
    
    Tensao_Direta_1 = Ex_3 * (Constante_A_Direta*X1 + Constante_B_Direta*Y1)
    Tensao_Direta_2 = Ex_3 * (Constante_A_Direta*X2 + Constante_B_Direta*Y2)
    Tensao_Direta_3 = Ex_3 * (Constante_A_Direta*X3 + Constante_B_Direta*Y3)
    Tensao_Direta_4 = Ex_3 * (Constante_A_Direta*X4 + Constante_B_Direta*Y4)
    
    if Falha and A3 != 0:
        for Tensao_Direta in (Tensao_Direta_1,Tensao_Direta_2,Tensao_Direta_3,Tensao_Direta_4):
            Falha_Return = Teste_de_falha.Tensoes_Eixos_Camada(Tensao_Direta, 0, 0, Laminado_3)
            if not Debug.DEBUG and Falha_Return: 
                return None, Falha_Return
        
    #Forcas de tracao/compressao
    
    Pz_1 = Tensao_Direta_1 * A_tensores_i
    Pz_2 = Tensao_Direta_2 * A_tensores_i
    Pz_3 = Tensao_Direta_3 * A_tensores_i
    Pz_4 = Tensao_Direta_4 * A_tensores_i
    
    #Forcas transversais
    
    Px_1 = Pz_1*(delta_x_1/delta_z)
    Py_1 = Pz_1*(delta_y_1/delta_z)
    
    Px_2 = Pz_2*(delta_x_2/delta_z)
    Py_2 = Pz_2*(delta_y_2/delta_z)
    
    Px_3 = Pz_3*(delta_x_3/delta_z)
    Py_3 = Pz_3*(delta_y_3/delta_z)

    Px_4 = Pz_4*(delta_x_4/delta_z)
    Py_4 = Pz_4*(delta_y_4/delta_z)

    Px = (Px_1, Px_2, Px_3, Px_4)
    Py = (Py_1, Py_2, Py_3, Py_4)

    Sx_w = Forca_SX - (Px_3+Px_2+Px_4+Px_1)
    Sy_w = Forca_SY - (Py_3+Py_2+Py_4+Py_1)

    Sw = (Sx_w,Sy_w)
    
    return (Sw, Px, Py), None