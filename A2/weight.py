# Weight Approx
import numpy as np
import math
import matplotlib.pyplot as plt
def weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, prop_eff, m_fuel, P, P_DP, S, S_DP, max_interations = 500):
    iteration = 0
    g = 32.17 # ft/s^2
    R = 425328 # ft
    A = 0.74 # From table 2.1 metabook
    C = -0.03 # From table 2.1 metabook
    wing_density = 2.5 # lb/ft^2 from table 7.1 pg76
    AR = 8
    e = 0.8
    k = 1 / (np.pi * e * AR)
    #Cf = 0.006
    #CDo = Cf * ((2 * S) / S)
    # From figure 3.21a (same c_f as Cessna 180 and P-35, comparable aircraft)
    #c_f = 0.0060
    # From tables 3.4 and 3.5 (pg. 122)
    a = -2.3010 # for c_f = 0.005
    b = 1 # for all c_f values
    c = 1.0447 # for ag plane
    d = 0.5326 # for ag plane
    e = 0.82 #range 0.80 - 0.85
    # Calculating C_Do
    S_wet = 10**(c+d*math.log10(Wo))
    #print(f'S_wet is {S_wet}')
    #S_wet = S*1.25
    f = a*S_wet**b
    f = 10**(a+b*math.log10(S_wet))
    CDo = f/S
    CL = np.sqrt(CDo / k)
    LD = (0.94 * CL) / (CDo + (k * CL**2))
    err = 1e-6
    delta = 2*err
    convergedweight = []
    iterationcount = []
    v = 250 # ft/s
    n_f = .9 # percent of power used for turboprop
    n_b = 1 - n_f # percent of power used for battery
    rho50k = 0.002378 * .1522
    rho51k = 0.002378 * .1451
    rho52k = 0.002378 * .1383
    rho53k = 0.002378 * .1318
    rho54k = 0.002378 * .1256
    rho55k = 0.002378 * .1197
    rho56k = 0.002378 * .1141
    rho57k = 0.002378 * .1087
    rho58k = 0.002378 * .1036
    rho59k = 0.002378 * .09878
    rho60k = 0.002378 * .09414
    
    while delta > err and iteration < max_interations:
        W_eng = P**0.9306 * 10**(-0.1205)
        W_engDP = P_DP**0.9306 * 10**(-0.1205)
        We_Wo = A * Wo ** C
        We = We_Wo * Wo
        We = We + wing_density * (S - S_DP)
        We = We + W_eng - W_engDP
        We_Wo = We / Wo
        m_batt = (R * Wo) / (batt_eff * batt_se * LD)
        P_aircraftb = 750 * n_b# [HP]
        Tb = (P_aircraftb) * 550 / (v) # [lbf]
        cb = 0.25 * (Tb / m_batt) * (1 / 3600 * 32.17) # [1/s]
        W1 = .996 * Wo
        W2 = W1 * .998
        W3 = W2 * math.exp(-((R * cb) / (v * LD)))
        W4 = W3 * .999
        W5 = W4 * .998
        E01_EC = (1 - (W1/Wo)) * (Wo / W3)
        E12_EC = (1 - (W2/W1)) * (W1 / W3)
        E23_EC = 1 # b/c E_cruise/ E_cruise = 1
        E34_EC = (1 - (W4/W3)) * (W3 / W3)
        E45_EC = (1 - (W5/W4)) * (W4 / W3)
    
        P_aircraftf = 750 * n_f# [HP]
        Tp = (P_aircraftf) * 550 / (v) # [lbf]
        cf = 0.25 * (Tp / m_fuel) * (1 / 3600) # [1/s]
        #print(cf)
        Wtaxi_Wo = 1 - (cf * 900 * 0.05 / prop_eff * (P / Wo))
        #print(Wtaxi_Wo)
        Wtaxi = Wtaxi_Wo * Wo
        Wtakeoff_Wtaxi = 1 - (cf * 60 / prop_eff * (P / Wtaxi))
        #print(Wtakeoff_Wtaxi)
        #if W1_Wo >= 1:
            #W1_Wo = 0.998
        #prob_var = W_takeoff / P
        Wclimb_Wtakeoff = .998
        CLcruise1 = (2 * Wclimb_Wtakeoff* (Wtakeoff_Wtaxi * Wtaxi)) / (rho50k * v**2 * S)
        LDcruise1 = CLcruise1 / (CDo + k * CLcruise1**2)
        deltaR = 75000
        Wcruise1_Wclimb = math.exp(-((deltaR * cf) / (v * LDcruise1)))
        CLcruise2 = (2 * Wcruise1_Wclimb* (Wclimb_Wtakeoff * Wtakeoff_Wtaxi * Wtaxi)) / (rho50k * v**2 * S)
        LDcruise2 = CLcruise2 / (CDo + k * CLcruise2**2)
        Wcruise2_Wcruise1 = math.exp(-((deltaR * cf) / (v * LDcruise2)))
        CLcruise3 = (2 * Wcruise2_Wcruise1* (Wcruise1_Wclimb * Wclimb_Wtakeoff * Wtakeoff_Wtaxi * Wtaxi)) / (rho50k * v**2 * S)
        LDcruise3 = CLcruise3 / (CDo + k * CLcruise3**2)
        Wcruise3_Wcruise2 = math.exp(-((deltaR * cf) / (v * LDcruise3)))
        CLcruise4 = (2 * Wcruise3_Wcruise2 * (Wcruise2_Wcruise1 * Wcruise1_Wclimb * Wclimb_Wtakeoff * Wtakeoff_Wtaxi * Wtaxi)) / (rho50k * v**2 * S)
        LDcruise4 = CLcruise4 / (CDo + k * CLcruise4**2)
        Wcruise4_Wcruise3 = math.exp(-((deltaR * cf) / (v * LDcruise4)))
        Wdescent_Wcruise = .999
        Wlanding_Wdescent = .998
        New_W5_Wo = Wlanding_Wdescent * Wdescent_Wcruise * Wcruise4_Wcruise3 * Wcruise3_Wcruise2 * Wcruise2_Wcruise1 * Wcruise1_Wclimb * Wclimb_Wtakeoff * Wtakeoff_Wtaxi * Wtaxi_Wo
        W5_Wo = New_W5_Wo
        Wf_Wo = (1- W5_Wo) * 1.10
        New_Wo = (Wcrew + Wpayload) / (1 - We_Wo - ((Wf_Wo) + (((m_batt*g)/ Wo) * (1 + E01_EC + E12_EC + E23_EC + E34_EC + E45_EC))))
        delta = abs(New_Wo - Wo) / abs(New_Wo)
        Wo = New_Wo
        m_fuel = Wf_Wo * Wo
        convergedweight.append(New_Wo)
        iterationcount.append(iteration)
        iteration += 1
        print(Wo)
        
    return iterationcount, convergedweight


Wcrew = 180 # lbm * g / 32.17 lbm = lbf
Wpayload = 2000 # lbm * g / 32.17 lbm = lbf
Wo = 15000 # lbm * g / 32.17 lbm = lbf
batt_se = 23264069.84 #1204910.008 #23264069.84# ft-lbf/slug
batt_eff = 0.7
prop_eff = 0.7
m_fuel =  1000 # lbm
S_DP = 380 #ft^2
S = 600
P = 1100
P_DP = 750 #Hp
numiterations, converged_weight = weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, prop_eff, m_fuel, P, P_DP, S, S_DP)
plt.plot(numiterations, converged_weight, color="g", marker = "s", markersize=4, markerfacecolor="green")
plt.title('Preliminary Estimation of Takeoff Weight (W\u2080)')
#plt.legend(loc='best')
plt.xlabel('# of iterations')
plt.ylabel('Preliminary Takeoff Weight [lbs]')
plt.show()