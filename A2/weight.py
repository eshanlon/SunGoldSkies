# Weight Approx
import numpy as np
import math
import matplotlib.pyplot as plt
def weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, LD, max_interations = 20):
    iteration = 0
    g = 32.17 # ft/s^2
    R = 425328 # ft
    A = 0.74 # From table 2.1 metabook
    C = -0.03 # From table 2.1 metabook
    err = 1e-6
    delta = 2*err
    convergedweight = []
    iterationcount = []
    v = 250 # ft/s
    n_f = .9 # percent of power used for turboprop
    n_b = 1 - n_f # percent of power used for battery
    while delta > err and iteration < max_interations:
        We_Wo = A * Wo ** C
        m_batt = (R * Wo) / (batt_eff * batt_se * LD)
        P_aircraft = v * (Wo / LD) # [ft-lbf/s]
        T = (P_aircraft) / (v) # [lbf]
        cb = 0.25 / 32.17 * (T / m_batt) * (1 / 3600) # [1/s]
        W1 = .996 * Wo
        W2 = W1 * .998
        W3 = W2 * math.exp(-((R * cb) / (v * LD)))
        W4 = W3 * .999
        W5 = W4 * .998
        E01_EC = (1 - (W1/Wo)) * (Wo / W3)
        E12_EC = (1 - (W2/W1)) * (W1 / W3)
        E23_EC = 1 #1 # b/c E_cruise/ E_cruise = 1
        E34_EC = (1 - (W4/W3)) * (W3 / W3)
        E45_EC = (1 - (W5/W4)) * (W4 / W3)
        W5_Wo = W5 / Wo
        while delta > err and iteration < max_interations:
            Wf_Wo = 1 - W5_Wo
            Wf = Wo * Wf_Wo
            m_fuel = Wf
            cf = 0.25 / 32.17 * (T / m_fuel) * (1 / 3600) # [1/s]
            W1_Wo = .996
            W2_W1 = .998
            W3_W2 = math.exp(-((R * cf) / (v * LD)))
            W4_W3 = .999
            W5_W4 = .998
            New_W5_Wo = W5_W4 * W4_W3 * W3_W2 * W2_W1 * W1_Wo
            delta = abs(New_W5_Wo - W5_Wo) / abs(New_W5_Wo)
            W5_Wo = New_W5_Wo
            print(W1)
        New_Wo = (Wcrew + Wpayload) / (1 - We_Wo - ((n_f * Wf_Wo) + (n_b * ((m_batt)/ Wo) * (1 + E01_EC + E12_EC + E23_EC + E34_EC + E45_EC))))
        delta = abs(New_Wo - Wo) / abs(New_Wo)
        Wo = New_Wo
        convergedweight.append(New_Wo)
        iterationcount.append(iteration)
        iteration += 1
    return iterationcount, convergedweight

Wcrew = 180 # lbm * g / 32.17 lbm = lbf
Wpayload = 2000 # lbm * g / 32.17 lbm = lbf
Wo = 15000 # lbm * g / 32.17 lbm = lbf
batt_se = 23332171.3#1204910.008 # ft-lbf/lbm
batt_eff = 0.905
LD = 8
numiterations, converged_weight = weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, LD)
plt.plot(numiterations, converged_weight, color="g", marker = "s", markersize=4, markerfacecolor="green")
plt.title('Preliminary Estimation of Takeoff Weight (W\u2080)')
plt.legend(loc='best')
plt.xlabel('# of iterations')
plt.ylabel('Preliminary Takeoff Weight [lbs]')
plt.show()