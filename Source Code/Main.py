from Constantes import *
import Definicao_Laminado
import Analise_Estrutural
import Materiais

import Condicoes_Iniciais

def Main():
    
    # Obter Laminado
    
    Laminado_1 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_1)
    Laminado_2 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_2)
    Laminado_3 = Definicao_Laminado.Obter_Laminado(Condicoes_Iniciais.Laminado_Lista_3)
    
    