from Constantes import *

def F_Afilamento(Centroide, Segundo_Momentos_De_Area, Geometria_Media, Elasticidades, Momentos):

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
    Tensao_Direta = Ex_2 * (Constante_A_Direta*Coordenada_X + Constante_B_Direta*Coordenada_Y)

    