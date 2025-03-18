import math
import numpy as np

# Known Parameters
rho = 1.8683e-3 #slugs/ft^3
v_cruise = 225 #ft/s

A = 8 #aspect ratio
B_w = 55.14 #ft, wing span
D = 9 #ft, fuselage structural depth
Ht_Hv = 0.5 #0 for conventional tail, 1.0 for T tail, so assumed 0.5 for cruciform tail
lambda_h = 0.59 #taper ratio of horizontal tail
lambda_ht = 0 #sweep angle of horizontal tail
lambda_s = 0 #degrees, sweep angle
lambda_t = 1 #taper ratio of main wing
lambda_vt = 0.65 #taper ratio of vertical tail
lambda_vt_s = 0 #sweep angle of vertical tail
L = 34.94 #ft, fuselage structural length (excludes radome, tail cap)
L_m = 48 #in, length of main landing gear
L_n = 36 #in, nose gear length or tail gear length in our case
L_t = 19.6 #ft, tail length: wing quarter MAC to tail quarter MAC
N_en = 1 #number of engines
N_l = 5.7 #ultimate landing load factor = N_gear*1.5
N_z = 3.8 #ultimate load factor = 1.5*limit load factor
q = 0.5*rho*v_cruise**2 #lb/ft^2, dynamic pressure at cruise
S_f = 1004 #ft^2, fuselage wetted area
S_ht = 64.8 #ft^2, horizontal tail area
S_vt = 27.88 #ft^2, vertical tail area
S_w = 380 #ft, wing area
t_c = 0.12
V_i = 50 #gal, integral tanks volume
V_t = 200 #gal, total fuel volume
W_dg = 13757 #lb, design gross weight
W_en = 331 #lb, engine weight for each engine
W_fw = 700 #lb, weight of fuel in wing
W_l = W_dg*0.03 #lb, landing design gross weight
W_press = 0 #weight penalty due to pressurization, N/A for our aircraft
W_uav = 1000 #lb, uninstalled avionics weight (typically 800-1400 lb)


################# Calculating Component Weights ##########################
# Main wing weight
W_wing = 0.036*S_w**0.758*W_fw**0.0035*(A/math.cos(lambda_s)**2)**0.6*q**0.006*lambda_t**0.04*(100*t_c/math.cos(lambda_s))**(-0.3)*(N_z*W_dg)**0.49
# Horizontal tail weight
W_ht = 0.016*(N_z*W_dg)**0.414*q**0.168*S_ht**0.896*(100*t_c/math.cos(lambda_s))**(-0.12)*(A/math.cos(lambda_ht)**2)**0.043*lambda_h**(-0.02)
# Vertical tail weight
W_vt = 0.073*(1+0.2*Ht_Hv)*(N_z*W_dg)**0.376*q**0.122*S_vt**0.873*(100*t_c/math.cos(lambda_vt_s))**(-0.49)*(A/math.cos(lambda_vt_s)**2)**0.357*lambda_vt**0.039
# Fuselage weight
W_fuselage = 2*(0.052*S_f**1.086*(N_z*W_dg)**0.177*L_t**(-0.051)**(L/D)**(-0.072)*q**0.241+W_press) #the multiplying everything by 2 is a fudge factor
# Main landing gear weight
W_mainlandinggear = 0.095*(N_l*W_l)**0.768*(L_m/12)**0.409
# Nose landing gear weight (tail gear weight in our case)
W_taillandinggear = 0.125*(N_l*W_l)**0.566*(L_n/12)**0.845
# Installed engine weight
W_installedengine = 2.575*W_en**0.922*N_en + W_en #added portion is for electric motor
# Fuel system weight
W_fuelsystem = 2.49*V_t**0.726*(1/(1+V_i/V_t))**0.363*N_l**0.242*N_en**0.157
# Flight controls weight
W_flightcontrols = 0.053*L**1.536*B_w**0.371*(N_z*W_dg*10**-4)**0.8
# Hydraulics weight
W_hydraulics = 0.001*W_dg
# Avionics weight
W_avionics = 2.117*W_uav**0.933
# Electrical Weight
W_electrical = 12.57*(W_fuelsystem+W_avionics)**0.51
# Furnishings weight
W_furnishings = 0.0582*W_dg-65
# Battery Weight
W_battery = 2*(304.36 *2.205) #kg to lbs
# Payload Weight
W_payload = 2000 

print(f'Wing Weight = {W_wing}')
print(f'Horizontal Tail Weight = {W_ht}')
print(f'Vertical Tail Weight = {W_vt}')
print(f'Fuselage Weight = {W_fuselage}')
print(f'Main Landing Gear Weight = {W_mainlandinggear}')
print(f'Tail Landing Gear Weight = {W_taillandinggear}')
print(f'Installed Engine Weight = {W_installedengine}')
print(f'Fuel System Weight = {W_fuelsystem}')
print(f'flight Controls Weight = {W_flightcontrols}')
print(f'Hydraulics Weight = {W_hydraulics}')
print(f'Avionics Weight = {W_avionics}')
print(f'Electrical Weight = {W_electrical}')
print(f'Furnishings Weight = {W_furnishings}')
print(f'Battery Weight = {W_battery}')
print(f'Payload Weight = {W_payload}')
total_weight = W_wing+W_ht+W_vt+W_fuselage+W_mainlandinggear+W_taillandinggear+W_installedengine+W_fuelsystem+W_flightcontrols+W_hydraulics+W_avionics+W_electrical+W_furnishings+W_battery+W_payload
print(f'Total Weight = {total_weight}')