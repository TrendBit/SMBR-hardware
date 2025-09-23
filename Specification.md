# General specification for SMBR modules
This specification describes the characteristics of modules that should be adhered to under ideal conditions when developing new modules. The purpose is to ensure maximum consistency between modules and thus increase the compatibility of firmware modules and components. However, this should not be at the expense of reduced functionality or user discomfort. 

## MCU
For maximum FW compatibility (modules, components, libraries), the RP2040 microcontroller from the RaspberryPi Foundation should be used. Alternatively, if it is not suitable, then the RP2354 or other future models can be used, provided they are compatible with the FW base. The advantage of using the same MCU is, for example, that identical code can be used for CAN bus content, message routing, and administrative message processing, regardless of which module it is located on. The standard MCU speed is 200 MHz with a 12 MHz crystal.

#### CAN Bus
The bus interface is ideally connected to the GPIO_4(TX) and GPIO_5(RX) pins of the MCU. The converter is capable of reaching speeds of 1 Mbit/s (e.g., SN65HVD230 in HighSpeed mode), but the actual speed used is 500 kB/s. Overvoltage protection on bus lines. Termination should be on the furthest module, but due to potentially strong interference, it is primarily expected on the Sensor module. If termination is installed on other modules by default, it should be disconnectable using a switch/jumper/pin header. The second termination is permanently installed on the Interface module.

#### Flash Memory
Externally connected QSPI Flash memory for the MCU program. It should not be used for storing persistent data (calibration) but for the program (main and bootloader). Minimum size 16 MBit(MB). To store application data, the module should contain some additional memory, such as I2C EEPROM. 

EEPROM is used as standard memory and connected to I2C1 on pins GPIO18/19 with address 0x50 (7-bit). It is used to store information about the module and its instance.

## Interfaces
Standard interfaces used for communication with the board. CAN bus is the only application interface; the others are used for development and debugging.

#### USB-Type C
Port enabling data transfer via USB FS with UBS Type-C connector. It is connected to the MCU's USB_Dx pins. It must contain CC pull-down resistors (2x 5.1k) and should enable power supply to the device via USB so that the module's firmware can be updated.

It allows you to upload a CAN bootloader (catapult) or standard application firmware for testing using a USB bootloader. It can also be used to connect to the module's CLI interface, which contains information about when the system was built and can provide additional development tools.

#### UART + SWD
Development interface enabling FW stepping with the help of a connected debug probe. The use of an RPi Debug probe is primarily assumed, which corresponds to the pinout of the connectors. The FW logger output is connected to the serial port, but the logger must be enabled in the FW configuration and set to a sufficient level. The serial port speed is 921600 baud.

#### CAN connector
Connector for CAN BUS application interface. It can exist in multiple form factors, but two are most common are 10-pin IDC connector for internal connections within the device and external SATA connector (7-pin).

#### Tag connector
The tag connector is an alternative programming connector that allows you to work with the board when connected via pogo pins (available as a special counterpart). It contains SWD and a serial link. Its primary use is for quick connection to the board for the purpose of changing the firmware.

#### Version resistors
A divider consisting of two resistors that defines the HW version of its output voltage. The resistor values for each version should be identical between modules. The divider is connected to the ADC0 input of the RP2040 MCU.

Values (1% precision):
| Version | R_V1 | R_V2 | Voltage |
|---------|------|------|---------|
|   X.0   |  1k  |  10k |  3.00 V |
|   X.1   |  10k |  1k  |  0.30 V |
|   X.2   |  10k | 5.1k |  1.11 V |
|   X.3   | 5.1k |  10k |  2.18 V |
|   X.4   | 5.1k |  1k  |  0.54 V |
|   X.5   |  1k  | 5.1k |  2.76 V |


Reserved values:
0V, 3.3V, 1.65V

#### Buttons
Buttons for basic control of the board. These are the reset and boot buttons. The reset button is connected to the MCU RUN pin. Pressing it resets the MCU, pressing it twice in quick succession starts the built-in CAN bootloader and pauses the boot process so that the FW can be uploaded via CAN. However, the CAN bootloader must already be uploaded to the system in some way (it can also be together with the application FW). Holding down the BOOT button during startup or reset activates the USB bootloader, allowing you to upload the CAN bootloader, application firmware, or both. The BOOT button is connected to the CS pin of the Flash memory.

#### LEDs
Each module should contain at least one primary diagnostic LED (LED1) indicating the status of the device. This LED should be visible to the user without major modifications to the device. The preferred color of this signal LED is green, and it should be on pin GPIO24 of the RP2040 MCU. This LED is configurable for each module, so it can be set using FW. However, it is also used by the bootloader (Katapult) and should therefore be on the same pin on all devices, as this allows the same bootloader firmware to be used on all boards. The function of this LED is defined by an abstract class from which all modules are derived, and its behavior is therefore the same for all modules. During bootloader operation, it flashes slowly (1 Hz) and indicates the firmware flashing process. During application operation, it flashes quickly (2.5 Hz) and stops flashing in the event of a critical error.

It is recommended to connect the secondary LED (LED2) to GPIO25 MCU, and it should be yellow. The function of this LED is not defined, but it should indicate ongoing processes related to a specific function of the model (for example, OJIP measurement on the sensor module).

Additional red LEDs should ideally indicate active power branches. This can be used to detect power supply problems, for example, in external modules that may be powered by a hybrid power supply.

#### Enumeration interface
Button and indicator LED designed for modules that allow multiple instances in the system, such as the pump module. Pressing the button sets the instance, which is then indicated by the color of the LED. The button is normally connected to GPIO22. An RGB LED is used as the LED and can be controlled arbitrarily, but it is recommended to use a single-pin addressing protocol (such as WS2818) on GPIO23. 
