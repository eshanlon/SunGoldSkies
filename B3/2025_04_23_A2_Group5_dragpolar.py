import numpy as np
import matplotlib.pyplot as plt
import math

# === Aircraft Parameters ===
Sref = 380  # ft^2, reference wing area
c_bar = 6.93  # ft, mean aerodynamic chord
xw = 11.5  # ft, aerodynamic center
x = 13.5  # ft, CG location
St = 79.58  # ft^2, horizontal tail area
VHT = 0.55  # horizontal tail volume coefficient
ARt = 2.7  # aspect ratio of tail

# === Trim Drag Calculation ===
CM_ac_t = -0.03  # moment coefficient at ac
CLw = 0.55  # lift coefficient of wing

et = 1.78 * (1 - 0.045 * (ARt ** 0.68)) - 0.64
CLt = ((CLw * (xw / c_bar)) + CM_ac_t) * ((x / c_bar - xw / c_bar) * (1 / VHT))
CDi_tail = (CLt ** 2) / (math.pi * et * ARt)
CDtrim = CDi_tail * (St / Sref)

# === Flap Drag Calculation (update these for each config) ===
def flap_drag(Sf, delta_deg, Cf_c):
    delta_rad = np.radians(delta_deg)
    return 1.7 * (Cf_c ** 1.38) * (Sf / Sref) * (np.sin(delta_rad) ** 2)

# === Induced Drag Parameters (from AVL or assumed) ===
AR = 8.0
e_clean = 0.82
e_takeoff = 0.77
e_landing = 0.73

# === Zero-Lift Drag ===
CD0_clean = 0.0205
CD0_takeoff = CD0_clean + 0.015  # + flap delta
CD0_landing = CD0_clean + 0.065 + 0.02  # + flap + gear

# === Flap drag additions (example values) ===
delta_CD_flap_takeoff = flap_drag(Sf=100, delta_deg=20, Cf_c=0.3)
delta_CD_flap_landing = flap_drag(Sf=130, delta_deg=40, Cf_c=0.3)

# === CL Ranges ===
CL_range = np.linspace(0, 1.8, 100)

# === Drag Calculations ===
def total_CD(CL, CD0, e):
    return CD0 + CDtrim + (CL ** 2) / (math.pi * e * AR)

CD_clean = total_CD(CL_range, CD0_clean, e_clean)
CD_takeoff = total_CD(CL_range, CD0_takeoff + delta_CD_flap_takeoff, e_takeoff)
CD_landing = total_CD(CL_range, CD0_landing + delta_CD_flap_landing, e_landing)

# === Reflecting the lower portion of each drag polar ===
index_clean = CL_range <= (1.5 - 0.1)
CL_clean_low = -CL_range[index_clean]
CD_clean_low = CD_clean[index_clean]

index_takeoff = CL_range <= (1.65 - 0.2)
CL_takeoff_low = -CL_range[index_takeoff]
CD_takeoff_low = CD_takeoff[index_takeoff]

index_landing = CL_range <= (1.8 - 0.2)
CL_landing_low = -CL_range[index_landing]
CD_landing_low = CD_landing[index_landing]

### Plot####
plt.figure(figsize=(10, 6))
plt.plot(CD_clean, CL_range, label='Clean', color='red')
plt.plot(CD_clean_low, CL_clean_low, color='red')

plt.plot(CD_takeoff, CL_range, label='Takeoff Flaps + Gear Down', color='green')
plt.plot(CD_takeoff_low, CL_takeoff_low, color='green')

plt.plot(CD_landing, CL_range, label='Landing Flaps + Gear Down', color='blue')
plt.plot(CD_landing_low, CL_landing_low, color='blue')

plt.xlabel(r'$C_D$')
plt.ylabel(r'$C_L$')
plt.title(r'$C_L$ vs $C_D$ for Various Configurations')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

