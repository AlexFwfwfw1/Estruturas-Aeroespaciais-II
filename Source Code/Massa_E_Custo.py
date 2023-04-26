from Constantes import *
from math import pi

import numpy as np

NUMERO_DE_SECCOES = 10

h_altura = [0.9*(1-0.5*z/COMPRIMENTO_FUSELAGEM) for z in np.linspace(0, COMPRIMENTO_FUSELAGEM, NUMERO_DE_SECCOES)]
w_diametro = [1.5*(1-0.7*z/COMPRIMENTO_FUSELAGEM) for z in np.linspace(0, COMPRIMENTO_FUSELAGEM, NUMERO_DE_SECCOES)]

A_semicircuf_i = sum([w_diametro_i for w_diametro_i in  w_diametro])
#A_horizontal_i = A_semicircuf_i
A_vertical_i = sum([h_altura_i for h_altura_i in  h_altura])

# h_altura = array(h_altura)
# w_diametro = array(w_diametro)

Pace_Z = COMPRIMENTO_FUSELAGEM/NUMERO_DE_SECCOES

K = 4* COMPRIMENTO_FUSELAGEM
K2 =-K
K3 = pi*0.5*A_semicircuf_i* Pace_Z
K4 = 2*A_semicircuf_i* Pace_Z
K5= 2*A_vertical_i* Pace_Z

rho_Hs = 1600
rho_Hf = 1600
rho_G = 1900

Rho = ESPESSURA_CAMADA*np.array([rho_Hs,rho_Hf,rho_G])

Custo_Hc = 100
Custo_Hf = 120
Custo_G = 50

Custo = ESPESSURA_CAMADA*np.array([Custo_Hc*rho_Hs,Custo_Hf*rho_Hf,Custo_G*rho_G])

def Precalcular_Funcao_Minimo(Laminado1, Laminado2, Laminado3):
    Laminado1_Lista_K, Laminado2_Lista_K, Laminado3_Lista_K = np.sum(Laminado1,axis=1), np.sum(Laminado2,axis=1), np.sum(Laminado3,axis=1)
    
    Massa_laminado1, Massa_laminado2, Massa_laminado3 = np.inner(Laminado1_Lista_K,Rho),np.inner(Laminado2_Lista_K,Rho), np.inner(Laminado3_Lista_K,Rho)
    Custo_laminado1, Custo_laminado2, Custo_laminado3 = np.inner(Laminado1_Lista_K,Custo),np.inner(Laminado2_Lista_K,Custo), np.inner(Laminado3_Lista_K,Custo)
    return Massa_laminado1, Massa_laminado2, Massa_laminado3, Custo_laminado1, Custo_laminado2, Custo_laminado3
    
def Massa(Massa_laminado1, Massa_laminado2, Massa_laminado3, Custo_laminado1, Custo_laminado2, Custo_laminado3, Espessura):
    M_Total = Massa_laminado1*K3 + Massa_laminado2*K2*Massa_laminado1 + Massa_laminado2*K4 + K5*Massa_laminado1 + Massa_laminado3*Espessura*K
    C_Total = Custo_laminado1*K3 + Custo_laminado2*K2*Custo_laminado1 + Custo_laminado2*K4 + K5*Custo_laminado1 + Custo_laminado3*Espessura*K
    
    return M_Total*0.6 + 0.004*C_Total
    