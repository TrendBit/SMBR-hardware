# Changelog

## [Unreleased] Control board v1.2
#### Changed
- Update LED driver input filter values in order to work in both modes:
    - Analog mode, limited to range 25-100% with input frequency of 1 MHz
    - PWM mode, full range but flickering at input frequency of 1 kHz

- Unify motor current sensing resistors for all driver to 150mR
    - Lower threshold cause issues with inrush current
    - Assembly price is lower with only one type of component instead of three types

#### Fixed
- Reduce value of motor filtering capacitors to 10nF (from 1uf)
    - Because sometimes triggered over-current protection of driver 

## Control board v1.1

#### Added
- Bulk capacitance to motor drivers
- Additional decoupling capacitor to motor drivers
- Table in schematic with mapping between GPIOs and PWM channels or PIOs
- Add project logo to backside of board

#### Fixed
- Orientation of LED connector and its silkscreen marking is now compatible with Illumination board (Basic RGBW)
    - Swap LED channels (0<->3, 1<->2)
- Modify Fan MOSFET to correct footprint

#### Changed
- Update values of LED signaling resistors for more uniform light intensity
- Change CAN receiver R_s resistor in order to select high-speed mode
    - This could result in higher electromagnetic emission (but almost negligible)
- Select higher precision (5.1k - 0.1%) resistors for temperature sensing
- Exchange on board thermistor for one with more suitable curve (beta 3050 -> 3950)
    - Also package change from 0402 to 0603 (unification of case sizes)
- Update resistor values of fan tachometric filter
    - Cutoff frequency of filter is set to 50Hz
- Change values of motor driver sense resistor
    - Each driver has now different value in order to limit peak current
    - This also enables current control of motor
- Change GPIO connections to have Motor Inputs (IN1, IN2, VREF) controlled by PWM
    - This will enabled motor PWm control with or without current limiting
    - As part of this LED2 was moved from GPIO22 to GPIO24

