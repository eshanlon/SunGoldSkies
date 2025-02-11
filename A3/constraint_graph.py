import numpy as np
import math
import matplotlib.pyplot as plt
CDo = 0.03
def density_ratio(h):
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
rho_rhoo = density_ratio(1)
def stall_speed(rho, vstall, CLmax):
    #rho = The density of desired alt
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

def landingfield_length(rho_rhoo, CLmaxL, Sa, prop_eff, vstall, rho):
    #rho = Density of desired alt
    #CL_maxL = CL during landing
    #Sa = Braking distance
    #0.65 = Macimum landing to takeoff weight ratio(needs to be changed
    #ks = 1.2
    #vL = ks * vstall
    #P_W = 0.09 # From historical data
    #TL_WL = (prop_eff / vL) * P_W
    #WL_Sref = .5 * rho * (vL**2) * CLmaxL
    TOP = 103.268 #WL_Sref / (rho_rhoo * CLmaxL * TL_WL)
    BFL = TOP * 37.5
    print(BFL)
    Sland = BFL
    W_S = np.zeros(100)
    for i in range(len(W_S)):
        W_S[i] = rho_rhoo * CLmaxL * (Sland - Sa) / (80 * 0.65)
    W_P = np.linspace(1, 60, 100)
    return W_S, W_P

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
    #print("test")
    #print(WTO_Sref_Cl)
        #T_W = (((ks^2) * CDo) / CLmaxCL) + ((k) * (CLmaxCL / (ks**2))) + G
    WCL_PCL = (18.97 * prop_eff * rho_rhoo * np.sqrt(CLmaxCL)) / ((G + (LD**-1)) * np.sqrt(WTO_Sref_Cl))

    #HERE I REALIZED MAYBE I CAN JUST SOLVE FOR THE CLIMB CONSTRAINT VALUES USING
    #Lecture 7 Slide 45

    

    return WTO_Sref_Cl, WCL_PCL

def cruise_speed(v, CDo, e, AR, CLcruise, rho, prop_eff):
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
    #T_W = np.zeros(100)
    Wc_Wto = 0.9
    Pto_Pc = 1.175
    W_P = np.zeros(100)
    P_W = np.zeros(100)
    W_S = np.linspace(1, 100, 100)
    for i in range(len(W_S)):
        P_W[i] = (((qcr * v)* (CDo + (((W_S[i]**2) * (Wc_Wto**2) * k)/(qcr**2)))) / (550 * prop_eff * W_S[i])) * (Pto_Pc)
        #] = ((qcr * CDo) * (1 / W_S[i])) + ((k / qcr) * W_S[i])
    W_P = 1 / P_W
    #for i in range(len(W_S)):
        #v[i] = math.sqrt((2 * W_S[i]) / (rho * CLcruise))
        #W_P[i] = prop_eff / (T_W[i] * v[i])
    return W_S, W_P

def absolute_ceiling(e, AR, CDo, rho, CLmaxCL, prop_eff):
    #e = Wing efficiency ratio
    #AR = Aspect Ratio
    #CDo = Minimum drag coefficent
    k = 1 / (np.pi * e * AR)
    W_S = np.linspace(1, 100, 100)
    T_W = np.zeros(100)
    W_P = np.zeros(100)
    v = np.zeros(100)
    for i in range(len(W_S)):
        T_W[i] = 2 * math.sqrt(k * CDo)
    print(T_W)
    for i in range(len(W_S)):
        v[i] = math.sqrt((2 * W_S[i]) / (rho * CLmaxCL))
        W_P[i] = prop_eff *550 / (T_W[i] * v[i])
    return W_S, W_P

def sustained_turn(CDo, rho, v, e, AR, n, CL, prop_eff):
    #
    #
    #
    #
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
        print(v)
        W_P[i] = prop_eff *550 / (T_W[i] * v[i])
    return W_S, W_P

WTO_Sref_Cl, WCL_PCL = climb(0.083, density_ratio(30), 8, 100, 0.7, 13757, 118.15)
#W_P, W_S = takeoff_distance(rho_rhoo, vstall = 101.269, CLmaxTO = 1.2, rho = 0.002377, prop_eff = 0.7)
W_S1, W_P1 = stall_speed(rho = 0.002377, vstall = 120.269, CLmax = 2.5)
W_S2, W_P2 = landingfield_length(rho_rhoo, CLmaxL = 1.3, Sa = 600, prop_eff = 0.7, vstall = 101.269, rho = 0.002377)
W_S3, W_P3 = cruise_speed(v = 250, CDo = 0.03, e = 0.8, AR = 8, CLcruise = 1.2, rho = 0.002377, prop_eff = 0.7)
W_S4, W_P4 = absolute_ceiling(e = 0.8, AR = 8, CDo = 0.03, rho = 0.002377, CLmaxCL = 1.2, prop_eff = 0.7)
W_S5, W_P5 = sustained_turn(CDo = 0.03, rho = 0.002377, v = 250, e = 0.8, AR = 8, n = .5, CL = 1.2, prop_eff = 0.7)
WTO_Sref, TTO_WTO = takeoff_distance(density_ratio(15), 1.4, 100, 0.7)
plt.plot(WTO_Sref, TTO_WTO, color="g", marker = "s", markersize=1, label = "Takeoff Distance Req")
#print(WCL_PCL)
plt.plot(WTO_Sref_Cl, WCL_PCL, color = "red", marker = "s", markersize=1, label = "Climb")
#plt.plot(W_S, W_P, color="g", marker = "s", markersize=1, markerfacecolor="green")
plt.plot(W_S1, W_P1, color="r", marker = "s", markersize=1, markerfacecolor="red")
plt.plot(W_S2, W_P2, color="b", marker = "s", markersize=1, markerfacecolor="red")
plt.plot(W_S3, W_P3, color="g", marker = "s", markersize=1, markerfacecolor="red")
plt.plot(W_S4, W_P4, color="r", marker = "s", markersize=1, markerfacecolor="red")
plt.plot(W_S5, W_P5, color="b", marker = "s", markersize=1, markerfacecolor="red")
plt.xlim(10,90)
plt.ylim(0, 100)
plt.title('Preliminary Sizing')
plt.legend(loc='best')
plt.xlabel('W/S')
plt.ylabel('W/P')
plt.show()