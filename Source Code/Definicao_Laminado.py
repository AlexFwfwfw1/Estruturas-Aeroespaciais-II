from Constantes import *
from Materiais import *
import math

import numpy as np

class Laminado_Class:
    def __init__(self,Matriz_Laminado, Matriz_K_Possibilities, Matriz_Theta_Possibilidades):
        self.Matriz_Laminado = Matriz_Laminado
        self.Obter_Laminado(Matriz_K_Possibilities,Matriz_Theta_Possibilidades)
        self.Propriadades()      
        
    def Propriadades(self):
        self.Ex = 1/(self.Espessura_Total*self.Matriz_A_Inversa[0][0])
        self.Ey = 1/(self.Espessura_Total*self.Matriz_A_Inversa[1][1])
        self.Gxy = 1/(self.Espessura_Total*self.Matriz_A_Inversa[2][2])
        self.Vxy = -self.Matriz_A_Inversa[0][1]/self.Matriz_A_Inversa[0][0]
        self.Vyx= -self.Matriz_A_Inversa[0][1]/self.Matriz_A_Inversa[1][1]
        self.Mx = -self.Matriz_A_Inversa[0][2]/self.Matriz_A_Inversa[0][0]
        self.My = - self.Matriz_A_Inversa[1][2]/self.Matriz_A_Inversa[1][1]
        
    def Escrever_Propriadades(self):
        print(f"Ex : {self.Ex}\nEy : {self.Ey}\nGxy : {self.Gxy}\nvxy : {self.Vxy}\nvyx : {self.Vyx}\nmx : {self.Mx}\nmy : {self.My}\nt_total : {self.t_total}")
        
    def Obter_Laminado(self,Matriz_K_Possibilities,Matriz_Theta_Possibilidades):

        Espessura_Camada = ESPESSURA_CAMADA
        self.Num_Camadas = np.sum(self.Matriz_Laminado)
        
        self.Espessura_Total = Espessura_Camada*self.Num_Camadas
        Shape_Lam = np.shape(self.Matriz_Laminado)
        self.Matriz_K_Laminado = np.zeros((Shape_Lam[0],Shape_Lam[1],3,3))
        
        for i in range(Shape_Lam[0]):
            for j in range(Shape_Lam[1]):
                self.Matriz_K_Laminado[i,j] = Matriz_K_Possibilities[i,j]* self.Matriz_Laminado[i,j]
        self.Matriz_A = np.sum(np.sum(self.Matriz_K_Laminado, axis = 0),axis = 0)
        self.Matriz_A = Espessura_Camada * np.array(self.Matriz_A)
        
        self.Matriz_A_Inversa = np.linalg.inv(self.Matriz_A)

        self.List_Matriz_Stress = []
        for i in range(Shape_Lam[0]):
            for j in range(Shape_Lam[1]):
                if self.Matriz_Laminado[i,j] == 0:
                    continue
                self.List_Matriz_Stress.append((self.Espessura_Total*np.matmul(Matriz_Theta_Possibilidades[i,j], np.matmul(Matriz_K_Possibilities[i,j], self.Matriz_A_Inversa)), Materials_List[j]))
                

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
    
    Matriz_Theta = np.matrix([
                [m**2,               n**2,              2*n*m],
                [n**2,               m**2,              -2*n*m],
                [-n*m,               n*m,               m-n]
                ]) 
    
    #Matriz_Theta será necessaria nos calculos para o stress.
    
    Matriz_Tensoes_12 =  np.matmul(Matriz_Rotacao_Inversa,Matriz_K)
    Matriz_K_Barra = np.matmul(Matriz_Tensoes_12, Matriz_Rotacao)
    
    return Matriz_K_Barra,Matriz_Theta
    
    
def Obter_Matriz_K_Possibilities(Possible_Angles, Possible_Materials):

    Matriz_K_Possibilities = np.zeros((len(Possible_Angles),len(Possible_Materials), 3, 3))
    Matriz_Theta_Possibilidades = np.zeros((len(Possible_Angles),len(Possible_Materials), 3, 3))
    
    for Angle in range(0,len(Possible_Angles)):
        for Material in range(0,len(Possible_Materials)):
            Matriz_K_Camada,Matriz_Theta = Obter_Matriz_K_Barra(Possible_Materials[Material], Possible_Angles[Angle])
            Matriz_K_Possibilities[Angle,Material] = Matriz_K_Camada
            Matriz_Theta_Possibilidades[Angle,Material] = Matriz_Theta
    
    return Matriz_K_Possibilities,Matriz_Theta_Possibilidades

