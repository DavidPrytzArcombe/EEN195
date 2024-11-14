# EEN195
# DCDC converter design
import numpy as np

# Switcing frequency
f_sw = 500*10**3
slew_rate = 0.5*10**6
R_T = 41550000 / f_sw - 2.2
print(R_T)

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
L_o = V_out_nom * (V_in_max - V_out_nom) / (V_in_max * I_ripple * f_sw)

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
C_in = 10*10**-6
Delta_V_in = (I_out + I_ripple / 2) / (4 * C_in * f_sw)

# Soft start
T_ss = 5 * 10**-3
I_ss = 1*10**-6
C_ss = T_ss * I_ss / (V_out_nom * 0.8)


# Output voltage resistors
R_ratio = 5/0.6-1
R_l = 10**3
R_u = R_l*R_ratio


print('Output inductor:', L_o*10**6, 'µH')
print('Output capacitor:', C_out*10**6, 'µF')
print('ESR:',ESR,'Ω')