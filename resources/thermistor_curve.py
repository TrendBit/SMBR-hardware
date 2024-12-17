import numpy as np
import matplotlib.pyplot as plt

def thermistor_voltage_curve(beta, t_nominal, r_nominal, r_top, temp_range):
    """
    Calculate and plot the voltage curve of a thermistor in a voltage divider.

    Parameters:
        beta (float): Beta coefficient of the thermistor (in K).
        t_nominal (float): Nominal temperature (in Celsius) at which r_nominal is defined.
        r_nominal (float): Resistance of the thermistor at t_nominal (in ohms).
        r_top (float): Value of the top resistor in the voltage divider (in ohms).
        temp_range (tuple): Range of temperatures (in Celsius) as (min_temp, max_temp, step).
    """
    # Convert nominal temperature to Kelvin
    t_nominal_k = t_nominal + 273.15

    # Generate temperature values in the specified range and convert to Kelvin
    temperatures_c = np.arange(*temp_range)
    temperatures_k = temperatures_c + 273.15

    # Calculate thermistor resistance at each temperature using the Steinhart-Hart equation
    r_thermistor = r_nominal * np.exp(beta * ((1 / temperatures_k) - (1 / t_nominal_k)))

    # Calculate voltage across the thermistor in the voltage divider
    v_in = 5.0  # Assume a 5V input to the divider
    v_out = (v_in * r_thermistor) / (r_top + r_thermistor)

    # Normalize voltage to range 0-1 for ADC simulation
    v_out_normalized = v_out / v_in

    # Plot the curve
    plt.figure(figsize=(8, 6))
    plt.plot(v_out_normalized, temperatures_c, label="Temperature vs. ADC Value")
    plt.xlabel("Normalized ADC Value (0 to 1.0)")
    plt.ylabel("Temperature (°C)")
    plt.title("Thermistor Voltage Divider Output")
    plt.grid(True)
    plt.legend()
    plt.show()

# Example usage:
beta_value = 3950          # Beta coefficient in K
t_nominal = 25             # Nominal temperature in Celsius
r_nominal = 100000          # Resistance at nominal temperature in ohms
r_top = 100000               # Top resistor value in ohms
temp_range = (-50, 150, 1) # Temperature range: min, max, step

thermistor_voltage_curve(beta_value, t_nominal, r_nominal, r_top, temp_range)
