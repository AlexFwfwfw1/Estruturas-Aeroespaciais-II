import Materiais
import numpy as np
import Definicao_Laminado

Angulos_Possiveis = (0, 45, -45, 90)
i_Angulos_Possiveis = len(Angulos_Possiveis)
Materiais_Possiveis = Materiais.Materials_List
j_Materiais_Possiveis = len(Materiais_Possiveis)

Matriz_K_Possbilities,Matriz_Theta_Possibilidades = Definicao_Laminado.Obter_Matriz_K_Possibilities(Angulos_Possiveis, Materiais_Possiveis)

Laminado_Lista_1 = np.array([
    [2,0,0],
    [0,0,0],
    [0,0,2],
    [1,0,0],
])

Laminado_Lista_2 = np.array([
    [2,0,0],
    [0,0,0],
    [0,0,2],
    [1,0,0],
])

Laminado_Lista_3 = np.array([
    [2,0,0]
])

Espessura_Tensor = 0