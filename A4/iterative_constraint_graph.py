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
folder_path = os.path.abspath("A2")  # Use forward slashes
if folder_path not in sys.path:
    sys.path.append(folder_path)

import weight



################ Constraint Graph Iteration #################################
# Defining known variables
T_guess = 1000 #placeholder
error = 1e-6



# Defining S range to iterate over and setting up empty T arrays
S = np.linspace(200,400,20)
import numpy as np

T_climb = np.empty(len(S))
T_takeoff_distance = np.empty(len(S))
T_stall_speed = np.empty(len(S))
T_landingfield_length = np.empty(len(S))
T_cruise_speed = np.empty(len(S))  # Fixed double underscore
T_absolute_ceiling = np.empty(len(S))
T_sustained_turn = np.empty(len(S))


#starting with only doing the line for climb conditions
T = np.empty(len(S))
converged = False
for i in range(len(S)):
    S_o = S[i]
    T[i] = T_guess
    #while converged == False:
        #W = 


print("Code ran successfully")
    
