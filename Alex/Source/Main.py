from Constantes import *
import Definicao_Laminado
import Analise_Estrutural
import Materiais

Laminado_Lista_1 = [
    {"Material": Materiais.MATERIAL_CFRP_HS, "Angulo_Graus": 0},
    {"Material": Materiais.MATERIAL_CFRP_HS, "Angulo_Graus": 90},
    {"Material": Materiais.MATERIAL_CFRP_HS, "Angulo_Graus": 90},
    {"Material": Materiais.MATERIAL_CFRP_HS, "Angulo_Graus": 0},
]

Laminado_Lista_2 = [
    {"Material": Materiais.MATERIAL_GFRP, "Angulo_Graus": -45},
    {"Material": Materiais.MATERIAL_GFRP, "Angulo_Graus": 45},
    {"Material": Materiais.MATERIAL_GFRP, "Angulo_Graus": 45},
    {"Material": Materiais.MATERIAL_GFRP, "Angulo_Graus": -45},
]

Laminado_Lista_3 = [
    {"Material": Materiais.MATERIAL_CFRP_HF, "Angulo_Graus": 0},
    {"Material": Materiais.MATERIAL_CFRP_HF, "Angulo_Graus": 0},
]

def Main():
    
    # Obter Laminado
    
    Laminado_1 = Definicao_Laminado.Obter_Laminado(Laminado_Lista_1)
    Laminado_2 = Definicao_Laminado.Obter_Laminado(Laminado_Lista_2)
    Laminado_3 = Definicao_Laminado.Obter_Laminado(Laminado_Lista_3)
    
    