from Constantes import *

import math
import numpy as np

NUMERO_DE_PONTOS = 100

# TEM DE SER UM FUNCAO AO CENTROIDE

def Tensao_Direta(Geometria_Media, Centroide, Segundo_Momentos_De_Area, Momentos, Laminados):

    Altura_Media, Raio_Medio = Geometria_Media
    Centroide_X, Centroide_Y = Centroide
    I_xx, I_yy, Ixy_ = Segundo_Momentos_De_Area

    Momento_X, Momento_Y = Momentos
    
    Ex_1 = Laminados[0].Ex
    Ex_2 = Laminados[1].Ex
    
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
        
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Coordenada_X = -Raio_Medio - Centroide_X
        Coordenada_Y = - Altura_Media + Ponto_S - Centroide_Y
        Tensao_Direta = Ex_1 * (Constante_A*Coordenada_X + Constante_B*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
        
    for Ponto_S in np.linspace(0, math.pi , NUMERO_DE_PONTOS):
        Coordenada_X = -Raio_Medio*math.cos(Ponto_S) - Centroide_X
        Coordenada_Y = -Raio_Medio*math.sin(Ponto_S) - Centroide_Y
        Tensao_Direta = Ex_1 * (Constante_A*Coordenada_X + Constante_B*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
        
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Coordenada_X = Raio_Medio - Centroide_X
        Coordenada_Y = - Ponto_S - Centroide_Y
        Tensao_Direta = Ex_1 * (Constante_A*Coordenada_X + Constante_B*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
        
    for Ponto_S in np.linspace(0, Raio_Medio , NUMERO_DE_PONTOS):
        Coordenada_X = Ponto_S - Raio_Medio - Centroide_X
        Coordenada_Y = - Altura_Media - Centroide_Y
        Tensao_Direta = Ex_2 * (Constante_A*Coordenada_X + Constante_B*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
        
    return Tensoes_Diretas
