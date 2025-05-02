#Standard Imports
import math
import pandas as pd
from scipy import integrate
import numpy as np
import os
import matplotlib.pyplot as plt
#import vivi
### JUPYTER NOTEBOOK SETTINGS ###
#matplotlib inline
#Disable python warning output. only for production, remove for debugging
import warnings
warnings.filterwarnings('ignore')
#Set default figure apperance
import seaborn as sns #fancy plotting package
#no background fill, legend font scale, frame on legend
sns.set(style = 'whitegrid', font_scale = 1.5, rc = {'legend.frameon': True})
#Mark ticks with border on all four sides(override 'whitegrid')
sns.set_style('ticks')
#ticks point in
sns.set_style({"xtick.direction": "in", "ytick.direction": "in"})
#fix invisible marker bug
sns.set_context(rc = {'lines.markeredgewidth': 0.1})
#retore default matplotlib colormap
mplcolors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
'#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
sns.set_palette(mplcolors)

#Get color cycle for manual colors
colors = sns.color_palette()
#set matplotlib defaults
#(call after seaborn, which changes some defaults)
params = {
#Font sizes
'axes.labelsize' : 30, #Axis labels
'axes.titlesize' : 30, #Title
'font.size' : 28, #textbox
'xtick.labelsize' : 22, #axis tick labels
'ytick.labelsize' : 22, #axis tick labels
'legend.fontsize' : 24, #legend font size
'font.family' : 'serif',
'font.fantasy' : 'xkcd',
'font.sans-serif' : 'Helvetica',
'font.monospace' : 'Courier',
#Axis Properties
'axes.titlepad' : 2*6.0, #title spacing from axis
'axes.grid' : True, #grid on plot
'figure.figsize' : (8,8), #square plots
'savefig.bbox' : 'tight', #reduce whitespace in saved figures
#legend properties
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
import matplotlib
matplotlib.rcParams.update(params) #update matplotlib defaults, call after
#end of boilerplate#
colors = sns.color_palette()#color cycle

W_max = 9923.42 #lbf
W_min = 6470.18  #lbf
CL_max = 1.65
CL_min = -0.8
S = 380 #ft^2
Vc = 250 #ft/s

rho0k = 0.002378
rho12k = 0.002378 * .6822
rho25k = 0.002378 * .4481
rho37k = 0.002378 * .2843
rho50k = 0.002378 * .1522
rho51k = 0.002378 * .1451
rho52k = 0.002378 * .1383
rho53k = 0.002378 * .1318
rho54k = 0.002378 * .1256
rho55k = 0.002378 * .1197
rho56k = 0.002378 * .1141
rho57k = 0.002378 * .1087
rho58k = 0.002378 * .1036
rho59k = 0.002378 * .09878
rho60k = 0.002378 * .09414

Veas = np.linspace(0, 400, 401)
Vs1 = math.sqrt((2 * W_max) / (rho0k * S * CL_max))
Vsneg1 = math.sqrt((-2 * W_max) / (rho0k * S * CL_min))
Vd = 1.25 * Vc
npos = 2.1 + 24000 / (W_max + 10000)
nneg = -0.4 * npos

nstall = (rho0k * Veas**2 * CL_max) / (2 * W_max / S)
nstall2 = []
for i in nstall:
    if i >= npos:
        break
    nstall2.append(i)
num = len(nstall2)
Veas2 = []
for i in Veas:
    if i >= num:
        break
    Veas2.append(i)

nnegstall = (rho0k * Veas**2 * CL_min) / (2 * W_max / S)
nnegstall2 = []
for i in nnegstall:
    if i <= nneg:
        break
    nnegstall2.append(i)
num2 = len(nnegstall2)
Veas3 = []
for i in Veas:
    if i >= num2:
        break
    Veas3.append(i)

nstall2last = nstall2[-1]
Veas2last = Veas2[-1]
nnegstall2last = nnegstall2[-1]
Veas3last = Veas3[-1]

mu = 2 * (W_max / S) / (rho0k * 6.89 * .11 * 32.17)
kg = 0.88 * mu / (5.3 + mu)
ngustb = 1 + (kg * .11 * 56 * 250) / (498 * W_max / S) 
# nneggustb = 1 - (kg * .11 * 56 * 250) / (498 * W_max / S) #REMOVED
# Vgustb = Vs1 * ngustb * 1.5 #REMOVED
# ngustc = 1 + (kg * .11 * 56 * 250) / (498 * W_max / S) #REMOVED

#Luis Work 5/1/25 - GUST
Vb = Vs1 * ngustb * 1.5
print("Vs:", Vs1)
print("Vb:", Vb)
nbGust = 1 + (kg * .11 * 56 * Vb) / (498 * W_max / S)
ncGust = 1 + (kg * .11 * 56 * Vc) / (498 * W_max / S)
ndGust = 1 + (kg * .11 * (56/2) * Vd) / (498 * W_max / S)


plt.plot(Veas2, nstall2, color="r", linestyle = "-", linewidth=2)
plt.plot(Veas3, nnegstall2, color='r', linestyle = "-", linewidth=2)
plt.plot([Veas2last, Vd],[nstall2last, nstall2last], color="r", linestyle = "-", linewidth=2)
plt.plot([Veas3last, Vc],[nnegstall2last, nnegstall2last], color="r", linestyle = "-", linewidth=2)
plt.plot([Vc, Vd], [nnegstall2last, 0], color="r", linestyle = "-", linewidth=2)
plt.plot([Vd, Vd], [nstall2last, 0], color="r", linestyle = "-", linewidth=2)

#plt.scatter(Vgustb, ngustb, color = 'b', marker = '*',s = 500) #REMOVED
#plt.scatter(Vgustb, nneggustb, color = 'b', marker = '*',s = 500) #REMOVED

#ADDED (To Create Gust Linear Lines)
def get_slope_equation(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    return m


#Plotting Gusts Points(Pos)
plt.scatter(Vb, 1+ nbGust, color = 'g', marker = '*',s = 500) # added
plt.text(Vb + 5, 1+ nbGust, 'Vb', color='g', va='center')
plt.scatter(Vc, 1+ ncGust, color = 'y', marker = '*',s = 500) # added
plt.scatter(Vd, 1+ ndGust, color = 'purple', marker = '*',s = 500) # added

#Plotting Gusts Lines (Pos)
VbGustSlope = get_slope_equation(0, 1, Vb, 1+ nbGust)
VcGustSlope = get_slope_equation(0, 1, Vc, 1+ ncGust)
VdGustSlope = get_slope_equation(0, 1, Vd, 1+ ndGust)
plt.plot((np.linspace(0, Vb, 100)), ((np.linspace(0, Vb, 100))*VbGustSlope) + 1, color="g", linestyle = "--", linewidth=2, label = "Vb Gust Line")
plt.plot((np.linspace(0, Vc, 100)), ((np.linspace(0, Vc, 100))*VcGustSlope) + 1, color="y", linestyle = "--", linewidth=2, label = "Vc Gust Line")
plt.plot((np.linspace(0, Vd, 100)), ((np.linspace(0, Vd, 100))*VdGustSlope) + 1, color="purple", linestyle = "--", linewidth=2, label = "Vd Gust Line")

#Plotting Gusts Points (Neg)
plt.scatter(Vb, 1+ (-1*nbGust), color = 'g', marker = '*',s = 500) # added
plt.scatter(Vc, 1+ (-1*ncGust), color = 'y', marker = '*',s = 500) # added
plt.scatter(Vd, 1+ (-1*ndGust), color = 'purple', marker = '*',s = 500) # added

#Plotting Gusts Lines (Neg)
plt.plot((np.linspace(0, Vb, 100)), ((np.linspace(0, Vb, 100))* -1*VbGustSlope) + 1, color="g", linestyle = "--", linewidth=2)
plt.plot((np.linspace(0, Vc, 100)), ((np.linspace(0, Vc, 100))* -1*VcGustSlope) + 1, color="y", linestyle = "--", linewidth=2)
plt.plot((np.linspace(0, Vd, 100)), ((np.linspace(0, Vd, 100))* -1*VdGustSlope) + 1, color="purple", linestyle = "--", linewidth=2)


#plt.scatter(Vc, 1+ngustc, color = 'b', marker = '*',s = 500)
# Vs point (top)
plt.scatter(Vs1, 1, color='k', s=200, marker='o')
plt.text(Vs1 - 15, 1, 'Vs', color='k', va='center')

# -Vs point (bottom)
plt.scatter(Vsneg1, -1, color='k', s=200, marker='o')
plt.text(Vsneg1 - 18, -1.1, '-Vs', color='k', va='center')

# Vd at nstall2last
plt.scatter(Vd, nstall2last, color='k', s=200, marker='o')
plt.text(Vd + 3, nstall2last, 'Vd', color='k', va='center')

# Vc at nnegstall2last
plt.scatter(Vc, nnegstall2last, color='k', s=200, marker='o')
plt.text(Vc + 3, nnegstall2last - 0.1, 'Vc', color='k', va='center')

#Va
plt.scatter(Veas2last, nstall2last, color='k', s=200, marker='o')
plt.text(Veas2last -15 , nstall2last, 'Va', color='k', va='center')

# Vd at 0 (if needed separately)
plt.scatter(Vd, 0, color='k', s=200, marker='o')  # no repeated label
plt.text(Vd + 3, 0, 'Vd', color='k', va='center')

plt.title('Maximum Weight Vn-Diagram - Gust Overlayed')
plt.legend(loc='best')
plt.xlabel('Equivalent Airspeed')
plt.ylabel('n(Load Factor)')
plt.show()

### Max Weight Vn Diagram - Gust Adjusted

plt.plot(Veas2, nstall2, color="r", linestyle = "-", linewidth=2)
plt.plot(Veas3, nnegstall2, color='r', linestyle = "-", linewidth=2)
plt.plot([Veas2last, Vd],[nstall2last, nstall2last], color="r", linestyle = "-", linewidth=2)
plt.plot([Veas3last, Vc],[nnegstall2last, nnegstall2last], color="r", linestyle = "-", linewidth=2)
plt.plot([Vc, Vd], [nnegstall2last, 1+(Vd*-1*VdGustSlope)], color="r", linestyle = "-", linewidth=2)
plt.plot([Vd, Vd], [nstall2last, 1+(Vd*-1*VdGustSlope)], color="r", linestyle = "-", linewidth=2)

# Vs point (top)
plt.scatter(Vs1, 1, color='k', s=200, marker='o')
plt.text(Vs1 - 15, 1, 'Vs', color='k', va='center')

# -Vs point (bottom)
plt.scatter(Vsneg1, -1, color='k', s=200, marker='o')
plt.text(Vsneg1 - 18, -1.1, '-Vs', color='k', va='center')

# Vd at nstall2last
plt.scatter(Vd, nstall2last, color='k', s=200, marker='o')
plt.text(Vd + 3, nstall2last, 'Vd', color='k', va='center')

# Vc at nnegstall2last
plt.scatter(Vc, nnegstall2last, color='k', s=200, marker='o')
plt.text(Vc + 3, nnegstall2last - 0.1, 'Vc', color='k', va='center')

#Va
plt.scatter(Veas2last, nstall2last, color='k', s=200, marker='o')
plt.text(Veas2last -15 , nstall2last, 'Va', color='k', va='center')

# Vd at 0 (if needed separately)
plt.scatter(Vd, 1+(Vd*-1*VdGustSlope), color='k', s=200, marker='o')  # no repeated label
plt.text(Vd + 3, 0, 'Vd', color='k', va='center')

plt.title('Maximum Weight Vn-Diagram - Gust Adjusted')
plt.legend(loc='best')
plt.xlabel('Equivalent Airspeed')
plt.ylabel('n(Load Factor)')
plt.show()




###VN MIN condition

Veas = np.linspace(0, 400, 401)
Vs1 = math.sqrt((2 * W_min) / (rho0k * S * CL_max))
Vsneg1 = math.sqrt((-2 * W_min) / (rho0k * S * CL_min))
Vd = 1.25 * Vc
npos = 2.1 + 24000 / (W_max + 10000)
nneg = -0.4 * npos

nstall = (rho0k * Veas**2 * CL_max) / (2 * W_min / S)
nstall2 = []
for i in nstall:
    if i >= npos:
        break
    nstall2.append(i)
num = len(nstall2)
Veas2 = []
for i in Veas:
    if i >= num:
        break
    Veas2.append(i)

nnegstall = (rho0k * Veas**2 * CL_min) / (2 * W_min / S)
nnegstall2 = []
for i in nnegstall:
    if i <= nneg:
        break
    nnegstall2.append(i)
num2 = len(nnegstall2)
Veas3 = []
for i in Veas:
    if i >= num2:
        break
    Veas3.append(i)

nstall2last = nstall2[-1]
Veas2last = Veas2[-1]
nnegstall2last = nnegstall2[-1]
Veas3last = Veas3[-1]

mu = 2 * (W_min / S) / (rho0k * 6.89 * .11 * 32.17)
kg = 0.88 * mu / (5.3 + mu)
ngustb = 1 + (kg * .11 * 56 * 250) / (498 * W_min / S) 
# nneggustb = 1 - (kg * .11 * 56 * 250) / (498 * W_max / S) #REMOVED
# Vgustb = Vs1 * ngustb * 1.5 #REMOVED
# ngustc = 1 + (kg * .11 * 56 * 250) / (498 * W_max / S) #REMOVED

#Luis Work 5/1/25 - GUST
Vb = Vs1 * ngustb * 1.5
print("Vs:", Vs1)
print("Vb:", Vb)
nbGust = 1 + (kg * .11 * 56 * Vb) / (498 * W_min / S)
ncGust = 1 + (kg * .11 * 56 * Vc) / (498 * W_min / S)
ndGust = 1 + (kg * .11 * (56/2) * Vd) / (498 * W_min / S)


plt.plot(Veas2, nstall2, color="r", linestyle = "-", linewidth=2)
plt.plot(Veas3, nnegstall2, color='r', linestyle = "-", linewidth=2)
plt.plot([Veas2last, Vd],[nstall2last, nstall2last], color="r", linestyle = "-", linewidth=2)
plt.plot([Veas3last, Vc],[nnegstall2last, nnegstall2last], color="r", linestyle = "-", linewidth=2)
plt.plot([Vc, Vd], [nnegstall2last, 0], color="r", linestyle = "-", linewidth=2)
plt.plot([Vd, Vd], [nstall2last, 0], color="r", linestyle = "-", linewidth=2)

#plt.scatter(Vgustb, ngustb, color = 'b', marker = '*',s = 500) #REMOVED
#plt.scatter(Vgustb, nneggustb, color = 'b', marker = '*',s = 500) #REMOVED

#ADDED (To Create Gust Linear Lines)
def get_slope_equation(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    return m


#Plotting Gusts Points(Pos)
plt.scatter(Vb, 1+ nbGust, color = 'g', marker = '*',s = 500) # added
plt.text(Vb + 5, 1+ nbGust, 'Vb', color='g', va='center')
plt.scatter(Vc, 1+ ncGust, color = 'y', marker = '*',s = 500) # added
plt.scatter(Vd, 1+ ndGust, color = 'purple', marker = '*',s = 500) # added

#Plotting Gusts Lines (Pos)
VbGustSlope = get_slope_equation(0, 1, Vb, 1+ nbGust)
VcGustSlope = get_slope_equation(0, 1, Vc, 1+ ncGust)
VdGustSlope = get_slope_equation(0, 1, Vd, 1+ ndGust)
plt.plot((np.linspace(0, Vb, 100)), ((np.linspace(0, Vb, 100))*VbGustSlope) + 1, color="g", linestyle = "--", linewidth=2, label = "Vb Gust Line")
plt.plot((np.linspace(0, Vc, 100)), ((np.linspace(0, Vc, 100))*VcGustSlope) + 1, color="y", linestyle = "--", linewidth=2, label = "Vc Gust Line")
plt.plot((np.linspace(0, Vd, 100)), ((np.linspace(0, Vd, 100))*VdGustSlope) + 1, color="purple", linestyle = "--", linewidth=2, label = "Vd Gust Line")

#Plotting Gusts Points (Neg)
plt.scatter(Vb, 1+ (-1*nbGust), color = 'g', marker = '*',s = 500) # added
plt.scatter(Vc, 1+ (-1*ncGust), color = 'y', marker = '*',s = 500) # added
plt.scatter(Vd, 1+ (-1*ndGust), color = 'purple', marker = '*',s = 500) # added

#Plotting Gusts Lines (Neg)
plt.plot((np.linspace(0, Vb, 100)), ((np.linspace(0, Vb, 100))* -1*VbGustSlope) + 1, color="g", linestyle = "--", linewidth=2)
plt.plot((np.linspace(0, Vc, 100)), ((np.linspace(0, Vc, 100))* -1*VcGustSlope) + 1, color="y", linestyle = "--", linewidth=2)
plt.plot((np.linspace(0, Vd, 100)), ((np.linspace(0, Vd, 100))* -1*VdGustSlope) + 1, color="purple", linestyle = "--", linewidth=2)


#plt.scatter(Vc, 1+ngustc, color = 'b', marker = '*',s = 500)
# Vs point (top)
plt.scatter(Vs1, 1, color='k', s=200, marker='o')
plt.text(Vs1 - 15, 1, 'Vs', color='k', va='center')

# -Vs point (bottom)
plt.scatter(Vsneg1, -1, color='k', s=200, marker='o')
plt.text(Vsneg1 - 18, -1.1, '-Vs', color='k', va='center')

# Vd at nstall2last
plt.scatter(Vd, nstall2last, color='k', s=200, marker='o')
plt.text(Vd + 3, nstall2last, 'Vd', color='k', va='center')

# Vc at nnegstall2last
plt.scatter(Vc, nnegstall2last, color='k', s=200, marker='o')
plt.text(Vc + 3, nnegstall2last - 0.1, 'Vc', color='k', va='center')

#Va
plt.scatter(Veas2last, nstall2last, color='k', s=200, marker='o')
plt.text(Veas2last -15 , nstall2last, 'Va', color='k', va='center')

# Vd at 0 (if needed separately)
plt.scatter(Vd, 0, color='k', s=200, marker='o')  # no repeated label
plt.text(Vd + 3, 0, 'Vd', color='k', va='center')

plt.title('Minimum Weight Vn-Diagram - Gust Overlayed')
plt.legend(loc='best')
plt.xlabel('Equivalent Airspeed')
plt.ylabel('n(Load Factor)')
plt.show()

###Vn Min Weight - Gust Adjusted
plt.plot(Veas2, nstall2, color="r", linestyle = "-", linewidth=2)
plt.plot(Veas3, nnegstall2, color='r', linestyle = "-", linewidth=2)
plt.plot([Veas2last, Vd],[nstall2last, nstall2last], color="r", linestyle = "-", linewidth=2)
plt.plot([Veas3last, Vc],[nnegstall2last, nnegstall2last], color="r", linestyle = "-", linewidth=2)
plt.plot([Vc, Vd], [nnegstall2last, 1+ (-1*VdGustSlope*Vd)], color="r", linestyle = "-", linewidth=2)
plt.plot([Vd, Vd], [nstall2last, 1+ (-1*VdGustSlope*Vd)], color="r", linestyle = "-", linewidth=2)

# Vs point (top)
plt.scatter(Vs1, 1, color='k', s=200, marker='o')
plt.text(Vs1 - 15, 1, 'Vs', color='k', va='center')

# -Vs point (bottom)
plt.scatter(Vsneg1, -1, color='k', s=200, marker='o')
plt.text(Vsneg1 - 18, -1.1, '-Vs', color='k', va='center')

# Vd at nstall2last
plt.scatter(Vd, nstall2last, color='k', s=200, marker='o')
plt.text(Vd + 3, nstall2last, 'Vd', color='k', va='center')

# Vc at nnegstall2last
plt.scatter(Vc, nnegstall2last, color='k', s=200, marker='o')
plt.text(Vc + 3, nnegstall2last - 0.1, 'Vc', color='k', va='center')

#Va
plt.scatter(Veas2last, nstall2last, color='k', s=200, marker='o')
plt.text(Veas2last -15 , nstall2last, 'Va', color='k', va='center')

# Vd at 0 (if needed separately)
plt.scatter(Vd, 1+(-1*VdGustSlope*Vd), color='k', s=200, marker='o')  # no repeated label
plt.text(Vd + 3, 0, 'Vd', color='k', va='center')

plt.title('Minimum Weight Vn-Diagram - Gust Adjusted')
plt.legend(loc='best')
plt.xlabel('Equivalent Airspeed')
plt.ylabel('n(Load Factor)')
plt.show()