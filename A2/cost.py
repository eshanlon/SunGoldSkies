# Cost Analysis
# Cost Analysis Calculations


import math


'''Notes:
- All eqns are assumed from metabook unless specified
'''
# Defined Parameters
b_year = 2025
t_year = 2035
mtow = 8000 #lbs
W_e = 6000 #lbs - empty takeoff weight
W_1 = 200 #lbs - weight of landing gear
W_2 = 200 #lbs - weight of engine, motor, batteries
W_3 = 200 #lbs - weight of avionics and instruments
W_4 = 20 #lbs - weight of oil
hp = 180 #horsepower
kWh = 10 #kWh of engine or motor
V_max = 250 #knts - max design speed
N_rdte = 4 #number of airframes/airplanes used for testing, 2-8 for commercial programs
F_diff = 1.5
F_cad = 0.8
W_b = 100
P_elec = 20
e_elec = 10

# def cost(b_year, t_year, mtow, W_e, W_1,W_2, W_3, W_4, hp, kWh, V_max, N_rdte, F_diff, F_cad, C_fin_r):

# Adjusting for Inflation
b_cef = 5.17053 + 0.104981*(b_year - 2006)
t_cef = 5.17053 + 0.104981*(t_year - 2006)
cef = t_cef/b_cef
print(f'The cef is {cef}')


# Aircraft Price
#prices for aircraft and engine are for non-electric airplanes
#this is compensated for in C_elec_aircraft
C_aircraft = 10**(-0.6681 + 1.5799*math.log10(mtow)) * cef
# the eqn above was found in Roskam Part VII Appendix A
# "engine type does not seem to have significant effect on ag. airplane price"
C_engines = 10**(2.5262 + 0.9465*math.log10(hp)) * cef
#the above eqn is only valid for 400-5,000 shaft hp
C_motors = 150*hp * cef
C_batteries = 520*kWh * cef


C_elec_aircraft = C_aircraft - C_engines + C_motors + C_batteries
print(f'The predicted electric aircraft price is {C_elec_aircraft}')




#RDT&E Costs (using Roskam)
R_e = 40 #engineering manhour rate USD/hour
W_amp = W_e - (W_1 + W_2 + W_3 + W_4) #weight of just airplane shell (engines, landing gear, avionics, etc... ommited)
#alternative W_amp is below if doen't know component weights (less accurate):
W_amp = 10**(0.1936 + 0.8645(math.log10(mtow)))
C_aed_r = (0.0396*W_amp**0.791 * V_max**1.526 * N_rdte**0.183 * F_diff*F_cad) * R_e


N_e = 1 #number of engines
C_p = 1000 #cost per propeller, see appendix B in Roskam to actually calculate
N_p = 1 #number of propellers
C_avionics = 1000 #avionics cost, see appendix C for acutla calculation
N_st = 2 #number of statis test airplanes
C_ea = (C_engines*N_e + C_p*N_p + C_avionics)*(N_rdte-N_st)
C_dst_r = 0.008325*W_amp**0.873 * V_max**1.89 * N_rdte**0.346 * cef * F_diff
R_m = 30 #manufacturing labor rate, see figure 3.4 and note after eqn 3.6
C_man = (28.984*W_amp**0.740 * V_max**0.543 * N_rdte**0.524 * F_diff) * R_m
F_mat = 2 #changes depending on what material you use, page 31
C_mat = 37.632*F_mat*W_amp**0.689 * V_max**0.624 * N_rdte**0.792 * cef
N_r = 0.33 #rdte production rate in units per month, typically 0.33
C_tool = (4.0127*W_amp)**0.764 * V_max**0.899 * N_rdte**0.178 * N_r**0.066 * F_diff
C_qc = 0.13*C_man
C_fta_r = C_ea + C_man +C_mat + C_tool + C_qc
F_obs = 1.0 #importance of having low observables, with no stealth requirement = 1.0
C_fto_r = 0.001244*W_amp**1.60 * V_max**1.371 * (N_rdte-N_st)**1.281 * cef * F_diff * F_obs
C_tsf_r = 0 #if no extra test facilities are required
F_pro = 0.10 #suggested profit of 10%


# C_rdte = C_aed_r + C_dst_r + C_fta_r + C_fto_r + C_tsf_r + (C_rdte * F_pro) + C_fin_r






#Fly away cost per airplane for 10% profit margin




# Direct Operating Costs (COC + FOC)
#COC
C_elec = 1.05*W_b*P_elec*e_elec #1.05 is charging effeciency

#oil is negligable because all electric
#we are assuming maintenance costs are negligible (metabook says to)





# Cost Analysis Calculations

import math

'''Notes:
- All eqns are assumed from metabook unless specified
'''
# Defined Parameters
b_year = 2025
t_year = 2035
mtow = 8000 #lbs
W_e = 6000 #lbs - empty takeoff weight
W_1 = 200 #lbs - weight of landing gear
W_2 = 200 #lbs - weight of engine, motor, batteries
W_3 = 200 #lbs - weight of avionics and instruments
W_4 = 20 #lbs - weight of oil
hp = 180 #horsepower
kWh = 10 #kWh of engine or motor
V_max = 250 #knts - max design speed
N_rdte = 4 #number of airframes/airplanes used for testing, 2-8 for commercial programs
F_diff = 1.5
F_cad = 0.8

# Adjusting for Inflation
b_cef = 5.17053 + 0.104981*(b_year - 2006)
t_cef = 5.17053 + 0.104981*(t_year - 2006)
cef = t_cef/b_cef
print(f'The cef is {cef}')

# Aircraft Price
#prices for aircraft and engine are for non-electric airplanes
#this is compensated for in C_elec_aircraft
C_aircraft = 10**(-0.6681 + 1.5799*math.log10(mtow)) * cef
# the eqn above was found in Roskam Part VII Appendix A
# "engine type does not seem to have significant effect on ag. airplane price"
C_engines = 10**(2.5262 + 0.9465*math.log10(hp)) * cef
#the above eqn is only valid for 400-5,000 shaft hp
C_motors = 150*hp * cef
C_batteries = 520*kWh * cef

C_elec_aircraft = C_aircraft - C_engines + C_motors + C_batteries
print(f'The predicted electric aircraft price is {C_elec_aircraft}')


#RDT&E Costs (using Roskam)
R_e = 40 #engineering manhour rate USD/hour
W_amp = W_e - (W_1 + W_2 + W_3 + W_4) #weight of just airplane shell (engines, landing gear, avionics, etc... ommited)
#alternative W_amp is below if doen't know component weights (less accurate):
W_amp = 10**(0.1936 + 0.8645(math.log10(mtow)))
C_aed_r = (0.0396*W_amp**0.791 * V_max**1.526 * N_rdte**0.183 * F_diff*F_cad) * R_e

N_e = 1 #number of engines
C_p = 1000 #cost per propeller, see appendix B in Roskam to actually calculate
N_p = 1 #number of propellers
C_avionics = 1000 #avionics cost, see appendix C for acutla calculation
N_st = 2 #number of statis test airplanes
C_ea = (C_engines*N_e + C_p*N_p + C_avionics)*(N_rdte-N_st)
C_dst_r = 0.008325*W_amp**0.873 * V_max**1.89 * N_rdte**0.346 * cef * F_diff
R_m = 30 #manufacturing labor rate, see figure 3.4 and note after eqn 3.6
C_man = (28.984*W_amp**0.740 * V_max**0.543 * N_rdte**0.524 * F_diff) * R_m
F_mat = 2 #changes depending on what material you use, page 31
C_mat = 37.632*F_mat*W_amp**0.689 * V_max**0.624 * N_rdte**0.792 * cef
N_r = 0.33 #rdte production rate in units per month, typically 0.33
C_tool = (4.0127*W_amp)**0.764 * V_max**0.899 * N_rdte**0.178 * N_r**0.066 * F_diff
C_qc = 0.13*C_man
C_fta_r = C_ea + C_man +C_mat + C_tool + C_qc
F_obs = 1.0 #importance of having low observables, with no stealth requirement = 1.0
C_fto_r = 0.001244*W_amp**1.60 * V_max**1.371 * (N_rdte-N_st)**1.281 * cef * F_diff * F_obs
C_tsf_r = 0 #if no extra test facilities are required 
F_pro = 0.10 #suggested profit of 10%
F_fin = 0.1 #interest rate

C_rdte = C_aed_r + C_dst_r + C_fta_r + C_fto_r + C_tsf_r + (C_rdte * F_pro) + (C_rdte + F_fin)



#Fly away cost per airplane for 10% profit margin


# Direct Operating Costs (COC + FOC)
#we are assuming maintenance costs are negligible (metabook says to)

