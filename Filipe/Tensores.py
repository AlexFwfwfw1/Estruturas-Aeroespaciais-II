from Constantes import *
import Forcas_Momentos

#Numeracao dos tensores:
# 1 2
# 3 4

#Largura do cone
w_raiz = 1.5*(1-0.7*0/COMPRIMENTO_FUSELAGEM)
w_ponta = 1.5*(1-0.7*COMPRIMENTO_FUSELAGEM/COMPRIMENTO_FUSELAGEM)

#Posicao dos tensores
x1_raiz = -

#Momentos
Mx_raiz = (CARGA_EMPENAGEM_HORIZONTAL-FORCA_3)*(5.18-2.2)+(CARGA_EMPENAGEM_HORIZONTAL-FORCA_3-FORCA_2)*(2.2-0.6)+(CARGA_EMPENAGEM_HORIZONTAL-FORCA_3-FORCA_2-FORCA_1)*0.6
My_raiz = FORCA_HORIZONTAL*COMPRIMENTO_FUSELAGEM
Mx_ponta = 0
My_ponta = 0

print(w_raiz)
print(w_ponta)
print(Mx_raiz,My_raiz,Mx_ponta,My_ponta)