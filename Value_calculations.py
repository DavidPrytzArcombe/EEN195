# EEN195
# DCDC converter design
import numpy as np

# Switcing frequency
f_sw = 500*10**3
slew_rate = 0.5*10**6
R_T = 41550000 / f_sw - 2.2

# Input voltages
V_in_nom = 14.5
V_in_max = 16
V_in_min = 9

# Output voltages
V_out_nom = 5
V_out_min = 4.75
V_out_max = 5.25

# Output current
I_out = 3
I_out_min = 0.1
I_ripple_percentage = 0.3
I_ripple = I_out * I_ripple_percentage

# Output inductor
L_o = V_out_nom * (1 - V_out_nom / V_in_max) / (I_ripple * f_sw)

# Output capacitor
# 1. Maintain output current
Delta_I = slew_rate / f_sw
Delta_V = V_out_max - V_out_nom
C_out1 = 2 * Delta_I / (f_sw * Delta_V)

# 2. Absorbing energy during rapid load decrease
C_out2 = L_o * (I_out**2 - I_out_min**2) / (V_out_max**2 - V_out_nom**2)

# 3. Handle output voltage ripple
V_ripple = V_out_max - V_out_min
C_out3 = 1/(8 * f_sw) * I_ripple / (V_ripple)

C_out = np.max([C_out1, C_out2, C_out3])

# 4. ESR
ESR = V_ripple/I_ripple

# 5. RMS output capacitor current
I_co_rms = V_out_nom * (V_in_max - V_out_nom) / (np.sqrt(12) * V_in_max * L_o * f_sw)


# Input capacitor
# Ceramic
eta = 0.85
dc = V_out_nom / (V_in_nom * eta)
V_Pmax = 75 * 10**-3
C_in = I_out * dc * (1 - dc) / (f_sw * V_Pmax)
Delta_V_in = (I_out + I_ripple / 2) / (4 * C_in * f_sw)
I_cin_rms = I_out * V_out_nom / V_in_nom * np.sqrt(V_in_nom / V_out_nom - 1)

# Bulk
Delta_V_in = 0.35
L_f = 1*10**-6
I_tr = 3.16 - 0.05
C_bulk = 1.21 * I_tr**2 * L_f / Delta_V_in**2
print('Input bulk capacitance:','%.2f' % (C_bulk*10**6),'µF')


# Soft start
T_ss = 40* 10**-3
I_ss = 1*10**-6
C_ss = T_ss * I_ss / 0.6


# Output voltage resistors
R_ratio = 5/0.6-1
R_FB1 = 20*10**3
R_FB2 = R_FB1*R_ratio


# Bootstrap capacitor
Q_g = 9.4 * 10**-9
INTVCC_min = 4.6
U_schottky = 0.2
C_b = Q_g / (INTVCC_min - U_schottky) * 100

print('Output inductor:', '%.2f' % (L_o*10**6), 'µH')
print('Output capacitor:', '%.2f' % (C_out*10**6), 'µF')
print('ESR:','%.2f' % ESR,'Ω')
print('R_FB1:','%.2f' % (R_FB1/1000),'kΩ')
print('R_FB2:','%.2f' % (R_FB2/1000),'kΩ')
print('R_T:','%.2f' % R_T,'Ω')
print('C_b:','%.2f' % (C_b*10**9),'nF')
print('C_ss:','%.2f' % (C_ss*10**9),'nF')
print('Ceramic input capacitance:','%.2f' % (C_in*10**6),'µF')
print('I_cin_rms:','%.2f' % I_cin_rms,'A')