from Constantes import *

def F_Afilamento(Centroide, Segundo_Momentos_De_Area, Geometria_Media, Elasticidades, Momentos, Laminado_3, b):

    Altura_Media, Diametro_Medio, Area_Total = Geometria_Media
    Centroide_X, Centroide_Y = Centroide
    I_xx, I_yy, Ixy = Segundo_Momentos_De_Area
    Ex_1,Ex_2,Ex_3 = Elasticidades

    Momento_X, Momento_Y = Momentos

    Raio_Medio = Diametro_Medio/2

    Constante_A_Direta = (Momento_Y / I_yy)
    Constante_B_Direta = (Momento_X / I_xx)

    Coordenada_X = Raio_Medio - Centroide_X
    Coordenada_Y = -Altura_Media - Centroide_Y

    X1,X2,X3,X4 = Coordenada_X
    Y1,Y2,Y3,Y4 = Coordenada_Y

    Tensao_Direta = Ex_2 * (Constante_A_Direta*Coordenada_X + Constante_B_Direta*Coordenada_Y)

    Area_laminado3 = b * Laminado_3.Espessura
    A_tensores_i = 4*Area_laminado3

    #Dimensoes da cauda na raiz e na ponta
    w_raiz = 1.5*(1-0.7*0/COMPRIMENTO_FUSELAGEM)
    w_ponta = 1.5*(1-0.7*COMPRIMENTO_FUSELAGEM/COMPRIMENTO_FUSELAGEM)
    h_raiz = 0.9*(1-0.5*0/COMPRIMENTO_FUSELAGEM)
    h_ponta = 0.9*(1-0.5*COMPRIMENTO_FUSELAGEM/COMPRIMENTO_FUSELAGEM)

    #Posicao dos tensores na raiz e na ponta
    x_raiz_IE = x_raiz_SE = -w_raiz/2
    x_raiz_ID = x_raiz_SD = w_raiz/2
    y_raiz_IE = y_raiz_ID = -h_raiz
    y_raiz_SE = y_raiz_SD = 0

    x_ponta_IE = x_ponta_SE = -w_ponta/2
    x_ponta_ID = x_ponta_SD = w_ponta/2
    y_ponta_IE = y_ponta_ID = -h_ponta
    y_ponta_SE = y_ponta_SD = 0

    #Deltas
    delta_x_IE = x_ponta_IE - x_raiz_IE
    delta_y_IE = y_ponta_IE - y_raiz_IE

    delta_x_ID = x_ponta_ID - x_raiz_ID
    delta_y_ID = y_ponta_ID - y_raiz_ID
    
    delta_x_SE = x_ponta_SE - x_raiz_SE
    delta_y_SE = y_ponta_SE - y_raiz_SE
    
    delta_x_SD = x_ponta_SD - x_raiz_SD
    delta_y_SD = y_ponta_SD - y_raiz_SD
    
    delta_z = COMPRIMENTO_FUSELAGEM

    #Tensores diretas em cada tensor
    Tensao_Direta_IE = Ex_2 * (Constante_A_Direta*X3+ Constante_B_Direta*Y3)
    Tensao_Direta_ID = Ex_2 * (Constante_A_Direta*X4 + Constante_B_Direta*Y4)
    Tensao_Direta_SE = Ex_2 * (Constante_A_Direta*X1+ Constante_B_Direta*Y1)
    Tensao_Direta_SD = Ex_2 * (Constante_A_Direta*X2 + Constante_B_Direta*Y2)
    
    #Forcas de tracao/compressao
    Pz_IE = Tensao_Direta_IE * A_tensores_i
    Pz_ID = Tensao_Direta_ID * A_tensores_i
    Pz_SE = Tensao_Direta_SE * A_tensores_i
    Pz_SD = Tensao_Direta_SD * A_tensores_i
    
    #Forcas transversais
    Px_IE = Pz_IE*(delta_x_IE/delta_z)
    Py_IE = Pz_IE*(delta_y_IE/delta_z)

    Px_ID = Pz_ID*(delta_x_ID/delta_z)
    Py_ID = Pz_ID*(delta_y_ID/delta_z)

    Px_SE = Pz_SE*(delta_x_SE/delta_z)
    Py_SE = Pz_SE*(delta_y_SE/delta_z)

    Px_SD = Pz_SD*(delta_x_SD/delta_z)
    Py_SD = Pz_SD*(delta_y_SD/delta_z)

    Sx_w = S_x - Px_IE+Px_ID+Px_SE+Px_SD
    Sy_w = S_y - Py_IE+Py_ID+Py_SE+Py_SD

    return(Sx_w,Sy_w)