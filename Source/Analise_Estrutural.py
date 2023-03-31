from Constantes import *
import Propriadades
import Definicao_Laminado
import Carregamento

import math

PARTICOES_CADA_TROCO = 100

def Obter_Geometria_Media(z, Laminado_1,Laminado_2):
    
    Altura = 0.9*(1 - 0.5*z/COMPRIMENTO_FUSELAGEM)
    Diametro = 1.5*(1-0.7*z/COMPRIMENTO_FUSELAGEM)
    
    Altura_Media = Altura - Laminado_2.Espessura/2 
    Raio_Medio = Diametro/2 - Laminado_1.Espessura/2
    
    return Altura_Media, Raio_Medio

# TEM DE SER UM FUNCAO AO CENTROIDE
def Obter_Coordenadas_Vertical_Esquerda(S_Coordenada, z, Altura_Media, Raio_Medio):
    Coordenada_X = -Raio_Medio
    Coordenada_Y = - Altura_Media + S_Coordenada
    return Coordenada_X,Coordenada_Y

def Obter_Coordenadas_Semicirculo(S_Coordenada, z, Altura_Media, Raio_Medio):
    Coordenada_X = -Raio_Medio*math.cos(S_Coordenada)
    Coordenada_Y = -Raio_Medio*math.sin(S_Coordenada) 
    return Coordenada_X,Coordenada_Y
    

def Analise_Tensao_Direta(z, Laminado_1, Laminado_2, Laminado_3):
    
    Altura_Media, Raio_Medio = Propriadades.Obter_Geometria_Media(z)
    Centroide_Y, Centroide_X = Propriadades.Obter_Centroide(z)
   
    Propriadades_da_Seccao = Propriadades.Obter_Propriades(z)
    
    Barra_Vertical_D = Propriadades_da_Seccao.Barra_Vertical_D
    Barra_Vertical_E = Propriadades_da_Seccao.Barra_Vertical_E
    Barra_Horizontal = Propriadades_da_Seccao.Barra_Horizontal
    SemiCirculo      = Propriadades_da_Seccao.SemiCirculo
    Tensores         = Propriadades_da_Seccao.Tensores
    
    Troços = {Barra_Vertical_D, Barra_Vertical_E, Barra_Horizontal, SemiCirculo, Tensores}
    
    Forca_Vertical, Forca_Horizontal = Carregamento.Obter_Forcas(z)
    Momento_Vertical, Momento_Horizontal = Carregamento.Obter_Momentos(z)
    
        