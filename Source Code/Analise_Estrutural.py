from Constantes import *

import math
import numpy as np

NUMERO_DE_PONTOS = 100

# TEM DE SER UM FUNCAO AO CENTROIDE

def Tensao_Direta(Geometria_Media, Centroide, Segundo_Momentos_De_Area, Momentos, Elasticidades):

    Altura_Media, Raio_Medio = Geometria_Media
    Centroide_X, Centroide_Y = Centroide
    I_xx, I_yy, Ixy_ = Segundo_Momentos_De_Area
    Ex_1,Ex_2,Ex_3 = Elasticidades
    
    Momento_X, Momento_Y = Momentos
    
    # Analise comeca no meio da barra horizontal.

    Constante_A = (Momento_Y / I_yy)
    Constante_B = (Momento_X / I_xx)

    Tensoes_Diretas = []
    
    #VIGA HORIZONTAL, MEIO ATE PONTA
    for Ponto_S in np.linspace(0, Raio_Medio , NUMERO_DE_PONTOS):
        Coordenada_X = Ponto_S - Centroide_X
        Coordenada_Y = -Altura_Media - Centroide_Y
        Tensao_Direta = Ex_2 * (Constante_A*Coordenada_X + Constante_B*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
    #VIGA VERTICAL ESQUERDA    
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Coordenada_X = -Raio_Medio - Centroide_X
        Coordenada_Y = - Altura_Media + Ponto_S - Centroide_Y
        Tensao_Direta = Ex_1 * (Constante_A*Coordenada_X + Constante_B*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
    #VIGA SEMICIRCULO 
    for Ponto_S in np.linspace(0, math.pi , NUMERO_DE_PONTOS):
        Coordenada_X = -Raio_Medio*math.cos(Ponto_S) - Centroide_X
        Coordenada_Y = -Raio_Medio*math.sin(Ponto_S) - Centroide_Y
        Tensao_Direta = Ex_1 * (Constante_A*Coordenada_X + Constante_B*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
    #VIGA VERTICAL DIREITA
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Coordenada_X = Raio_Medio - Centroide_X
        Coordenada_Y = - Ponto_S - Centroide_Y
        Tensao_Direta = Ex_1 * (Constante_A*Coordenada_X + Constante_B*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
    #VIGA HORIZONTAL DA PONTA ATE O MEIO
    for Ponto_S in np.linspace(0, Raio_Medio , NUMERO_DE_PONTOS):
        Coordenada_X = Ponto_S - Raio_Medio - Centroide_X
        Coordenada_Y = - Altura_Media - Centroide_Y
        Tensao_Direta = Ex_2 * (Constante_A*Coordenada_X + Constante_B*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
        
    return Tensoes_Diretas

def Tensao_de_Corte(Geometria_Media, Centroide, Segundo_Momentos_De_Area, Forcas_Afilamento, Elasticidades, Espessuras, Coordenadas_Y, Coordenadas_X):
    Altura_Media, Raio_Medio = Geometria_Media
    Centroide_X, Centroide_Y = Centroide
    I_xx, I_yy, Ixy = Segundo_Momentos_De_Area
    Ex_1,Ex_2,Ex_3 = Elasticidades
    T1,T2,A3 = Espessuras
    
    X1,X2,X3,X4 = Coordenadas_X
    Y1,Y2,Y3,Y4 = Coordenadas_Y

    Forca_SX_W, Forca_SY_W = Forcas_Afilamento
    
    Constante_A = (Forca_SX_W / I_yy)
    Constante_B = (Forca_SY_W / I_xx)
    
    Fluxos_Corte = []
    Tensoes_Corte = []
    
    Qb1, Qb2, Qb3, Qb4, QbC = 0,0,0,0,0
    
    #VIGA HORIZONTAL, MEIO ATE PONTA
    for Ponto_S in np.linspace(0, Raio_Medio , NUMERO_DE_PONTOS):
        Fluxo_Corte = Ex_2 * (Constante_A*Ponto_S*Y2*T2 + Constante_B*T2*(-0.5*Ponto_S**2))
        Tensao_de_Corte = Fluxo_Corte/T2
        Coordenada_X = Ponto_S - Centroide_X
        Coordenada_Y = -Altura_Media - Centroide_Y
        Fluxos_Corte.append({"Coords" : (1,Ponto_S), "Tensao" : Fluxo_Corte})
        Tensoes_Corte.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_de_Corte})
        Qb3 = Fluxo_Corte

    #VIGA VERTICAL ESQUERDA    
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Fluxo_Corte = Ex_1 * (Constante_A*(Ponto_S*Y3*T1 + T1*0.5*Ponto_S**2 + A3*Y3) + Constante_B*(T1*X3*Ponto_S+A3*X3)) + Qb3
        Tensao_de_Corte = Fluxo_Corte/T1
        Coordenada_X = -Raio_Medio - Centroide_X
        Coordenada_Y = - Altura_Media + Ponto_S - Centroide_Y
        Fluxos_Corte.append({"Coords" : (2,Ponto_S), "Tensao" : Fluxo_Corte})
        Tensoes_Corte.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_de_Corte})
        Qb4 = Fluxo_Corte
    #VIGA SEMICIRCULO 
    for Ponto_S in np.linspace(0, math.pi , NUMERO_DE_PONTOS):
        Fluxo_Corte = Ex_1 * (Constante_A*(T1*Raio_Medio*Y1*Ponto_S + T1*(Raio_Medio**2)*(1-math.cos(Ponto_S)) + A3*Y4) + Constante_B*(-T1*(Raio_Medio**2)*math.sin(Ponto_S)+A3*X4)) + Qb4
        Tensao_de_Corte = Fluxo_Corte/T1
        Coordenada_X = -Raio_Medio*math.cos(Ponto_S) - Centroide_X
        Coordenada_Y = -Raio_Medio*math.sin(Ponto_S) - Centroide_Y
        Fluxos_Corte.append({"Coords" : (3,Ponto_S), "Tensao" : Fluxo_Corte})
        Tensoes_Corte.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_de_Corte})
        Qb1 = Fluxo_Corte
    #VIGA VERTICAL DIREITA
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Fluxo_Corte = Ex_1 * (Constante_A*(T1*(Y1*Ponto_S - 0.5*Ponto_S**2) + Y1*A3) + Constante_B*(T1*X1*Ponto_S + A3*X1)) + Qb1
        Tensao_de_Corte = Fluxo_Corte/T1
        Coordenada_X = Raio_Medio - Centroide_X
        Coordenada_Y = - Ponto_S - Centroide_Y
        Fluxos_Corte.append({"Coords" : (4,Ponto_S), "Tensao" : Fluxo_Corte})
        Tensoes_Corte.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_de_Corte})
        Qb2 = Fluxo_Corte
    #VIGA HORIZONTAL DA PONTA ATE O MEIO
    for Ponto_S in np.linspace(0, Raio_Medio , NUMERO_DE_PONTOS):
        Fluxo_Corte = Ex_2 * (Constante_A*(T2*Y2*Ponto_S + A3*Y2) + Constante_B*(T2*(X2*Ponto_S - 0.5*Ponto_S**2) + A3*X2)) + Qb2
        Tensao_de_Corte = Fluxo_Corte/T2
        Coordenada_X = Ponto_S - Raio_Medio - Centroide_X
        Coordenada_Y = - Altura_Media - Centroide_Y
        Fluxos_Corte.append({"Coords" : (5,Ponto_S), "Tensao" : Fluxo_Corte})
        Tensoes_Corte.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_de_Corte})
        QbC = Fluxo_Corte
    
    #print(Qb1, Qb2, Qb3, Qb4, QbC)    
    return Fluxos_Corte