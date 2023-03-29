from Constants import *

K_CONSTANT = -0.5*DENSITY*WING_CHORD*C_M*AREA_ALAR
K1_CONSTANT = K_CONSTANT/(Z_W + COMPRIMENTO_L)

class Condicao_de_Voo:
    def __init__(self, Fator_de_carga, Velocidade_de_Voo):
        self.Fator_de_carga = Fator_de_carga
        self.Velocidade_de_Voo = Velocidade_de_Voo
        self.Fz_t = -K1_CONSTANT*Velocidade_de_Voo**2
        self.Sustentação_L = Fator_de_carga*PESO_PLANE_N
        self.Coeficiente_Sustentação = self.Sustentação_L / \
            (0.5*Velocidade_de_Voo**2 * DENSITY*AREA_ALAR)
        self.Angulo_de_Ataque = self.Coeficiente_Sustentação * \
            (ENVERGADURA + 2*WING_CHORD)/(0.011*math.pi**2 * ENVERGADURA)
        self.S_y = self.Fz_t*math.cos(math.radians(self.Angulo_de_Ataque))
        self.S_x = self.S_y*0.5
        self.S_z = self.Fz_t*math.sin(math.radians(self.Angulo_de_Ataque))


List_Condicoes_de_Voo = {Condicao_de_Voo(4, 45.601935), Condicao_de_Voo(
    4, 80), Condicao_de_Voo(-2, 45.601935), Condicao_de_Voo(-2, 54.584), Condicao_de_Voo(0, 80)}


# for Condicao in List_Condicoes_de_Voo:
#     print("Fz_t: " , vars(Condicao))