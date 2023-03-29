import numpy as np

def Camada_Propriadades(Camada):
    E1, E2, v12, G12, theta = Camada["E1"], Camada["E2"], Camada["v12"], Camada["G12"], Camada["theta"]
    if G12 == None and E1 == E2:
        print("G12 not found. Assuming isotropic material.")
        G12 = E1/(2+2*v12)
    v21 = v12 * E2/E1

    m = np.cos(np.radians(theta))
    n = np.sin(np.radians(theta))

    T = [
        [m**4, n**4, 2*m**2*n**2, 4*m**2*n**2],
        [n**4, m**4, 2*m**2*n**2, 4*m**2*n**2],
        [m**2*n**2, m**2*n**2, -2*m**2*n**2, (m**2-n**2)**2],
        [m**2*n**2, m**2*n**2, m**4+n**2, -4*m**2*n**2],
        [m**3*n, -m*n**3, m*n**3-m**3*n, 2*(m*n**3-m**3*n)],
        [m*n**3, -m**3*n, m**3*n-m*n**3, 2*(m**3*n-m*n**3)]
    ]

    T = np.matrix(T)
    
    K = np.matrix([E1/(1-v12*v21),
        E2/(1-v12*v21),
        E1*v21/(1-v12*v21),
        G12
    ]).T
    
    print(K)
    
    K_h = np.array(T*K)
    K_hat =np.matrix([
       [K_h[0][0], K_h[3][0], K_h[4][0]] ,
       [K_h[3][0], K_h[1][0], K_h[5][0]] ,
       [K_h[4][0], K_h[5][0], K_h[2][0]]   
    ])
    
    return K_hat

def Obter_Propriadades_Laminado(a, t):
    Ex = 1/(t*a[0][0])
    Ey = 1/(t*a[1][1])
    Gxy = 1/(t*a[2][2])
    vxy = -a[0][1]/a[0][0]
    vyx= -a[0][1]/a[1][1]
    mx = -a[0][2]/a[0][0]
    my = - a[1][2]/a[1][1]
    print(f"Ex : {Ex}\nEy : {Ey}\nGxy : {Gxy}\nvxy : {vxy}\nvyx : {vyx}\nmx : {mx}\nmy : {my}")

def Laminado(Camadas):
    A = np.zeros((3,3), dtype=np.float64)
    t_total = 0
    for Camada in Camadas:
        print(Camada)
        K_Hat = Camada_Propriadades(Camada)
        A += K_Hat*Camada["t"]
        t_total += Camada["t"]
    a = np.linalg.inv(A)
    Obter_Propriadades_Laminado(a,t_total)


Camadas = [
    {"E1": 200000,"E2": 15000,"G12": 10000,"v12": 0.3,"theta": 30, "t":0.13},
    {"E1": 140000,"E2": 10000,"G12": 5000,"v12": 0.3,"theta": 45, "t":0.13},
    {"E1": 140000,"E2": 10000,"G12": 5000,"v12": 0.3,"theta": 45, "t":0.13},
    {"E1": 200000,"E2": 15000,"G12": 10000,"v12": 0.3,"theta": 30, "t":0.13},
 
]

Laminado(Camadas)
