Lista_de_Falhas = []
DEBUG = False
List_Of_Esforcos = ("Tensao_X", "Tensao_Y", "Compressao_X", "Compressao_Y", "Corte", "Tsai_Hill", "Hoffman")

def Resetar_Debug():
    Lista_de_Falhas = []
    
def Adiocionar_Ponto(ponto):
    Lista_de_Falhas.append(ponto)
    
def Sort_By_FS():
    Minimo,Minimo_Point = 10e100, None
    for Ponto_Falha in Lista_de_Falhas:
        if Ponto_Falha[0] < Minimo:
            Minimo = Ponto_Falha[0]
            Minimo_Point = Ponto_Falha
    return Minimo_Point

def Sort_By_Esforco(Esforco):
    
    if Esforco in List_Of_Esforcos:
        Lista_Filtrada = []
        for Ponto_Falha in Lista_de_Falhas:
            if Ponto_Falha[1] == Esforco:
                Lista_Filtrada.append(Ponto_Falha)
    elif Esforco ==  None:
        return sorted(Lista_de_Falhas, key=lambda x: x[0])[0]
    else:
        raise TypeError