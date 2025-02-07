import numpy as np
import math
import matplotlib.pyplot as plt
#CDo = 0.03
def stall_speed(rho, vstall, CLmax):
    #rho = The density of desired alt
    #v_stall = Maximum stall speed set by the far requirment. Can also set stall lower speed
    #CL_max = 1.3-1.9
    W_Sref = 1/2 * rho * (vstall**2) * CLmax
    return W_Sref

def takeoff_distance(rho_rhoo, CLmaxTO, W_Sref, rho, prop_eff):
    #rho_rhoo = Density ratio for alt
    #CLmaxTO = CL of choice
    #BFL = ?
    #W_sref = Wing loading obtained 
    #rho = Air density of choice
    #prop_eff = Propeller effiency
    WTO_Sref = .5 * rho * (vTO**2) *
    TOP = WTO_Sref / (rho_rhoo * CLmaxTO * TTO_WTO)
    T_W = []
    W_Sref = np.linspace(1, 300, 50)
    T_W = W_Sref * (1 / (rho_rhoo * CLmaxTO * (TOP * 37.5)))
    v = math.sqrt((2 * W_Sref) / (rho * CLmaxTO))
    W_P = prop_eff / (T_W * v)
    return W_P

def landingfield_length(rho_rhoo, CLmaxL, Sa, BFL):
    #rho = Density of desired alt
    #CL_maxL = CL during landing
    #Sa = Braking distance
    #0.65 = Macimum landing to takeoff weight ratio(needs to be changed)
    Sland = BFL * 0.6
    W_S = rho_rhoo * CLmaxL * (Sland - Sa) / (80 * 0.65)

    return W_S

def climb(ks, CLmaxCL, CDo, e, AR, W_Sref, rho, prop_eff):
    #ks = Speed to stall speed ratio
    #CLmaxCL - CL during climb
    #CDo = Minimum drag coefficent
    #e = Wing efficieny ratio
    #AR = Aspect Ratio
    #W_sref = Wing loading obtained 
    #rho = Air density of choice
    #prop_eff = Propeller effiency
    G = 0.083
    k = 1 / (np.pi * e * AR)
    T_W = []
    T_W = (1 / 0.94)((ks**2) * CDo / CLmaxCL) + (CLmaxCL * k / (ks**2)) + G
    v = math.sqrt((2 * W_Sref) / (rho * CLmaxCL))
    W_P = prop_eff / (T_W * v)
    return W_P

def cruise_speed(v, CDo, e, AR, W_Sref, CLcruise, rho, prop_eff):
    #v = Velocity during cruise
    #CDo = Minimum drag coefficent
    #e = Wing efficiency ratio
    #AR = Aspect Ratio
    #W_sref = Wing loading obtained 
    #rho = Air density of choice
    #prop_eff = Propeller effiency
    #CLcruise = CL during cruise
    qcr = 0.5 * rho * (v**2)
    k = 1 / (np.pi * e * AR)
    T_W = []
    W_S = np.linspace(1, 300, 50)
    T_w = ((qcr * CDo) * (1 / W_Sref)) + ((k / qcr) * W_Sref)
    v = math.sqrt((2 * W_Sref) / (rho * CLcruise))
    W_P = prop_eff / (T_W * v)
    return W_P

def absolute_ceiling(e, AR, CDo):
    #e = Wing efficiency ratio
    #AR = Aspect Ratio
    #CDo = Minimum drag coefficent
    T_W = 2 * math.sqrt(k * CDo)
    return T_W

def sustained_turn(q, CDo, k, n):
    #
    #
    #
    #
    T_W = []
    W_Sref = np.linspace(1, 300, 50)
    T_W = ((q * CDo) * (1 / W_Sref)) + (k(n**2/q)*W_Sref)
    return T_W

def density(h):
    #h = height[m]
    #
    #
    #
    #
    lamb = 0.0065 #[K/m]
    To = 288.15 #[K]
    g = 9.81 #[m/s^2]
    R = 287 #[J/kg*K]

    rho_rhoo = (1 + ((lamb * h)/ To))**(-((g/ (R * lamb)) + 1))
    return rho_rhoo

W_S = np.linspace(1, 500, 50)
plt.plot(, W_S, color="g", marker = "s", markersize=1, markerfacecolor="green")
plt.title('Preliminary Sizing')
plt.legend(loc='best')
plt.xlabel('W/S')
plt.ylabel('W/P')
plt.show()