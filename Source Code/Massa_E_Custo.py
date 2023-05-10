from Constantes import *
from math import pi
import itertools
import numpy as np

NUMERO_DE_SECCOES = 50

h_altura = [0.9*(1-0.5*z/COMPRIMENTO_FUSELAGEM) for z in np.linspace(0, COMPRIMENTO_FUSELAGEM, NUMERO_DE_SECCOES)]
w_diametro = [1.5*(1-0.7*z/COMPRIMENTO_FUSELAGEM) for z in np.linspace(0, COMPRIMENTO_FUSELAGEM, NUMERO_DE_SECCOES)]

W_Diametro_Sum = sum([w_diametro_i for w_diametro_i in  w_diametro])
#A_horizontal_i = A_semicircuf_i
H_Altura_Sum = sum([h_altura_i for h_altura_i in  h_altura])

# h_altura = array(h_altura)
# w_diametro = array(w_diametro)

Pace_Z = COMPRIMENTO_FUSELAGEM/NUMERO_DE_SECCOES

K1 = ESPESSURA_CAMADA*Pace_Z*H_Altura_Sum + ESPESSURA_CAMADA*Pace_Z*pi*0.5*W_Diametro_Sum
K2 = ESPESSURA_CAMADA*Pace_Z*W_Diametro_Sum
K3 = ESPESSURA_CAMADA*COMPRIMENTO_FUSELAGEM

rho_Hs = 1600
rho_Hf = 1600
rho_G = 1900

Rho = np.array([rho_Hs,rho_Hf,rho_G])

Custo_Hs = 100
Custo_Hf = 120
Custo_G = 50

Custo_Vector = np.array([Custo_Hs*rho_Hs,Custo_Hf*rho_Hf,Custo_G*rho_G])

def Precalcular_Funcao_Minimo(Laminado1, Laminado2, Laminado3):
    Laminado1_Lista_K, Laminado2_Lista_K, Laminado3_Lista_K = np.sum(Laminado1,axis=1), np.sum(Laminado2,axis=1), np.sum(Laminado3,axis=1)
    
    Massa_laminado1, Massa_laminado2, Massa_laminado3 = np.inner(Laminado1_Lista_K,Rho),np.inner(Laminado2_Lista_K,Rho), np.inner(Laminado3_Lista_K,Rho)
    Custo_laminado1, Custo_laminado2, Custo_laminado3 = np.inner(Laminado1_Lista_K,Custo_Vector), np.inner(Laminado2_Lista_K,Custo_Vector), np.inner(Laminado3_Lista_K,Custo_Vector)
    
    return Massa_laminado1, Massa_laminado2, Massa_laminado3, Custo_laminado1, Custo_laminado2, Custo_laminado3
    
def Funcao_Minimizante(Massa_laminado1, Massa_laminado2, Massa_laminado3, Custo_laminado1, Custo_laminado2, Custo_laminado3, Espessura):
    M_Total = Massa_laminado1*K1 + Massa_laminado2*K2+ Massa_laminado3*Espessura*K3
    C_Total = Custo_laminado1*K1 + Custo_laminado2*K2+ Custo_laminado3*Espessura*K3
    
    return M_Total*0.6 + 0.004*C_Total
    
def Massa(Laminado1, Laminado2, Laminado3, Espessura):
    Laminado1_Lista_K, Laminado2_Lista_K, Laminado3_Lista_K = np.sum(Laminado1,axis=1), np.sum(Laminado2,axis=1), np.sum(Laminado3,axis=1)
    assert np.shape(Laminado1_Lista_K) == (3) 
    
    Massa_laminado1, Massa_laminado2, Massa_laminado3 = np.inner(Laminado1_Lista_K,Rho),np.inner(Laminado2_Lista_K,Rho), np.inner(Laminado3_Lista_K,Rho)
    return Massa_laminado1*K1 + Massa_laminado2*K2+ Massa_laminado3*Espessura*K3
    
def Custo(Laminado1, Laminado2, Laminado3, Espessura):
    Laminado1_Lista_K, Laminado2_Lista_K, Laminado3_Lista_K = np.sum(Laminado1,axis=1), np.sum(Laminado2,axis=1), np.sum(Laminado3,axis=1)
    Custo_laminado1, Custo_laminado2, Custo_laminado3 = np.inner(Laminado1_Lista_K,Custo_Vector),np.inner(Laminado2_Lista_K,Custo_Vector), np.inner(Laminado3_Lista_K,Custo_Vector)
    return Custo_laminado1*K1 + Custo_laminado2*K2+ Custo_laminado3*Espessura*K3

# def Calcular_Em_Paralelo_FMin()

def Recalcular_Funcao_Minimo(Laminado1, Laminado2, Laminado3, Espessura):
    Laminado1_Lista_K, Laminado2_Lista_K, Laminado3_Lista_K = np.sum(Laminado1,axis=0), np.sum(Laminado2,axis=0), np.sum(Laminado3,axis=0)
    
    Rho = np.array([rho_Hs,rho_Hf,rho_G])
    Custo_Vector = np.array([Custo_Hs*rho_Hs,Custo_Hf*rho_Hf,Custo_G*rho_G])
    
    N1, N2, N3 = np.sum(Laminado1_Lista_K), np.sum(Laminado2_Lista_K), np.sum(Laminado3_Lista_K)
    Rho_1, Rho_2, Rho_3 = np.inner(Laminado1_Lista_K,Rho)/N1,np.inner(Laminado2_Lista_K,Rho)/N2, np.inner(Laminado3_Lista_K,Rho)/N3
    Custo_1, Custo_2, Custo_3 = np.inner(Laminado1_Lista_K,Custo_Vector)/N1, np.inner(Laminado2_Lista_K,Custo_Vector)/N2, np.inner(Laminado3_Lista_K,Custo_Vector)/N3
    
    Espessura_laminado1 = N1*ESPESSURA_CAMADA
    Espessura_laminado2 = N2*ESPESSURA_CAMADA
    Espessura_laminado3 = N3*ESPESSURA_CAMADA
    
    A_v = Pace_Z*2*sum([(h_altura_i*Espessura_laminado1) for h_altura_i in  h_altura])
    A_sc = Pace_Z*sum([pi/8*(w_diametro_i*w_diametro_i-(w_diametro_i - 2*Espessura_laminado1 )*(w_diametro_i - 2*Espessura_laminado1 )) for w_diametro_i in w_diametro])
    A_h = Pace_Z*sum([(w_diametro_i - 2*Espessura_laminado1)*Espessura_laminado2 for w_diametro_i in w_diametro])
    A_t = COMPRIMENTO_FUSELAGEM*4*Espessura_laminado3*Espessura
    
    M_Total = Rho_1*(A_v + A_sc) + Rho_2*A_h + Rho_3*Espessura*A_t
    C_Total = Custo_1*(A_v + A_sc) + Custo_2*A_h + Custo_3*Espessura*A_t
    
    return M_Total*0.6 + 0.4*C_Total/100

def Funcao_Minimo_Organizado(Massa_laminado1, Massa_laminado2, Massa_laminado3, Custo_laminado1, Custo_laminado2, Custo_laminado3, Espessura, Lam_1, Lam_3, Min):
    
    M_Total = Massa_laminado1[Lam_1]*K1 + Massa_laminado2*K2+ Massa_laminado3[Lam_3]*Espessura*K3
    C_Total = Custo_laminado1[Lam_1]*K1 + Custo_laminado2*K2+ Custo_laminado3[Lam_3]*Espessura*K3
    F_Min = M_Total*0.6 + 0.004*C_Total
    
    Range = np.argsort(F_Min[F_Min < Min])
    
    return Range