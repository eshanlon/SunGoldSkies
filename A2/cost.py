# Cost Analysis

# Cost Analysis Calculations

import math
from sympy import symbols, Eq, solve
import pandas as pd

'''Notes:
- All eqns are assumed from metabook unless specified
'''
# Defined Parameters
#cost_parameters = pd.read_csv('A2\cost_estimate_sheet.csv')
#print(cost_parameters)



# Read the Excel file
data = pd.read_excel('A2\cost_estimate_sheet.xlsx', header=None)  # Read without headers if not needed

# Select the portion you want (e.g., rows 1 to 5 and columns 2 to 4)
subset = data.iloc[1:8, 1:7]  # .iloc[row_start:row_end, col_start:col_end]

# Convert the subset to a NumPy array
cost_parameters = subset.to_numpy()

print(cost_parameters)


#RDTE costs according to the slides
# Parameters
W_empty = 5000
#W_airframe = 0.40*W_empty
W_airframe = 1100
V_max = 180 #ktas
Q = 450 #number of aircraft produced in a 5 year period
then_year = 2035
R_eng = 2.576*then_year-5058
R_tool = 2.883*then_year-5666
R_qc = 2.60*then_year-5112
R_manufacturing = 2.316*then_year-4552
cpi = 1 #THIS IS A PLACEHOLDER LOOK UP EQN LATER!!!!!!!

###################### Development Costs #############################################################
#Cost of Engineering
start_row = 0
start_column = 0
F_cert = cost_parameters[start_row,start_column]
F_comp = cost_parameters[start_row,start_column+1]
F_taper = cost_parameters[start_row,start_column+2]
F_cf = cost_parameters[start_row,start_column+3]
F_press = cost_parameters[start_row,start_column+4]
F_hye = cost_parameters[start_row,start_column+5]
C_eng = 0.083*W_airframe**0.791*V_max**1.521*Q**0.183*F_cert*F_cf*F_comp*F_press*F_hye*R_eng*cpi
print(f'C_eng = {C_eng}')

#Tooling Costs
F_cert = cost_parameters[start_row+1,start_column]
F_comp = cost_parameters[start_row+1,start_column+1]
F_taper = cost_parameters[start_row+1,start_column+2]
F_cf = cost_parameters[start_row+1,start_column+3]
F_press = cost_parameters[start_row+1,start_column+4]
F_hye = cost_parameters[start_row+1,start_column+5]
C_tool = 2.1036*W_airframe**0.764*V_max**0.899*Q**0.178*F_taper*F_cf*F_comp*F_press*F_hye*R_tool*cpi
print(f'C_tool = {C_tool}')

#Manufacturing Costs
F_cert = cost_parameters[start_row+2,start_column]
F_comp = cost_parameters[start_row+2,start_column+1]
F_taper = cost_parameters[start_row+2,start_column+2]
F_cf = cost_parameters[start_row+2,start_column+3]
F_press = cost_parameters[start_row+2,start_column+4]
F_hye = cost_parameters[start_row+2,start_column+5]
C_manufacturing = 20.2588*W_airframe**0.74*V_max**0.543*Q**0.524*F_cert*F_cf*F_comp*F_hye*R_manufacturing*cpi
print(f'C_manufacturing = {C_manufacturing}')

#Development Support Costs
F_cert = cost_parameters[start_row+3,start_column]
F_comp = cost_parameters[start_row+3,start_column+1]
F_taper = cost_parameters[start_row+3,start_column+2]
F_cf = cost_parameters[start_row+3,start_column+3]
F_press = cost_parameters[start_row+3,start_column+4]
F_hye = cost_parameters[start_row+3,start_column+5]
C_dev = 0.06458*W_airframe**0.873*V_max**1.89*Q**0.346*F_cert*F_cf*F_comp*F_press*F_hye*cpi
print(f'C_dev = {C_dev}')

#Flight Test Operations Costs
F_cert = cost_parameters[start_row+4,start_column]
F_comp = cost_parameters[start_row+4,start_column+1]
F_taper = cost_parameters[start_row+4,start_column+2]
F_cf = cost_parameters[start_row+4,start_column+3]
F_press = cost_parameters[start_row+4,start_column+4]
F_hye = cost_parameters[start_row+4,start_column+5]
C_ft = 0.009646*W_airframe**1.16*V_max**1.3718*Q**1.281*F_cert*F_hye*cpi
print(f'C_ft = {C_ft}')

#Quality Control Costs
F_cert = cost_parameters[start_row+5,start_column]
F_comp = cost_parameters[start_row+5,start_column+1]
F_taper = cost_parameters[start_row+5,start_column+2]
F_cf = cost_parameters[start_row+5,start_column+3]
F_press = cost_parameters[start_row+5,start_column+4]
F_hye = cost_parameters[start_row+5,start_column+5]
C_qc = 0.13*C_manufacturing*F_cert*F_comp*F_hye
print(f'C_qc = {C_qc}')

#Materials Cost
F_cert = cost_parameters[start_row+6,start_column]
F_comp = cost_parameters[start_row+6,start_column+1]
F_taper = cost_parameters[start_row+6,start_column+2]
F_cf = cost_parameters[start_row+6,start_column+3]
F_press = cost_parameters[start_row+6,start_column+4]
F_hye = cost_parameters[start_row+6,start_column+5]
C_mat = 24.896*W_airframe**0.689*V_max**0.624*Q**0.792*cpi*F_cert*F_cf*F_press*F_hye
print(f'C_mat = {C_mat}')


'''
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
'''
'''
# Adjusting for Inflation
b_cef = 5.17053 + 0.104981*(b_year - 2006)
t_cef = 5.17053 + 0.104981*(t_year - 2006)
cef = t_cef/b_cef
print(f'The cef is {cef}')

#Fly away cost per airplane for 10% profit margin
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
C_elec_aircraft = C_elec_aircraft + C_elec_aircraft*0.10 #applying 10% profit margin
print(f'The predicted electric aircraft price is {C_elec_aircraft}')



'''




'''
#RDT&E Costs (using Roskam)
R_e = 40 #engineering manhour rate USD/hour
W_amp = W_e - (W_1 + W_2 + W_3 + W_4) #weight of just airplane shell (engines, landing gear, avionics, etc... ommited)
#alternative W_amp is below if doen't know component weights (less accurate):
W_amp = 10**(0.1936 + 0.8645*(math.log10(mtow)))
C_aed_r = (0.0396*W_amp**0.791 * V_max**1.526 * N_rdte**0.183 * F_diff*F_cad) * R_e

N_e = 1 #number of engines
#C_p = 10**(0.6119 + 1.1432*(math.log10(hp))) #for metal propeller, hp is supposed to be shp
C_p = 10**(0.7746 + 1.1432*(math.log10(hp))) #for composite propeller
N_p = 1 #number of propellers
C_avionics = 1000 #avionics cost, see appendix C for acutla calculation
# ok actually the apendix C is way to complicated to calc cost of avionics
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

C_rdte = symbols('C_rdte')
rdte_eqn = Eq(C_rdte, C_aed_r + C_dst_r + C_fta_r + C_fto_r + C_tsf_r + (C_rdte * F_pro) + (C_rdte * F_fin))
rdte_solution = solve(rdte_eqn, C_rdte)

print(f'The RDTE cost is {rdte_solution}')
'''


# Direct Operating Costs (COC + FOC)
#we are assuming maintenance costs are negligible (metabook says to)

