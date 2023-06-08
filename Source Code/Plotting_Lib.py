from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

PONTOFS = []
Ponto_X_Plot = []
Ponto_Y_Plot = []
Ponto_Z_Plot = []
A = 1

def Adiocionar_Ponto(ponto):
    PONTOFS.append(ponto)
    
def Adicionar_Coor(X,Y,Z):
    
    global Ponto_X_Plot
    global Ponto_Y_Plot
    global Ponto_Z_Plot
    
    Ponto_X_Plot.append(X)
    Ponto_Y_Plot.append(Y)
    Ponto_Z_Plot.append(Z)

def Plot():
    
    global PONTOFS
    global Ponto_X_Plot
    global Ponto_Y_Plot
    global Ponto_Z_Plot
    print(len(PONTOFS))
    print(len(Ponto_X_Plot))

    Ponto_X_Plot  = np.array(Ponto_X_Plot) 
    Ponto_Y_Plot  = np.array(Ponto_Y_Plot) 
    Ponto_Z_Plot  = np.array(Ponto_Z_Plot) 
    PONTOFS = np.array(PONTOFS)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # ax.set_proj_type('persp', focal_length=0.2)
    img = ax.scatter( Ponto_Z_Plot,Ponto_X_Plot ,Ponto_Y_Plot, c=PONTOFS, cmap="Spectral")
    fig.colorbar(img)
    plt.show()