#STANDARD IMPORTS
import numpy as np
import os
import matplotlib.pyplot as plt
import math
from scipy.linalg import inv
### JUPYTER NOTEBOOK SETTINGS ########################################
#Plot all figures in full-size cells, no scroll bars
#matplotlib inline
#Disable Python Warning Output
#(NOTE: Only for production, comment out for debugging)
import warnings
warnings.filterwarnings('ignore')
### PLOTTING DEFAULTS BOILERPLATE (OPTIONAL) #########################
#SET DEFAULT FIGURE APPERANCE
import seaborn as sns #Fancy plotting package
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
'font.size' : 16, #Textbox
'xtick.labelsize': 22, #Axis tick labels
'ytick.labelsize': 22, #Axis tick labels
'legend.fontsize': 16, #Legend font size
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
'legend.handlelength' : 1,
'legend.labelspacing' : 0,
}
import matplotlib
matplotlib.rcParams.update(params) #update matplotlib defaults, call after￿
### END OF BOILERPLATE ##################################################
colors = sns.color_palette() #color cycle

###A4 Specific Component Power Constraint Graph
#Parallel Hybird Powertrain:
#Battery > Controller > EM > Gearbox                    > Propeller
#Fuel > Gas Turbine/ Thermodynamic Cycle > Gearbox

#Definning Component efficiencies (%) and powers [kW]
n_TC = 0.50 #Thermo Cycle, ie Gas Turbine
n_C = 0.98 #Controller
n_EM = 0.95 #Electric Motor
n_GB = 0.98 #Gear Box
n_Pp1 = 0.88 #Propeller

###Discussion for P_F and P_B specifically
#Having trouble identifying numbers for the fuel mass and battery mass. Therefore, let's make some assumptions.
#UPDATE: Mass Values provided by team on 2/22/25 8pm, taken from A2
#m_fuel = 500 [lbs]; m_bat = 304.36 [kg]
#Bridging Mass to Power
#From Lec 9, Slide 83; Battery Pack Specific Power: 1 [kW/kg]
#According to ChatGPT: 500lbs => 1461.9 kW (w/ 1hr fuel burn assumption and TC eff)
# 304.36kg => 304.36 kW


#P_F = 1353.99 #[hp]; PREV VALUE: 1960.44 [hp] by LM => 1461.9 [kW]
#P_B = 408.15 #[hp] => 304.36 [kW]
"""
P_TC = n_TC * P_F
P_C = n_C * P_B
P_EM = n_EM * P_C
P_S = n_GB * (P_EM + P_TC)
P_Pp1 = n_Pp1 * P_S #I believe this value is also P_Aircraft
p_Pp2 = 0
P_P = 1 #[hp], Loosely based on Shaft Power from A2
"""
#W_To = 13757 #[lbs], From A2

l_phi = 0 #Shaft Power Ratio

phi = 0.23 #Supplied Power Ratio => Solved via P_B / (P_B + P_F)



###Implementing Linear Power Balance Matrix. Lecture 9, Slide 70

# Define the coefficient matrix A
A = np.array([
    [-1,  n_TC,  0,  0,  0,  0,  0,  0],
    [ 0, -1,  0, n_C, -1,  0,  0,  0],
    [ 0,  0,  0,  0, -n_EM,  1,  0,  0],
    [ 0, -n_GB,  1,  0,  0, -n_GB,  0,  0],
    [ 0,  0, -n_Pp1,  0,  0,  0,  1,  0],
    [ l_phi - 1,  l_phi,  0,  0,  0,  0,  0,  0],
    [ phi - 1,  0,  0,  phi,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  1,  1]
])

"""
A = np.array([
    [-n_TC,  1,      0,     0,      0,     0,     0,     0,     0,     0],
    [  0,  -n_GB,    1,     1,      0,     0,     0,     0,     0,     0],
    [  0,    0,      0,   -n_Pp1,   0,     0,     0,     0,     1,     0],
    [  0,    0,    -n_EM,   0,      1,     0,     0,     0,     0,     0],
    [  0,    0,      0,     0,    -n_C,  -n_C,    0,     0,     0,     0],
    [  0,    0,      0,     0,      0,     0,     0,     1,     0,     0],
    [  0,    0,      0,     0,      0,     0,     0,     0,     0,     1],
    [ phi,   0,      0,     0,      0,  (phi-1),  0,     0,     0,     0],
    [  0,    0,      0,   l_phi,    0,     0,     0, (l_phi-1), 0,     0],
    [  0,    0,      0,     0,      0,     0,     0,     0,     1,     1],
])
"""

"""
#Define the Component Power Vector
x = np.array([
    P_F,
    P_TC,
    P_S,
    P_B,
    P_C,
    P_EM,
    P_Pp1,
    p_Pp2,

    modified order
    P_F
    P_TC
    P_EM
    P_S
    P_C
    P_B
    P_P1
    P_P2

])
"""


"""
# Define the right-hand side result vector
b = np.array([0, 0, 0, 0, 0, 0, 0, P_P])


###Solving for P_P via b vector in Ax = b
b = np.dot(A, x)
P_P = b[7] #Aquiring P_P value from the b Vector

print(P_P)
"""
"""
#REMOVED CODE.
###
###Dividing by W_To, inverting to achieve Power Loading (W/P)
W_To = 13757 #[lbs], From A2


#Diagonal_x
# Define the coefficient matrix A
D_x = np.array([
    [P_F/W_To,  0,          0,          0,         0,         0,        0,        0],
    [  0,    P_TC/W_To,     0,          0,         0,         0,        0,        0],
    [  0,       0,      P_S/W_To,       0,         0,         0,        0,        0],
    [  0,       0,          0,       P_B/W_To,     0,         0,        0,        0],
    [  0,       0,          0,          0,      P_C/W_To,     0,        0,        0],
    [  0,       0,          0,          0,         0,      P_EM/W_To,   0,        0],
    [  0,       0,          0,          0,         0,         0,    P_Pp1/W_To,   0],
    [  0,       0,          0,          0,         0,         0,        0,    p_Pp2/W_To]
])

#det_D_x = np.linalg.det(D_x)
#print("Determinant of D_x:", det_D_x)
#D_x_inv = np.linalg.inv(D_x)

#D_b_inv = A * D_x_inv
# Define the element-wise inverse variable vector (unknowns)
x_inv = np.array([
    W_To / P_F,
    W_To / P_TC,
    W_To / P_S,
    W_To / P_B,
    W_To / P_C,
    W_To / P_EM,
    W_To / P_Pp1,
    W_To / p_Pp2,
])
"""
"""
# Solve the system Ax = b
solution = np.linalg.solve(A, b)

# Print the solution
print("Solution vector (x):", solution)
"""

### Modified A2 Constraint Graph Code. 2/24/25 by LM
# Now includes addition P_component function input for EACH constraint parameter curve.
# Input the Power Component variable that is desired for the resulting Specific Constraint graph. Ie if desired result is W/P_EM, input P_EM into functions below.

def density_ratio(h):
    #h = height[m]
    lamb = 0.00357 #[K/m]
    To = 518.67 #[K]
    g = 31.17 #[m/s^2]
    R = 1716 #[J/kg*K]

    rho_rhoo = (1 + ((lamb * h)/ To))**(-((g/ (R * lamb)) + 1))
    return rho_rhoo
rho_rhoo = density_ratio(1)

def stall_speed(rho, vstall, CLmax):
    #rho = height of crop dusting
    #v_stall = Maximum stall speed set by the far requirment. Can also set stall lower speed
    #rho = The density of desired alt
    #v_stall = Maximum stall speed set by the far requirment. Can also set stall lower speed
    #CL_max = 1.3-1.9
    W_S = np.zeros(175)
    for i in range(len(W_S)):
        W_S[i] = 1/2 * rho * (vstall**2) * CLmax
    W_P = np.linspace(1, 60, 175)
    return W_S, W_P

def takeoff_distance(rho_rhoo, vstall, CLmaxTO, rho, prop_eff):
    #rho_rhoo = Density ratio for alt
    #CLmaxTO = CL of choice
    #W_sref = Wing loading obtained 
    #rho = Air density of choice
    #prop_eff = Propeller effiency
    n = 175
    TOP = 158.222 #WTO_Sref / (rho_rhoo * CLmaxTO * P_W)
    P_W = np.zeros(n)
    #v = np.zeros(n)
    W_P = np.zeros(n)
    W_S = np.linspace(1, 175, n)
    for i in range(len(W_S)):
        P_W[i] = W_S[i] * (1 / (rho_rhoo * CLmaxTO * (TOP)))
    W_P = (1 / P_W)
    return W_S, W_P

def landingfield_length(rho_rhoo, CLmaxL, Sa):
    #rho = Density of desired alt
    #CL_maxL = CL during landing
    #Sa = Braking distance
    #0.7 = Maximum landing to takeoff weight ratio(needs to be changed
    TOP = 158.222 # solved for TOP by is using the equation from lecture 6 slide 34 (STO = 8.134TOP...., STO = 1000ft from at502)
    BFL = TOP * 37.5
    Sland = BFL
    W_S = np.zeros(175)
    for i in range(len(W_S)):
        W_S[i] = rho_rhoo * CLmaxL * (Sland - Sa) / (80 * 0.7)
    W_P = np.linspace(1, 60, 175)
    return W_S, W_P

def climb(AR, e, CDo, W_Sref_cap, prop_eff, rho , CLmaxCL):
    #CDo = Minimum drag coefficent
    #e = Wing efficiency ratio, .7 for rectangular wings, 1 for elliptical
    #AR = Aspect Ratio from AT502
    #rho = Freestream Air density of choice
    #prop_eff = Propeller effiency
    ks =1.3
    k = 1 / (np.pi * e * AR)
    G = 0.083 #FAR23 requiremnt
    T_W = np.zeros(175)
    WCL_PCL = np.zeros(175)
    v = np.zeros(175)
    WTO_Sref_Cl = np.linspace(10, W_Sref_cap, 175)
    for i in range(len(WTO_Sref_Cl)):
        T_W[i] = ((ks**2 * CDo)/(CLmaxCL) + (k * (CLmaxCL/ks**2)) + G)
    for i in range(len(WTO_Sref_Cl)):
        v[i] = math.sqrt((2 * WTO_Sref_Cl[i]) / (rho * CLmaxCL))
        WCL_PCL[i] = prop_eff * 550 / (T_W[i] * v[i])
    return WTO_Sref_Cl, WCL_PCL

def cruise_speed(v, CDo, e, AR, rho, prop_eff):
    #v = Velocity during cruise
    #CDo = Minimum drag coefficent
    #e = Wing efficiency ratio, .7 for rectangular wings, 1 for elliptical
    #AR = Aspect Ratio from AT502
    #rho = Air density of choice
    #prop_eff = Propeller effiency
    qcr = 0.5 * rho * (v**2)
    k = 1 / (np.pi * e * AR)
    Wc_Wto = 0.8 #weight aproximation code 
    Pto_Pc = 1.253 #0.94/.75, max engine power / typical power used during cruise
    W_P = np.zeros(175)
    P_W = np.zeros(175)
    W_S = np.linspace(1, 175, 175)
    for i in range(len(W_S)):
        P_W[i] = (((qcr * v)* (CDo + (((W_S[i]**2) * (Wc_Wto**2) * k)/(qcr**2)))) / (550 * prop_eff * W_S[i])) * (Pto_Pc)
    W_P = (1 / P_W) 
    return W_S, W_P

def absolute_ceiling(e, AR, CDo, rho, CLmaxCL, prop_eff):
    #e = Wing efficiency ratio, .7 for rectangular wings, 1 for elliptical
    #AR = Aspect Ratio from AT502
    #CDo = Minimum drag coefficent
    k = 1 / (np.pi * e * AR)
    W_S = np.linspace(1, 175, 175)
    T_W = np.zeros(175)
    W_P = np.zeros(175)
    v = np.zeros(175)
    for i in range(len(W_S)):
        T_W[i] = 2 * math.sqrt(k * CDo)
    for i in range(len(W_S)):
        v[i] = math.sqrt((2 * W_S[i]) / (rho * CLmaxCL))
        W_P[i] = (prop_eff *550 / (T_W[i] * v[i])) 
    return W_S, W_P

def sustained_turn(CDo, rho, v, e, AR, R, CL, prop_eff):
    #CDo = Minimum drag coefficent
    #e = Wing efficiency ratio, .7 for rectangular wings, 1 for elliptical
    #AR = Aspect Ratio from AT502
    #rho = Air density of choice
    #R = turn radius
    #CL = CL during cruise
    #prop_eff = propeller effiecncy
    g = 32.17 #ft/s^2
    n = np.sqrt((v**2/(R * g))**2 + 1)
    k = 1 / (np.pi * e * AR)
    qst = 0.5 * rho * (v**2)
    T_W = np.zeros(175)
    W_P = np.zeros(175)
    v = np.zeros(175)
    W_S = np.linspace(1, 175, 175)
    for i in range(len(W_S)):
        T_W[i] = ((qst * CDo) * (1 / W_S[i])) + (k * (n**2 / qst) * W_S[i])
    for i in range(len(W_S)):
        v[i] = math.sqrt((2 * W_S[i]) / (rho * CL))
        W_P[i] = (prop_eff *550 / (T_W[i] * v[i])) 
    return W_S, W_P

#P_P Constraint Graph 
WTO_Sref_Cl, WCL_PCL = climb(AR = 8, e = 0.8, CDo = 0.0284, W_Sref_cap = 175, prop_eff = 0.7, rho = (density_ratio(500) * 0.002378) , CLmaxCL = 1.5)
WTO_Sref_Cl2, WCL_PCL2 = climb(AR = 8, e = 0.8, CDo = 0.0284, W_Sref_cap = 175, prop_eff = 0.7, rho = (density_ratio(1500) * 0.002378) , CLmaxCL = 1.5)
WTO_Sref_Cl3, WCL_PCL3 = climb(AR = 8, e = 0.8, CDo = 0.0284, W_Sref_cap = 175, prop_eff = 0.7, rho = (density_ratio(3000) * 0.002378) , CLmaxCL = 1.5)
W_S, W_P = takeoff_distance(rho_rhoo = density_ratio(10), CLmaxTO = 1.65, prop_eff = 0.7, vstall = 118.147, rho = 0.00237)
W_S1, W_P1 = stall_speed(rho = 0.002377, vstall = 118.147, CLmax = 1.8)
W_S2, W_P2 = landingfield_length(rho_rhoo, CLmaxL = 1.8, Sa = 600)
W_S3, W_P3 = cruise_speed(v = 225, CDo = 0.006, e = 0.8, AR = 8, rho = 0.002242, prop_eff = 0.7)
W_S4, W_P4 = absolute_ceiling(e = 0.8, AR = 8, CDo = 0.0284, rho = 0.00176, CLmaxCL = 1.5, prop_eff = 0.7) #rho = density 10000ft
W_S5, W_P5 = sustained_turn(CDo = 0.0284, rho = 0.002242, v = 250, e = 0.8, AR = 8, R = 1000, CL = 1.5, prop_eff = 0.7) #rho = density 2000ft


plt.plot(WTO_Sref_Cl, WCL_PCL, color = "#FF0000", marker = "s", markersize=0, label = "Climb1 Req")
plt.plot(WTO_Sref_Cl2, WCL_PCL2, color = "k", marker = "s", markersize=0, label = "Climb2 Req")
plt.plot(WTO_Sref_Cl3, WCL_PCL3, color = "#80FF00", marker = "s", markersize=0, label = "Climb3 Req"), 
plt.plot(W_S, W_P, color="#FF8000", marker = "s", markersize=0, label = "Takeoff Distance Req")
plt.plot(W_S1, W_P1, color="#0080FF", marker = "s", markersize=0, label = "Stall Req")
plt.plot(W_S2, W_P2, color="#FF00FF", marker = "s", markersize=0, label = "Landingfield Length Req")
plt.plot(W_S3, W_P3, color="brown", marker = "s", markersize=0, label = "Cruise Speed Req")
plt.plot(W_S4, W_P4, color="#00FFFF", marker = "s", markersize=0, label = "Ceiling Req")
plt.plot(W_S5, W_P5, color="#7F00FF", marker = "s", markersize=0, label = "Sustained Turn Req")

plt.scatter([29.89], [8.34], label = 'Design Point', color = '#CD2305', s = 200, marker = '*')
plt.xlim(10,175)
plt.ylim(0, 50)
plt.title('Constraint Graph W/P vs W/S')
plt.legend(loc='best', fontsize = 'small')
plt.xlabel('W/S(lb/ft^2)')
plt.ylabel('W/P(lb/hp)')
plt.show()

inv_climb1 = 1 / WCL_PCL
inv_climb2 = 1 / WCL_PCL2
inv_climb3 = 1 / WCL_PCL3
inv_takeoffdistance = 1 / W_P
inv_stallspeed = 1 / W_P1
inv_landingfieldlength = 1 / W_P2
inv_cruisespeed = 1 / W_P3
inv_absoluteceiling = 1 / W_P4
inv_sustainedturn = 1 / W_P5

###Solving x = A^-1 * b with specific constraint curves as b (P_P) for x (component powers)
#A_inv = np.linalg.inv(A)
#Solution for x = A^-1 * b will have the elements in the vector in this order:


def compPowerstoWeightConstCurveDep(inv_curve):
    inv_size = len(inv_curve)
    b = np.array([np.zeros(inv_size), np.zeros(inv_size), np.zeros(inv_size), np.zeros(inv_size), np.zeros(inv_size), np.zeros(inv_size), np.zeros(inv_size), inv_curve])
    
    
    x = np.linalg.solve(A, b)
    """
    #Define the Component Power Vector
    x = np.array([
    P_F/W_TO,
    P_TC/W_TO,
    P_S/W_TO,
    P_B/W_TO,
    P_C/W_TO,
    P_EM/W_TO,
    P_Pp1/W_TO,
    p_Pp2/W_TO,
    ])
    """
    x = np.array(x)
   
    return x

x_takeoffCompPower = compPowerstoWeightConstCurveDep(inv_takeoffdistance)
#print(x_takeoffCompPower)


def graphSpecCompPowerLoading(x_CompPtoW, index): #index option: 0=P_F, 1=P_TC, 2=P_S, 3=P_B, 4=P_C, 5=P_EM, 6=P_P1, 7=P_P2
    x_selectedCompPtoW = x_CompPtoW[index]
    print(x_selectedCompPtoW)
    x_selectedCompWtoP = 1 / x_selectedCompPtoW
    
    print("running")
    plt.plot(np.linspace(1,len(x_selectedCompPtoW), len(x_selectedCompPtoW)), x_selectedCompWtoP, color = "#FF0000", marker = "s", markersize=0, label = "Climb1 Req")
    #plt.xlim(10,175)
    #plt.ylim(0, 50)
    plt.title('Constraint Graph W/P vs W/S')
    plt.legend(loc='best', fontsize = 'small')
    plt.xlabel('W/S(lb/ft^2)')
    plt.ylabel('W/P(lb/hp)')
    plt.show()
    print("done")

graphSpecCompPowerLoading(x_takeoffCompPower, 3)

#NOTE: CODE FAILS TO OUTPUT SUCCESSFUL COMPONENT POWER LOADING VS WING LOADING GRAPH. WORK IN PROGRESS BY LM 2/24/25
#We are confident that a successful version of the specific component constraint graph code is obtainable in the near future and present the targeted battery Power Loading vs Wing Loading graph in a future iteration of this Assignment.