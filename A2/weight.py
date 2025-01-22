# Weight Approx
import numpy as np
import math
def weight_estimation(Wcrew, Wpayload, Wempty, Wo, m_batt, batt_se, prop_eff, LD, tolerance = 1e-6, max_iterations = 100):
    g = 32.17 #ft/s^2
    iteration = 0
    while iteration < max_iterations:
        R = prop_eff * np.exp(batt_se) * LD (m_batt / Wo)
        New_Wo = (Wcrew + Wpayload) / (1 - (Wempty/Wo) - (R * g / (prop_eff * np.exp(batt_se) * LD)))

        if abs(New_Wo - Wo) < tolerance:
            return New_Wo
        
        Wo = New_Wo
        iteration += 1

    raise ValueError("Convergence not possible with current max_iterations.")