# Weight Approx
import numpy as np
import math
import matplotlib.pyplot as plt

#ADDED LUIS + DIANA WORK 1/26/25
flight_t = 0.833 #[hr] ; Based on Velis electro. Refer to notes
Pbat = 24 #[kW] ; Based on Velis electro kWh * flight_t
specific_e = 0.2 #[kWh/kg]; Based on industry avg research
LD = 10 #Metabook Fig 2.4 Approx for Fixed Gear Prop Aircraft
m_batR = ((flight_t * Pbat) / specific_e) * 2.20462 #[lbs]; Eqs 2.19 Martins
efficiency = 2

R = 25*6076.12  #[nmi => ft]; RFP Design Mission Profile "Range"
v = 90*1.68781 #[kts => ft/s]; Approx based on Diana's kts vs kmi graph, kmi of R=25knmi based on RFP Mission.

T = 371.167 #[lbf]; Check notes for solution
c = 74.23 #[1/hr]; Check notes for derivation

###Phases - Weight Fractions 
#MetaBook Notation
#Hydrocarbon Equivalent Fuel Fractions
w1w0 = 0.995 #w3w1 Roskam ; Engine Start/Takeoff
w2w1 = 0.998 #w4w3 Roskam ; Climb
w4w3 = 0.999 #w7w5 Roskam ; Descent
w5w4 = 0.998 #w8w7 Roskam ; Landing

g = 32.17 #ft/s^2
#Cruise - Hydrocarbon Equivalent Fuel Fractions

w3w2 = math.exp(-((R * c)/(v * LD)))
print("w3w2:", w3w2)


def weight_estimation(Wcrew, Wpayload, Wempty, Wo, w1w0, w2w1, w3w2, w4w3, w5w4, tolerance = 1e-6, max_interations = 20):
    g = 32.17 #ft/s^2
    iteration = 0
    iterationCount = []
    convergedWeight = []
    delta = 2*tolerance
    while delta > tolerance and iteration < max_interations:
        #R = prop_eff * np.exp(batt_se) * LD (m_batt / Wo)
        New_Wo = (Wcrew + Wpayload) / (1 - (0.74*(Wo**(-0.03))) - (((((25*6076.12*Wo)/(efficiency*specific_e*LD))*g)/Wo) + (1-(w1w0)) + ((1-w2w1)*w1w0) + ((1-w4w3)*(w3w2*w2w1*w1w0)) + ((1-w5w4)*(w4w3*w3w2*w2w1*w1w0))))
    
        #New_Wo = (Wcrew + Wpayload) / (1  - (.5035)- (0.74*(Wo**(-0.03))))
       
        print("Wo:", Wo)
        print("New_Wo:", New_Wo)
        
        iterationCount.append(iteration)
        convergedWeight.append(New_Wo/32.17dx)
        delta = (abs(New_Wo - Wo)/abs(New_Wo))
        print("Test")
        
            
        Wo = New_Wo
        iteration += 1

    return iterationCount, convergedWeight
    #raise ValueError("Convergence not possible with current max_iterations.")

numiterations, converged_weight = weight_estimation(180 * g, 2000 * g, 4000 * g, 7500 * g, w1w0, w2w1, w3w2, w4w3, w5w4)

plt.plot(numiterations, converged_weight, color="g", marker = "s", markersize=4, markerfacecolor="green")
plt.title('Preliminary Estimation of Takeoff Weight (W\u2080)')
plt.legend(loc='best')
plt.xlabel('# of iterations')
plt.ylabel('Preliminary Takeoff Weight [lbs]')
plt.show()