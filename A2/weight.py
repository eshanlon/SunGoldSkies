# Weight Approx
import numpy as np
import math
import matplotlib.pyplot as plt
def weight_estimation(Wcrew, Wpayload, Wo, batt_se, prop_eff, LD, max_interations = 20):
    iteration = 0
    g = 32.17 # ft/s^2
    R = 417420 # ft
    A = 0.74 # From table 2.1 metabook
    C = -0.03 # From table 2.1 metabook
    err = 1e-6
    delta = 2*err
    convergedweight = []
    iterationcount = []
    v = 337.562
    T = (P_aircraft * n * 550) / 
    W1 = .996 * Wo
    W2 = W1 * .998
    W3 = W2 * (math.exp(-((R * c)/(v * LD))))
    W4 = W3 * .999
    W5 = W4 * .998
    E01_EC = (1 - (W1/Wo)) * (Wo / W3)
    E12_EC = (1 - (W2/W1)) * (W1 / W3)
    E23_EC = 1 # b/c E_cruise/ E_cruise = 1
    E34_EC = (1 - (W4/W3)) * (W3 / W3)
    E45_EC = (1 - (W5/W4)) * (W4 / W3)
    while delta > err and iteration < max_interations:
        We_Wo = A * Wo ** C
        m_batt = (R * Wo) / (prop_eff * batt_se * LD)
        New_Wo = (Wcrew + Wpayload) / (1 - We_Wo - (((m_batt * g)/ Wo) * (1 + E01_EC + E12_EC + E23_EC + E34_EC + E45_EC)))
        delta = abs(New_Wo - Wo) / abs(New_Wo)
        Wo = New_Wo
        convergedweight.append(New_Wo)
        iterationcount.append(iteration)
        iteration += 1
    return iterationcount, convergedweight

Wcrew = 180 * 32.17 # lbm * g = lbf
Wpayload = 2000 * 32.17 # lbm * g = lbf
Wo = 15000 * 32.17 # lbm * g = lbf
batt_se = 722946.005 # ft-lbf/lbm
prop_eff = 0.5
LD = 10
R = 417420 # ft
numiterations, converged_weight = weight_estimation(Wcrew, Wpayload, Wo, batt_se, LD)
converged_weight = converged_weight
plt.plot(numiterations, converged_weight, color="g", marker = "s", markersize=4, markerfacecolor="green")
plt.title('Preliminary Estimation of Takeoff Weight (W\u2080)')
plt.legend(loc='best')
plt.xlabel('# of iterations')
plt.ylabel('Preliminary Takeoff Weight [lbs]')
plt.show()
#iterationcount, convergedweight = weight_estimation(Wcrew, Wpayload, Wo, batt_se, prop_eff, LD)
#plt.plot(iterationcount, convergedweight, color="g", marker = "s", markersize=4, markerfacecolor="green")
#plt.title('Preliminary Estimation of Takeoff Weight (W\u2080)')
#plt.legend(loc='best')
#plt.xlabel('# of iterations')
#plt.ylabel('Preliminary Takeoff Weight [lbs]')
#plt.show()