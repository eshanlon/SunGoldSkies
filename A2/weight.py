# Weight Approx
import numpy as np
import math
def weight_estimation(Wcrew, Wpayload, Wempty, Wo, m_batt, batt_se, prop_eff, LD):
    g = 32.17 #ft/s^2
    R = prop_eff * np.exp(batt_se) * LD (m_batt / Wo)
    Wo = (Wcrew + Wpayload) / (1 - (Wempty/Wo) - (R * g / (prop_eff * np.exp(batt_se) * LD)))