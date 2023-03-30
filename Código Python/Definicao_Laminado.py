from Constantes import *
from Materiais import *
import math

import numpy as np

class Laminado_Class:
    def __init__(self, Ex, Ey, Gxy, Vxy, Vyx, Mx, My):
        self.Ex = Ex
        self.Ey = Ey
        self.Gxy = Gxy
        self.Vxy = Vxy
        self.Vyx = Vyx
        self.Mx = Mx
        self.My = My
    def Escrever_Propriadades(self):
        print(f"Ex : {self.Ex}\nEy : {self.Ey}\nGxy : {self.Gxy}\nvxy : {self.Vxy}\nvyx : {self.Vyx}\nmx : {self.Mx}\nmy : {self.My}")
        

def Obter_Matriz_K_Barra(Material, angulo):
    
    angulo = math.radians(angulo)
    
    m = np.cos(angulo)
    n = np.sin(angulo)
    
    K11 = Material.E1/(1-Material.v12*Material.v21)
    K22 = Material.E2/(1-Material.v12*Material.v21)
    K12 = K11*Material.v21
    K33 = Material.G12
    
    Vetor_K = np.array([K11,K22,K12,K33])
    Matriz_K = np.matrix([
        [K11, K12, 0],
        [K12, K22, 0],
        [0, 0, K33]
    ])
    
    Matriz_Rotacao = np.matrix([
        [m**2, n**2, m*n],
        [n**2, m**2, -m*n],
        [-2*m*n, 2*m*n, m**2-n**2]
    ])
    
    Matriz_Rotacao_Inversa = np.matrix([
        [m**2, n**2, -2*m*n],
        [n**2, m**2, 2*m*n],
        [m*n, -m*n, m**2-n**2]
    ])
    
    Matriz_Tensoes_12 =  np.matmul(Matriz_Rotacao_Inversa,Matriz_K)
    Matriz_K_Barra = np.matmul(Matriz_Tensoes_12, Matriz_Rotacao)
    
    return Matriz_K_Barra

def Obter_Propriadades_Equivalentes_Lamindado(Matriz_A, Espessura_Total):
    
    Ex = 1/(Espessura_Total*Matriz_A[0][0])
    Ey = 1/(Espessura_Total*Matriz_A[1][1])
    Gxy = 1/(Espessura_Total*Matriz_A[2][2])
    Vxy = -Matriz_A[0][1]/Matriz_A[0][0]
    Vyx= -Matriz_A[0][1]/Matriz_A[1][1]
    Mx = -Matriz_A[0][2]/Matriz_A[0][0]
    My = - Matriz_A[1][2]/Matriz_A[1][1]
    
    return Laminado_Class(Ex, Ey, Gxy, Vxy, Vyx, Mx, My)

def Obter_Laminado(Laminado_Lista):

    Espessura_Camada = ESPESSURA_CAMADA
    Matriz_A = np.zeros((3,3))
    Espessura_Total = Espessura_Camada*len(Laminado_Lista)
    
    ### CONSEGUIR MATRIZ A
    
    for Camada in Laminado_Lista:
        Matriz_K_Camada = Obter_Matriz_K_Barra(Camada["Material"], Camada["Angulo_Graus"])
        Matriz_A = Matriz_A + Matriz_K_Camada
        
    Matriz_A = np.array( Matriz_K_Camada * Matriz_A)
    
    Matriz_A_Inversa = np.linalg.inv(Matriz_A)
        
    Laminado_Objeto = Obter_Propriadades_Equivalentes_Lamindado(Matriz_A_Inversa, Espessura_Total)
    
    return Laminado_Objeto
    
Laminado_Lista = [
    {"Material": MATERIAL_CFRP_HS, "Angulo_Graus": 0}
]

print(Obter_Matriz_K_Barra(MATERIAL_CFRP_HS,0))

Laminado = Obter_Laminado(Laminado_Lista)
Laminado.Escrever_Propriadades()