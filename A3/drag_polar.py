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
### END OF BOILERPLATE ##################################################
colors = sns.color_palette() #color cycle

############ Inputs #########################
AR = 7.32
W_to = 3100 #lb
S = 174 #ft^2
C_Lmax = 2.2
C_L = np.linspace(0,C_Lmax,100)

############ Inputs Based on Roskam Tables #######################
# From figure 2.31a (same c_f as Cessna 180 and P-35, comparable aircraft)
c_f = 0.0060
# From tables 3.4 and 3.5 (pg. 122)
a = -2.2218 # for c_f = 0.006
b = 1 # for all c_f values
c = 1.0447 # for ag plane
d = 0.5326 # for ag plane
e = 0.8 #range 0.80 - 0.85
# From table 3.6 (pg.127)
delta_CDo_takeoffflapsdown = 0.015 #range 0.010 - 0.020
e_takeoffflapsdown = 0.83 #range 0.80 - 0.85
delta_CDo_landingflapsdown = 0.065 #range 0.055 - 0.075
e_landingflapsdown = 0.77 #range 0.75 - 0.80
delta_CDo_landinggeardown = 0.020 #range 0.015 - 0.025
e_landinggeardown = e #landing gear down has no effect on e
#see Roskam to determine what side of the range to choose from

############ Calculating C_D #######################
# Calculating C_Do
S_wet = 10**(c+d*math.log10(W_to))
#f = a*S_wet**b
f = 10**(a+b*math.log10(S_wet))
C_Do = f/S

# Gear is down for all drag polars
# Clean drag polar
C_D = (C_Do+delta_CDo_landinggeardown) + ((C_L**2)/(math.pi*e_landinggeardown*AR))

# Takeoff Flaps down drag polar
C_D_takeoffflapsdown = (C_Do+delta_CDo_landinggeardown+delta_CDo_takeoffflapsdown) + ((C_L**2)/(math.pi*e_takeoffflapsdown*AR))

# Landing Flaps down drag polar
C_D_landingflapsdown = (C_Do+delta_CDo_landinggeardown+delta_CDo_landingflapsdown) + ((C_L**2)/(math.pi*e_landingflapsdown*AR))

############# Plotting ###########################
# Plotting Cp Distribution for AOA = 8
plt.figure(figsize=(10, 6))
plt.grid(True)
plt.xlabel('$C_D$', fontsize=16)
plt.ylabel('$C_L$', fontsize=16)
plt.plot(C_D, C_L,label='Gear down, cruise', color='red')
plt.plot(C_D, -C_L, color='red')
plt.plot(C_D_takeoffflapsdown, C_L,label='Takeoff flaps, gear down', color='green')
plt.plot(C_D_takeoffflapsdown, -C_L, color='green')
plt.plot(C_D_landingflapsdown, C_L,label='Landing flaps, gear down', color='blue')
plt.plot(C_D_landingflapsdown, -C_L, color='blue')
plt.title('Drag Polar', fontsize=16)
plt.legend(loc='best')
plt.show()