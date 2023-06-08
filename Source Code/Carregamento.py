from Constantes import *
from Configuration import NUMERO_DE_SECCOES
from math import pi
import numpy as np

Lift = FATOR_DE_CARGA*PESO
Coeficiente_Sustentacao = 2*Lift/(DENSIDADE*VELOCIDADE_DO_AVIAO**2*AREA_ALAR*CORDA_MEDIA)
Alpha = Coeficiente_Sustentacao*(ENVERGADURA+2*CORDA_MEDIA)/(0.011*ENVERGADURA*pi**2) - 4

#Cargas de inercia
Forca_1 = MASSA_INERCIA_1*ACELERACAO_GRAVITICA*FATOR_DE_CARGA * np.cos(Alpha)
Forca_2 = MASSA_INERCIA_2*ACELERACAO_GRAVITICA*FATOR_DE_CARGA * np.cos(Alpha)
Forca_3 = MASSA_INERCIA_3*ACELERACAO_GRAVITICA*FATOR_DE_CARGA * np.cos(Alpha)

MOMENTO_EMPENAGEM_HORIZONTAL = 0.5*DENSIDADE*VELOCIDADE_DO_AVIAO**2*AREA_ALAR*CORDA_MEDIA*COEFICIENTE_DE_MOMENTO
CARGA_EMPENAGEM_HORIZONTAL = (MOMENTO_EMPENAGEM_HORIZONTAL-FATOR_DE_CARGA*PESO*CENTRO_GRAVIDADE)/(COMPRIMENTO_FUSELAGEM-CENTRO_AERODINAMICO) * np.cos(Alpha)
FORCA_HORIZONTAL = CARGA_EMPENAGEM_HORIZONTAL/2

Delta_Z = COMPRIMENTO_FUSELAGEM/NUMERO_DE_SECCOES

#Forcas em X
ForcaX = FORCA_HORIZONTAL

Usar_Massa_Fuselagem = True
def Obter_Forcas_e_Momentos(z, Peso_Por_Metro, Peso_Cauda): 
    
    #Centroide Peso
    Peso_Cauda.append((Peso_Por_Metro*Delta_Z, (z + Delta_Z/2))) 

    Peso_Cauda_Total, Centroide_Peso_Cauda = 0, 0
    for Peso_Ponto in Peso_Cauda:
        Peso_Distribuido, C_Temp = Peso_Ponto 
        Centroide_Peso_Cauda += C_Temp*Peso_Distribuido
        Peso_Cauda_Total += Peso_Distribuido
    if Peso_Cauda_Total != 0:
        Centroide_Peso_Cauda  = Centroide_Peso_Cauda/Peso_Cauda_Total  
        Peso_Cauda_Total = Peso_Cauda_Total*FATOR_DE_CARGA *np.cos(Alpha)
    #Edge Case
    if 0 > z or z > COMPRIMENTO_FUSELAGEM:  
        raise ValueError(f"Lamento. A Seccao em z = {z} está fora dos limites da fuselagem.")  
        
    #Momentos em Y
    MomentoY = FORCA_HORIZONTAL*(COMPRIMENTO_FUSELAGEM - z)

    if not Usar_Massa_Fuselagem:
        Peso_Cauda_Total = 0
        
    #Forcas em Y
    if 0 <= z < 0.6:
        ForcaY = CARGA_EMPENAGEM_HORIZONTAL-Forca_3-Forca_2-Forca_1 - Peso_Cauda_Total
    if 0.6 <= z < 2.2:
        ForcaY = CARGA_EMPENAGEM_HORIZONTAL-Forca_3-Forca_2 - Peso_Cauda_Total
    if 2.2 <= z <= COMPRIMENTO_FUSELAGEM:
        ForcaY = CARGA_EMPENAGEM_HORIZONTAL-Forca_3 - Peso_Cauda_Total
        
    ForcaZ = ForcaY*np.tan(Alpha) #sin/cos = tan
    
    #Momentos em X
    if 0 <= z < 0.6:
        MomentoX = (CARGA_EMPENAGEM_HORIZONTAL-Forca_3)*(COMPRIMENTO_FUSELAGEM-2.2)+(CARGA_EMPENAGEM_HORIZONTAL-Forca_3-Forca_2)*(2.2-0.6)+(CARGA_EMPENAGEM_HORIZONTAL-Forca_3-Forca_2-Forca_1)*(0.6-z)- Peso_Cauda_Total*(Centroide_Peso_Cauda - z)
    if 0.6 <= z < 2.2:
        MomentoX = (CARGA_EMPENAGEM_HORIZONTAL-Forca_3)*(COMPRIMENTO_FUSELAGEM-2.2)+(CARGA_EMPENAGEM_HORIZONTAL-Forca_3-Forca_2)*(2.2-z) - Peso_Cauda_Total*(Centroide_Peso_Cauda - z) 
    if 2.2 <= z <= COMPRIMENTO_FUSELAGEM:
        MomentoX = (CARGA_EMPENAGEM_HORIZONTAL-Forca_3)*(COMPRIMENTO_FUSELAGEM-z) - Peso_Cauda_Total*(Centroide_Peso_Cauda - z)

    return (ForcaX,ForcaY,ForcaZ),(-MomentoX,-MomentoY)
