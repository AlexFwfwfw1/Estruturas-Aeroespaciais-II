from Constantes import *
import Propriadades_Seccao

# from Afilamento import *

# Lista_Px , Lista_Py = Afilamento.Obter_Forcas_Afilamento(z)


def qs_0(z, Laminado_1, Laminado_2, Laminado_3, b):
    A_i = 12
    B_i = 12

    Segundo_Momentos_De_Area, Centroide, Geometria_Media = Propriadades_Seccao.Momentos_Area(
        z, Laminado_1, Laminado_2, Laminado_3, b)

    Espessura_laminado1 = Laminado_1.Espessura
    Espessura_laminado2 = Laminado_2.Espessura
    Espessura_laminado3 = Laminado_3.Espessura
    Area_laminado3 = b * Laminado_3.Espessura

    #I_C3 = A_i/2 *  y_horizontal_i * (w_diametro_ii/2)**2 - B_i /6* (w_diametro_ii/2)**3
    #I_34 = A_i * (Espessura_laminado1 * y_horizontal_i * h_altura_ii)

    print(Segundo_Momentos_De_Area)
