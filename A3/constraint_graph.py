import numpy as np
import math
#CDo = 0.03
def stall_speed(rho, vstall, CLmax):
    #rho = the density of desired alt
    #v_stall = maximum stall speed set by the far requirment. Can also set stall speed lower
    #CL_max = 1.3-1.9
    W_Sref = 1/2 * rho * (vstall**2) * CLmax
    return W_Sref

def takeoff_distance(rho, CLmaxTO, BFL):
    #rho = density of desired alt
    #CL_maxTO = CL of choice
    #BFL = ?
    rhoSL = 0.002378 #slug/ft^3
    TTO_WTO = []
    W_Sref = np.linspace(1, 300, 50)
    TTO_WTO = W_Sref * (1 / ((rho/rhoSL) * CLmaxTO * (BFL / 37.5)))
    return TTO_WTO

def landingfield_length(rho, CLmaxL, Sa):
    #rho = density of desired alt
    #CL_maxL = CL of choice
    #Sa = Braking distance
    rhoSL = 0.002378 #slug/ft^3
    SL = []
    W_Sref = np.linspace(1, 300, 50)
    SL = 80 * W_Sref * (1 / ((rho/rhoSL) * CLmaxL)) + Sa
    return SL

def climb(ks, CLmaxCL, CDo, k, G):
    #
    #
    #
    #
    #
    T_W = []
    T_W = ((ks**2) * CDo / CLmaxCL) + (CLmaxCL * k / (ks**2)) + G
    return T_W

def cruise_speed(qcr, CDo, k):
    #
    #
    #
    T_W = []
    W_Sref = np.linspace(1, 300, 50)
    T_w = ((qcr * CDo) * (1 / W_Sref)) + ((k / qcr) * W_Sref)
    return T_W

def absolute_ceiling(k, CDo):
    #
    #
    T_W = 2 * math.sqrt(k * CDo)
    return T_W

def sustained_turn(q, CDo, k, n):
    #
    #
    #
    #
    T_W = []
    W_Sref = np.linspace(1, 300, 50)
    T_W = ((q * CDo) * (1 / W_Sref)) + (k(n**2/q)*W_Sref)