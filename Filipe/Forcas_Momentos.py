from Constantes import *

def Obter_Forcas(z):
    #Forcas em X
    if 0 <= z <= COMPRIMENTO_FUSELAGEM:
        forcaX = FORCA_HORIZONTAL

    #Forcas em Y
    if 0 <= z < 0.6:
        forcaY = CARGA_EMPENAGEM_HORIZONTAL-FORCA_3-FORCA_2-FORCA_1
    if 0.6 <= z < 2.2:
        forcaY = CARGA_EMPENAGEM_HORIZONTAL-FORCA_3-FORCA_2
    if 2.2 <= z <= COMPRIMENTO_FUSELAGEM:
        forcaY = CARGA_EMPENAGEM_HORIZONTAL-FORCA_3

    #Momentos em X
    if 0 <= z < 0.6:
        momentoX = (CARGA_EMPENAGEM_HORIZONTAL-FORCA_3)*(5.18-2.2)+(CARGA_EMPENAGEM_HORIZONTAL-FORCA_3-FORCA_2)*(2.2-0.6)+(CARGA_EMPENAGEM_HORIZONTAL-FORCA_3-FORCA_2-FORCA_1)*(0.6-z)
    if 0.6 <= z < 2.2:
        momentoX = (CARGA_EMPENAGEM_HORIZONTAL-FORCA_3)*(5.18-2.2)+(CARGA_EMPENAGEM_HORIZONTAL-FORCA_3-FORCA_2)*(2.2-z)
    if 2.2 <= z <= COMPRIMENTO_FUSELAGEM:
        momentoX = (CARGA_EMPENAGEM_HORIZONTAL-FORCA_3)*(5.18-z)

    #Momentos em Y
    if 0 <= z <= COMPRIMENTO_FUSELAGEM:
        momentoY = FORCA_HORIZONTAL*(COMPRIMENTO_FUSELAGEM-z)

    return forcaX,forcaY,momentoX,momentoY

print(Obter_Forcas(5.18))