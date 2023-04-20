from Constantes import *

Area_laminado3 = 12 * Laminado_3.Espessura

#Largura do cone
w_raiz = 1.5*(1-0.7*0/COMPRIMENTO_FUSELAGEM)
w_ponta = 1.5*(1-0.7*COMPRIMENTO_FUSELAGEM/COMPRIMENTO_FUSELAGEM)

#Posicao dos tensores na raiz
x1_raiz = -w_raiz/2-Espessura_laminado1
x2_raiz = w_raiz/2-Espessura_laminado1
x3_raiz = -w_raiz/2-Espessura_laminado1
x4_raiz = w_raiz/2-Espessura_laminado1

#Posicao dos tensores na ponta
x1_ponta = -w_ponta/2-Espessura_laminado1
x2_ponta = w_ponta/2-Espessura_laminado1
x3_ponta = -w_ponta/2-Espessura_laminado1
x4_ponta = w_ponta/2-Espessura_laminado1

#Momentos
Mx_raiz = (CARGA_EMPENAGEM_HORIZONTAL-FORCA_3)*(5.18-2.2)+(CARGA_EMPENAGEM_HORIZONTAL-FORCA_3-FORCA_2)*(2.2-0.6)+(CARGA_EMPENAGEM_HORIZONTAL-FORCA_3-FORCA_2-FORCA_1)*0.6
My_raiz = FORCA_HORIZONTAL*COMPRIMENTO_FUSELAGEM
Mx_ponta = 0
My_ponta = 0

print(w_raiz)
print(w_ponta)
print(x1_ponta,x1_raiz)