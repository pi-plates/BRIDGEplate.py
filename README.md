# BRIDGEplate Python Library

Python library for controlling Pi-Plates devices through the BRIDGEplate USB interface. Provides a single USB connection to control multiple Pi-Plates products including ADC, DAQC, DAQC2, CURRENT, DIGI, RELAY, RELAY2, and THERMO plates.

## Features

- **Cross-Platform Support** - Works on Windows, Linux, and macOS
- **Automatic Device Detection** - Finds BRIDGEplate via USB VID/PID
- **Multiple Pi-Plates Support** - Control up to 8 devices of each type
- **Comprehensive API** - Complete access to all Pi-Plates functions
- **Event-Driven Architecture** - Support for interrupts and events

## Supported Pi-Plates

| Plate | Description | Key Features |
|-------|-------------|--------------|
| **ADCplate** | High-precision analog input | 24-bit resolution, 8 single-ended or 4 differential inputs, 4-20mA current loop |
| **DAQCplate** | Data acquisition & control | 8 analog inputs (10-bit), 8 digital inputs, 7 digital outputs, 2 PWM, 2 DAC |
| **DAQC2plate** | Enhanced data acquisition | 16-bit ADC, RGB LED, 8 digital inputs, 8 digital outputs, PWMs, DACs, function generator, oscilloscope mode |
| **CURRENTplate** | Current measurement | 8 channels, high-precision current sensing |
| **DIGIplate** | Digital input & frequency | 8 digital inputs, frequency measurement on 6 channels |
| **RELAYplate** | Relay control | 7 electromechanical relays |
| **RELAY2plate** | Enhanced relay control | 8 electromechanical relays |
| **THERMOplate** | Temperature measurement | 8 thermocouple inputs (Type J/K), 4 DS18B20 inputs |

## Installation

### Requirements

```bash
pip install Pi-Plates
or
pip install --break-system-packages Pi-Plates
```

### Platform-Specific Setup

**Linux:**
```bash
# Add user to dialout group for serial port access
sudo usermod -a -G dialout $USER
# Logout and login for changes to take effect
```

**macOS:**
- Grant terminal permissions in **System Preferences > Security & Privacy**
- No additional setup typically required

**Windows:**
- No additional setup required
- USB drivers typically install automatically

## Quick Start

```python
from BRIDGEplate import *

# The module automatically connects to BRIDGEplate on import

# Poll for connected devices
POLL()

# Read analog input from DAQCplate at address 0
voltage = DAQC.getADC(0, 0)
print(f"Voltage: {voltage} V")

# Control relay on RELAYplate at address 1
RELAY.relayON(1, 1)  # Turn on relay 1

# Read temperature from THERMOplate at address 2
temp = THERMO.getTEMP(2, 1, 'c')  # Channel 1 in Celsius
print(f"Temperature: {temp}°C")
```

## Usage Examples

### ADCplate - High-Precision Analog Input

```python
from BRIDGEplate import *

addr = 0

# Read single-ended channel
voltage = ADC.getADC(addr, 0)  # Channels 0-7

# Read differential channel
diff_voltage = ADC.getADC(addr, 8)  # Channels 8-11

# Read 4-20mA current loop
current = ADC.getADC(addr, 12)  # Channels 12-15

# Read all channels at once (returns 12 values)
values = ADC.getADCall(addr)
```

### DAQCplate - Data Acquisition

```python
from BRIDGEplate import *

addr = 0

# Analog input (10-bit, 0-4.095V)
voltage = DAQC.getADC(addr, 0)

# Digital I/O
DAQC.setDOUTbit(addr, 0)  # Set output high
state = DAQC.getDINbit(addr, 0)  # Read input

# PWM output (0-1023)
DAQC.setPWM(addr, 0, 512)  # 50% duty cycle

# DAC output (0-4.095V)
DAQC.setDAC(addr, 0, 2.5)  # 2.5V output
```

### THERMOplate - Temperature Measurement

```python
from BRIDGEplate import *

addr = 0

# Configure for Type K thermocouple
THERMO.setTYPE(addr, 1, 'k')
THERMO.setLINEFREQ(addr, 60)  # 60 Hz

# Read temperature in Celsius
temp_c = THERMO.getTEMP(addr, 1, 'c')

# Read temperature in Fahrenheit
temp_f = THERMO.getTEMP(addr, 1, 'f')

# Read DS18B20 sensor (channels 9-12)
ds_temp = THERMO.getTEMP(addr, 9, 'c')
```

### DIGIplate - Digital Input & Frequency

```python
from BRIDGEplate import *

addr = 0

# Read single digital input
state = DIGI.getDINbit(addr, 1)  # Channels 1-8

# Read all inputs
all_inputs = DIGI.getDINall(addr)

# Measure frequency (channels 1-6 only)
freq = DIGI.getFREQ(addr, 1)
print(f"Frequency: {freq} Hz")

# Read all frequencies at once
frequencies = DIGI.getFREQall(addr)  # Returns 6 values
```

### RELAYplate - Relay Control

```python
from BRIDGEplate import *

addr = 0

# Control individual relays
RELAY.relayON(addr, 1)      # Turn on relay 1 (1-7)
RELAY.relayOFF(addr, 1)     # Turn off relay 1
RELAY.relayTOGGLE(addr, 1)  # Toggle relay 1

# Control all relays at once
RELAY.relayALL(addr, 0x7F)  # All on (binary 1111111)
RELAY.relayALL(addr, 0x00)  # All off

# Read relay states
state = RELAY.relaySTATE(addr)
```

## API Reference

### Common Functions (All Plates)

```python
# Board information
getADDR(addr)    # Verify board presence
getID(addr)      # Get device ID
getHWrev(addr)   # Get hardware revision
getFWrev(addr)   # Get firmware revision

# LED control
setLED(addr)     # Turn on LED
clrLED(addr)     # Turn off LED
toggleLED(addr)  # Toggle LED
```

### Argument Ranges

| Parameter | Range | Description |
|-----------|-------|-------------|
| `addr` | 0-7 | Board address (set via jumpers) |
| ADC channels | 0-7 (SE), 8-11 (DIFF), 12-15 (I) | Single-ended, differential, current |
| DAQC/DAQC2 channels | 0-7 | Analog input channels |
| CURRENT channels | 1-8 | Current measurement channels |
| DIGI inputs | 1-8 | Digital input channels |
| DIGI frequency | 1-6 | Frequency measurement channels |
| RELAY relays | 1-7 | Relay numbers (RELAYplate) |
| RELAY2 relays | 1-8 | Relay numbers (RELAY2plate) |
| THERMO channels | 1-8 (TC), 9-12 (DS18B20) | Thermocouple or DS18B20 |
| Temperature scale | 'c', 'f', 'k' | Celsius, Fahrenheit, Kelvin |
| Interrupt edge | 'r', 'f', 'b' | Rising, falling, both |

## Documentation

Complete documentation available in [BRIDGEplate_Users_Guide_Complete.md](BRIDGEplate_Users_Guide_Complete.md)

Topics covered:
- Installation and setup for all platforms
- Complete function reference with arguments
- Hardware specifications
- Wiring examples
- Troubleshooting guide
- Example programs

## Platform Support

| Platform | Port Format | Status |
|----------|-------------|--------|
| Windows | COM3, COM4, etc. | ✅ Tested |
| Linux | /dev/ttyACM0, /dev/ttyUSB0 | ✅ Tested |
| macOS | /dev/cu.usbmodem* | ✅ Tested |

### Platform-Specific Notes

**Windows:**
- Automatic USB driver installation
- No additional permissions required

**Linux:**
- Requires user in `dialout` group
- May need udev rules for consistent device naming

**macOS:**
- May require security permissions for terminal
- Use `/dev/cu.usbmodem*` ports (not `/dev/tty.usbmodem*`)

## Troubleshooting

### BRIDGEplate Not Detected

The library will display helpful error messages:

```
No serial port found with attached BRIDGEplate.
Platform: Linux
Please ensure:
  1. BRIDGEplate is connected via USB
  2. USB drivers are installed
  3. Your user is in the 'dialout' group: sudo usermod -a -G dialout $USER
     (logout and login required after adding to group)
```

**Linux - Check device:**
```bash
lsusb | grep 2e8a
ls /dev/ttyACM* /dev/ttyUSB*
```

**macOS - Check device:**
```bash
system_profiler SPUSBDataType | grep -A 10 "2e8a"
ls /dev/cu.usbmodem*
```

**Windows - Check device:**
- Open Device Manager
- Look under "Ports (COM & LPT)"
- Verify device shows as USB Serial Device

### Common Issues

**"Permission denied" on Linux:**
```bash
sudo usermod -a -G dialout $USER
# Then logout and login
```

**Multiple COM ports on Windows:**
- The library automatically selects the correct port by VID/PID

**Port already in use:**
- Close other applications using the serial port
- Only one program can access the port at a time

## Hardware

### BRIDGEplate Specifications

- **Interface:** USB 2.0 Full Speed
- **VID:PID:** 2E8A:10E3 (Raspberry Pi RP2040/RP2350)
- **Baud Rate:** 115200
- **Max Plates:** 8 of each type
- **Power:** USB bus powered
- **Connections:** Standard Pi-Plates stacking header

### Address Selection

Each Pi-Plate has jumpers to set its address (0-7):
- Different plate types can share the same address
- Each plate of the same type must have a unique address
- Addresses set via 3-pin jumper header on each board

## Examples

See the [Complete Example Programs](BRIDGEplate_Users_Guide_Complete.md#complete-example-programs) section in the user's guide for:
- Multi-plate data acquisition
- Temperature monitoring systems
- Current measurement logging
- Digital I/O control
- PWM motor control
- Frequency measurement
- Relay automation

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- New features
- Documentation improvements
- Platform-specific enhancements

## License

This software is provided for use with Pi-Plates hardware products.

## Support

- **Documentation:** [Complete User's Guide](BRIDGEplate_Users_Guide_Complete.md)
- **Pi-Plates Website:** https://pi-plates.com
- **Pi-Plates Documentation:** https://pi-plates.com/documentation/

## Credits

- **Hardware:** Pi-Plates by WallyWare, Inc.
- **Python Library:** BRIDGEplate interface implementation
- **Platform Support:** Windows, Linux, and macOS compatibility layer

## Version History

### Version 2.1
- Added macOS support with automatic platform detection
- Enhanced error messages with platform-specific troubleshooting
- Improved USB device detection across all platforms
- Added DIGI frequency measurement functions
- Updated documentation with complete argument specifications

### Version 2.0
- Initial BRIDGEplate release
- Support for all Pi-Plates products
- Cross-platform Windows and Linux support
- Automatic device detection via VID/PID

---

**Note:** This library requires the BRIDGEplate hardware to function. Pi-Plates boards cannot be used directly with this library - they must be connected through a BRIDGEplate interface.
