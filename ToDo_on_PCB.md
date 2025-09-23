# Pump board v 1.1
- [ ] Fix incorrect type of Barrel jack connector

# Fluoro LED board v1.3
- [ ] Change PCB from aluminum backed to normal FR4 with heat vias
    - In this case connectors can be used
- [ ] Use one 4-pin connector for  to reduce number of wires

# Sensor board v1.2
- [ ] Add protection resistors to SWD connector (100R) based on pico-probe
- [ ] Connect Fluorometer LED with 3 or 4 wire cable

# Control board v1.3
- [ ] Add protection resistors to SWD connector (100R) based on pico-probe
- [ ] Reduce input current limitation on FAN control MOSFETs
    - Those resistors limits how fast can FAN MOSFET close and open
- [ ] Mark CAN bus resistors as DNP (those should be placed on Sensor module)
    - Or make them possible to enable by resistor

