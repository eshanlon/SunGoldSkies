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
    #E01_EC = 1 # fill in from somewhere
    #E12_EC = 1 # fill in from somewhere
    #E23_EC = 1 # fill in from somewhere
    #E34_EC = 1 # fill in from somewhere
    #E45_EC = 1 # fill in from somewhere
    #* (1 + E01_EC + E12_EC + E23_EC + E34_EC + E45_EC)))
    c = 0.02061944444 #[1/s]; Check notes for derivation
    v = 151.903 #[ft/s]; Approx based on Diana's kts vs kmi graph, kmi of R=25knmi based on RFP Mission.
    w1w0 = 0.995 #w3w1 Roskam ; Engine Start/Takeoff
    w2w1 = 0.998 #w4w3 Roskam ; Climb
    w4w3 = 0.999 #w7w5 Roskam ; Descent
    w5w4 = 0.998 #w8w7 Roskam ; Landing

    #Cruise - Hydrocarbon Equivalent Fuel Fractions

    w3w2 = math.exp(-((R * c)/(v * LD)))
    while delta > err and iteration < max_interations:
        We_Wo = A * Wo ** C
        m_batt = (R * Wo) / (prop_eff * batt_se * LD)
        New_Wo = (Wcrew + Wpayload) / (1 - We_Wo - (((m_batt * g) / Wo) + (1-(w1w0)) + ((1-w2w1)*w1w0) + ((1-w4w3)*(w3w2*w2w1*w1w0)) + ((1-w5w4)*(w4w3*w3w2*w2w1*w1w0))))
        delta = abs(New_Wo - Wo) / abs(New_Wo)
        Wo = New_Wo
        convergedweight.append(New_Wo)
        iterationcount.append(iteration)
        iteration += 1
    print(Wo)
    return iterationcount, convergedweight

Wcrew = 180 * 32.17 # lbm * g = lbf
Wpayload = 2000 * 32.17 # lbm * g = lbf
Wo = 15000 * 32.17 # lbm * g = lbf
batt_se = 722946.005 # ft-lbf/lbm
prop_eff = 0.5
LD = 10
R = 417420 # ft
#m_batt = (R * Wo) / (prop_eff * batt_se * LD)
#print(m_batt)
#A = 0.74
#C = -0.03
#g = 32.17 #ft/s^2
#We_Wo = A * Wo ** C
#print(We_Wo)
w1w0 = 0.995 #w3w1 Roskam ; Engine Start/Takeoff
w2w1 = 0.998 #w4w3 Roskam ; Climb
w4w3 = 0.999 #w7w5 Roskam ; Descent
w5w4 = 0.998 #w8w7 Roskam ; Landing
 #Cruise - Hydrocarbon Equivalent Fuel Fractions
c = 0.02061944444 #[1/s]; Check notes for derivation
v = 151.903
w3w2 = math.exp(-((R * c)/(v * LD)))
print(w3w2)
m_batt = (R * Wo) / (prop_eff * batt_se * LD)
g = 32.17 # ft/s^2
test = - (((m_batt * g) / Wo) + (1-(w1w0)) + ((1-w2w1)*w1w0) + ((1-w4w3)*(w3w2*w2w1*w1w0)) + ((1-w5w4)*(w4w3*w3w2*w2w1*w1w0)))
print(test)
#iterationcount, convergedweight = weight_estimation(Wcrew, Wpayload, Wo, batt_se, prop_eff, LD)
#plt.plot(iterationcount, convergedweight, color="g", marker = "s", markersize=4, markerfacecolor="green")
#plt.title('Preliminary Estimation of Takeoff Weight (W\u2080)')
#plt.legend(loc='best')
#plt.xlabel('# of iterations')
#plt.ylabel('Preliminary Takeoff Weight [lbs]')
#plt.show()