# Main Code for Assignment 2 Weight and Cost Estimations
import cost
import weight
import matplotlib.pyplot as plt
############## Design 1: D&L ##########################
cost.cost_analysis('A2/cost_estimate_DL.xlsx')


############## Design 2: E&K ###########################
cost.cost_analysis('A2/cost_estimate_EK.xlsx')


############## Design 3: A&C ###########################
cost.cost_analysis('A2/cost_estimate_AC.xlsx')

############## Design 1: Weight Estimation #############
Wcrew = 180 * 32.17 # lbm * g = lbf
Wpayload = 2000 * 32.17 # lbm * g = lbf
Wo = 9000 * 32.17 # lbm * g = lbf
batt_se = 1204910.008 # ft-lbf/lbm
batt_eff = 0.905
LD = 7
numiterations, converged_weight = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, LD)
plt.plot(numiterations, converged_weight, color="g", marker = "s", markersize=4, markerfacecolor="green")
plt.title('Preliminary Estimation of Takeoff Weight (W\u2080)')
plt.legend(loc='best')
plt.xlabel('# of iterations')
plt.ylabel('Preliminary Takeoff Weight [lbs]')
plt.show()

############## Design 2: Weight Estimation #############
batt_eff = 0.905
LD = 7
numiterations, converged_weight = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, LD)
plt.plot(numiterations, converged_weight, color="g", marker = "s", markersize=4, markerfacecolor="green")
plt.title('Preliminary Estimation of Takeoff Weight (W\u2080)')
plt.legend(loc='best')
plt.xlabel('# of iterations')
plt.ylabel('Preliminary Takeoff Weight [lbs]')
plt.show()

############## Design 3: Weight Estimation #############
batt_eff = 0.905
LD = 8
numiterations, converged_weight = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, LD)
plt.plot(numiterations, converged_weight, color="g", marker = "s", markersize=4, markerfacecolor="green")
plt.title('Preliminary Estimation of Takeoff Weight (W\u2080)')
plt.legend(loc='best')
plt.xlabel('# of iterations')
plt.ylabel('Preliminary Takeoff Weight [lbs]')
plt.show()