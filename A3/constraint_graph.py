
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


def takeoff_distance(rho_rhoo, CLmaxTO, W_Sref_cap, prop_eff):
    #rho_rhoo = Density ratio for alt"""

    #CLmaxTO = CL of choice
    #BFL = ? (TO SOLVE)
    #W_sref = Wing loading obtained 
    #rho = Air density of choice
    Ks = 1.1 #Estimation
    rho_sl = 0.002377 #[slugs/ft^3]
    vstall = 118.15 #[ft/s], 70 [kts], estimation
    prop_eff = prop_eff #Propeller effiency, estimation. 0.7 works.
    P_W = 0.09 #[hp/lb] Lecture 5, Slide 31
    vTO = Ks * vstall
    Tto_Wto = (prop_eff/vTO) * P_W
    Wto_Sref = .5 * (rho_rhoo * rho_sl) * (vTO**2) * CLmaxTO #At runway height
    TOP_25 = Wto_Sref / (rho_rhoo * CLmaxTO * Tto_Wto)
    BFL = 37.5 * TOP_25
    #T_W = []
    WTO_Sref = np.linspace(1, W_Sref_cap, 100)
    TTO_WTO = (37.5 / (BFL * rho_rhoo * CLmaxTO)) * WTO_Sref
    print(TTO_WTO)
    
    return WTO_Sref, TTO_WTO





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
    # Density Correction Equation. Pulled from Lecture 7 Slide 15.
    # Equation originally in [SI]. Converted to English Units.
    # h = height[ft]
    #
    #
    #
    #
    lamb = 0.00357 #[F/ft]
    To = 59 #[F]
    g = 32.19 #[ft/s^2]
    R = 14.50 #[ft*lbf/(slug*F)]


    rho_rhoo = (1 + ((lamb * h)/ To))**(-((g/ (R * lamb)) + 1))
    return rho_rhoo

#Calling and Graphing takeoff_distance() function results. 
WTO_Sref, TTO_WTO = takeoff_distance(density(52), 1.4, 50, 0.7)
plt.plot(WTO_Sref, TTO_WTO, color="g", marker = "s", markersize=1, markerfacecolor="green")
plt.title('Takeoff Distance')
plt.legend(loc='best')
plt.xlabel('W/S')
plt.ylabel('W/P')
plt.show()