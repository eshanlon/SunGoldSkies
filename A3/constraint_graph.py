
import numpy as np
import math
import matplotlib.pyplot as plt
#CDo = 0.03

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

"""
def stall_speed(rho, vstall, CLmax):
    #rho = The density of desired alt
    #v_stall = Maximum stall speed set by the far requirment. Can also set stall lower speed
    #CL_max = 1.3-1.9
    W_Sref = 1/2 * rho * (vstall**2) * CLmax
    return W_Sref
"""

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
    Wto_Sref = .5 * (rho_rhoo * rho_sl) * (vTO**2) * CLmaxTO #At runway height
    #v = math.sqrt((2/(rho_sl*CLmaxTO))* Wto_Sref)
    Tto_Wto = (prop_eff/vTO) * P_W
    TOP_25 = Wto_Sref / (rho_rhoo * CLmaxTO * Tto_Wto)
    BFL = 37.5 * TOP_25
    
    WTO_Sref = np.linspace(10, W_Sref_cap, 100)
    WTO_PTO = ((BFL * rho_rhoo * CLmaxTO * (prop_eff/np.sqrt((2/(rho_rhoo*rho_sl*CLmaxTO))*WTO_Sref)))/(37.5 * WTO_Sref))
    
    return WTO_Sref, WTO_PTO


"""
def landingfield_length(rho_rhoo, CLmaxL, Sa, BFL):
    #rho = Density of desired alt
    #CL_maxL = CL during landing
    #Sa = Braking distance
    #0.65 = Macimum landing to takeoff weight ratio(needs to be changed)
    Sland = BFL * 0.6
    W_S = rho_rhoo * CLmaxL * (Sland - Sa) / (80 * 0.65)

    return W_S
"""
    
def climb(G, rho_rhoo, LD, W_Sref_cap, prop_eff, W_TO, vstall):
    #ks = Speed to stall speed ratio
    #CLmaxCL - CL during climb
    #CDo = Minimum drag coefficent
    #e = Wing efficieny ratio
    #AR = Aspect Ratio
    #W_sref = Wing loading obtained 
    #rho_inf = Freestream Air density of choice
    #prop_eff = Propeller effiency
    G = G #0.083, Unsure where value was obtained
    ks = 1.1
    CDo = 0.015
    e = 0.83
    AR = 7.32
    #W_TO = 13757
    rho_inf = 0.07635 #[lbm/ft^3]
    #vstall = 118.15
    k = 1 / (np.pi * e * AR)
    #T_W = []
    CLmaxCL = (2 * W_TO) / (vstall**2 * rho_inf)
    WTO_Sref_Cl = np.linspace(10, W_Sref_cap, 100)
    print("test")
    print(WTO_Sref_Cl)

    #T_W = (((ks^2) * CDo) / CLmaxCL) + ((k) * (CLmaxCL / (ks**2))) + G
    WCL_PCL = (18.97 * prop_eff * rho_rhoo * CLmaxCL) / ((G + (LD**-1)) * np.sqrt(WTO_Sref_Cl))

    #HERE I REALIZED MAYBE I CAN JUST SOLVE FOR THE CLIMB CONSTRAINT VALUES USING
    #Lecture 7 Slide 45

    

    return WTO_Sref_Cl, WCL_PCL



"""
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

"""

#Calling Climb() function
WTO_Sref_Cl, WCL_PCL = climb(0.083, density(100), 8, 50, 0.7, 13757, 118.15)

#Calling and Graphing takeoff_distance() function results. 
WTO_Sref, TTO_WTO = takeoff_distance(density(52), 1.4, 50, 0.7)
plt.plot(WTO_Sref, TTO_WTO, color="g", marker = "s", markersize=1, label = "Takeoff Distance Req")
plt.plot(WTO_Sref_Cl, WCL_PCL, color = "red", marker = "s", markersize=1, label = "Climb")
plt.title('Takeoff Distance')
plt.legend(loc='best')
plt.xlabel('W/S')
plt.ylabel('W/P')
plt.show()