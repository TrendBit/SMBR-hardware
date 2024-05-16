# RPI - Can bus  

 - Add overlay to load during boot to `/boot/firmware/config.txt`  
```  
dtparam=spi=on  
dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000  
```  
- Install tool: `sudo apt-get install can-utils`  
- Setup interface: `sudo ip link set can0 up type can bitrate 1000000`  
- Persistently configure interface in file `/etc/network/interfaces`
```
auto can0
iface can0 can static
        bitrate 1000000
```

## Test  
CAN interface can be setup in loopback mode.  
```  
sudo ip link set can0 down  
sudo ip link set can0 type can bitrate 1000000 loopback on  
sudo ip link set can0 up type can bitrate 1000000  
```  
In two terminals run this commands:  
Term #1 - `candump can0`  
Term #2 - `cansend can0  000#11.22.33.44`  

Result should be two lines (one for send, one for receive via loopback):
```
  can0  000   [4]  11 22 33 44
  can0  000   [4]  11 22 33 44
```
If interface is not setup as loopback no data will be visible in `candump` because frame was not ACKed.
