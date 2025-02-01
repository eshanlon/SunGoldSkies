import math
from sympy import symbols, Eq, solve
from openpyxl import load_workbook
import pandas as pd


def cost_analysis(filepath):

    # Cost Analysis
    # Cost Analysis Calculations


    # Read the Excel file
    data = pd.read_excel(filepath, header=None)  # Read without headers if not needed
    excel = load_workbook(filepath)
    cost_sheet = excel.active

    # Parameters
    W_mtow = data.iloc[0,1]
    W_empty = data.iloc[1,1]
    W_airframe = data.iloc[2,1]
    W_b = data.iloc[3,1] #weight of battery in kg
    V_max = data.iloc[4,1]
    Q = data.iloc[5,1]
    Q_m = data.iloc[6,1]
    base_year = data.iloc[7,1]
    then_year = data.iloc[8,1]
    N_motor = data.iloc[9,1]
    N_engine = N_motor #for the type of hybrid electric we are doing
    P_em = data.iloc[10,1] #hp
    P_em_total = data.iloc[11,1]
    E_bat = data.iloc[12,1] #battery capacity
    e_elec = data.iloc[13,1] #specific energy of the battery in Wh/kg
    P_elec = data.iloc[14,1] #price of electricity in $/kWh
    N_prop = data.iloc[15,1]
    D_p = data.iloc[16,1]
    P_shp = data.iloc[17,1]
    R_L = data.iloc[18,1] #maintainence labor rate in USD/hr
    t_b = data.iloc[19,1] #mission block time in hours
    IR_a = data.iloc[20,1] #hull insurance rate usually assumed to be 2% according to metabook
    K_depreciation = data.iloc[21,1] #aircraft residual value factor
    n = data.iloc[22,1] #number of years the aircraft is used
    W_f = data.iloc[23,1]  # Weight of fuel lbs
    P_f = data.iloc[24,1]  # Price per gallon of jet fuel USD/gal
    rho_f = data.iloc[25,1]  # Fuel density lbs/gal
    P_oil = data.iloc[26,1]  # Cost per gallon of oil USD/gal
    rho_oil = data.iloc[27,1]  # Density of oil
    SHP_TO = data.iloc[28,1]  # Takeoff shaft horsepower
    H_em = data.iloc[29,1]  # Number of hours between engine overhauls (usually between 3000-5000)
    P_ice = data.iloc[30,1]  #ICE power
    print(f'P_ice = {P_ice}')

    #Adjustment factors table
    data_subset = data.iloc[33:40, 1:7]  # .iloc[row_start:row_end, col_start:col_end]
    cost_parameters = data_subset.to_numpy()
    print(cost_parameters)

    ###################### Development Costs #############################################################
    #Labor Rates
    R_eng = 2.576*then_year-5058
    R_tool = 2.883*then_year-5666
    R_qc = 2.60*then_year-5112
    R_manufacturing = 2.316*then_year-4552
    cpi = 1.39 #2012 to 2025 dollars since Finger wrote in 2021

    #Cost of Engineering
    F_cert = cost_parameters[0,0]
    F_comp = cost_parameters[0,1]
    F_taper = cost_parameters[0,2]
    F_cf = cost_parameters[0,3]
    F_press = cost_parameters[0,4]
    F_hye = cost_parameters[0,5]
    C_eng = 0.083*W_airframe**0.791*V_max**1.521*Q**0.183*F_cert*F_cf*F_comp*F_press*F_hye*R_eng*cpi
    print(C_eng)

    #Tooling Costs
    F_cert = cost_parameters[1,0]
    F_comp = cost_parameters[1,1]
    F_taper = cost_parameters[1,2]
    F_cf = cost_parameters[1,3]
    F_press = cost_parameters[1,4]
    F_hye = cost_parameters[1,5]
    C_tool = 2.1036*W_airframe**0.764*V_max**0.899*Q**0.178*Q_m**0.066*F_taper*F_cf*F_comp*F_press*F_hye*R_tool*cpi
    print(C_tool)

    #Manufacturing Costs
    F_cert = cost_parameters[2,0]
    F_comp = cost_parameters[2,1]
    F_taper = cost_parameters[2,2]
    F_cf = cost_parameters[2,3]
    F_press = cost_parameters[2,4]
    F_hye = cost_parameters[2,5]
    C_manufacturing = 20.2588*W_airframe**0.74*V_max**0.543*Q**0.524*F_cert*F_cf*F_comp*F_hye*R_manufacturing*cpi
    print(C_manufacturing)

    #Development Support Costs
    F_cert = cost_parameters[3,0]
    F_comp = cost_parameters[3,1]
    F_taper = cost_parameters[3,2]
    F_cf = cost_parameters[3,3]
    F_press = cost_parameters[3,4]
    F_hye = cost_parameters[3,5]
    C_dev = 0.06458*W_airframe**0.873*V_max**1.89*Q**0.346*F_cert*F_cf*F_comp*F_press*F_hye*cpi
    print(C_dev)

    #Flight Test Operations Costs
    F_cert = cost_parameters[4,0]
    F_comp = cost_parameters[4,1]
    F_taper = cost_parameters[4,2]
    F_cf = cost_parameters[4,3]
    F_press = cost_parameters[4,4]
    F_hye = cost_parameters[4,5]
    C_ft = 0.009646*W_airframe**1.16*V_max**1.3718*Q**1.281*F_cert*F_hye*cpi
    print(C_ft)

    #Quality Control Costs
    F_cert = cost_parameters[5,0]
    F_comp = cost_parameters[5,1]
    F_taper = cost_parameters[5,2]
    F_cf = cost_parameters[5,3]
    F_press = cost_parameters[5,4]
    F_hye = cost_parameters[5,5]
    C_qc = 0.13*C_manufacturing*F_cert*F_comp*F_hye
    print(C_qc)

    #Materials Cost
    F_cert = cost_parameters[6,0]
    F_comp = cost_parameters[6,1]
    F_taper = cost_parameters[6,2]
    F_cf = cost_parameters[6,3]
    F_press = cost_parameters[6,4]
    F_hye = cost_parameters[6,5]
    C_mat = 24.896*W_airframe**0.689*V_max**0.624*Q**0.792*cpi*F_cert*F_cf*F_press*F_hye
    print(C_mat)

    #Electric Motor Cost
    C_em = 174*N_motor*P_em*cpi

    #Power Management System Cost
    C_pms = 150*P_em_total*cpi

    #Battery Cost
    C_bat = 200*E_bat*cpi

    #Propeller Cost
    C_prop = 210*N_prop*cpi*D_p**2*(P_shp/D_p)**0.12

    #Internal Combustion Engine Cost
    C_engines = 174*N_engine*P_ice*cpi

    #Misc. Cost
    C_lg = -7500 #fixed landing gear cost
    C_av = 4500 #avionics cost

    #Quality Discount Factor
    F_exp = 0.95
    qdf = F_exp**(1.4427*math.log(Q))

    #Total Cost to Produce
    C_total = C_eng+C_tool+C_dev+C_ft+C_qc+qdf*(C_mat+C_manufacturing+Q*(C_em+C_pms+C_bat+C_prop+C_lg+C_av))
    print(f'C_total = {C_total}')
    C_profit = (0.1*C_total)/Q
    C_aircraft = C_total/Q

    C_rdte = C_eng+C_tool+C_manufacturing+C_dev+C_ft+C_qc+C_mat

    #Sales Price
    C_sales = C_aircraft+C_profit



    ################## Direct Operating Costs (COC + FOC) ####################################
    # Adjusting for Inflation
    b_cef = 5.17053 + 0.104981*(base_year - 2006)
    t_cef = 5.17053 + 0.104981*(then_year - 2006)
    cef = t_cef/b_cef


    #COC
    c_motors = 150*P_em  # $150/hp using 2018 base year
    c_batteries = 520*E_bat  # $520/kWh using 2018 base year
    C_fuel = 1.02*W_f*(P_f/rho_f)
    W_oil = 0.0125 * W_f * (t_b/100)
    C_oil = 1.02 * W_oil * (P_oil/rho_oil)
    C_elec = 1.05*W_b*P_elec*e_elec #1.05 is charging effeciency
    C_ML_air = 1.03*(3+((0.67*W_airframe)/1000))*R_L
    C_MM = 1.03*(30*cef)+0.79e-5*(C_aircraft - C_em) #c_airframe = (C_aircraft - C_engines)
    C_ML_eng = 1.03*1.3*(0.4956+(0.0532*((SHP_TO/N_motor)/1000)*(1100/H_em))+0.1)*R_L
    C_eng_mtc = N_motor*(C_ML_eng+C_MM)*t_b
    C_elec_air = C_aircraft - C_engines + c_motors + c_batteries
    C_air_man = (C_ML_air +C_MM)*t_b
    coc = C_fuel + C_elec+C_oil+W_oil+ C_ML_air+ C_MM + C_ML_eng+C_air_man+C_eng_mtc+C_elec_air

    #FOC
    U_annual = (1.5e3)*((3.4546*t_b)+2.994-((12.289*(t_b)**2)-(5.6626*t_b)+8.964)**0.5)
    C_insurance = ((IR_a*C_aircraft)/U_annual)*t_b
    C_depreciation = (C_aircraft *(1-K_depreciation)*t_b)/(n*U_annual)
    doc_reg = coc + U_annual+C_insurance+C_depreciation
    C_registration = (0.001+((10**-8)*W_mtow))*doc_reg

    foc = U_annual + C_insurance + C_depreciation + C_registration

    doc = coc+foc

    #oil is negligable because all electric
    #we are assuming maintenance costs are negligible (metabook says to)

    ########## Outputting to Excel ######################
    cost_sheet["B44"] = C_rdte
    cost_sheet["B47"] = C_eng/Q
    cost_sheet["B48"] = C_tool/Q
    cost_sheet["B49"] = C_manufacturing/Q
    cost_sheet["B50"] = C_dev/Q
    cost_sheet["B51"] = C_ft/Q
    cost_sheet["B52"] = C_qc/Q
    cost_sheet["B53"] = C_mat/Q
    cost_sheet["B54"] = C_em
    cost_sheet["B55"] = C_pms
    cost_sheet["B56"] = C_bat
    cost_sheet["B57"] = C_prop
    cost_sheet["B58"] = C_lg
    cost_sheet["B59"] = C_av
    cost_sheet["B60"] = C_aircraft
    cost_sheet["B61"] = C_profit
    cost_sheet["B62"] = C_sales
    cost_sheet["B65"] = coc
    cost_sheet["B66"] = foc
    cost_sheet["B67"] = doc


    excel.save(filepath)
    print(f'Cost Analysis completed in {filepath}')

