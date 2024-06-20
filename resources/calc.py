# MP3306  calculation

# Minimal required inductance

efficiency = 0.9
v_out = 14.5
v_in = 12
frequency = 700000
I_load = 0.75

duty_cycle = 1 - (v_in/v_out)

L = (efficiency * v_out * duty_cycle * (1-duty_cycle**2))/(2 * frequency * I_load)

print("Duty cycle = {} %".format(round(duty_cycle*100,2)))
print("Minimal inductance = {} uH".format(round(L*1000000,3)))

# Sense resistor

R_sense = 0.202/I_load

print("Sense resistor = {} Ω".format(round(R_sense,3)))

# Maximal load current

selected_inductance = 15 # uH
peak_current_limit = 1.9 # A

I_load_max = (peak_current_limit - (v_in*duty_cycle)/(2*selected_inductance*frequency))*(1-duty_cycle)*0.8

print("Maximum load current with {} uH inductor = {} A".format(selected_inductance,round(I_load_max,2)))

# OVP threshold

ovp_th = 15.5 # V

r2 = 100 # kR

r3 = (r2*1.22)/(ovp_th-1.22)

print("Values of OVP settings resistor R3 = {} kΩ with R2 = {} kΩ for OVP of {} V".format(round(r3,2),r2, ovp_th))

# PWM filtration capacitor

R_internal = 100000 # Ω

dimming_frequency = 10000 # Hz

dimming_period = 1/dimming_frequency

C_pwmo = (10*dimming_period)/R_internal

print("For {} kHz dimming frequency, filtering capacitor should have value at least {} nF".format(dimming_frequency/1000,C_pwmo*1000000000))
