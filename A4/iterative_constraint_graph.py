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



################ Constraint Graph Iteration #################################

# Constants for weight estimation code
Wcrew = 180 # lbm * g / 32.17 lbm = lbf
Wpayload = 2000 # lbm * g / 32.17 lbm = lbf
Wo = 15000 # lbm * g / 32.17 lbm = lbf
batt_se = 23264069.84 #1204910.008 #23264069.84# ft-lbf/slug
batt_eff = 0.7
m_fuel =  1000 # lbm
S_DP = 400
#S = 600
#P = 1100
P_DP = 1333.33


############### For stall speed constraint #######################################
# this calculates W_S, stall_speed function does not depend on S or P, so no iterations
# convergence tolerance
error = 1
# varibale to iterate over
P_stall_speed = np.linspace(200,400,10)
# variable to be calculated, setting up as empty
S_stall_speed = np.empty(len(P_stall_speed))
# Inputs for takeoff_distance function
CLmax = 1.8
rho = 0.002377
vstall = 118.47

'''
for i in range(len(P_stall_speed)):
    W = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P_stall_speed[i], P_DP, S_stall_speed[i], S_DP, max_interations = 20)
    W_S = constraint_graph.stall_speed(rho, vstall, CLmax)
    S_new = (1/W_S)*W
    S_stall_speed[i] = S_new
        
        #print(f'This is iteration {iteration_count} where S = {S_landingfield_length[i]}')
    #print('And now we out of the while loop')

#print(S_landingfield_length)
'''



############### For takeoff distance constraint ##################################
# takeoff does not calculate W/S so iterate over S values to calculate P
# convergence tolerance
error = 1
# varibale to iterate over
S_takeoff_distance = np.linspace(200,600,20)
# variable to be calculated, setting up as empty
P_takeoff_distance = np.empty(len(S_takeoff_distance))
# initial guess
P_guess = 400 #placeholder
# Inputs for takeoff_distance function
rho_rhoo = constraint_graph.density_ratio(10)
CLmaxTO = 1.65
rho = 0.00237

for i in range(len(S_takeoff_distance)):
    converged = False
    S_o = S_takeoff_distance[i]
    P_takeoff_distance[i] = P_guess
    iteration_count = 0
    while converged == False and iteration_count < 10:
        W = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P_takeoff_distance[i], P_DP, S_o, S_DP, max_interations = 20)
        #W = 9000
        W_So = W/S_o
        # need to make the function below a function of W/S_o that outputs W_P
        W_P = constraint_graph.takeoff_distance(rho_rhoo, CLmaxTO, W_So)
        P_new = (1/W_P)*W
        delta = abs(P_new-P_takeoff_distance[i])
        if delta <= error:
            converged = True
        P_takeoff_distance[i] = P_new
        iteration_count = iteration_count+1
        #print(f'This is iteration {iteration_count} where P = {P_takeoff_distance[i]}')
    #print('And now we out of the while loop')

#print(P_takeoff_distance)




################ For landing distance constraint #################################
# this calculates W/P so solve S for a range of T values
# convergence tolerance
error = 1
# varibale to iterate over
P_landingfield_length = np.linspace(200,600,20)
# variable to be calculated, setting up as empty
S_landingfield_length = np.empty(len(P_landingfield_length))
# initial guess
S_guess = 400 #placeholder
# Inputs for takeoff_distance function
rho_rhoo = constraint_graph.density_ratio(10) #actually don't know if this is right
CLmaxL = 1.8
Sa = 600

for i in range(len(P_landingfield_length)):
    converged = False
    P_o = P_landingfield_length[i]
    S_landingfield_length[i] = S_guess
    iteration_count = 0
    while converged == False and iteration_count < 10:
        W = weight.weight_estimation(Wcrew, Wpayload, Wo, batt_se, batt_eff, m_fuel, P_o, P_DP, S_landingfield_length[i], S_DP, max_interations = 20)
        #W = 9000
        W_S = constraint_graph.landingfield_length(rho_rhoo, CLmaxL, Sa)
        S_new = (1/W_S)*W
        delta = abs(S_new-S_landingfield_length[i])
        if delta <= error:
            converged = True
        S_landingfield_length[i] = S_new
        iteration_count = iteration_count+1
        #print(f'This is iteration {iteration_count} where S = {S_landingfield_length[i]}')
    #print('And now we out of the while loop')

#print(S_landingfield_length)

    

######################### For climb constraint #########################



######################## For crusie speed constraint ####################
# cruise speed does not calculate W/S so iterate over S values to calculate P
# convergence tolerance
error = 1
# varibale to iterate over
S_cruise_speed = np.linspace(200,600,20)
# variable to be calculated, setting up as empty
P_cruise_speed = np.empty(len(S_cruise_speed))
# initial guess
P_guess = 400 #placeholder
# Inputs for cruise_speed function
v = 225
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
        #print(f'This is iteration {iteration_count} where P = {P_cruise_speed[i]}')
    #print('And now we out of the while loop')

#print(P_cruise_speed)




##################### For absolute ceiling constraint ########################
# cruise speed does not calculate W/S so iterate over S values to calculate P
# convergence tolerance
error = 1
# varibale to iterate over
S_absolute_ceiling = np.linspace(200,600,20)
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



####################################################################
################## Plotting ########################################
#plt.plot(WTO_Sref_Cl, WCL_PCL, color = "#FF0000", marker = "s", markersize=1, label = "Climb1 Req")
#plt.plot(WTO_Sref_Cl2, WCL_PCL2, color = "k", marker = "s", markersize=1, label = "Climb2 Req")
#plt.plot(WTO_Sref_Cl3, WCL_PCL3, color = "#80FF00", marker = "s", markersize=1, label = "Climb3 Req")
plt.plot(S_takeoff_distance, P_takeoff_distance, color="#FF8000", marker = "s", markersize=1, label = "Takeoff Distance Req")
#plt.plot(S_stall_speed, P_stall_speed, color="#0080FF", marker = "s", markersize=1, label = "Stall Req")
plt.plot(S_landingfield_length, P_landingfield_length, color="#FF00FF", marker = "s", markersize=1, label = "Landingfield Length Req")
plt.plot(S_cruise_speed, P_cruise_speed, color="brown", marker = "s", markersize=1, label = "Cruise Speed Req")
plt.plot(S_absolute_ceiling, P_absolute_ceiling, color="#00FFFF", marker = "s", markersize=1, label = "Ceiling Req")
#plt.plot(W_S5, W_P5, color="#7F00FF", marker = "s", markersize=1, label = "Sustained Turn Req")
#plt.scatter([29.89], [8.34], label = 'Design Point', color = '#CD2305', s = 200, marker = '*')
#plt.xlim(10,175)
#plt.ylim(0, 50)
plt.title('Constraint Graph P vs S')
plt.legend(loc='best', fontsize = 'small')
plt.xlabel('S (ft^2)')
plt.ylabel('P (hp)')
plt.show()