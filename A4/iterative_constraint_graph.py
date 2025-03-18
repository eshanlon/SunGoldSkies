################## Imports and Graph Setup #########################
import math
import numpy as np
import os
import matplotlib.pyplot as plt # type: ignore
from matplotlib.lines import Line2D

#SET DEFAULT FIGURE APPERANCE
import seaborn as sns # type: ignore #Fancy plotting package
#No Background fill, legend font scale, frame on legend
sns.set(style='whitegrid', font_scale=1.5, rc={'legend.frameon': True})
#Mark ticks with border on all four sides (overrides 'whitegrid')
sns.set_style('ticks')
#ticks point in
sns.set_style({"xtick.direction": "in","ytick.direction": "in"})
#fix invisible marker bug
sns.set_context(rc={'lines.markeredgewidth': 0.1})
#restore default matplotlib colormap
mplcolors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
'#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
sns.set_palette(mplcolors)
#Get color cycle for manual colors
colors = sns.color_palette()
#SET MATPLOTLIB DEFAULTS
#(call after seaborn, which changes some defaults)
params = {
#FONT SIZES
'axes.labelsize' : 30, #Axis Labels
'axes.titlesize' : 30, #Title
'font.size' : 28, #Textbox
'xtick.labelsize': 22, #Axis tick labels
'ytick.labelsize': 22, #Axis tick labels
'legend.fontsize': 24, #Legend font size
'font.family' : 'serif',
'font.fantasy' : 'xkcd',
'font.sans-serif': 'Helvetica',
'font.monospace' : 'Courier',
#AXIS PROPERTIES
'axes.titlepad' : 2*6.0, #title spacing from axis
'axes.grid' : True, #grid on plot
'figure.figsize' : (8,8), #square plots
'savefig.bbox' : 'tight', #reduce whitespace in saved figures
#LEGEND PROPERTIES
'legend.framealpha' : 0.5,
'legend.fancybox' : True,
'legend.frameon' : True,
'legend.numpoints' : 1,
'legend.scatterpoints' : 1,
'legend.borderpad' : 0.1,
'legend.borderaxespad' : 0.1,
'legend.handletextpad' : 0.2,
'legend.handlelength' : 1.0,
'legend.labelspacing' : 0,
}
import matplotlib # type: ignore
matplotlib.rcParams.update(params) #update matplotlib defaults, call after￿
colors = sns.color_palette() #color cycle

# Code below is to import the weight estimation code from a different folder
import os
import sys
folder_path = os.path.abspath("A2") 
if folder_path not in sys.path:
    sys.path.append(folder_path)
import weight

# Importing constraint graph code
folder_path = os.path.abspath("A3") 
if folder_path not in sys.path:
    sys.path.append(folder_path)
import constraint_graph

#print(sys.path)

################ Constraint Graph Iteration #################################

# Constants for weight estimation code
Wcrew = 180 # lbm * g / 32.17 lbm = lbf
Wpayload = 4700 # lbm * g / 32.17 lbm = lbf
Wo = 10000 # lbm * g / 32.17 lbm = lbf
batt_se = 23264069.84 #1204910.008 #23264069.84# ft-lbf/slug
batt_eff = 0.7
m_fuel =  900 # lbm
S_DP = 350
S = 350
P = 800
P_DP = 800


############### For stall speed constraint #######################################
# this calculates W/P so solve S for a range of P values
# convergence tolerance
error = 1
# varibale to iterate over
P_stall_speed = np.linspace(250,1400,40)
# variable to be calculated, setting up as empty
S_stall_speed = np.empty(len(P_stall_speed))
# Initial guess
S_guess = 400
# Inputs for takeoff_distance function
CLmax = 1.9
rho = 0.002377
vstall = 130


for i in range(len(P_stall_speed)):
    converged = False
    P_o = P_stall_speed[i]
    S_stall_speed[i] = S_guess
    iteration_count = 0
    while converged == False and iteration_count < 10:
        W = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P_o, P_DP, S_stall_speed[i], S_DP, max_interations = 20)
        #W = 9000
        W_S = constraint_graph.stall_speed(rho, vstall, CLmax)
        S_new = (1/W_S)*W
        delta = abs(S_new-S_stall_speed[i])
        if delta <= error:
            converged = True
        S_stall_speed[i] = S_new
        iteration_count = iteration_count+1
        #print(f'This is iteration {iteration_count} where S = {S_stall_speed[i]}')
    #print('And now we out of the while loop')

#print(S_stall_speed)
#print(P_stall_speed)




############### For takeoff distance constraint ##################################
# takeoff does not calculate W/S so iterate over S values to calculate P
# convergence tolerance
error = 1
# varibale to iterate over
S_takeoff_distance = np.linspace(250,800,40)
# variable to be calculated, setting up as empty
P_takeoff_distance = np.empty(len(S_takeoff_distance))
# initial guess
P_guess = 400 #placeholder
# Inputs for takeoff_distance function
rho_rhoo = constraint_graph.density_ratio(10)
CLmaxTO = 2.9
rho = 0.00237

for i in range(len(S_takeoff_distance)):
    converged = False
    S_o = S_takeoff_distance[i]
    P_takeoff_distance[i] = P_guess
    iteration_count = 0
    while converged == False and iteration_count < 10:
        W = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P_takeoff_distance[i], P_DP, S_o, S_DP, max_interations = 20)
        #print(W)
        W_So = W/S_o
        # need to make the function below a function of W/S_o that outputs W_P
        W_P = constraint_graph.takeoff_distance(rho_rhoo, CLmaxTO, W_So)
        P_new = (1/W_P)*W
        delta = abs(P_new-P_takeoff_distance[i])
        if delta <= error:
            converged = True
            #if P_new > 0:
                #P_takeoff_distance[i] = P_new
        if P_new != 'nan':
            P_takeoff_distance[i] = P_new
        iteration_count = iteration_count+1
        #print(f'This is iteration {iteration_count} where P = {P_takeoff_distance[i]}')
    #print('And now we out of the while loop')



#print(P_takeoff_distance)




################ For landing distance constraint #################################
# this calculates W/P so solve S for a range of P values
# convergence tolerance
error = 1
# varibale to iterate over
P_landingfield_length = np.linspace(100,1400,40)
# variable to be calculated, setting up as empty
S_landingfield_length = np.empty(len(P_landingfield_length))
# initial guess
S_guess = 400 #placeholder
# Inputs for takeoff_distance function
rho_rhoo = constraint_graph.density_ratio(10) #actually don't know if this is right
CLmaxL = 1.8
Sa = 600
Wo = 10000 # lbm * g / 32.17 lbm = lbf

for i in range(len(P_landingfield_length)):
    converged = False
    P_o = P_landingfield_length[i]
    S_landingfield_length[i] = S_guess
    iteration_count = 1
    while converged == False and iteration_count <= 1:
        W = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P_o, P_DP, S_landingfield_length[i], S_DP, max_interations = 20)
        #W = 9000
        W_S = constraint_graph.landingfield_length(rho_rhoo, CLmaxL, Sa)
        S_new = (1/W_S)*W
        delta = abs(S_new-S_landingfield_length[i])
        if delta <= error:
            converged = True
        S_landingfield_length[i] = S_new + 250
        iteration_count = iteration_count+1
        #print(f'This is iteration {iteration_count} where S = {S_landingfield_length[i]}')
    #print('And now we out of the while loop')

#print(S_landingfield_length)

    

######################### For climb constraint 1 #########################
# climb does not calculate W/S so iterate over S values to calculate P
# convergence tolerance
error = 1
# varibale to iterate over
S_climb1 = np.linspace(250,800,40)
# variable to be calculated, setting up as empty
P_climb1 = np.empty(len(S_climb1))
# initial guess
P_guess = 300 #placeholder
# Inputs for climb1 function
AR = 8
e = 0.8
CDo = 0.0284
prop_eff = 0.7
rho = constraint_graph.density_ratio(500) * 0.002378
CLmaxCL = 2

for i in range(len(S_climb1)):
    converged = False
    S_o = S_climb1[i]
    P_climb1[i] = P_guess
    iteration_count = 0
    while converged == False and iteration_count < 10:
        W = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P_climb1[i], P_DP, S_o, S_DP, max_interations = 20)
        #W = 9000
        W_So = W/S_o
        # need to make the function below a function of W/S_o that outputs W_P
        W_P = constraint_graph.climb(AR, e, CDo, prop_eff, rho , CLmaxCL, W_So)
        P_new = (1/W_P)*W
        delta = abs(P_new-P_climb1[i])
        if delta <= error:
            converged = True
        P_climb1[i] = P_new
        iteration_count = iteration_count+1
        #print(f'This is iteration {iteration_count} where W = {W} and P = {P_climb1[i]}')
    #print('And now we out of the while loop')

#print(P_climb1)




######################### For climb constraint 2 #########################
# climb does not calculate W/S so iterate over S values to calculate P
# convergence tolerance
error = 1
# varibale to iterate over
S_climb2 = np.linspace(250,800,40)
# variable to be calculated, setting up as empty
P_climb2 = np.empty(len(S_climb2))
# initial guess
P_guess = 300 #placeholder
# Inputs for climb2 function
AR = 8
e = 0.8
CDo = 0.0284
prop_eff = 0.7
rho = constraint_graph.density_ratio(1500) * 0.002378
CLmaxCL = 2

for i in range(len(S_climb2)):
    converged = False
    S_o = S_climb2[i]
    P_climb2[i] = P_guess
    iteration_count = 0
    while converged == False and iteration_count < 10:
        W = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P_climb2[i], P_DP, S_o, S_DP, max_interations = 20)
        #W = 9000
        W_So = W/S_o
        # need to make the function below a function of W/S_o that outputs W_P
        W_P = constraint_graph.climb(AR, e, CDo, prop_eff, rho , CLmaxCL, W_So)
        P_new = (1/W_P)*W
        delta = abs(P_new-P_climb2[i])
        if delta <= error:
            converged = True
        P_climb2[i] = P_new
        iteration_count = iteration_count+1
        #print(f'This is iteration {iteration_count} where W = {W} and P = {P_climb2[i]}')
    #print('And now we out of the while loop')

#print(P_climb2)





######################### For climb constraint 3 #########################
# climb does not calculate W/S so iterate over S values to calculate P
# convergence tolerance
error = 1
# varibale to iterate over
S_climb3 = np.linspace(250,800,40)
# variable to be calculated, setting up as empty
P_climb3 = np.empty(len(S_climb3))
# initial guess
P_guess = 300 #placeholder
# Inputs for climb3 function
AR = 8
e = 0.8
CDo = 0.0284
prop_eff = 0.7
rho = constraint_graph.density_ratio(3000) * 0.002378
CLmaxCL = 2

for i in range(len(S_climb3)):
    converged = False
    S_o = S_climb3[i]
    P_climb3[i] = P_guess
    iteration_count = 0
    while converged == False and iteration_count < 10:
        W = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P_climb3[i], P_DP, S_o, S_DP, max_interations = 20)
        #W = 9000
        W_So = W/S_o
        # need to make the function below a function of W/S_o that outputs W_P
        W_P = constraint_graph.climb(AR, e, CDo, prop_eff, rho , CLmaxCL, W_So)
        P_new = (1/W_P)*W
        delta = abs(P_new-P_climb3[i])
        if delta <= error:
            converged = True
        P_climb3[i] = P_new
        iteration_count = iteration_count+1
        #print(f'This is iteration {iteration_count} where W = {W} and P = {P_climb3[i]}')
    #print('And now we out of the while loop')

#print(P_climb3)




######################## For cruise speed constraint ####################
# cruise speed does not calculate W/S so iterate over S values to calculate P
# convergence tolerance
error = 1
# varibale to iterate over
S_cruise_speed = np.linspace(250,800,40)
# variable to be calculated, setting up as empty
P_cruise_speed = np.empty(len(S_cruise_speed))
# initial guess
P_guess = 300 #placeholder
# Inputs for cruise_speed function
v = 236.319  
CDo = 0.006
e = 0.8
AR = 8
rho = 0.002242
prop_eff = 0.7

for i in range(len(S_cruise_speed)):
    converged = False
    S_o = S_cruise_speed[i]
    P_cruise_speed[i] = P_guess
    iteration_count = 0
    while converged == False and iteration_count < 10:
        W = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P_cruise_speed[i], P_DP, S_o, S_DP, max_interations = 20)
        #W = 9000
        W_So = W/S_o
        # need to make the function below a function of W/S_o that outputs W_P
        W_P = constraint_graph.cruise_speed(v, CDo, e, AR, rho, prop_eff, W_So)
        P_new = (1/W_P)*W
        delta = abs(P_new-P_cruise_speed[i])
        if delta <= error:
            converged = True
        P_cruise_speed[i] = P_new
        iteration_count = iteration_count+1
        #print(f'This is iteration {iteration_count} where W = {W} and P = {P_cruise_speed[i]}')
    #print('And now we out of the while loop')

#print(P_cruise_speed)




##################### For absolute ceiling constraint ########################
# cruise speed does not calculate W/S so iterate over S values to calculate P
# convergence tolerance
error = 1
# varibale to iterate over
S_absolute_ceiling = np.linspace(250,800,40)
# variable to be calculated, setting up as empty
P_absolute_ceiling = np.empty(len(S_absolute_ceiling))
# initial guess
P_guess = 400 #placeholder
# Inputs for absolute_ceiling function
CLmaxCL = 1.5
CDo = 0.0284
e = 0.8
AR = 8
rho = 0.00176
prop_eff = 0.7

for i in range(len(S_absolute_ceiling)):
    converged = False
    S_o = S_absolute_ceiling[i]
    P_absolute_ceiling[i] = P_guess
    iteration_count = 0
    while converged == False and iteration_count < 10:
        W = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P_absolute_ceiling[i], P_DP, S_o, S_DP, max_interations = 20)
        #W = 9000
        W_So = W/S_o
        # need to make the function below a function of W/S_o that outputs W_P
        W_P = constraint_graph.absolute_ceiling(e, AR, CDo, rho, CLmaxCL, prop_eff, W_So)
        P_new = (1/W_P)*W
        delta = abs(P_new-P_absolute_ceiling[i])
        if delta <= error:
            converged = True
        P_absolute_ceiling[i] = P_new
        iteration_count = iteration_count+1
        #print(f'This is iteration {iteration_count} where P = {P_absolute_ceiling[i]}')
    #print('And now we out of the while loop')

#print(P_absolute_ceiling)



#################### For sustained turn constraint ####################
# cruise speed does not calculate W/S so iterate over S values to calculate P
# convergence tolerance
error = 1
# varibale to iterate over
S_sustained_turn = np.linspace(250,800,40)
# variable to be calculated, setting up as empty
P_sustained_turn = np.empty(len(S_sustained_turn))
# initial guess
P_guess = 400 #placeholder
# Inputs for sustained_turn function
CDo = 0.0284
rho = 0.002242
v = 236.319 
e = 0.8
AR = 8
R = 1200
CL = 1.5
prop_eff = 0.7

for i in range(len(S_sustained_turn)):
    converged = False
    S_o = S_sustained_turn[i]
    P_sustained_turn[i] = P_guess
    iteration_count = 0
    while converged == False and iteration_count < 10:
        W = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P_sustained_turn[i], P_DP, S_o, S_DP, max_interations = 20)
        #W = 9000
        W_So = W/S_o
        # need to make the function below a function of W/S_o that outputs W_P
        W_P = constraint_graph.sustained_turn(CDo, rho, v, e, AR, R, CL, prop_eff, W_So)
        P_new = (1/W_P)*W
        delta = abs(P_new-P_sustained_turn[i])
        if delta <= error:
            converged = True
        P_sustained_turn[i] = P_new
        iteration_count = iteration_count+1
        #print(f'This is iteration {iteration_count} where P = {P_sustained_turn[i]}')
    #print('And now we out of the while loop')

#print(P_sustained_turn)



################## Comparable aircraft points ###################
#MTOW (lb)
MTOW_T510G=10500
MTOW_AT502B= 9400
MTOW_AT802A= 16000
MTOW_C188= 4200

#Wing area (m2)
wing_area_T510G= 350
wing_area_AT502B= 312
wing_area_AT802A= 401
#wing_area_C188= 205.05

#power (hp)
power_T510G= 800
power_AT502B= 750
power_AT802A= 1295
#power_C188= 300.389


# Choosing Design Point
design_S = 350
design_P = 800

####################################################################
################## Plotting ########################################
plt.plot(S_climb1, P_climb1, color = "#FF0000", marker = "s", markersize=1, label = "Climb1 Req")
plt.plot(S_climb2, P_climb2, color = "k", marker = "s", markersize=1, label = "Climb2 Req")
plt.plot(S_climb3, P_climb3, color = "#80FF00", marker = "s", markersize=1, label = "Climb3 Req")
plt.plot(S_takeoff_distance, P_takeoff_distance, color="#FF8000", marker = "s", markersize=1, label = "Takeoff Distance Req")
plt.plot(S_stall_speed, P_stall_speed, color="#0080FF", marker = "s", markersize=1, label = "Stall Req")
plt.plot(S_landingfield_length, P_landingfield_length, color="#FF00FF", marker = "s", markersize=1, label = "Landingfield Length Req")
plt.plot(S_cruise_speed, P_cruise_speed, color="brown", marker = "s", markersize=1, label = "Cruise Speed Req")
plt.plot(S_absolute_ceiling, P_absolute_ceiling, color="#00FFFF", marker = "s", markersize=1, label = "Ceiling Req")
plt.plot(S_sustained_turn, P_sustained_turn, color="#7F00FF", marker = "s", markersize=1, label = "Sustained Turn Req")
#plt.scatter(wing_area_T510G, power_T510G, label= "T510G", color='red')
#plt.scatter(wing_area_AT502B, power_AT502B, label= "AT502B", color='green')
#plt.scatter(wing_area_AT802A, power_AT802A, label= "AT802A", color='blue')
plt.scatter(design_S, design_P, label= "Design Point", color='purple', marker = '*', s = 200)
plt.xlim(240,800)
plt.ylim(200,1200)
plt.title('Constraint Graph P vs S')
plt.legend(loc='best', fontsize = 'small')
plt.xlabel('S ($ft^2$)')
plt.ylabel('P (hp)')
plt.show()


print("code ran successfully")