# Cost Analysis

# Cost Analysis Calculations

import math
from sympy import symbols, Eq, solve
import pandas as pd


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
Q_m = 7.5 #number of aircraft produced in one month

then_year = 2025
R_eng = 2.576*then_year-5058
print(f'Rate of engineering is {R_eng}')
R_tool = 2.883*then_year-5666
print(f'Rate of tooling is {R_tool}')
R_qc = 2.60*then_year-5112
print(f'Rate of qc is {R_qc}')
R_manufacturing = 2.316*then_year-4552
print(f'Rate of manufacturing is {R_manufacturing}')
cpi = 1 #THIS IS A PLACEHOLDER LOOK UP EQN LATER!!!!!!!

R_eng = 92
R_tool = 61
R_manufacturing = 53
R_qc = 60
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
C_tool = 2.1036*W_airframe**0.764*V_max**0.899*Q**0.178*Q_m**0.066*F_taper*F_cf*F_comp*F_press*F_hye*R_tool*cpi
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



