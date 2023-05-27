from Constantes import *
from math import pi
import numpy as np

NUMERO_DE_SECCOES = 100

#Definir uma array com as dimensoes H e W entre 0 a COMPRIMENTO DA FUSELAGEM com tamanho de NUMERO_DE_SECCOES
h_altura = [0.9*(1-0.5*Z/COMPRIMENTO_FUSELAGEM) for Z in np.linspace(0, COMPRIMENTO_FUSELAGEM, NUMERO_DE_SECCOES)]
w_diametro = [1.5*(1-0.7*Z/COMPRIMENTO_FUSELAGEM) for Z in np.linspace(0, COMPRIMENTO_FUSELAGEM, NUMERO_DE_SECCOES)]

#PASSO DE Z, distancia entre cada seccao.
Passo_Z = COMPRIMENTO_FUSELAGEM/NUMERO_DE_SECCOES

#Rhos, bro, nem preciso de comentar isto.
rho_Hs = 1600
rho_Hf = 1600
rho_G  = 1900

Custo_Hs = 100
Custo_Hf = 120
Custo_G  = 50

Rho_Vector = np.array([rho_Hs,
                       rho_Hf,
                       rho_G])
Custo_Vector = np.array([Custo_Hs * rho_Hs,
                         Custo_Hf * rho_Hf,
                         Custo_G  * rho_G])



def Recalcular_Funcao_Minimo(Laminado1, Laminado2, Laminado3, Espessura):
    #Pegar nos laminados e somar todos as camadas com os mesmos angulos
    Laminado1_Lista_K, Laminado2_Lista_K, Laminado3_Lista_K = np.sum(Laminado1,axis=0), np.sum(Laminado2,axis=0), np.sum(Laminado3,axis=0)
    
    #Calcular N de cada laminado
    N1 = np.sum(Laminado1_Lista_K)
    N2 = np.sum(Laminado2_Lista_K)
    N3 = np.sum(Laminado3_Lista_K)
    #Calcular o rho medio de cada laminado
    Rho_1 = np.inner(Laminado1_Lista_K,Rho_Vector)/N1
    Rho_2 = np.inner(Laminado2_Lista_K,Rho_Vector)/N2
    Rho_3 = np.inner(Laminado3_Lista_K,Rho_Vector)/N3
    #Calcular o custo medio de cada laminado
    Custo_1 = np.inner(Laminado1_Lista_K,Custo_Vector)/N1
    Custo_2 = np.inner(Laminado2_Lista_K,Custo_Vector)/N2
    Custo_3 = np.inner(Laminado3_Lista_K,Custo_Vector)/N3
    #Calcular a espessura de cada laminado
    T1 = N1*ESPESSURA_CAMADA
    T2 = N2*ESPESSURA_CAMADA
    T3 = N3*ESPESSURA_CAMADA
    
    #Para cada seccao, calcular as areas respetivas, depois simplesmente soma todas as seccoes.
    #Como o processo é uma soma, podes somar em separado as barras verticais, horizontais, etc..
    #E so depois somar tudo utilizando as densidades e custo associado a cada barra
    V_Barras_Vertical  = Passo_Z*2*sum([((h_altura_i - T2/2)*T1) for h_altura_i in  h_altura])
    V_Semicirculo      = Passo_Z*sum([pi/8*(w_diametro_i**2 - (w_diametro_i - 2*T1 )**2) for w_diametro_i in w_diametro])
    V_Barra_Horizontal = Passo_Z*sum([(w_diametro_i - 2*T1)*T2 for w_diametro_i in w_diametro])
    V_Tensores         = COMPRIMENTO_FUSELAGEM*4*T3*Espessura
    
    M_Total = Rho_1*(V_Barras_Vertical + V_Semicirculo) + Rho_2*V_Barra_Horizontal + Rho_3*V_Tensores
    C_Total = Custo_1*(V_Barras_Vertical + V_Semicirculo) + Custo_2*V_Barra_Horizontal + Custo_3*V_Tensores
    
    #Funcao Minimizante
    F_min =  M_Total*0.6 + 0.4*C_Total/100
    return F_min

#######
W_Diametro_Sum = sum([w_diametro_i for w_diametro_i in  w_diametro])
#A_horizontal_i = A_semicircuf_i
H_Altura_Sum = sum([h_altura_i for h_altura_i in  h_altura])

K1 = ESPESSURA_CAMADA*Passo_Z*H_Altura_Sum + ESPESSURA_CAMADA*Passo_Z*pi*0.5*W_Diametro_Sum
K2 = ESPESSURA_CAMADA*Passo_Z*W_Diametro_Sum
K3 = ESPESSURA_CAMADA*COMPRIMENTO_FUSELAGEM

Rho = Rho_Vector
######

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


def Funcao_Minimo_Organizado(Massa_laminado1, Massa_laminado2, Massa_laminado3, Custo_laminado1, Custo_laminado2, Custo_laminado3, Espessura, Lam_1, Lam_3, Min):
    
    M_Total = Massa_laminado1[Lam_1]*K1 + Massa_laminado2*K2+ Massa_laminado3[Lam_3]*Espessura*K3
    C_Total = Custo_laminado1[Lam_1]*K1 + Custo_laminado2*K2+ Custo_laminado3[Lam_3]*Espessura*K3
    F_Min = M_Total*0.6 + 0.004*C_Total
    
    Range = np.argsort(F_Min[F_Min < Min])
    
    return Range