from Constantes import *
import math

def Momentos_Area(z, Laminado_1, Laminado_2, Laminado_3, b):

    Espessura_laminado1 = Laminado_1.Espessura
    Espessura_laminado2 = Laminado_2.Espessura
    Espessura_laminado3 = Laminado_3.Espessura
    Area_laminado3 = b * Laminado_3.Espessura

    Ez_1 = Laminado_1.Ex
    Ez_2 = Laminado_2.Ex
    Ez_3 = Laminado_3.Ex

    h_altura_i = 0.9*(1-0.5*z/COMPRIMENTO_FUSELAGEM)
    w_diametro_i = 1.5*(1-0.7*z/COMPRIMENTO_FUSELAGEM)
    h_altura_ii = h_altura_i - Espessura_laminado2/2
    w_diametro_ii = w_diametro_i - Espessura_laminado1

    A_semicircuf_i = math.pi/8*(w_diametro_i**2-(w_diametro_i - 2*Espessura_laminado1 )**2)
    A_horizontal_i = (w_diametro_i - 2*Espessura_laminado1)*Espessura_laminado2
    A_vertical_i = 2*(h_altura_i*Espessura_laminado1)
    A_tensores_i = 4*Area_laminado3
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
    distancia_y_tensoresUp_i = -y_CG
    distancia_y_tensoresDown_i = y_horizontal_i - y_CG

    distancia_x_semicircuf_i = 0 
    distancia_x_horizontal_i = 0
    distancia_x_vertical_i = w_diametro_ii/2
    distancia_x_tensores_i = w_diametro_ii/2

    Ixx_semicircuf_i = Ez_1 * math.pi/128 * (w_diametro_i**4 - (w_diametro_i - Espessura_laminado1)**4) - A_semicircuf_i * y_semicircuf_i**2 + A_semicircuf_i * (distancia_y_semicircuf_i)**2
    Ixx_vertical_i = Ez_1 * 2 * ((Espessura_laminado1 * h_altura_i**3)/12 + Espessura_laminado1 * h_altura_i * distancia_x_vertical_i**2)
    Ixx_horizontal_i = Ez_2 * (w_diametro_ii - Espessura_laminado1) * Espessura_laminado2 * distancia_y_horizontal_i**2
    Ixx_tensores_i = Ez_3 * 2 * (Espessura_laminado3 * b) * (distancia_y_tensoresUp_i**2 + distancia_y_tensoresDown_i**2)
    Ixx_total_i = Ixx_semicircuf_i + Ixx_vertical_i + Ixx_horizontal_i + Ixx_tensores_i

    Iyy_semicircuf_i = Ez_1 * math.pi/128 * (w_diametro_i**4 - (w_diametro_i - Espessura_laminado1)**4)
    Iyy_vertical_i = Ez_1 * 2 * h_altura_i * Espessura_laminado1 * distancia_x_vertical_i
    Iyy_horizontal_i = Ez_2 * (Espessura_laminado2 * (w_diametro_ii - Espessura_laminado1)**3) /12
    Iyy_tensores_i = Ez_3 * 4 * (Espessura_laminado3 * b * distancia_x_tensores_i**2)
    Iyy_total_i = Iyy_semicircuf_i + Iyy_vertical_i + Iyy_horizontal_i + Iyy_tensores_i

    Ixy_semicircuf_i = 0
    Ixy_vertical_i = 0
    Ixy_horizontal_i = 0
    Ixy_tensores_i = 0
    Ixy_total_i = 0

    return Ixx_total_i , Iyy_total_i , Ixy_total_i , y_CG , x_CG , h_altura_ii , w_diametro_ii


    






