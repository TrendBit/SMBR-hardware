# v1.0

- #1 - Reset pin of CAN transceiver (MCP2515) should be tied to 3.3V otherwise chip will not be registered in RPi
    - Fix: Short pin 19 (RESET) to neighbor pin 20 (VCC) with solder, but it is better to use 10kR resistor
