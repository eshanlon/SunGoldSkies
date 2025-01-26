# Weight Approx
import numpy as np
import math
def weight_estimation(Wcrew, Wpayload, Wo, m_batt, batt_se, prop_eff, LD):
    g = 32.17 # ft/s^2
    R = 417420 # ft
    A = 0.74 # From table 2.1 metabook
    C = -0.03 # From table 2.1 metabook
    err = 1e-6
    delta = 2*err
    E01_EC = 1 # fill in from somewhere
    E12_EC = 1 # fill in from somewhere
    E23_EC = 1 # fill in from somewhere
    E34_EC = 1 # fill in from somewhere
    E45_EC = 1 # fill in from somewhere
    while delta > err:
        We_Wo = A * Wo ** C
        m_batt = (R * Wo) / (prop_eff * batt_se * LD)
        New_Wo = (Wcrew + Wpayload) / (1 - We_Wo - (((m_batt * g) / Wo) * (1 + E01_EC + E12_EC + E23_EC + E34_EC + E45_EC)))
        delta = abs(New_Wo - Wo) / abs(New_Wo)
        Wo = New_Wo
    print(Wo)

Wcrew = 180 * 32.17 # lbm * g = lbf
Wpayload = 2000 * 32.17 # lbm * g = lbf
Wo = 15000 * 32.17 # lbm * g = lbf
batt_se = 722946.005 # ft-lbf/lbm
prop_eff = 0.5
LD = 10
R = 417420 # ft
m_batt = (R * Wo) / (prop_eff * batt_se * LD)
print(m_batt)
A = 0.74
C = -0.03
g = 32.17 #ft/s^2
We_Wo = A * Wo ** C
print(We_Wo)

#weight_estimation(Wcrew, Wpayload, Wo, m_batt, batt_se, prop_eff, LD)