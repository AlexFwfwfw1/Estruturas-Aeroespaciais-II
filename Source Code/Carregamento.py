from Constantes import *

MOMENTO_EMPENAGEM_HORIZONTAL = 0.5*DENSIDADE*VELOCIDADE_DO_AVIAO**2*AREA_ALAR*CORDA_MEDIA*COEFICIENTE_DE_MOMENTO
CARGA_EMPENAGEM_HORIZONTAL = (MOMENTO_EMPENAGEM_HORIZONTAL-FATOR_DE_CARGA*PESO*CENTRO_GRAVIDADE)/(COMPRIMENTO_FUSELAGEM-CENTRO_AERODINAMICO)
FORCA_HORIZONTAL = CARGA_EMPENAGEM_HORIZONTAL/2

#Cargas de inercia
Forca_1 = MASSA_INERCIA_1*ACELERACAO_GRAVITICA*FATOR_DE_CARGA
Forca_2 = MASSA_INERCIA_2*ACELERACAO_GRAVITICA*FATOR_DE_CARGA
Forca_3 = MASSA_INERCIA_3*ACELERACAO_GRAVITICA*FATOR_DE_CARGA


def Obter_Forcas_e_Momentos(z):
        
    #Edge Case
    if 0 > z or z > COMPRIMENTO_FUSELAGEM:  
        raise ValueError(f"Lamento. A Seccao em z = {z} está fora dos limites da fuselagem.")  
        
    #Forcas em X
    ForcaX = FORCA_HORIZONTAL
        
    #Momentos em Y
    MomentoY = FORCA_HORIZONTAL*(5.18 - z)

    #Forcas em Y
    if 0 <= z < 0.6:
        ForcaY = CARGA_EMPENAGEM_HORIZONTAL-Forca_3-Forca_2-Forca_1
    if 0.6 <= z < 2.2:
        ForcaY = CARGA_EMPENAGEM_HORIZONTAL-Forca_3-Forca_2
    if 2.2 <= z <= COMPRIMENTO_FUSELAGEM:
        ForcaY = CARGA_EMPENAGEM_HORIZONTAL-Forca_3

    #Momentos em X
    if 0 <= z < 0.6:
        MomentoX = (CARGA_EMPENAGEM_HORIZONTAL-Forca_3)*(5.18-2.2)+(CARGA_EMPENAGEM_HORIZONTAL-Forca_3-Forca_2)*(2.2-0.6)+(CARGA_EMPENAGEM_HORIZONTAL-Forca_3-Forca_2-Forca_1)*(0.6-z)
    if 0.6 <= z < 2.2:
        MomentoX = (CARGA_EMPENAGEM_HORIZONTAL-Forca_3)*(5.18-2.2)+(CARGA_EMPENAGEM_HORIZONTAL-Forca_3-Forca_2)*(2.2-z)
    if 2.2 <= z <= COMPRIMENTO_FUSELAGEM:
        MomentoX = (CARGA_EMPENAGEM_HORIZONTAL-Forca_3)*(5.18-z)

    return (ForcaX,ForcaY),(MomentoX,MomentoY)
