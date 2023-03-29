from Constantes import *

Massas_De_Inercia = {"M1": {"Mass": 250, "Pos": 0.6}, "M2": {
    "Mass": 250, "Pos": 2.2}, "M3": {"Mass": 150, "Pos": COMPRIMENTO_FUSELAGEM}}


def Obter_Momento_Aerodinamico():
    Area_Alar = CORDA_MEDIA*ENVERGADURA
    M_Ca = 0.5*Velocidade_do_Aviao**2*Area_Alar * \
        CORDA_MEDIA*COEFICIENTE_DE_MOMENTO*DENSIDADE
    return M_Ca


def Obter_Peso():
    return 9.80665*MASSA_AVIAO


def Distancia_Cg_para_Ca():
    return 0.05*CORDA_MEDIA


def Distancia_Ca_para_Raiz():
    return 0.5


def Obter_Carga_de_Balanceamento():

    M_Ca = Obter_Momento_Aerodinamico()
    Peso = Obter_Peso()
    x_w = Distancia_Cg_para_Ca()
    Ca = Distancia_Ca_para_Raiz()
    Ca_para_Ponta = Ca + COMPRIMENTO_FUSELAGEM

    Fz_t = (M_Ca - Fator_de_Carga * Peso * x_w)/(Ca_para_Ponta)
    return Fz_t


Obter_Carga_de_Balanceamento()
