import numpy as np
from scipy import integrate
from Configuration import NUMERO_DE_SECCOES

def Deformacao_E_Torcao(Torcao, Deflecao, Paco_Z):
    Torcao, Deflecao = np.flip(np.array(Torcao)), np.flip(np.array(Deflecao))
    Torcao_Ponta = integrate.romb(np.array(Torcao), dx = Paco_Z, show=False)
    Deflecao_Ponta = integrate.romb(np.array(Deflecao), dx = Paco_Z, show=False)
    Deflecao_Int_Temp = [integrate.simpson(Deflecao[0:i+1], dx = Paco_Z) for i in range(NUMERO_DE_SECCOES)]
    Deflecao_Int_Metro = integrate.romb(np.array(Deflecao_Int_Temp), dx = Paco_Z, show=False) 
    
    Torcao_Ponta = np.rad2deg(np.arctan(Torcao_Ponta))
    Deflecao_Ponta = np.rad2deg(np.arctan(Deflecao_Ponta))
    return Torcao_Ponta, Deflecao_Ponta, Deflecao_Int_Metro