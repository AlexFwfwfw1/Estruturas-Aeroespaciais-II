class Material_Composito:
    def __init__(self, rho, E1, E2, G12, v12, Xt, Xc, Yt, Yc, S, Cost):
        self.Densidade = rho
        self.E1  = E1
        self.E2  = E2
        self.G12 = G12
        self.v12 = v12
        self.v21 = v12*E2/E1
        self.Xt  = Xt
        self.Xc  = Xc
        self.Yt  = Yt
        self.Yc  = Yc
        self.S   = S
        self.Cost = Cost


MATERIAL_CFRP_HS = Material_Composito(
    rho=1600, E1=140E9, E2=10E9, G12=5E9,
    v12=0.3,  Xt=1500E6, Xc=1200E6, Yt=50E6,
    Yc =250E6,  S =70E6, Cost=100)

MATERIAL_CFRP_HM = Material_Composito(
    rho=1600, E1=180E9, E2=8E9, G12=5E9, 
    v12=0.3,  Xt=1000E6, Xc=850E6, Yt=40E6,
    Yc =200E6,  S =120E6, Cost=120)

MATERIAL_GFRP    = Material_Composito(
    rho=1900, E1=40E9, E2=8E9, G12=4E9,
    v12=0.25, Xt=1000E6, Xc=600E6, Yt=30E6,
    Yc =110E6 , S =50E6, Cost=50)

print("Materiais Definidos")
