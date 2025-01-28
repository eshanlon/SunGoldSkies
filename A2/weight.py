# Weight Approx
import numpy as np
import math
import matplotlib.pyplot as plt

#ADDED LUIS + DIANA WORK 1/26/25
flight_t = 0.833 #[hr] ; Based on Velis electro. Refer to notes
Pbat = 90 #[kW] ; Based on Velis electro kWh * flight_t
specific_e = 0.6 #[kWh/kg]; Based on industry avg research
LD = 10 #Metabook Fig 2.4 Approx for Fixed Gear Prop Aircraft
m_batR = ((flight_t * Pbat) / specific_e) * 2.20462 #[lbs]; Eqs 2.19 Martins

R = 70 #[nmi]; RFP Design Mission Profile "Range"
v = 200#[kts]; Approx based on Diana's kts vs kmi graph, kmi of R=25knmi based on RFP Mission.

T = 371.167 #[lbf]; Check notes for solution
c = 74.23 #[1/hr]; Check notes for derivation

#Cruise - Hydrocarbon Equivalent Fuel Fractions

def weight_estimation(Wcrew, Wpayload, Wo, tolerance = 1e-6, max_interations = 100):
    g = 32.17 #ft/s^2
    iteration = 0
    iterationCount = []
    convergedWeight = []
    delta = 2*tolerance
    We_Wo = (0.74*(Wo**(-0.03)))
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
    while delta > tolerance and iteration < max_interations:
        
        New_Wo = (Wcrew + Wpayload) / (1 - We_Wo - (((m_batR * g)/ Wo) * (1 + E01_EC + E12_EC + E23_EC + E34_EC + E45_EC)))
        
        iterationCount.append(iteration)
        convergedWeight.append(New_Wo / 32.17)
        delta = (abs(New_Wo - Wo)/abs(New_Wo))
        
        Wo = New_Wo
        print(Wo)
        iteration += 1

    return iterationCount, convergedWeight

numiterations, converged_weight = weight_estimation(180 * 32.17, 2000 * 32.17, 10000 * 32.17)
converged_weight = converged_weight
plt.plot(numiterations, converged_weight, color="g", marker = "s", markersize=4, markerfacecolor="green")
plt.title('Preliminary Estimation of Takeoff Weight (W\u2080)')
plt.legend(loc='best')
plt.xlabel('# of iterations')
plt.ylabel('Preliminary Takeoff Weight [lbs]')
plt.show()
