from Constantes import *
import Propriadades
import Definicao_Laminado
import Carregamento
import Afilamento

import math
import numpy as np

NUMERO_DE_PONTOS = 100

# TEM DE SER UM FUNCAO AO CENTROIDE

def Analise_Tensao_Direta(z, Laminado_1, Laminado_2, Laminado_3):

    Altura_Media, Raio_Medio = Propriadades.Obter_Geometria_Media(z)
    Centroide_X, Centroide_Y = Propriadades.Obter_Centroide(z)
    I_xx, I_yy = Propriadades.Obter_Segundo_Momentos_De_Area(z)

    Propriadades_da_Seccao = Propriadades.Obter_Propriades(z)

    Barra_Vertical = Propriadades_da_Seccao.Barra_Vertical_D
    Barra_Horizontal = Propriadades_da_Seccao.Barra_Horizontal
    SemiCirculo = Propriadades_da_Seccao.SemiCirculo
    Tensores = Propriadades_da_Seccao.Tensores

    Forca_X, Forca_Y = Carregamento.Obter_Forcas(z)
    Momento_X, Momento_Y = Carregamento.Obter_Momentos(z)
    
    Lista_Px,Lista_Py = Afilamento.Obter_Forcas_Afilamento(z) 
    
    # Analise comeca no meio da barra horizontal.

    Constante_Em_X = (Momento_Y / I_yy)
    Constante_Em_Y = (Momento_X / I_xx)

    Tensoes_Diretas = []
    
    #VIGA HORIZONTAL, MEIO ATE PONTA
    for Ponto_S in np.linspace(0, Raio_Medio , NUMERO_DE_PONTOS):
        Coordenada_X = Ponto_S - Centroide_X
        Coordenada_Y = -Altura_Media - Centroide_Y
        Tensao_Direta = Barra_Horizontal.Ex * (Constante_Em_X*Coordenada_X + Constante_Em_Y*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
        
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Coordenada_X = -Raio_Medio - Centroide_X
        Coordenada_Y = - Altura_Media + Ponto_S - Centroide_Y
        Tensao_Direta = Barra_Vertical.Ex * (Constante_Em_X*Coordenada_X + Constante_Em_Y*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
        
    for Ponto_S in np.linspace(0, math.pi , NUMERO_DE_PONTOS):
        Coordenada_X = -Raio_Medio*math.cos(Ponto_S) - Centroide_X
        Coordenada_Y = -Raio_Medio*math.sin(Ponto_S) - Centroide_Y
        Tensao_Direta = SemiCirculo.Ex * (Constante_Em_X*Coordenada_X + Constante_Em_Y*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
        
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Coordenada_X = Raio_Medio - Centroide_X
        Coordenada_Y = - Ponto_S - Centroide_Y
        Tensao_Direta = Barra_Vertical.Ex * (Constante_Em_X*Coordenada_X + Constante_Em_Y*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
        
    for Ponto_S in np.linspace(0, Raio_Medio , NUMERO_DE_PONTOS):
        Coordenada_X = Ponto_S - Raio_Medio - Centroide_X
        Coordenada_Y = - Altura_Media - Centroide_Y
        Tensao_Direta = Barra_Horizontal.Ex * (Constante_Em_X*Coordenada_X + Constante_Em_Y*Coordenada_Y)
        Tensoes_Diretas.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Direta})
        
    return Tensoes_Diretas


def Analise_Tensao_Corte(z, Laminado_1, Laminado_2, Laminado_3):

    Altura_Media, Raio_Medio = Propriadades.Obter_Geometria_Media(z)
    Centroide_X, Centroide_Y = Propriadades.Obter_Centroide(z)
    I_xx, I_yy = Propriadades.Obter_Segundo_Momentos_De_Area(z)

    Propriadades_da_Seccao = Propriadades.Obter_Propriades(z)

    Barra_Vertical = Propriadades_da_Seccao.Barra_Vertical_D
    Barra_Horizontal = Propriadades_da_Seccao.Barra_Horizontal
    SemiCirculo = Propriadades_da_Seccao.SemiCirculo
    Tensores = Propriadades_da_Seccao.Tensores
    
    Distancias = Propriadades.Obter_Distancias(z)

    Forca_X, Forca_Y = Carregamento.Obter_Forcas(z)
    Momento_X, Momento_Y = Carregamento.Obter_Momentos(z)

    # Analise comeca no meio da barra horizontal.
    
    Constante_Em_X = (Forca_X / I_yy)
    Constante_Em_Y = (Forca_Y / I_xx)

    Tensoes_Corte = []
    
    #VIGA HORIZONTAL, MEIO ATE PONTA
    for Ponto_S in np.linspace(0, Raio_Medio , NUMERO_DE_PONTOS):
        Coordenada_X = Ponto_S - Centroide_X
        Coordenada_Y = -Altura_Media - Centroide_Y
        Tensao_Corte = Barra_Horizontal.Ex * (Constante_Em_X*(Espessura_2*) + Constante_Em_Y*(Coordenada_Y))
        Tensoes_Corte.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Corte})
        
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Coordenada_X = -Raio_Medio - Centroide_X
        Coordenada_Y = - Altura_Media + Ponto_S - Centroide_Y
        #Tensao_Corte = Barra_Vertical.Ex * (Constante_Em_X*Coordenada_X + Constante_Em_Y*Coordenada_Y)
        Tensoes_Corte.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Corte})
        
    for Ponto_S in np.linspace(0, math.pi , NUMERO_DE_PONTOS):
        Coordenada_X = -Raio_Medio*math.cos(Ponto_S) - Centroide_X
        Coordenada_Y = -Raio_Medio*math.sin(Ponto_S) - Centroide_Y
        #Tensao_Corte = SemiCirculo.Ex * (Constante_Em_X*Coordenada_X + Constante_Em_Y*Coordenada_Y)
        Tensoes_Corte.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Corte})
        
    for Ponto_S in np.linspace(0, Altura_Media , NUMERO_DE_PONTOS):
        Coordenada_X = Raio_Medio - Centroide_X
        Coordenada_Y = - Ponto_S - Centroide_Y
        #Tensao_Corte = Barra_Vertical.Ex * (Constante_Em_X*Coordenada_X + Constante_Em_Y*Coordenada_Y)
        Tensoes_Corte.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Corte})
        
    for Ponto_S in np.linspace(0, Raio_Medio , NUMERO_DE_PONTOS):
        Coordenada_X = Ponto_S - Raio_Medio - Centroide_X
        Coordenada_Y = - Altura_Media - Centroide_Y
        #Tensao_Corte = Barra_Horizontal.Ex * (Constante_Em_X*Coordenada_X + Constante_Em_Y*Coordenada_Y)
        Tensoes_Corte.append({"Coords" : (Coordenada_X, Coordenada_Y), "Tensao" : Tensao_Corte})
        
    return Tensoes_Corte


def Analise_Seccao(z,Laminado_1, Laminado_2, Laminado_3):