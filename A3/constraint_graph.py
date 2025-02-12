import numpy as np
import math
import matplotlib.pyplot as plt

def density_ratio(h):
    #h = height[m]
    lamb = 0.0065 #[K/m]
    To = 288.15 #[K]
    g = 9.81 #[m/s^2]
    R = 287 #[J/kg*K]

    rho_rhoo = (1 + ((lamb * h)/ To))**(-((g/ (R * lamb)) + 1))
    return rho_rhoo
rho_rhoo = density_ratio(100)
print(rho_rhoo)

def stall_speed(rho, vstall, CLmax):
    #rho = height of crop dusting
    #v_stall = Maximum stall speed set by the far requirment. Can also set stall lower speed
    #rho = The density of desired alt
    #v_stall = Maximum stall speed set by the far requirment. Can also set stall lower speed
    #CL_max = 1.3-1.9
    W_S = np.zeros(100)
    for i in range(len(W_S)):
        W_S[i] = 1/2 * rho * (vstall**2) * CLmax
    W_P = np.linspace(1, 60, 100)
    return W_S, W_P

def takeoff_distance(rho_rhoo, CLmaxTO, W_Sref_cap, prop_eff):
    #rho_rhoo = Density ratio for alt"""
    #CLmaxTO = CL of choice
    #BFL = ? (TO SOLVE)
    #W_sref = Wing loading obtained 
    #rho = Air density of choice
    Ks = 1.2 #Estimation
    rho_sl = 0.002378 #[slugs/ft^3]
    vstall = 118.15 #[ft/s], 70 [kts], estimation
    prop_eff = prop_eff #Propeller effiency, estimation. 0.7 works.
    P_W = 0.09 #[hp/lb] Lecture 5, Slide 31
    vTO = Ks * vstall
    Wto_Sref = .5 * (rho_rhoo * rho_sl) * (vTO**2) * CLmaxTO #At runway height
    Tto_Wto = (prop_eff/vTO) * P_W
    TOP_25 = Wto_Sref / (rho_rhoo * CLmaxTO * Tto_Wto)
    BFL = 37.5 * TOP_25
    
    WTO_Sref = np.linspace(10, W_Sref_cap, 100)
    WTO_PTO = ((BFL * rho_rhoo * CLmaxTO * (prop_eff/np.sqrt((2/(rho_rhoo*rho_sl*CLmaxTO))*WTO_Sref)))/(37.5 * WTO_Sref))
    
    return WTO_Sref, WTO_PTO

def landingfield_length(rho_rhoo, CLmaxL, Sa):
    #rho = Density of desired alt
    #CL_maxL = CL during landing
    #Sa = Braking distance
    #0.7 = Maximum landing to takeoff weight ratio(needs to be changed
    TOP = 115.651 # solved for TOP by is using the equation from lecture 6 slide 34 (STO = 8.134TOP...., STO = 1000ft from at502)
    BFL = TOP * 37.5
    Sland = BFL
    W_S = np.zeros(100)
    for i in range(len(W_S)):
        W_S[i] = rho_rhoo * CLmaxL * (Sland - Sa) / (80 * 0.7)
    W_P = np.linspace(1, 60, 100)
    return W_S, W_P

def climb(AR, e, CDo, W_Sref_cap, prop_eff, rho , CLmaxCL):
    #CDo = Minimum drag coefficent
    #e = Wing efficiency ratio, .7 for rectangular wings, 1 for elliptical
    #AR = Aspect Ratio from AT502
    #rho = Freestream Air density of choice
    #prop_eff = Propeller effiency
    ks =1.3
    k = 1 / (np.pi * e * AR)
    G = 0.083 #FAR23 requiremnt
    T_W = np.zeros(100)
    WCL_PCL = np.zeros(100)
    v = np.zeros(100)
    WTO_Sref_Cl = np.linspace(10, W_Sref_cap, 100)
    for i in range(len(WTO_Sref_Cl)):
        T_W[i] = ((ks**2 * CDo)/(CLmaxCL) + (k * (CLmaxCL/ks**2)) + G)
    for i in range(len(WTO_Sref_Cl)):
        v[i] = math.sqrt((2 * WTO_Sref_Cl[i]) / (rho * CLmaxCL))
        WCL_PCL[i] = prop_eff * 550 / (T_W[i] * v[i])
    return WTO_Sref_Cl, WCL_PCL

def cruise_speed(v, CDo, e, AR, rho, prop_eff):
    #v = Velocity during cruise
    #CDo = Minimum drag coefficent
    #e = Wing efficiency ratio, .7 for rectangular wings, 1 for elliptical
    #AR = Aspect Ratio from AT502
    #rho = Air density of choice
    #prop_eff = Propeller effiency
    qcr = 0.5 * rho * (v**2)
    k = 1 / (np.pi * e * AR)
    Wc_Wto = 0.8 #weight aproximation code 
    Pto_Pc = 1.253 #0.94/.75, max engine power / typical power used during cruise
    W_P = np.zeros(100)
    P_W = np.zeros(100)
    W_S = np.linspace(1, 100, 100)
    for i in range(len(W_S)):
        P_W[i] = (((qcr * v)* (CDo + (((W_S[i]**2) * (Wc_Wto**2) * k)/(qcr**2)))) / (550 * prop_eff * W_S[i])) * (Pto_Pc)
    W_P = 1 / P_W
    return W_S, W_P

def absolute_ceiling(e, AR, CDo, rho, CLmaxCL, prop_eff):
    #e = Wing efficiency ratio, .7 for rectangular wings, 1 for elliptical
    #AR = Aspect Ratio from AT502
    #CDo = Minimum drag coefficent
    k = 1 / (np.pi * e * AR)
    W_S = np.linspace(1, 100, 100)
    T_W = np.zeros(100)
    W_P = np.zeros(100)
    v = np.zeros(100)
    for i in range(len(W_S)):
        T_W[i] = 2 * math.sqrt(k * CDo)
    for i in range(len(W_S)):
        v[i] = math.sqrt((2 * W_S[i]) / (rho * CLmaxCL))
        W_P[i] = prop_eff *550 / (T_W[i] * v[i])
    return W_S, W_P

def sustained_turn(CDo, rho, v, e, AR, R, CL, prop_eff):
    #e = Wing efficiency ratio, .7 for rectangular wings, 1 for elliptical
    #AR = Aspect Ratio from AT502
    #rho = Air density of choice
    #
    g = 32.17 #ft/s^2
    n = np.sqrt((v**2/(R * g))**2 + 1)
    k = 1 / (np.pi * e * AR)
    qst = 0.5 * rho * (v**2)
    T_W = np.zeros(100)
    W_P = np.zeros(100)
    v = np.zeros(100)
    W_S = np.linspace(1, 100, 100)
    for i in range(len(W_S)):
        T_W[i] = ((qst * CDo) * (1 / W_S[i])) + (k * (n**2 / qst) * W_S[i])
    for i in range(len(W_S)):
        v[i] = math.sqrt((2 * W_S[i]) / (rho * CL))
        W_P[i] = prop_eff *550 / (T_W[i] * v[i])
    return W_S, W_P

WTO_Sref_Cl, WCL_PCL = climb(AR = 8, e = 0.7, CDo = 0.03, W_Sref_cap = 100, prop_eff = 0.7, rho = (density_ratio(152) * 0.002378) , CLmaxCL = 1.3)
WTO_Sref_Cl2, WCL_PCL2 = climb(AR = 8, e = 0.7, CDo = 0.03, W_Sref_cap = 100, prop_eff = 0.7, rho = (density_ratio(609) * 0.002378) , CLmaxCL = 1.3)
WTO_Sref_Cl3, WCL_PCL3 = climb(AR = 8, e = 0.7, CDo = 0.03, W_Sref_cap = 100, prop_eff = 0.7, rho = (density_ratio(914) * 0.002378) , CLmaxCL = 1.3)
W_S, W_P = takeoff_distance(rho_rhoo = density_ratio(10), CLmaxTO = 1.4, W_Sref_cap = 100, prop_eff = 0.7)
W_S1, W_P1 = stall_speed(rho = 0.002377, vstall = 118.147, CLmax = 1.9)
W_S2, W_P2 = landingfield_length(rho_rhoo, CLmaxL = 1.3, Sa = 600)
W_S3, W_P3 = cruise_speed(v = 250, CDo = 0.03, e = 0.7, AR = 8, rho = 0.002242, prop_eff = 0.7)
W_S4, W_P4 = absolute_ceiling(e = 0.7, AR = 8, CDo = 0.03, rho = 0.00176, CLmaxCL = 1.2, prop_eff = 0.7) #rho = density 10000ft
W_S5, W_P5 = sustained_turn(CDo = 0.03, rho = 0.002242, v = 250, e = 0.7, AR = 8, R = 1000, CL = 1.2, prop_eff = 0.7) #rho = density 2000ft
plt.plot(WTO_Sref_Cl, WCL_PCL, color = "#FF0000", marker = "s", markersize=1, label = "Climb1 Req")
plt.plot(WTO_Sref_Cl2, WCL_PCL2, color = "#CC0000", marker = "s", markersize=1, label = "Climb2 Req")
plt.plot(WTO_Sref_Cl3, WCL_PCL3, color = "#FF9999", marker = "s", markersize=1, label = "Climb3 Req")
plt.plot(W_S, W_P, color="#FF8000", marker = "s", markersize=1, label = "Takeoff Distance Req")
plt.plot(W_S1, W_P1, color="#0080FF", marker = "s", markersize=1, label = "Stall Req")
plt.plot(W_S2, W_P2, color="#FF00FF", marker = "s", markersize=1, label = "Landingfield Length Req")
plt.plot(W_S3, W_P3, color="#80FF00", marker = "s", markersize=1, label = "Cruise Speed Req")
plt.plot(W_S4, W_P4, color="#00FFFF", marker = "s", markersize=1, label = "Ceiling Req")
plt.plot(W_S5, W_P5, color="#7F00FF", marker = "s", markersize=1, label = "Sustained Turn Req")
plt.xlim(10,100)
plt.ylim(0, 50)
plt.title('Preliminary Sizing')
plt.legend(loc='best')
plt.xlabel('W/S')
plt.ylabel('W/P')
plt.show()