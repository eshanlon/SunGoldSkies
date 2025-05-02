
import numpy as np
import matplotlib.pyplot as plt

##### Constants ####
gamma = 1.4
R = 1716
T = 518.67
rho = 0.002378
a = np.sqrt(gamma * R * T)
p_dynamic = 0.5 * rho * a**2

##### Aircraft Parameters ####
f_rest = 1.8401
CD0_w = 0.03
W = 9923.42  # Weight in lbf
e = 0.7746

##### Design Ranges ######
Mach_numbers = np.arange(0.20, 0.30, 0.02)
AR_values = np.arange(6, 11, 1)

####### Stall margin line inputs####
CL_max = 1.6109  
CL_limit = CL_max / (1.1**2)
M_ref = 0.22
q_ref = 0.5 * gamma * p_dynamic * M_ref**2
WS_limit = CL_limit * q_ref

###### Storage Arrays #####
WS_results = []
LD_results = []
AR_grid = []
Mach_grid = []

#### Iteration Parameters ####
max_iter = 10
tolerance = 1e-4

# ### Loop over AR and Mach number ####
for AR in AR_values:
    for M in Mach_numbers:
        CD0_guess = 0.030
        for _ in range(max_iter):
            CL = np.sqrt(CD0_guess * np.pi * AR * e)
            LD_max = 0.5 * np.sqrt(np.pi * AR * e / CD0_guess)
            q = 0.5 * gamma * p_dynamic * M**2
            WS = CL * q
            S = W / WS
            CD0_new = f_rest / S + CD0_w
            if abs(CD0_new - CD0_guess) < tolerance:
                break
            CD0_guess = CD0_new

        WS_results.append(WS)
        LD_results.append(LD_max)
        AR_grid.append(AR)
        Mach_grid.append(M)

#### Convert to arrays #####
WS_results = np.array(WS_results)
LD_results = np.array(LD_results)
AR_grid = np.array(AR_grid)
Mach_grid = np.array(Mach_grid)

#### Plotting ####
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_facecolor('white')

# Plot constant Mach lines
for M in np.unique(Mach_grid):
    idx = Mach_grid == M
    ax.plot(WS_results[idx], LD_results[idx], label=f'M = {M:.2f}', linewidth=2)

# Plot constant AR lines
for AR in np.unique(AR_grid):
    idx = AR_grid == AR
    ax.plot(WS_results[idx], LD_results[idx], '--', label=f'AR = {AR}', color='gray')

# Add red stall limit line
ax.axvline(WS_limit, color='red', linestyle='-', linewidth=2, label=f'Safe $W/S$ Limit = {WS_limit:.1f}')

# Shade unsafe region
ax.axvspan(WS_limit, WS_results.max() + 10, color='red', alpha=0.2, label='Unsafe $W/S$ Region')

# Labels and formatting
ax.set_title(r'$(L/D)_{max}$ vs Wing Loading $W/S$ with Stall Margin')
ax.set_xlabel(r'Wing Loading $W/S$ (lb/ft$^2$)')
ax.set_ylabel(r'Maximum Lift-to-Drag Ratio $(L/D)_{max}$')
ax.grid(True)
ax.legend()

plt.tight_layout()
plt.show()



