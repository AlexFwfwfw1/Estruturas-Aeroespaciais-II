from Constantes import *
import math

class Propriadades_Seccao_Objeto:
    def __init__(self,Segundo_Momentos_De_Area , Centroide , Geometria_Media, Areas , Elasticidades, Espessuras, Coordenadas_X,Coordenadas_Y,Peso_Por_Metro):
        self.Segundo_Momentos_De_Area = Segundo_Momentos_De_Area
        self.Centroide = Centroide 
        self.Geometria_Media = Geometria_Media
        self.Areas = Areas
        self.Elasticidades = Elasticidades
        self.Espessuras = Espessuras
        self.Coordenadas_X = Coordenadas_X
        self.Coordenadas_Y = Coordenadas_Y
        self.Peso_Por_Metro = Peso_Por_Metro
        

def Definir_Propriadades(z,Laminados, b):
    
    Laminado_1,Laminado_2,Laminado_3 = Laminados 

    rho_1 = Laminado_1.rho_Medio
    rho_2 = Laminado_2.rho_Medio
    rho_3 = Laminado_3.rho_Medio

    Espessura_laminado1 = Laminado_1.Espessura_Total
    Espessura_laminado2 = Laminado_2.Espessura_Total
    Area_laminado3 = Laminado_3.Espessura_Total*b

    Ez_1 = Laminado_1.Ex
    Ez_2 = Laminado_2.Ex
    Ez_3 = Laminado_3.Ex

    h_altura_i = 0.9*(1-0.5*z/COMPRIMENTO_FUSELAGEM)
    w_diametro_i = 1.5*(1-0.7*z/COMPRIMENTO_FUSELAGEM)
    h_altura_ii = h_altura_i - Espessura_laminado2/2
    w_diametro_ii = w_diametro_i - Espessura_laminado1

    A_semicircuf_i = math.pi/8*(w_diametro_i**2-(w_diametro_i - 2*Espessura_laminado1 )**2)
    A_horizontal_i = (w_diametro_i - 2*Espessura_laminado1)*Espessura_laminado2
    A_vertical_i = 2*(h_altura_ii*Espessura_laminado1)
    A_tensores_i = 4*Area_laminado3
    A_total_i = A_semicircuf_i + A_horizontal_i + A_vertical_i + A_tensores_i  
    A_total_with_Ez = A_semicircuf_i*Ez_1 + A_horizontal_i*Ez_2 + A_vertical_i*Ez_1 + A_tensores_i*Ez_3
    
    Massa_Por_Metro = A_semicircuf_i*rho_1 + A_horizontal_i*rho_2 + A_vertical_i*rho_1 + A_tensores_i*rho_3
    Peso_Por_Metro = Massa_Por_Metro*ACELERACAO_GRAVITICA

    y_semicircuf_i = w_diametro_ii/math.pi
    y_horizontal_i = (-h_altura_ii)
    y_vertical_i = (-h_altura_i/2)
    y_tensores_i = (-h_altura_ii/2)
    y_CG= (A_semicircuf_i*y_semicircuf_i + A_horizontal_i*y_horizontal_i + A_vertical_i*y_vertical_i + A_tensores_i*y_tensores_i)/A_total_i
    y_CG_with_Ez = (Ez_1*A_semicircuf_i*y_semicircuf_i + Ez_2*A_horizontal_i*y_horizontal_i + Ez_1*A_vertical_i*y_vertical_i + Ez_3*A_tensores_i*y_tensores_i)/A_total_with_Ez
    y_CG = y_CG_with_Ez

    x_semicircuf_i = 0
    x_horizontal_i = 0
    x_vertical_i = 0
    x_tensores_i = 0
    x_CG = (A_semicircuf_i*x_semicircuf_i + A_horizontal_i*x_horizontal_i + A_vertical_i*x_vertical_i + A_tensores_i*x_tensores_i)/A_total_i
    x_CG_with_Ez = (Ez_1*A_semicircuf_i*x_semicircuf_i + Ez_2*A_horizontal_i*x_horizontal_i + Ez_1*A_vertical_i*x_vertical_i + Ez_3*A_tensores_i*x_tensores_i)/A_total_with_Ez
    x_CG = x_CG_with_Ez
    
    distancia_y_semicircuf_i = y_semicircuf_i - y_CG
    distancia_y_horizontal_i = y_horizontal_i - y_CG
    distancia_y_vertical_i = y_vertical_i - y_CG
    distancia_y_tensoresUp_i = -y_CG
    distancia_y_tensoresDown_i = y_horizontal_i - y_CG

    # distancia_x_semicircuf_i = 0 
    # distancia_x_horizontal_i = 0
    distancia_x_vertical_i = w_diametro_ii/2
    distancia_x_tensores_i = w_diametro_ii/2

    Ixx_semicircuf_i = Ez_1 * math.pi/128 * (w_diametro_i**4 - (w_diametro_i - 2*Espessura_laminado1)**4) - A_semicircuf_i * y_semicircuf_i**2 + A_semicircuf_i * (distancia_y_semicircuf_i)**2
    Ixx_vertical_i =   Ez_1 * 2 * ((Espessura_laminado1 * h_altura_i**3)/12 + A_vertical_i * distancia_y_vertical_i**2) ## TAMBEM TINHA ERRO
    Ixx_horizontal_i = Ez_2 *  (Espessura_laminado1*(1/12)*(w_diametro_i - 2*Espessura_laminado1)**3 + A_horizontal_i * distancia_y_horizontal_i**2)
    Ixx_tensores_i =   Ez_3 * 2 * (Area_laminado3) * (distancia_y_tensoresUp_i**2 + distancia_y_tensoresDown_i**2)
    Ixx_total_i = Ixx_semicircuf_i + Ixx_vertical_i + Ixx_horizontal_i + Ixx_tensores_i

    Iyy_semicircuf_i = Ez_1 * math.pi/128 * (w_diametro_i**4 - (w_diametro_i - 2*Espessura_laminado1)**4)
    Iyy_vertical_i =   Ez_1 * 2 * h_altura_i * Espessura_laminado1 * distancia_x_vertical_i**2
    Iyy_horizontal_i = Ez_2 * (Espessura_laminado2 * (w_diametro_ii - Espessura_laminado1)**3) /12
    Iyy_tensores_i =   Ez_3 * 4 * (Area_laminado3 * distancia_x_tensores_i**2)
    Iyy_total_i = Iyy_semicircuf_i + Iyy_vertical_i + Iyy_horizontal_i + Iyy_tensores_i

    # Ixy_semicircuf_i = 0
    # Ixy_vertical_i = 0
    # Ixy_horizontal_i = 0
    # Ixy_tensores_i = 0
    Ixy_total_i = 0
    
    x_1 = distancia_x_vertical_i
    x_2 = x_1
    x_3 = - x_1
    x_4 = x_3
    y_1 = - y_CG
    y_2 = distancia_y_horizontal_i
    y_3 = y_2
    y_4 = y_1
    
    A_Varrida = h_altura_ii * w_diametro_ii + math.pi/2* (w_diametro_ii/2)**2
    
    Elasticidades = (Ez_1,Ez_2,Ez_3)
    Espessuras = (Espessura_laminado1,Espessura_laminado2,Area_laminado3)

    Segundo_Momentos_De_Area = (Ixx_total_i , Iyy_total_i , Ixy_total_i)
    Centroide = (x_CG, y_CG)
    Geometria_Media = (h_altura_ii , w_diametro_ii)
    Areas = (A_total_i, A_Varrida)
    Coordenadas_X = (x_1 , x_2 , x_3 , x_4)
    Coordenadas_Y = (y_1 , y_2 , y_3 , y_4)
    
    Seccao = Propriadades_Seccao_Objeto(Segundo_Momentos_De_Area , Centroide , Geometria_Media, Areas , Elasticidades, Espessuras,  Coordenadas_X,Coordenadas_Y, Peso_Por_Metro)

    return Seccao

