# Weight Approx
import numpy as np
import math
import matplotlib.pyplot as plt
def weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P, P_DP, S, S_DP, max_interations = 100):
    iteration = 0
    g = 32.17 # ft/s^2
    R = 425328 # ft
    A = 0.74 # From table 2.1 metabook
    C = -0.03 # From table 2.1 metabook
    wing_density = 2.5 # lb/ft^2 from table 7.1 pg76
    AR = 8
    e = 0.8
    k = 1 / (np.pi * e * AR)
    Cf = 0.006
    CDo = Cf * ((2 * S) / S)
    CL = np.sqrt(CDo / k)
    LD = (0.94 * CL) / (CDo + (k * CL**2))
    err = 1e-6
    delta = 2*err
    convergedweight = []
    iterationcount = []
    v = 250 # ft/s
    n_f = .9 # percent of power used for turboprop
    n_b = 1 - n_f # percent of power used for battery
    
    while delta > err and iteration < max_interations:
        W_eng = P**0.9306 * 10**(-0.1205)
        W_engDP = P_DP**0.9306 * 10**(-0.1205)
        We_Wo = A * Wo ** C
        We = We_Wo * Wo
        We = We + wing_density * (S - S_DP)
        We = We + W_eng - W_engDP
        We_Wo = We / Wo
        m_batt = (R * Wo) / (batt_eff * batt_se * LD)
        P_aircraftb = v * (Wo / LD) * n_b# [ft-lbf/s]
        Tb = (P_aircraftb) / (v) # [lbf]
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
    
        P_aircraftf = v * (Wo / LD) * n_f# [ft-lbf/s]
        Tp = (P_aircraftf) / (v) # [lbf]
        cf = 0.25 * (Tp / m_fuel) * (1 / 3600) # [1/s]
        W_taxi = 1 - (cf * 900 * 0.05 * (Wo / P))
        W_takeoff = W_taxi * Wo
        W1_Wo = 1 - (cf * 60 * (W_takeoff / P))
        #if W1_Wo >= 1:
            #W1_Wo = 0.998
        #prob_var = W_takeoff / P
        W2_W1 = .998
        W3_W2 = math.exp(-((R * cf) / (v * LD)))
        W4_W3 = .999
        W5_W4 = .998
        New_W5_Wo = W5_W4 * W4_W3 * W3_W2 * W2_W1 * W1_Wo * W_taxi
        W5_Wo = New_W5_Wo
        Wf_Wo = (1- W5_Wo) * 1.10
        New_Wo = (Wcrew + Wpayload) / (1 - We_Wo - ((Wf_Wo) + (((m_batt*g)/ Wo) * (1 + E01_EC + E12_EC + E23_EC + E34_EC + E45_EC))))
        delta = abs(New_Wo - Wo) / abs(New_Wo)
        Wo = New_Wo
        m_fuel = Wf_Wo * Wo
        convergedweight.append(New_Wo)
        iterationcount.append(iteration)
        iteration += 1
    return convergedweight[-1]

'''
Wcrew = 180 # lbm * g / 32.17 lbm = lbf
Wpayload = 2000 # lbm * g / 32.17 lbm = lbf
Wo = 15000 # lbm * g / 32.17 lbm = lbf
batt_se = 23264069.84 #1204910.008 #23264069.84# ft-lbf/slug
batt_eff = 0.7
m_fuel =  1000 # lbm
S_DP = 400
S = 600
P = 1100
P_DP = 1333.33
numiterations, converged_weight, finalweight = weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P, P_DP, S, S_DP)
plt.plot(numiterations, converged_weight, color="g", marker = "s", markersize=4, markerfacecolor="green")
plt.title('Preliminary Estimation of Takeoff Weight (W\u2080)')
#plt.legend(loc='best')
plt.xlabel('# of iterations')
plt.ylabel('Preliminary Takeoff Weight [lbs]')
plt.show()
print(f'The converged weight is {finalweight}')
'''
