from Constantes import *
import math

n_1 = 2
n_2 = 3
n_3 = 2
b = 0.05

Espessura_laminado1 = ESPESSURA_CAMADA * n_1
Espessura_laminado2 = ESPESSURA_CAMADA * n_2
Espessura_laminado3 = ESPESSURA_CAMADA * n_3
Area_lamindado3 = Espessura_laminado3 * b

def Momentos_Area(z, Laminado_1, Laminado_2, Lamindado_3):
    h_altura_i = 0.9*(1-0.5*z/COMPRIMENTO_FUSELAGEM)
    w_diametro_i = 1.5*(1-0.7*z/COMPRIMENTO_FUSELAGEM)
    h_altura_ii = h_altura_i - Espessura_laminado2/2
    w_diametro_ii = w_diametro_i - Espessura_laminado1

    A_semicircuf_i = math.pi/8*(w_diametro_i**2-(w_diametro_i - 2*Espessura_laminado1 )**2)
    A_horizontal_i = (w_diametro_i - 2*Espessura_laminado1)*Espessura_laminado2
    A_vertical_i = 2*(h_altura_i*Espessura_laminado1)
    A_tensores_i = 4*Area_lamindado3
    A_total_i = A_semicircuf_i + A_tensores_i + A_vertical_i + A_tensores_i

    y_semicircuf_i = w_diametro_ii/math.pi
    y_horizontal_i = (-h_altura_ii)
    y_vertical_i = (-h_altura_i/2)
    y_tensores_i = (-h_altura_ii/2)
    y_CG = (A_semicircuf_i*y_semicircuf_i+A_horizontal_i*y_horizontal_i+A_vertical_i*y_vertical_i+A_tensores_i*y_tensores_i)/A_total_i
    
    x_semicircuf_i = 0
    x_horizontal_i = 0
    x_vertical_i = 0
    x_tensores_i = 0
    x_CG = (A_semicircuf_i*x_semicircuf_i + A_horizontal_i*x_horizontal_i + A_vertical_i*x_vertical_i + A_tensores_i*x_tensores_i)/A_total_i

    distancia_y_semicircuf_i = y_semicircuf_i - y_CG
    distancia_y_horizontal_i = y_horizontal_i - y_CG
    distancia_y_vertical_i = y_vertical_i - y_CG
    distancia_y_tensoresUp_i = -Espessura_laminado3/2 - y_CG
    distancia_y_tensoresDown_i = abs(y_horizontal_i+Espessura_laminado2/2+Espessura_laminado3/2-y_CG)

    distancia_x_semicircuf_i = 0 
    distancia_x_horizontal_i = 0
    distancia_x_vertical_i = w_diametro_ii/2
    distancia_x_tensores_i = w_diametro_ii/2-b/2




    






