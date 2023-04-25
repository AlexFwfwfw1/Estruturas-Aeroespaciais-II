from Constantes import *
import Teste_de_falha

import math
import numpy as np

NUMERO_DE_PONTOS = 50

# TEM DE SER UM FUNCAO AO CENTROIDE
Plotting = True
import matplotlib.pyplot as plt

def Analise_Total(Propriadades_Seccao, Forcas_Afilamento, Momentos):
    Altura_Media, Diametro_Medio = Propriadades_Seccao.Geometria_Media
    Centroide_X, Centroide_Y = Propriadades_Seccao.Centroide
    I_xx, I_yy, Ixy = Propriadades_Seccao.Segundo_Momentos_De_Area
    Ex_1,Ex_2,Ex_3 = Propriadades_Seccao.Elasticidades
    T1,T2,A3 = Propriadades_Seccao.Espessuras
    
    Raio_Medio = Diametro_Medio/2
    
    X1,X2,X3,X4 = Propriadades_Seccao.Coordenadas_X
    Y1,Y2,Y3,Y4 = Propriadades_Seccao.Coordenadas_Y

    Forca_SX_W, Forca_SY_W = Forcas_Afilamento
    Momento_X, Momento_Y = Momentos
    
    Constante_A_Direta = (Momento_Y / I_yy)
    Constante_B_Direta = (Momento_X / I_xx)
    
    Constante_A_Corte = -(Forca_SY_W / I_yy)
    Constante_B_Corte = -(Forca_SX_W / I_xx)

    Coords_X,Coords_Y,Coords_Z = [],[],[]

    Qb3 = Ex_1 * (Constante_A_Corte*Raio_Medio*Y2*T2 + Constante_B_Corte*T2*(-0.5*Raio_Medio**2))
    Qb4 = Ex_1 * (Constante_A_Corte*(Altura_Media*Y3*T1 + T1*0.5*Altura_Media**2 + A3*Y3) + Constante_B_Corte*(T1*X3*Altura_Media+A3*X3)) +Qb3
    Qb1 = Ex_1 * (Constante_A_Corte*(T1*Raio_Medio*Y1*math.pi + T1*(Raio_Medio**2)*(1-math.cos(math.pi)) + A3*Y4) + Constante_B_Corte*(-T1*(Raio_Medio**2)*math.sin(math.pi)+A3*X4)) +Qb4
    Qbm = Ex_1 * (Constante_A_Corte*(T1*Raio_Medio*Y1*math.pi/2 + T1*(Raio_Medio**2)*(1-math.cos(math.pi/2)) + A3*Y4) + Constante_B_Corte*(-T1*(Raio_Medio**2)*math.sin(math.pi/2)+A3*X4)) +Qb4
    Qb2 = Ex_1 * (Constante_A_Corte*(T1*(Y1*Altura_Media - 0.5*Altura_Media**2) + Y1*A3) + Constante_B_Corte*(T1*X1*Altura_Media + A3*X1)) + Qb1
    QbC = Ex_1 * (Constante_A_Corte*(T2*Y2*Raio_Medio + A3*Y2) + Constante_B_Corte*(T2*(X2*Raio_Medio - 0.5*Raio_Medio**2) + A3*X2)) +Qb2
    
    # #valores a retirar do filipe
    # Px_1, Px_2, Px_3, Px_4 = 12, 12, 12, 12
    # Py_1, Py_2, Py_3, Py_4 = 12, 12, 12, 12
    # Sx = 76
    
    A_Varrida = Altura_Media * Raio_Medio + math.pi/2* Raio_Medio**2

    I_C3 = Constante_A_Corte/2 *  Y2 * Raio_Medio**2 - Constante_B_Corte /6* Raio_Medio**3
    I_34 = Constante_A_Corte * (T1 * Y3 * Altura_Media**2 /2 + T1 * Altura_Media**3 /6 + A3 * Y3 * Altura_Media) + Constante_B_Corte * (T1 * X3 * Altura_Media**2 /2 + A3 * X3 * Altura_Media) + Qb3 * Altura_Media 
    I_41 = Constante_A_Corte * (T1 * Raio_Medio**2 * Y1 * math.pi**2 /2 + T1 * Raio_Medio**3 * math.pi + A3 * Y4 * Raio_Medio * math.pi) + Constante_B_Corte * (-2* T1 * Raio_Medio**3 + A3 * X4 * Raio_Medio * math.pi) + Qb4 * math.pi * Raio_Medio
    I_12 = Constante_A_Corte * (T1 * Y1 * Altura_Media**2 /2 - T1 * Altura_Media**3 /6 + Y1 * A3 * Altura_Media) + Constante_B_Corte * (T1 * X1 * Altura_Media**2 /2 + Constante_B_Corte * X1 * Altura_Media) + Qb1 * Altura_Media
    I_2C = Constante_A_Corte * (T2 * Y2 * Raio_Medio**2 /2 + A3 * Y2 * Raio_Medio) + Constante_B_Corte * (T2 * X2 * Raio_Medio**2 /2 - T2 * Raio_Medio**3 /6 + A3 * X2 * Raio_Medio) + Qb2 * Raio_Medio

    #integração sentido horário
    I_total = - Altura_Media * I_C3 - Raio_Medio * I_34 - Raio_Medio * I_41 - Raio_Medio * I_12 - Altura_Media * I_2C

    PxBraço_1, PxBraço_2, PxBraço_3, PxBraço_4 = Px_1 * 0, Px_2 * Altura_Media , Px_3 * Altura_Media  , Px_4 * 0
    PyBraço_1, PyBraço_2, PyBraço_3, PyBraço_4 = Py_1 * Raio_Medio, Py_2 * Raio_Medio , Py_3 * (- Raio_Medio)  , Py_4 * (- Raio_Medio)
    Soma_PxB = PxBraço_1 + PxBraço_2 + PxBraço_3 + PxBraço_4
    Soma_PyB = PyBraço_1 + PyBraço_2 + PyBraço_3 + PyBraço_4

    qs_0_i = (Sx * 1.2 - I_total + Soma_PxB - Soma_PyB) / (2 * A_Varrida) #Area Errada, esta area nao é a area da seccao mas é a area interior á seccao media. Nao alterei manel. Altera Tu.
 
    Qb1, Qb2, Qb3, Qb4, QbC = 0,0,0,0,0
    
    #VIGA HORIZONTAL, MEIO ATE PONTA
    for Ponto_S in np.linspace(0, Raio_Medio , NUMERO_DE_PONTOS):
        Coordenada_X =  - Ponto_S
        Coordenada_Y = -Altura_Media - Centroide_Y
        Tensao_Direta = Ex_2 * (Constante_A_Direta*Coordenada_X + Constante_B_Direta*Coordenada_Y)
        Fluxo_Corte = Ex_2 * (Constante_A_Corte*Ponto_S*Y2*T2 + Constante_B_Corte*T2*(-0.5*Ponto_S**2))
        
        Tensao_de_Corte = Fluxo_Corte/T2
        
        # FS_Falha = (Tensao_Direta, 0, Tensao_de_Corte)
        # if FS_Falha > 1:
            # return FS_Falha
        
        if Plotting:
            Coords_X.append(Coordenada_X)
            Coords_Y.append(Coordenada_Y)
            Coords_Z.append(Fluxo_Corte)
        
    Qb3 = Fluxo_Corte

    #VIGA VERTICAL ESQUERDA    
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Coordenada_X = -Raio_Medio
        Coordenada_Y = - Altura_Media + Ponto_S - Centroide_Y
        Tensao_Direta = Ex_1 * (Constante_A_Direta*Coordenada_X + Constante_B_Direta*Coordenada_Y)
        Fluxo_Corte = Ex_1 * (Constante_A_Corte*(Ponto_S*Y3*T1 + T1*0.5*Ponto_S**2 + A3*Y3) + Constante_B_Corte*(T1*X3*Ponto_S+A3*X3)) + Qb3
        Tensao_de_Corte = Fluxo_Corte/T1
        
        # FS_Falha = Teste_de_falha.Falha(Tensao_Direta, 0, Tensao_de_Corte)
        # if FS_Falha > 1:
            # return FS_Falha
            
        if Plotting:
            Coords_X.append(Coordenada_X)
            Coords_Y.append(Coordenada_Y)
            Coords_Z.append(Fluxo_Corte)
        
    Qb4 = Fluxo_Corte
    #VIGA SEMICIRCULO 
    for Ponto_S in np.linspace(0, math.pi , NUMERO_DE_PONTOS):
        Coordenada_X = -Raio_Medio*math.cos(Ponto_S)
        Coordenada_Y = Raio_Medio*math.sin(Ponto_S) - Centroide_Y
        Tensao_Direta = Ex_1 * (Constante_A_Direta*Coordenada_X + Constante_B_Direta*Coordenada_Y)
        
        Fluxo_Corte = Ex_1 * (Constante_A_Corte*(T1*Raio_Medio*Y1*Ponto_S + T1*(Raio_Medio**2)*(1-math.cos(Ponto_S)) + A3*Y4) + Constante_B_Corte*(-T1*(Raio_Medio**2)*math.sin(Ponto_S)+A3*X4)) + Qb4
        Tensao_de_Corte = Fluxo_Corte/T1
        
        # FS_Falha = Teste_de_falha.Falha(Tensao_Direta, 0, Tensao_de_Corte)
        # if FS_Falha > 1:
            # return FS_Falha
            
        if Plotting:
            Coords_X.append(Coordenada_X)
            Coords_Y.append(Coordenada_Y)
            Coords_Z.append(Fluxo_Corte)
        
    Qb1 = Fluxo_Corte
    #VIGA VERTICAL DIREITA
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Coordenada_X = Raio_Medio
        Coordenada_Y = - Ponto_S - Centroide_Y
        Tensao_Direta = Ex_1 * (Constante_A_Direta*Coordenada_X + Constante_B_Direta*Coordenada_Y)
        
        Fluxo_Corte = Ex_1 * (Constante_A_Corte*(T1*(Y1*Ponto_S - 0.5*Ponto_S**2) + Y1*A3) + Constante_B_Corte*(T1*X1*Ponto_S + A3*X1)) + Qb1
        Tensao_de_Corte = Fluxo_Corte/T1
        
        # FS_Falha = Teste_de_falha.Falha(Tensao_Direta, 0, Tensao_de_Corte)
        # if FS_Falha > 1:
            # return FS_Falha
            
        if Plotting:
            Coords_X.append(Coordenada_X)
            Coords_Y.append(Coordenada_Y)
            Coords_Z.append(Fluxo_Corte)
        
    Qb2 = Fluxo_Corte
    #VIGA HORIZONTAL DA PONTA ATE O MEIO
    for Ponto_S in np.linspace(0, Raio_Medio , NUMERO_DE_PONTOS):
        Coordenada_X = -Ponto_S + Raio_Medio
        Coordenada_Y = - Altura_Media - Centroide_Y
        Tensao_Direta = Ex_2 * (Constante_A_Direta*Coordenada_X + Constante_B_Direta*Coordenada_Y)
        
        Fluxo_Corte = Ex_2 * (Constante_A_Corte*(T2*Y2*Ponto_S + A3*Y2) + Constante_B_Corte*(T2*(X2*Ponto_S - 0.5*Ponto_S**2) + A3*X2)) + Qb2
        Tensao_de_Corte = Fluxo_Corte/T2
        
        # FS_Falha = Teste_de_falha.Falha(Tensao_Direta, 0, Tensao_de_Corte)
        # if FS_Falha > 1:
            # return FS_Falha
            
        if Plotting:
            Coords_X.append(Coordenada_X)
            Coords_Y.append(Coordenada_Y)
            Coords_Z.append(Fluxo_Corte)
        
    QbC = Fluxo_Corte
    print(Qb1,Qb2,Qb3,Qb4,QbC)
    
    # return FS_Falha
    

    if Plotting:
        Coords_X, Coords_Y, Coords_Z = np.array(Coords_X),np.array(Coords_Y),np.array(Coords_Z)
        fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
        markerline, stemlines, baseline = ax.stem(
            Coords_X, Coords_Y, Coords_Z, linefmt='grey', markerfmt='D', bottom=0)
        markerline.set_markerfacecolor('none')
        ax.set_proj_type("ortho")

        plt.show()