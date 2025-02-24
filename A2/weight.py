# Weight Approx
import numpy as np
import math
import matplotlib.pyplot as plt
def weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, S_DP, max_interations = 20):
    iteration = 0
    Wo = np.ones(175) * Wo
    We_Wo = np.zeros(175)
    We = np.zeros(175)
    m_batt = np.zeros(175)
    m_fuel = np.ones(175) * m_fuel
    P_aircraftb = np.zeros(175)
    P_aircraftf = np.zeros(175)
    Tb = np.zeros(175)
    cb = np.zeros(175)
    Tp = np.zeros(175)
    cf = np.zeros(175)
    W1 = np.zeros(175)
    W2 = np.zeros(175)
    W3 = np.zeros(175)
    W4 = np.zeros(175)
    W5 = np.zeros(175)
    E01_EC = np.zeros(175)
    E12_EC = np.zeros(175)
    E23_EC = np.zeros(175)
    E34_EC = np.zeros(175)
    E45_EC = np.zeros(175)
    W_taxi = np.zeros(175)
    W1_Wo = np.zeros(175)
    W2_W1 = np.ones(175)
    W3_W2 = np.zeros(175)
    W4_W3 = np.ones(175)
    W5_W4 = np.ones(175)
    W5_Wo = np.zeros(175)
    Wf_Wo = np.zeros(175)
    New_Wo = np.zeros(175)
    g = 32.17 # ft/s^2
    R = 425328 # ft
    A = 0.74 # From table 2.1 metabook
    C = -0.03 # From table 2.1 metabook
    wing_density = 2.5 # lb/ft^2 from table 7.1 pg76
    AR = 8
    e = 0.8
    k = 1 / (np.pi * e * AR)
    S = np.linspace(1, 1000, 175)
    Cf = 0.002
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
    W_eng = 0
    W_engDP = 0
    while delta > err and iteration < max_interations:

        for i in range(len(S)):
            We_Wo[i] = A * Wo[i] ** C
            We[i] = We_Wo[i] * Wo[i]
            We[i] = We[i] + wing_density * (S[i] - S_DP)
            We[i] = We[i] + W_eng - W_engDP
            We_Wo[i] = We[i] / Wo[i]
            print(We_Wo)
            m_batt[i] = (R * Wo[i]) / (batt_eff * batt_se * LD)
            P_aircraftb[i] = v * (Wo[i] / LD) * n_b# [ft-lbf/s]
            Tb[i] = (P_aircraftb[i]) / (v) # [lbf]
            cb[i] = 0.25 * (Tb[i] / m_batt[i]) * (1 / 3600 * 32.17) # [1/s]
            W1[i] = .996 * Wo[i]
            W2[i] = W1[i] * .998
            W3[i] = W2[i] * math.exp(-((R * cb[i]) / (v * LD)))
            W4[i] = W3[i] * .999
            W5[i] = W4[i] * .998
            E01_EC[i] = (1 - (W1[i]/Wo[i])) * (Wo[i] / W3[i])
            E12_EC[i] = (1 - (W2[i]/W1[i])) * (W1[i] / W3[i])
            E23_EC[i] = 1 # b/c E_cruise/ E_cruise = 1
            E34_EC[i] = (1 - (W4[i]/W3[i])) * (W3[i] / W3[i])
            E45_EC[i] = (1 - (W5[i]/W4[i])) * (W4[i] / W3[i])
    
            P_aircraftf[i] = v * (Wo[i] / LD) * n_f# [ft-lbf/s]
            Tp[i] = (P_aircraftf[i]) / (v) # [lbf]
            cf[i] = 0.25 * (Tp[i] / m_fuel[i]) * (1 / 3600) # [1/s]
            W_taxi[i] = .997*W4_W3[i]#1 - c_SL
            W1_Wo[i] = .997*W4_W3[i]#1 - c_SL
            W2_W1[i] = W2_W1[i] * .998
            W3_W2[i] = math.exp(-((R * cf[i]) / (v * LD)))
            W4_W3[i] = W4_W3[i] * .999
            W5_W4[i] = W5_W4[i] * .998
            W5_Wo[i] = W5_W4[i] * W4_W3[i] * W3_W2[i] * W2_W1[i] * W1_Wo[i] * W_taxi[i]
            Wf_Wo[i] = (1- W5_Wo[i]) * 1.10

            New_Wo[i] = (Wcrew + Wpayload) / (1 - We_Wo[i] - ((Wf_Wo[i]) + (((m_batt[i]*g)/ Wo[i]) * (1 + E01_EC[i] + E12_EC[i] + E23_EC[i] + E34_EC[i] + E45_EC[i]))))
            delta[i] = abs(New_Wo[i]- Wo[i]) / abs(New_Wo[i])
            Wo[i] = New_Wo[i]
            m_fuel[i] = Wf_Wo[i] * Wo[i]
            convergedweight.append(New_Wo[i])
        iterationcount.append(iteration)
        iteration += 1
    return iterationcount, convergedweight

Wcrew = 180 # lbm * g / 32.17 lbm = lbf
Wpayload = 2000 # lbm * g / 32.17 lbm = lbf
Wo = 15000 # lbm * g / 32.17 lbm = lbf
batt_se = 23264069.84 #1204910.008 #23264069.84# ft-lbf/slug
batt_eff = 0.7
m_fuel =  1000 # lbm
S_DP = 400
numiterations, converged_weight = weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, S_DP)
plt.plot(numiterations, converged_weight, color="g", marker = "s", markersize=4, markerfacecolor="green")
plt.title('Preliminary Estimation of Takeoff Weight (W\u2080)')
plt.legend(loc='best')
plt.xlabel('# of iterations')
plt.ylabel('Preliminary Takeoff Weight [lbs]')
plt.show()