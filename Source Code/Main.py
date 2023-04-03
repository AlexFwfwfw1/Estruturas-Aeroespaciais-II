from Constantes import *
import Definicao_Laminado

import qs_0

import Condicoes_Iniciais

def Main():
    
    # Obter Laminado
    
    Seccao_Z = 0
    b = 0.001
    
    Laminado_1 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_1)
    Laminado_2 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_2)
    Laminado_3 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_3)
    
    Q = qs_0.qs_0(Seccao_Z, Laminado_1, Laminado_2, Laminado_3, b)
    
Main()