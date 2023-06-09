from Constantes import *
import Teste_de_falha
import Plotting_Lib

import math
import numpy as np

from Configuration import NUMERO_DE_PONTOS, Plotting, Falha
import Debug

import matplotlib.pyplot as plt


def Analise_Total(Propriadades_Seccao, Forcas, Momentos, Laminados, Forcas_Afilamento, Seccao):
    Altura_Media, Diametro_Medio = Propriadades_Seccao.Geometria_Media
    Centroide_X, Centroide_Y = Propriadades_Seccao.Centroide
    I_xx, I_yy, Ixy = Propriadades_Seccao.Segundo_Momentos_De_Area
    Ex_1,Ex_2,Ex_3 = Propriadades_Seccao.Elasticidades
    T1,T2,A3 = Propriadades_Seccao.Espessuras
    
    A_total_i, A_Varrida = Propriadades_Seccao.Areas

    Laminado_1,Laminado_2,Laminado_3 = Laminados 
    
    Raio_Medio = Diametro_Medio/2
    
    X1,X2,X3,X4 = Propriadades_Seccao.Coordenadas_X
    Y1,Y2,Y3,Y4 = Propriadades_Seccao.Coordenadas_Y
    
    Sw, Px, Py = Forcas_Afilamento
    Sx, Sy, Sz = Forcas

    Forca_SX_W, Forca_SY_W = Sw
    Px_1, Px_2, Px_3, Px_4 = Px 
    Py_1, Py_2, Py_3, Py_4 = Py 
    Momento_X, Momento_Y = Momentos
    
    #Forca_SX_W = 0
    
    Constante_A_Direta = (Momento_Y / I_yy)
    Constante_B_Direta = (Momento_X / I_xx)
    
    Constante_A_Corte = -(Forca_SY_W / I_yy)
    Constante_B_Corte = -(Forca_SX_W / I_xx)

    #Coords_X,Coords_Y,Coords_Z = [],[],[]

    Qb3 = Ex_2 * (Constante_A_Corte*Raio_Medio*Y2*T2 + Constante_B_Corte*T2*(-0.5*Raio_Medio**2))
    Qb4 = Ex_3 * (Constante_A_Corte*A3*Y3 + Constante_B_Corte*A3*X3) +  Ex_1 * (Constante_A_Corte*(Altura_Media*Y3*T1 + T1*0.5*Altura_Media**2) + Constante_B_Corte*(T1*X3*Altura_Media)) +Qb3
    Qb1 = Ex_3 * (Constante_A_Corte*A3*Y4 + Constante_B_Corte*A3*X4) + Ex_1 * (Constante_A_Corte*(T1*Raio_Medio*Y1*math.pi + T1*(Raio_Medio**2)*(1-math.cos(math.pi))) + Constante_B_Corte*(-T1*(Raio_Medio**2)*math.sin(math.pi))) +Qb4
    Qbm = Ex_1 * (Constante_A_Corte*(T1*Raio_Medio*Y1*math.pi/2 + T1*(Raio_Medio**2)*(1-math.cos(math.pi/2)) + A3*Y4) + Constante_B_Corte*(-T1*(Raio_Medio**2)*math.sin(math.pi/2)+A3*X4)) +Qb4
    Qb2 = Ex_3 * (Constante_A_Corte*A3*Y1 + Constante_B_Corte*A3*X1) + Ex_1 * (Constante_A_Corte*(T1*(Y1*Altura_Media - 0.5*Altura_Media**2) ) + Constante_B_Corte*(T1*X1*Altura_Media )) + Qb1
    QbC = Ex_3 * (Constante_A_Corte*A3*Y2 + Constante_B_Corte*A3*X2) +Ex_2 * (Constante_A_Corte*(T2*Y2*Raio_Medio) + Constante_B_Corte*(T2*(X2*Raio_Medio - 0.5*Raio_Medio**2))) +Qb2 

    I_C3 = Ex_2 * (Constante_A_Corte * T2 * 0.5 * Y2 * Raio_Medio**2 - T2 * Constante_B_Corte*(1/6) * Raio_Medio**3)
    I_34 = Ex_3 * (Constante_A_Corte*A3*Y3*Altura_Media + Constante_B_Corte*A3*X3*Altura_Media) + Ex_1 * (Constante_A_Corte * (T1 * Y3 * Altura_Media**2 * 0.5 + (1/6) * T1 * Altura_Media**3  ) + Constante_B_Corte * (T1 * X3 * 0.5 * Altura_Media**2  )) + Qb3 * Altura_Media 
    I_41 = Ex_3 * (Constante_A_Corte*A3 * Y4 * Raio_Medio * math.pi + Constante_B_Corte*+ A3 * X4 * Raio_Medio * math.pi) + Ex_1 * (Constante_A_Corte * (T1 * 0.5 * Raio_Medio**2 * Y1 * math.pi**2  + T1 * Raio_Medio**3 * math.pi ) + Constante_B_Corte * (-2* T1 * Raio_Medio**3 )) + Qb4 * math.pi * Raio_Medio
    I_41_= Raio_Medio*(Qb4*math.pi + Constante_A_Corte*Ex_1*math.pi*T1*Raio_Medio**2 + A3*Constante_B_Corte*Ex_3*math.pi*X4 + A3*Constante_A_Corte*Ex_3*math.pi*Y4 + (Constante_A_Corte*Ex_1*T1*Raio_Medio*Y4*math.pi**2)/2 + Constante_B_Corte*Ex_1*T1*math.cos(math.pi)*Raio_Medio**2 - Constante_A_Corte*Ex_1*T1*math.sin(math.pi)*Raio_Medio**2 )
    I_12 = Ex_3 * (Constante_A_Corte* Y1 * A3 * Altura_Media + Constante_B_Corte*A3 * X1 * Altura_Media) + Ex_1 * (Constante_A_Corte * (T1 * 0.5 * Y1 * Altura_Media**2  - (1/6) * T1 * Altura_Media**3  ) + Constante_B_Corte * (0.5 * T1 * X1 * Altura_Media**2 )) + Qb1 * Altura_Media
    I_12_= Qb1*Altura_Media - 0.166667*Constante_A_Corte*Ex_1*T1*Altura_Media**3  + A3*Constante_B_Corte*Ex_3*Altura_Media*X1 + (Constante_B_Corte*Ex_1*T1*X1*Altura_Media**2)/2 + A3*Constante_A_Corte*Ex_3*Altura_Media*Y1 + 0.5*Constante_A_Corte*Ex_1*T1*Y1*Altura_Media**2
    I_2C = Ex_3 * (Constante_A_Corte*A3 * Y2 * Raio_Medio + Constante_B_Corte*A3 * X2 * Raio_Medio) + Ex_2 * (Constante_A_Corte * (T2 * 0.5 * Y2 * Raio_Medio**2  ) + Constante_B_Corte * (0.5 * T2 * X2 * Raio_Medio**2  - (1/6) * T2 * Raio_Medio**3  )) + Qb2 * Raio_Medio
    #I_2C_ = Qb2*Raio_Medio - 0.166667*Constante_B_Corte*Ex_2*T2*Raio_Medio**3 + A3*Constante_B_Corte*Ex_2*Raio_Medio*X2 + 0.5*Constante_B_Corte*Ex_2*T2*X2*Raio_Medio**2 + A3*Constante_A_Corte*Ex_2*Raio_Medio*Y2 + (Constante_A_Corte*Ex_2*T2*Y2*Raio_Medio**2)/2

    #integração sentido horário
    I_total = - Altura_Media * I_C3 - Raio_Medio * I_34 - Raio_Medio * I_41_ - Raio_Medio * I_12_ - Altura_Media * I_2C

    PxBraço_1, PxBraço_2, PxBraço_3, PxBraço_4 = Px_1 * 0, Px_2 * Altura_Media , Px_3 * Altura_Media  , Px_4 * 0
    PyBraço_1, PyBraço_2, PyBraço_3, PyBraço_4 = Py_1 * Raio_Medio, Py_2 * Raio_Medio , Py_3 * (- Raio_Medio)  , Py_4 * (- Raio_Medio)
    Soma_PxB = PxBraço_1 + PxBraço_2 + PxBraço_3 + PxBraço_4
    Soma_PyB = PyBraço_1 + PyBraço_2 + PyBraço_3 + PyBraço_4

    qs_0_i = (Sx * 1.2 - I_total + Soma_PxB - Soma_PyB) / (2 * A_Varrida) 
    #qs_0_i = 0
    Qb1, Qb2, Qb3, Qb4, QbC = 0,0,0,0,0
    if Debug.DEBUG:
        Coords_X_,Coords_Y_,Coords_Z_, Modo_De_Falha = [],[],[],[]
        Coords_X,Coords_Y,Coords_Z = [],[],[]
    
    #qs_0_i = 0
    #VIGA HORIZONTAL, MEIO ATE PONTA
    for Ponto_S in np.linspace(0, Raio_Medio , NUMERO_DE_PONTOS):
        Coordenada_X =  - Ponto_S
        Coordenada_Y = -Altura_Media - Centroide_Y
        Tensao_Direta = Ex_2 * (Constante_A_Direta*Coordenada_X + Constante_B_Direta*Coordenada_Y) 
        Fluxo_Corte = Ex_2 * (Constante_A_Corte*Ponto_S*Y2*T2 + Constante_B_Corte*T2*(-0.5*Ponto_S**2))
        
        Tensao_de_Corte = (Fluxo_Corte + qs_0_i)/T2
        FS_Criterea = Teste_de_falha.Tensoes_Eixos_Camada(Tensao_Direta, 0, Tensao_de_Corte, Laminado_2)  
        
        if Falha and FS_Criterea:
            return True, 0, 0
        
        if Plotting:
            Coords_X.append(Coordenada_X)
            Coords_Y.append(Coordenada_Y)
            Coords_Z.append(Tensao_de_Corte)
            Plotting_Lib.Adicionar_Coor(Coordenada_X, Coordenada_Y, Seccao)
            
        
    Qb3 = Fluxo_Corte

    #VIGA VERTICAL ESQUERDA    
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Coordenada_X = -Raio_Medio
        Coordenada_Y = - Altura_Media + Ponto_S - Centroide_Y
        Tensao_Direta = Ex_1 * (Constante_A_Direta*Coordenada_X + Constante_B_Direta*Coordenada_Y)
        Fluxo_Corte = Ex_3*(Constante_A_Corte*A3*Y3 + Constante_B_Corte*A3*X3) + Ex_1 * (Constante_A_Corte*(Ponto_S*Y3*T1 + T1*0.5*Ponto_S**2 ) + Constante_B_Corte*(T1*X3*Ponto_S)) + Qb3
       
        
        Tensao_de_Corte = (Fluxo_Corte + qs_0_i)/T1
        FS_Criterea = Teste_de_falha.Tensoes_Eixos_Camada(Tensao_Direta, 0, Tensao_de_Corte, Laminado_1)
        if Falha and FS_Criterea:  
            return True, 0, 0
                
        if Plotting:
            Coords_X.append(Coordenada_X)
            Coords_Y.append(Coordenada_Y)
            Coords_Z.append(Tensao_de_Corte)
            
            Plotting_Lib.Adicionar_Coor(Coordenada_X, Coordenada_Y, Seccao)

            
        
    Qb4 = Fluxo_Corte
    #VIGA SEMICIRCULO 
    for Ponto_S in np.linspace(0, math.pi , NUMERO_DE_PONTOS):
        Coordenada_X = -Raio_Medio*math.cos(Ponto_S)
        Coordenada_Y = Raio_Medio*math.sin(Ponto_S) - Centroide_Y
        Tensao_Direta = Ex_1 * (Constante_A_Direta*Coordenada_X + Constante_B_Direta*Coordenada_Y)
        
        Fluxo_Corte = Ex_3*(Constante_A_Corte*A3*Y4 + Constante_B_Corte*A3*X4) + Ex_1 * (Constante_A_Corte*(T1*Raio_Medio*Y1*Ponto_S + T1*(Raio_Medio**2)*(1-math.cos(Ponto_S)) ) + Constante_B_Corte*(-T1*(Raio_Medio**2)*math.sin(Ponto_S))) + Qb4
        
        Tensao_de_Corte = (Fluxo_Corte + qs_0_i)/T1
        FS_Criterea = Teste_de_falha.Tensoes_Eixos_Camada(Tensao_Direta, 0, Tensao_de_Corte, Laminado_1)
        if Falha and FS_Criterea:  
            return True, 0, 0
                
        if Plotting:
            Coords_X.append(Coordenada_X)
            Coords_Y.append(Coordenada_Y)
            Coords_Z.append(Tensao_de_Corte)
            
            Plotting_Lib.Adicionar_Coor(Coordenada_X, Coordenada_Y, Seccao)

            
        
    Qb1 = Fluxo_Corte
    #VIGA VERTICAL DIREITA
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Coordenada_X = Raio_Medio
        Coordenada_Y = - Ponto_S - Centroide_Y
        Tensao_Direta = Ex_1 * (Constante_A_Direta*Coordenada_X + Constante_B_Direta*Coordenada_Y)
        
        Fluxo_Corte = Ex_3*(Constante_A_Corte*A3*Y1 + Constante_B_Corte*A3*X1) + Ex_1 * (Constante_A_Corte*(T1*(Y1*Ponto_S - 0.5*Ponto_S**2)) + Constante_B_Corte*(T1*X1*Ponto_S)) + Qb1
        
        Tensao_de_Corte = (Fluxo_Corte + qs_0_i)/T1
        FS_Criterea = Teste_de_falha.Tensoes_Eixos_Camada(Tensao_Direta, 0, Tensao_de_Corte, Laminado_1)
        if Falha and FS_Criterea:  
            return True, 0, 0
                
        if Plotting:
        #     Coords_X.append(Coordenada_X)
        #     Coords_Y.append(Coordenada_Y)
        #     Coords_Z.append(Tensao_de_Corte)
            
            Plotting_Lib.Adicionar_Coor(Coordenada_X, Coordenada_Y, Seccao)

            
        
    Qb2 = Fluxo_Corte
    #VIGA HORIZONTAL DA PONTA ATE O MEIO
    for Ponto_S in np.linspace(0, Raio_Medio , NUMERO_DE_PONTOS):
        Coordenada_X = -Ponto_S + Raio_Medio
        Coordenada_Y = - Altura_Media - Centroide_Y
        Tensao_Direta = Ex_2 * (Constante_A_Direta*Coordenada_X + Constante_B_Direta*Coordenada_Y)
        
        Fluxo_Corte = Ex_3*(Constante_A_Corte*A3*Y2 + Constante_B_Corte*A3*X2) + Ex_2 * (Constante_A_Corte*(T2*Y2*Ponto_S ) + Constante_B_Corte*(T2*(X2*Ponto_S - 0.5*Ponto_S**2))) + Qb2
        
        Tensao_de_Corte = (Fluxo_Corte + qs_0_i)/T2
        FS_Criterea = Teste_de_falha.Tensoes_Eixos_Camada(Tensao_Direta, 0, Tensao_de_Corte, Laminado_2)
        if Falha and FS_Criterea:  
            return True, 0, 0
                
        if Plotting:
            Coords_X.append(Coordenada_X)
            Coords_Y.append(Coordenada_Y)
            Coords_Z.append(Tensao_de_Corte)
            
            Plotting_Lib.Adicionar_Coor(Coordenada_X, Coordenada_Y, Seccao)

            
        
    QbC = Fluxo_Corte

    # TORSÃO E DEFLEXÃO 
    # Torção 
    G1 , G2 = Laminado_1.Gxy, Laminado_2.Gxy
    Taxa_Torcao = (I_C3 + I_2C) / (G2 * T2) + (I_34 + I_41 + I_12) / (G1 * T1)  + qs_0_i * ((2 * Altura_Media + math.pi * Raio_Medio) / (G1 * T1) + (2 * Raio_Medio) / (G2 * T2))
    Taxa_Torcao = Taxa_Torcao/(2*A_Varrida)
    # Deflexão
    Taxa_Deflecao = -Momento_X / I_xx
    
    # return FS_Falha

    # if Plotting:
    #     Coords_X, Coords_Y, Coords_Z = np.array(Coords_X),np.array(Coords_Y),np.array(Coords_Z)
    #     fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    #     markerline, stemlines, baseline = ax.stem(
    #         Coords_X, Coords_Y, Coords_Z, linefmt='grey', markerfmt='D', bottom=0)
    #     markerline.set_markerfacecolor('none')
    #     ax.set_proj_type("ortho")

    #     plt.show()
        
    
    return False, Taxa_Torcao, Taxa_Deflecao