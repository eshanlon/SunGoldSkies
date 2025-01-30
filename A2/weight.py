# Weight Approx
import numpy as np
import math
import matplotlib.pyplot as plt
def weight_estimation(Wcrew, Wpayload, Wo, batt_se, prop_eff, LD, max_interations = 20):
    iteration = 0
    g = 32.17 # ft/s^2
    R = 100000 # ft
    A = 0.74 # From table 2.1 metabook
    C = -0.03 # From table 2.1 metabook
    err = 1e-6
    delta = 2*err
    convergedweight = []
    iterationcount = []
    v = 337.562 # ft/s
    while delta > err and iteration < max_interations:
        We_Wo = A * Wo ** C
        m_batt = (R * Wo) / (prop_eff * batt_se * LD)
        P_aircraft = v * (Wo / LD) # [ft-lbf/s]
        T = (P_aircraft) / (v) # [lbf]
        c = 0.25 * (T / m_batt) * (1 / 3600) # [1/s]
        W1 = .996 * Wo
        W2 = W1 * .998
        W3 = W2 * math.exp(-((R * c) / (v * LD)))
        W4 = W3 * .999
        W5 = W4 * .998
        E01_EC = (1 - (W1/Wo)) * (Wo / W3)
        E12_EC = (1 - (W2/W1)) * (W1 / W3)
        E23_EC = 1 # b/c E_cruise/ E_cruise = 1
        E34_EC = (1 - (W4/W3)) * (W3 / W3)
        E45_EC = (1 - (W5/W4)) * (W4 / W3)
        New_Wo = (Wcrew + Wpayload) / (1 - We_Wo - (((m_batt * g)/ Wo) * (1 + E01_EC + E12_EC + E23_EC + E34_EC + E45_EC)))
        delta = abs(New_Wo - Wo) / abs(New_Wo)
        Wo = New_Wo
        convergedweight.append(New_Wo / 32.17)
        iterationcount.append(iteration)
        iteration += 1
        print(New_Wo/32.17)
    return iterationcount, convergedweight

#R = 303805.7745 # ft
#v = 337.562 # ft/s
#g = 32.17 # ft/s^2
#Wcrew = 180 * 32.17 # lbm * g = lbf
#Wpayload = 2000 * 32.17 # lbm * g = lbf
#Wo = 8000 * 32.17 # lbm * g = lbf
#batt_se = 963928.0066 # ft-lbf/lbm
#prop_eff = 0.9
#LD = 50
#A = 0.74 # From table 2.1 metabook
#C = -0.03 # From table 2.1 metabook
#We_Wo = A * Wo ** C
#m_batt = (R * Wo) / (prop_eff * batt_se * LD)
#P_aircraft = v * (Wo / LD)
#T = (P_aircraft) / (v) # [lbf]
#c = 0.25 * (T / m_batt) * (1 / 3600) # [1/s]
#test = math.exp(-((R * c) / (v * LD)))
#W1 = .996 * Wo
#W2 = W1 * .998
#W3 = W2 * math.exp(-((R * c) / (v * LD)))
#W4 = W3 * .999
#W5 = W4 * .998
#E01_EC = (1 - (W1/Wo)) * (Wo / W3)
#E12_EC = (1 - (W2/W1)) * (W1 / W3)
#E23_EC = 1 # b/c E_cruise/ E_cruise = 1
#E34_EC = (1 - (W4/W3)) * (W3 / W3)
#E45_EC = (1 - (W5/W4)) * (W4 / W3)
#New_Wo = (Wcrew + Wpayload) / (1 - We_Wo - (((m_batt * g)/ Wo) * (1 + E01_EC + E12_EC + E23_EC + E34_EC + E45_EC)))
#test = - ((m_batt * g)/ Wo)
#print(m_batt)
#print(test)

Wcrew = 180 * 32.17 # lbm * g = lbf
Wpayload = 2000 * 32.17 # lbm * g = lbf
Wo = 8000 * 32.17 # lbm * g = lbf
batt_se = 1204910.008 # ft-lbf/lbm
prop_eff = 0.9
LD = 17
numiterations, converged_weight = weight_estimation(Wcrew, Wpayload, Wo, batt_se, prop_eff, LD)
converged_weight = converged_weight
plt.plot(numiterations, converged_weight, color="g", marker = "s", markersize=4, markerfacecolor="green")
plt.title('Preliminary Estimation of Takeoff Weight (W\u2080)')
plt.legend(loc='best')
plt.xlabel('# of iterations')
plt.ylabel('Preliminary Takeoff Weight [lbs]')
plt.show()