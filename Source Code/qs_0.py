from Constantes import *
import Propriadades_Seccao
import math

# from Afilamento import *

# Lista_Px , Lista_Py = Afilamento.Obter_Forcas_Afilamento(z)


def qs_0(z, Laminado_1, Laminado_2, Laminado_3, b):
   
    #valores a retirar do alex
    A_i = 12
    B_i = 12
    q1, q2, q3, q4 = 1, 2, 3 , 4

    #valores a retirar do filipe
    Px_1, Px_2, Px_3, Px_4 = 12, 12, 12, 12
    Py_1, Py_2, Py_3, Py_4 = 12, 12, 12, 12
    Sx = 76
    

    Segundo_Momentos_De_Area , Centroide , Geometria_Media , Coordenadas_x , Coordenadas_y = Propriadades_Seccao.Momentos_Area(
        z, Laminado_1, Laminado_2, Laminado_3, b)

    Espessura_laminado1 = Laminado_1.Espessura
    Espessura_laminado2 = Laminado_2.Espessura
    Espessura_laminado3 = Laminado_3.Espessura
    Area_laminado3 = b * Laminado_3.Espessura

    x_1, x_2, x_3, x_4 = Coordenadas_x
    y_1, y_2, y_3, y_4 = Coordenadas_y
    w_linha = Geometria_Media[1]/2
    h_linha = Geometria_Media[0]
    A_total_i = h_linha * w_linha + math.pi/2* w_linha**2

    I_C3 = A_i/2 *  y_2 * w_linha**2 - B_i /6* w_linha**3
    I_34 = A_i * (Espessura_laminado1 * y_3 * h_linha**2 /2 + Espessura_laminado1 * h_linha**3 /6 + Area_laminado3 * y_3 * h_linha) + B_i * (Espessura_laminado1 * x_3 * h_linha**2 /2 + Area_laminado3 * x_3 * h_linha) + q3 * h_linha 
    I_41 = A_i * (Espessura_laminado1 * w_linha**2 * y_1 * math.pi**2 /2 + Espessura_laminado1 * w_linha**3 * math.pi + Area_laminado3 * y_4 * w_linha * math.pi) + B_i * (-2* Espessura_laminado1 * w_linha**3 + Area_laminado3 * x_4 * w_linha * math.pi) + q4 * math.pi * w_linha
    I_12 = A_i * (Espessura_laminado1 * y_1 * h_linha**2 /2 - Espessura_laminado1 * h_linha**3 /6 + y_1 * Area_laminado3 * h_linha) + B_i * (Espessura_laminado1 * x_1 * h_linha**2 /2 + B_i * x_1 * h_linha) + q1 * h_linha
    I_2C = A_i * (Espessura_laminado2 * y_2 * w_linha**2 /2 + Area_laminado3 * y_2 * w_linha) + B_i * (Espessura_laminado2 * x_2 * w_linha**2 /2 - Espessura_laminado2 * w_linha**3 /6 + Area_laminado3 * x_2 * w_linha) + q2 * w_linha

    #integração sentido horário
    I_total = - h_linha * I_C3 - w_linha * I_34 - w_linha * I_41 - w_linha * I_12 - h_linha * I_2C

    PxBraço_1, PxBraço_2, PxBraço_3, PxBraço_4 = Px_1 * 0, Px_2 * h_linha , Px_3 * h_linha  , Px_4 * 0
    PyBraço_1, PyBraço_2, PyBraço_3, PyBraço_4 = Py_1 * w_linha, Py_2 * w_linha , Py_3 * (- w_linha)  , Py_4 * (- w_linha)
    Soma_PxB = PxBraço_1 + PxBraço_2 + PxBraço_3 + PxBraço_4
    Soma_PyB = PyBraço_1 + PyBraço_2 + PyBraço_3 + PyBraço_4

    qs_0_i = (Sx * 1.2 - I_total + Soma_PxB - Soma_PyB) / (2 * A_total_i) #Area Errada, esta area nao é a area da seccao mas é a area interior á seccao media. Nao alterei manel. Altera Tu.

    return qs_0_i
