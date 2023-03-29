class Material_Composito:
    def __init__(self, rho, E1, E2, G12,v12):
        self.Densidade = rho
        self.E1 = E1
        self.E2 = E2
        self.G12 = G12
        self.v12 = v12
        self.v21 = v12*E2/E1
        
MATERIAL_CFRP_HS = Material_Composito(rho = 1600, E1 = 140E9, E2 = 10E9, G12 = 5E9, v12 = 0.3 ) 
MATERIAL_CFRP_HM = Material_Composito(rho = 1600, E1 = 180E9, E2 = 8E9 , G12 = 5E9, v12 = 0.3 ) 
MATERIAL_GFRP =    Material_Composito(rho = 1900, E1 = 40E9 , E2 = 8E9 , G12 = 4E9, v12 = 0.25)