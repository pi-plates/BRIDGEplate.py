# BRIDGEplate Python User's Guide
## Complete Reference with Argument Specifications

## Overview

The BRIDGEplate provides a bridge between a computer and multiple Pi-Plates devices through a single USB connection. This guide documents all Python functions available in `BRIDGEplate.py` for controlling Pi-Plates products, with complete argument specifications based on official Pi-Plates documentation.

**Cross-Platform Support:** The BRIDGEplate module works seamlessly on Windows, Linux, and macOS with automatic platform detection and port discovery.

## Table of Contents

1. [Installation and Setup](#installation-and-setup)
2. [Common Argument Definitions](#common-argument-definitions)
3. [BRIDGE Functions](#bridge-functions)
4. [ADC Functions](#adc-functions)
5. [DAQC Functions](#daqc-functions)
6. [DAQC2 Functions](#daqc2-functions)
7. [CURRENT Functions](#current-functions)
8. [DIGI Functions](#digi-functions)
9. [RELAY Functions](#relay-functions)
10. [RELAY2 Functions](#relay2-functions)
11. [THERMO Functions](#thermo-functions)
12. [Complete Example Programs](#complete-example-programs)
13. [Troubleshooting](#troubleshooting)
14. [Quick Reference Tables](#quick-reference-tables)
15. [Platform Compatibility](#platform-compatibility)
16. [Additional Resources](#additional-resources)

---

## Installation and Setup

### Requirements
```
pip install pyserial
```

### Platform Support

The BRIDGEplate Python module supports:
- **Windows** - COM ports (e.g., COM3, COM4)
- **Linux** - Serial ports (e.g., /dev/ttyACM0, /dev/ttyUSB0)
- **macOS** - Serial ports (e.g., /dev/cu.usbmodem*, /dev/tty.usbmodem*)

### Importing the Module
```
from BRIDGEplate import *
```

The module automatically detects and connects to the BRIDGEplate on import using VID:PID `2E8A:10E3`. Platform detection is automatic.

### Polling for Connected Plates
```
POLL()
```
Displays all connected Pi-Plates organized by type at addresses 0-7.

### Platform-Specific Setup

#### Windows
- No additional setup required after installing pyserial
- Driver installation may be required for USB serial devices

#### Linux
- Add your user to the `dialout` group for serial port access:
  ```
  sudo usermod -a -G dialout $USER
  ```
- Logout and login for group changes to take effect

#### macOS
- No additional setup typically required
- You may need to grant terminal permissions in **System Preferences > Security & Privacy**
- Serial ports appear as both `/dev/cu.usbmodem*` and `/dev/tty.usbmodem*` (use cu.* for outgoing connections)

---

## Common Argument Definitions

These argument definitions apply across multiple Pi-Plates product lines:

- **addr** - Board address (0-7). Set via address selection jumpers on each plate.
- **bit** - Bit or channel number. Range depends on function (typically 0-7 or 1-8).
- **channel** - Input/output channel number. Specific range varies by plate type.
- **value** - Numeric value. Range and units specified per function.
- **scale** - Temperature scale for THERMO functions: 'c' (Celsius), 'f' (Fahrenheit), 'k' (Kelvin)
- **edge** - Interrupt edge detection: 'r' (rising), 'f' (falling), 'b' (both)
- **mode** - Operating mode. Specific options vary by function.

---

## BRIDGE Functions

The BRIDGE functions provide system-level information and control for the BRIDGEplate itself.

### System Information Functions

#### BRIDGE.getVERSION()
Returns the BRIDGEplate firmware version string.

**Arguments:** None

**Returns:** String containing version information

**Example:**
```
version = BRIDGE.getVERSION()
print(f"Firmware version: {version}")
```

#### BRIDGE.getADDR()
Returns the BRIDGEplate address information.

**Arguments:** None

**Returns:** Address information

#### BRIDGE.getID()
Returns the BRIDGEplate device ID string.

**Arguments:** None

**Returns:** Device ID string

#### BRIDGE.getHWrev()
Returns the BRIDGEplate hardware revision.

**Arguments:** None

**Returns:** Hardware revision number

#### BRIDGE.getFWrev()
Returns the BRIDGEplate firmware revision.

**Arguments:** None

**Returns:** Firmware revision number

### LED Control Functions

#### BRIDGE.setLED()
Turns on the BRIDGEplate LED.

**Arguments:** None

#### BRIDGE.clrLED()
Turns off the BRIDGEplate LED.

**Arguments:** None

#### BRIDGE.toggleLED()
Toggles the BRIDGEplate LED state.

**Arguments:** None

---

## ADC Functions

The ADCplate provides 8 single-ended or 4 differential analog inputs with 16-bit resolution.

### Common Functions

#### ADC.getADDR(addr)
Verifies ADCplate presence at specified address.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Address if plate is present

**Example:**
```
address = ADC.getADDR(0)
```

#### ADC.getID(addr)
Returns device ID string.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Device ID string

#### ADC.getHWrev(addr)
Returns hardware revision number.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Hardware revision number

#### ADC.getFWrev(addr)
Returns firmware revision number.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Firmware revision number

### LED Functions

#### ADC.setLED(addr)
Turns on the LED.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

#### ADC.clrLED(addr)
Turns off the LED.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

#### ADC.toggleLED(addr)
Toggles the LED state.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

### Basic ADC Functions

#### ADC.getADC(addr, channel)
Reads voltage from a single channel.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): ADC channel number
  - **Range: 0-7** for single-ended inputs
  - **Range: 8-11** for differential inputs
  - **Range: 12-15** for 4-20mA current loop inputs

**Returns:** Voltage or current value

**Example:**
```
voltage = ADC.getADC(0, 0)     # Single-ended channel 0
diff = ADC.getADC(0, 8)        # Differential channel 0 (8)
current = ADC.getADC(0, 12)    # Current loop channel 0 (12)
```

#### ADC.getADCall(addr)
Reads all 12 ADC channels simultaneously.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** List of 12 values:
- Indices 0-7: Single-ended channels
- Indices 8-11: Differential channels
- (Note: Current loop values accessed via getIall)

**Example:**
```
values = ADC.getADCall(0)
for i, v in enumerate(values):
    if i < 8:
        print(f"Single-ended {i}: {v} V")
    else:
        print(f"Differential {i-8}: {v} V")
```

#### ADC.srTable()
Displays the ADC sample rate table.

**Arguments:** None

**Example:**
```
ADC.srTable()
```

#### ADC.initADC(addr)
Initializes the ADC system.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

#### ADC.getSall(addr)
Reads all single-ended channels.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** List of voltage values

#### ADC.getDall(addr)
Reads all differential channels.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** List of differential voltage values

#### ADC.getIall(addr)
Reads all channels as 4-20mA current values.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** List of current values in mA

### Mode Functions

#### ADC.setMODE(addr, mode)
Sets the ADC operating mode.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `mode` (str): Operating mode - **Options: 'single', 'diff', 'current'**

#### ADC.getMODE(addr)
Returns the current ADC operating mode.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Current mode setting

### Event Functions

#### ADC.enableEVENTS(addr)
Enables event detection.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

#### ADC.disableEVENTS(addr)
Disables event detection.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

#### ADC.check4EVENTS(addr)
Checks if events have occurred.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** True if events pending, False otherwise

#### ADC.getEVENTS(addr)
Retrieves pending events.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Event data

---

## DAQC Functions

The DAQCplate provides analog inputs, digital I/O, PWM outputs, and DAC functions.

### Common Functions

#### DAQC.getADDR(addr)
Verifies DAQCplate presence.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

#### DAQC.getID(addr), DAQC.getHWrev(addr), DAQC.getFWrev(addr)
Standard identification functions.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

### LED Functions

#### DAQC.setLED(addr), DAQC.clrLED(addr), DAQC.toggleLED(addr)
Standard LED control functions.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

### Analog Input Functions

#### DAQC.getADC(addr, channel)
Reads voltage from an analog input (10-bit resolution, 0-4.095V range).

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): Channel number - **Range: 0-7** (channel 8 returns 5VDC supply voltage)

**Returns:** Voltage value in volts - **Range: 0 to 4.095V**

**Specifications:**
- Resolution: 10-bit (4mV per bit)
- Maximum input: 4.095 volts
- Minimum measurable: ~65mV

**Example:**
```
voltage = DAQC.getADC(0, 0)
```

#### DAQC.getADCall(addr)
Reads all 8 analog inputs.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** List of 8 voltage values

### Digital I/O Functions

#### DAQC.getDINbit(addr, bit)
Reads a single digital input bit.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `bit` (int): Bit number - **Range: 0-7**

**Returns:** Digital state - **0 or 1**

#### DAQC.getDINall(addr)
Reads all digital inputs.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Byte value - **Range: 0-255**

#### DAQC.setDOUTbit(addr, bit)
Sets a digital output bit high.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `bit` (int): Bit number - **Range: 0-6**

#### DAQC.clrDOUTbit(addr, bit)
Sets a digital output bit low.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `bit` (int): Bit number - **Range: 0-6**

#### DAQC.toggleDOUTbit(addr, bit)
Toggles a digital output bit.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `bit` (int): Bit number - **Range: 0-6**

#### DAQC.setDOUTall(addr, value)
Sets all digital outputs at once.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `value` (int): Byte value - **Range: 0-127** (7 bits, one per output)

**Example:**
```
DAQC.setDOUTall(0, 0x7F)  # All outputs ON
DAQC.setDOUTall(0, 0x00)  # All outputs OFF
```

#### DAQC.getDOUTbyte(addr)
Reads current digital output state.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Byte value - **Range: 0-127**

### PWM Functions

#### DAQC.setPWM(addr, channel, value)
Sets PWM duty cycle.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): PWM channel - **Range: 0-1**
- `value` (int): Duty cycle value - **Range: 0-1023** (0 to 100%)

**Specifications:**
- 10-bit resolution
- Frequency: 15.9 kHz

**Example:**
```
DAQC.setPWM(0, 0, 512)  # 50% duty cycle
```

#### DAQC.getPWM(addr, channel)
Reads current PWM duty cycle.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): PWM channel - **Range: 0-1**

**Returns:** Duty cycle value - **Range: 0-1023**

### DAC Functions

#### DAQC.setDAC(addr, channel, voltage)
Sets DAC output voltage.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): DAC channel - **Range: 0-1**
- `voltage` (float): Voltage - **Range: 0.0 to 4.095V**

**Example:**
```
DAQC.setDAC(0, 0, 2.5)
```

#### DAQC.getDAC(addr, channel)
Reads DAC output setting.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): DAC channel - **Range: 0-1**

**Returns:** Voltage value - **Range: 0.0 to 4.095V**

#### DAQC.calDAC(addr)
Calibrates the DAC outputs.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

### Interrupt Functions

#### DAQC.enableDINint(addr, bit, edge)
Enables interrupt on digital input.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `bit` (int): Bit number - **Range: 0-7**
- `edge` (str): Edge type - **Options: 'r' (rising), 'f' (falling), 'b' (both)**

#### DAQC.disableDINint(addr, bit)
Disables interrupt on digital input.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `bit` (int): Bit number - **Range: 0-7**

#### DAQC.getINTflags(addr)
Reads interrupt flags (clears flags after reading).

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** 16-bit interrupt flag value

### Special Functions

#### DAQC.getTEMP(addr, bit, scale)
Reads DS18B20 1-wire temperature sensor.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `bit` (int): Digital input bit - **Range: 0-7**
- `scale` (str): Temperature scale - **Options: 'c', 'f', 'k'**

**Returns:** Temperature value in specified scale

**Note:** Takes approximately 1 second to complete

#### DAQC.getRANGE(addr, channel, units)
Measures distance using HC-SR04 ultrasonic sensor.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): Channel number - **Range: 0-6** (DOUT/DIN pair)
- `units` (str): Units - **Options: 'i' (inches), 'c' (centimeters)**

**Returns:** Distance value in specified units

**Connection:** Trigger→DOUT[channel], Echo→DIN[channel]

---

## DAQC2 Functions

The DAQC2plate provides enhanced data acquisition with 12-bit ADCs and additional features.

### Analog Input Functions

#### DAQC2.getADC(addr, channel)
Reads voltage from analog input (12-bit resolution).

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): Channel number - **Range: 0-7**

**Returns:** Voltage value - **Range: ±12V** (depends on configuration)

**Specifications:**
- Resolution: 12-bit
- Sample rate: Up to 1 million samples/second (oscilloscope mode)

#### DAQC2.getADCall(addr)
Reads all 8 analog inputs.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** List of 8 voltage values

### Digital I/O Functions

Same as DAQC, with one addition:

#### DAQC2.setDOUTall(addr, value)
**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `value` (int): Byte value - **Range: 0-255** (8 bits on DAQC2 vs 7 on DAQC)

### PWM and DAC Functions

Same interface as DAQC plate.

### LED Functions (RGB)

#### DAQC2.setLED(addr, color)
Controls RGB LED color.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `color` (str): Color name - **Options:**
  - 'off' - LED off
  - 'red' - Red
  - 'green' - Green
  - 'blue' - Blue
  - 'yellow' - Yellow
  - 'cyan' - Cyan
  - 'magenta' - Magenta
  - 'white' - White

**Example:**
```
DAQC2.setLED(0, 'red')      # Red
DAQC2.setLED(0, 'green')    # Green
DAQC2.setLED(0, 'blue')     # Blue
DAQC2.setLED(0, 'white')    # White
DAQC2.setLED(0, 'off')      # Off
```

### Frequency Counter

#### DAQC2.getFREQ(addr)
Measures frequency of input signal.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Frequency in Hz

**Specifications:**
- Input range: 3.3 to 5VDC ground-referenced signal

---

## CURRENT Functions

The CURRENTplate measures current with high precision.

### Current Measurement Functions

#### CURRENT.getI(addr, channel)
Reads current in amperes.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): Channel number - **Range: 1-8**

**Returns:** Current value in amperes

**Example:**
```
current = CURRENT.getI(0, 1)
print(f"Channel 1: {current} A")
```

#### CURRENT.getIall(addr)
Reads all channels in amperes.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** List of 8 current values in amperes

**Example:**
```
currents = CURRENT.getIall(0)
for i, current in enumerate(currents):
    print(f"Channel {i+1}: {current} A")
```

### Calibration Functions

#### CURRENT.setCAL(addr, channel, offset, gain)
Sets calibration values for a channel.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): Channel number - **Range: 1-8**
- `offset` (float): Offset calibration value
- `gain` (float): Gain calibration value

#### CURRENT.getCAL(addr, channel)
Retrieves calibration values.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): Channel number - **Range: 1-8**

**Returns:** Tuple of (offset, gain)

---

## DIGI Functions

The DIGIplate provides 8 digital input lines.

### Common Functions

#### DIGI.getADDR(addr)
Verifies DIGIplate presence.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Address if present

#### DIGI.getID(addr)
Returns device ID.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Device ID string

#### DIGI.getHWrev(addr)
Returns hardware revision.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Hardware revision number

#### DIGI.getFWrev(addr)
Returns firmware revision.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Firmware revision number

### LED Functions

#### DIGI.setLED(addr)
Turns on the LED.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

#### DIGI.clrLED(addr)
Turns off the LED.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

#### DIGI.toggleLED(addr)
Toggles the LED.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

### Digital Input Functions

#### DIGI.getDINbit(addr, bit)
Reads a digital input bit.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `bit` (int): Bit number - **Range: 1-8**

**Returns:** Digital state - **0 or 1**

**Example:**
```
state = DIGI.getDINbit(0, 1)
if state == 1:
    print("Input 1 is HIGH")
else:
    print("Input 1 is LOW")
```

#### DIGI.getDINall(addr)
Reads all 8 digital inputs.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** 8-bit value representing all inputs (channels 1-8)

**Example:**
```
all_inputs = DIGI.getDINall(0)
# Check individual bits (channels 1-8)
for bit in range(1, 9):
    if all_inputs & (1 << (bit - 1)):
        print(f"Input {bit} is HIGH")
```

### Frequency Measurement Functions

The DIGIplate can measure frequency on digital input channels 1-6.

#### DIGI.getFREQ(addr, channel)
Measures frequency on a single digital input channel.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): Channel number - **Range: 1-6** (frequency measurement only available on these channels)

**Returns:** Frequency in Hz

**Example:**
```
freq = DIGI.getFREQ(0, 1)
print(f"Frequency on channel 1: {freq} Hz")
```

#### DIGI.getFREQall(addr)
Measures frequency on all 6 frequency-capable channels.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** List of 6 frequency values in Hz (channels 1-6)

**Example:**
```
frequencies = DIGI.getFREQall(0)
for i, freq in enumerate(frequencies, start=1):
    if freq > 0:
        print(f"Channel {i}: {freq} Hz")
```

### Event Functions

#### DIGI.enableDINevent(addr, bit)
Enables event detection on a digital input.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `bit` (int): Bit number - **Range: 1-8**

**Example:**
```
DIGI.enableDINevent(0, 1)
```

#### DIGI.disableDINevent(addr, bit)
Disables event detection on a digital input.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `bit` (int): Bit number - **Range: 1-8**

**Example:**
```
DIGI.disableDINevent(0, 1)
```

#### DIGI.check4EVENTS(addr)
Checks if events have occurred.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** True if events pending, False otherwise

**Example:**
```
if DIGI.check4EVENTS(0):
    events = DIGI.getEVENTS(0)
```

#### DIGI.getEVENTS(addr)
Retrieves pending events.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Event data

**Example:**
```
events = DIGI.getEVENTS(0)
```

#### DIGI.eventEnable(addr)
Enables global event detection.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Example:**
```
DIGI.eventEnable(0)
```

#### DIGI.eventDisable(addr)
Disables global event detection.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Example:**
```
DIGI.eventDisable(0)
```

---

## RELAY Functions

The RELAYplate provides 7 electromechanical relays.

### Relay Control Functions

#### RELAY.relayON(addr, relay)
Turns on (closes) a relay.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `relay` (int): Relay number - **Range: 1-7**

**Example:**
```
RELAY.relayON(0, 1)  # Turn on relay 1
```

#### RELAY.relayOFF(addr, relay)
Turns off (opens) a relay.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `relay` (int): Relay number - **Range: 1-7**

#### RELAY.relayTOGGLE(addr, relay)
Toggles relay state.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `relay` (int): Relay number - **Range: 1-7**

#### RELAY.relayALL(addr, value)
Sets all relays at once.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `value` (int): 7-bit value - **Range: 0-127**
  - Bit 0 = relay 1, Bit 1 = relay 2, etc.
  - 1 = relay ON, 0 = relay OFF

**Example:**
```
RELAY.relayALL(0, 0x7F)  # All relays ON (binary 1111111)
RELAY.relayALL(0, 0x00)  # All relays OFF
RELAY.relayALL(0, 0x55)  # Relays 1,3,5,7 ON (binary 1010101)
```

#### RELAY.relaySTATE(addr)
Reads current state of all relays.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** 7-bit value - **Range: 0-127** (1=ON, 0=OFF for each relay)

---

## RELAY2 Functions

The RELAY2plate provides 8 electromechanical relays (upgraded from RELAY's 7 relays).

### Relay Control Functions

#### RELAY2.relayON(addr, relay)
Turns on (closes) a relay.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `relay` (int): Relay number - **Range: 1-8**

**Example:**
```
RELAY2.relayON(0, 1)  # Turn on relay 1
```

#### RELAY2.relayOFF(addr, relay)
Turns off (opens) a relay.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `relay` (int): Relay number - **Range: 1-8**

#### RELAY2.relayTOGGLE(addr, relay)
Toggles relay state.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `relay` (int): Relay number - **Range: 1-8**

#### RELAY2.relayALL(addr, value)
Sets all relays at once.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `value` (int): 8-bit value - **Range: 0-255**
  - Bit 0 = relay 1, Bit 1 = relay 2, etc.
  - 1 = relay ON, 0 = relay OFF

**Example:**
```
RELAY2.relayALL(0, 0xFF)  # All 8 relays ON (binary 11111111)
RELAY2.relayALL(0, 0x00)  # All relays OFF
RELAY2.relayALL(0, 0xAA)  # Relays 2,4,6,8 ON (binary 10101010)
```

#### RELAY2.relaySTATE(addr)
Reads current state of all relays.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** 8-bit value - **Range: 0-255** (1=ON, 0=OFF for each relay)

---

## THERMO Functions

The THERMOplate provides 8 thermocouple inputs with cold junction compensation.

### Temperature Measurement Functions

#### THERMO.getTEMP(addr, channel, scale)
Reads temperature from a thermocouple or DS18B20 sensor.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): Channel number
  - **Range: 1-8** for Type K/J thermocouples
  - **Range: 9-12** for DS18B20 digital sensors
- `scale` (str): Temperature scale (optional) - **Options: 'c', 'f', 'k'**
  - 'c' = Celsius
  - 'f' = Fahrenheit
  - 'k' = Kelvin
  - If omitted, uses global scale setting

**Returns:** Temperature value in specified scale

**Note:** Takes ~0.6 seconds for thermocouples (0.72s in Europe), ~1 second for DS18B20

**Example:**
```
temp_c = THERMO.getTEMP(0, 1, 'c')  # Channel 1 in Celsius
temp_f = THERMO.getTEMP(0, 1, 'f')  # Channel 1 in Fahrenheit
temp_k = THERMO.getTEMP(0, 1, 'k')  # Channel 1 in Kelvin
ds_temp = THERMO.getTEMP(0, 9, 'c')  # DS18B20 on channel 9
```

#### THERMO.getCOLD(addr, scale)
Reads cold junction (reference) temperature.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `scale` (str): Temperature scale (optional) - **Options: 'c', 'f', 'k'**

**Returns:** Cold junction temperature

**Example:**
```
cold_temp = THERMO.getCOLD(0, 'c')
```

#### THERMO.getRAW(addr, channel)
Reads raw ADC values from a thermocouple channel.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): Channel number - **Range: 1-8**

**Returns:** Raw ADC value

### Configuration Functions

#### THERMO.setSCALE(scale)
Sets the global default temperature scale for all THERMOplates.

**Arguments:**
- `scale` (str): Temperature scale - **Options: 'c', 'f', 'k'**

**Example:**
```
THERMO.setSCALE('c')  # Set to Celsius
THERMO.setSCALE('f')  # Set to Fahrenheit
THERMO.setSCALE('k')  # Set to Kelvin
```

#### THERMO.getSCALE()
Gets the current global temperature scale.

**Arguments:** None

**Returns:** Current scale - **'c', 'f', or 'k'**

#### THERMO.setTYPE(addr, channel, tc_type)
Sets thermocouple type for a channel.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): Channel number - **Range: 1-8** (thermocouple inputs only)
- `tc_type` (str): Thermocouple type - **Options: 'j', 'k'**
  - 'j' = Type J thermocouple
  - 'k' = Type K thermocouple

**Example:**
```
THERMO.setTYPE(0, 1, 'k')  # Channel 1 = Type K
THERMO.setTYPE(0, 2, 'j')  # Channel 2 = Type J
```

#### THERMO.getTYPE(addr, channel)
Gets thermocouple type for a channel.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): Channel number - **Range: 1-8**

**Returns:** Thermocouple type - **'j' or 'k'**

#### THERMO.setLINEFREQ(addr, frequency)
Sets AC line frequency for noise rejection.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `frequency` (int): Line frequency - **Options: 50 or 60 Hz**
  - 60 Hz for North America (default)
  - 50 Hz for Europe, UK, Asia

**Example:**
```
THERMO.setLINEFREQ(0, 60)  # 60 Hz
THERMO.setLINEFREQ(0, 50)  # 50 Hz
```

**Note:** Only needs to be called once at program start.

### Interrupt Functions

#### THERMO.intEnable(addr)
Enables interrupts on the THERMOplate.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

#### THERMO.intDisable(addr)
Disables interrupts.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

#### THERMO.setINTchannel(addr, channel)
Sets which channel triggers interrupts when new data is available.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**
- `channel` (int): Channel number - **Range: 1-12**

**Note:** Multiple channels can be enabled for interrupts.

#### THERMO.getINTflags(addr)
Reads interrupt flags and clears them.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** 8-bit value
- Bit 0: Thermocouple interrupt
- Bit 1: DS18B20 interrupt
- Bits 2-7: Not used

#### THERMO.getSRQ(addr)
Checks service request (interrupt) status.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Returns:** Interrupt status

#### THERMO.setINT(addr), THERMO.clrINT(addr)
Manual interrupt flag control.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

### System Functions

#### THERMO.RESET(addr)
Resets the THERMOplate to power-on state.

**Arguments:**
- `addr` (int): Address of the plate - **Range: 0-7**

**Note:** Returns temperature scale to Celsius.

---

## Complete Example Programs

### Example 1: Reading All Analog Inputs from a DAQCplate

```
from BRIDGEplate import *
import time

# Verify DAQCplate is present at address 0
addr = 0
if DAQC.getADDR(addr) == addr:
    print(f"DAQCplate found at address {addr}")
    
    # Turn on LED
    DAQC.setLED(addr)
    
    # Read all 8 analog inputs
    while True:
        voltages = DAQC.getADCall(addr)
        
        print("Analog Inputs:")
        for i, v in enumerate(voltages):
            print(f"  Channel {i}: {v:.3f} V")
        
        time.sleep(1)
else:
    print(f"No DAQCplate found at address {addr}")
```

### Example 2: Thermocouple Temperature Monitoring

```
from BRIDGEplate import *
import time

addr = 0

# Configure THERMOplate
THERMO.setSCALE('c')           # Use Celsius (global setting)
THERMO.setTYPE(addr, 1, 'k')   # Channel 1 is Type K
THERMO.setTYPE(addr, 2, 'j')   # Channel 2 is Type J
THERMO.setLINEFREQ(addr, 60)   # 60 Hz line frequency

while True:
    # Read temperatures
    temp1 = THERMO.getTEMP(addr, 1, 'c')
    temp2 = THERMO.getTEMP(addr, 2, 'c')
    cold = THERMO.getCOLD(addr, 'c')
    
    print(f"Channel 1 (K-type): {temp1:.2f} °C")
    print(f"Channel 2 (J-type): {temp2:.2f} °C")
    print(f"Cold Junction: {cold:.2f} °C")
    print()
    
    time.sleep(2)
```

### Example 3: Digital Input and Relay Control

```
from BRIDGEplate import *
import time

digi_addr = 0
relay_addr = 1

# DIGI plate is input only - no configuration needed
# Just read the inputs

while True:
    # Read input from DIGI plate
    button = DIGI.getDINbit(digi_addr, 0)
    
    if button == 0:  # Button pressed (active low with external pull-up)
        # Turn on relay 1
        RELAY.relayON(relay_addr, 1)
        print("Button pressed - Relay ON")
    else:
        # Turn off relay 1
        RELAY.relayOFF(relay_addr, 1)
        print("Button released - Relay OFF")
    
    time.sleep(0.1)
```

### Example 4: Current Monitoring with CURRENTplate

```
from BRIDGEplate import *
import time

addr = 0

print("Current Monitoring System")
print("=" * 40)

while True:
    # Read all channels in amperes
    currents = CURRENT.getIall(addr)
    
    total = sum(currents)
    
    print(f"\nTimestamp: {time.strftime('%H:%M:%S')}")
    for i, current in enumerate(currents):
        print(f"Channel {i+1}: {current:7.3f} A")
    print(f"Total:      {total:7.3f} A")
    
    time.sleep(1)
```

### Example 5: PWM Motor Speed Control

```
from BRIDGEplate import *
import time

addr = 0

# Sweep PWM from 0 to 100%
for duty in range(0, 1024, 10):
    DAQC.setPWM(addr, 0, duty)
    percent = (duty / 1023) * 100
    print(f"PWM: {duty}/1023 ({percent:.1f}%)")
    time.sleep(0.1)

# Stop motor
DAQC.setPWM(addr, 0, 0)
```

### Example 6: DIGI Frequency Measurement

```
from BRIDGEplate import *
import time

addr = 0

print("DIGI Frequency Monitor")
print("=" * 40)
print("Frequency measurement available on channels 1-6")

# Enable event detection
DIGI.eventEnable(addr)

# Enable events on specific channels
DIGI.enableDINevent(addr, 1)
DIGI.enableDINevent(addr, 2)
DIGI.enableDINevent(addr, 3)

while True:
    # Read frequency on channels 1, 2, 3
    freq1 = DIGI.getFREQ(addr, 1)
    freq2 = DIGI.getFREQ(addr, 2)
    freq3 = DIGI.getFREQ(addr, 3)
    
    print(f"\nTimestamp: {time.strftime('%H:%M:%S')}")
    print(f"Channel 1: {freq1:8.2f} Hz")
    print(f"Channel 2: {freq2:8.2f} Hz")
    print(f"Channel 3: {freq3:8.2f} Hz")
    
    # Check for events
    if DIGI.check4EVENTS(addr):
        events = DIGI.getEVENTS(addr)
        print(f"Events detected: {events}")
    
    time.sleep(1)
```

### Example 7: DIGI Monitor All Frequencies

```
from BRIDGEplate import *
import time

addr = 0

print("DIGI All Channel Frequency Monitor")
print("=" * 50)
print("Monitoring channels 1-6")

while True:
    # Read all frequencies at once (channels 1-6)
    frequencies = DIGI.getFREQall(addr)
    
    print(f"\nTimestamp: {time.strftime('%H:%M:%S')}")
    
    # Display all frequency channels
    active_channels = 0
    for i, freq in enumerate(frequencies, start=1):
        if freq > 0:
            print(f"  Channel {i}: {freq:10.2f} Hz")
            active_channels += 1
        else:
            print(f"  Channel {i}:       0.00 Hz")
    
    if active_channels == 0:
        print("  No active signals detected")
    
    time.sleep(1)
```

---

## Troubleshooting

### Connection Issues

If the BRIDGEplate is not detected, the error message will provide platform-specific guidance:

#### Windows
- Verify USB connection
- Check that the correct VID:PID (2E8A:10E3) is programmed
- Ensure USB drivers are installed (Windows may auto-install)
- Check Device Manager for "Ports (COM & LPT)" entries

#### Linux  
- Verify USB connection
- Check that pyserial is installed: `pip install pyserial`
- Ensure your user is in the 'dialout' group:
  ```
  sudo usermod -a -G dialout $USER
  ```
- Logout and login for group changes to take effect
- Check available ports: `ls /dev/ttyACM* /dev/ttyUSB*`
- Verify device with: `lsusb | grep 2e8a`

#### macOS
- Verify USB connection
- Check that pyserial is installed: `pip install pyserial`
- Grant terminal permissions in **System Preferences > Security & Privacy > Privacy > Full Disk Access**
- Check available ports: `ls /dev/cu.usbmodem* /dev/tty.usbmodem*`
- Verify device with: `system_profiler SPUSBDataType | grep -A 10 "2e8a"`

### Serial Port Detection

The module uses automatic VID/PID detection to find the BRIDGEplate:
- VID: 2E8A (Raspberry Pi)
- PID: 10E3 (RP2040/RP2350 USB Serial)

If detection fails, check that the BRIDGEplate firmware is properly programmed with the correct USB identifiers.

### Address Conflicts

Each Pi-Plate must have a unique address (0-7). Use the address selection switches on each plate to set unique addresses. Different plate types can share the same address.

### Argument Range Errors

Always verify arguments are within specified ranges:
- Addresses: 0-7
- Channels: Varies by plate (check function documentation)
- Bit values: Typically 0-7, 0-23, or 1-8 depending on plate
- Edge types: 'r', 'f', or 'b'
- Temperature scales: 'c', 'f', or 'k'

---

## Quick Reference Tables

### Argument Ranges by Plate Type

| Plate | Address | Digital I/O Bits | Analog Channels | Relays | Special |
|-------|---------|------------------|-----------------|--------|---------|
| ADC | 0-7 | - | SE:0-7, DIFF:8-11, I:12-15 | - | 16-bit, 12 values from getADCall |
| DAQC | 0-7 | DIN:0-7, DOUT:0-6 | ADC:0-7, DAC:0-1, PWM:0-1 | - | 10-bit |
| DAQC2 | 0-7 | DIN:0-7, DOUT:0-7 | ADC:0-7, DAC:0-3 | - | 12-bit, RGB LED |
| CURRENT | 0-7 | - | 1-8 (current) | - | Amperes |
| DIGI | 0-7 | DIN:1-8 (input only) | - | - | 8 inputs, freq on ch 1-6 |
| RELAY | 0-7 | - | - | 1-7 | 7 relays, 0-127 byte |
| RELAY2 | 0-7 | - | - | 1-8 | 8 relays, 0-255 byte |
| THERMO | 0-7 | - | 1-12 (temp) | - | TC:1-8, DS18B20:9-12 |

### ADC Channel Mapping

| Channel Range | Type | Description |
|--------------|------|-------------|
| 0-7 | Single-ended | 8 single-ended analog inputs |
| 8-11 | Differential | 4 differential analog inputs |
| 12-15 | Current loop | 4-20mA current loop inputs |

**Note:** `ADC.getADCall(addr)` returns 12 values (channels 0-11)

### Temperature Scales

| Scale | Character | Description |
|-------|-----------|-------------|
| Celsius | 'c' | Metric standard |
| Fahrenheit | 'f' | US standard |
| Kelvin | 'k' | Scientific absolute |

### Interrupt Edge Types

| Edge | Character | Description |
|------|-----------|-------------|
| Rising | 'r' | Low to high transition |
| Falling | 'f' | High to low transition |
| Both | 'b' | Either transition |

---

## Platform Compatibility

### Supported Operating Systems

The BRIDGEplate module has been tested and works on:
- **Windows 10/11** - COM port detection via VID/PID
- **Linux** (Ubuntu, Raspberry Pi OS, etc.) - /dev/ttyACM* or /dev/ttyUSB* detection
- **macOS** (10.13+) - /dev/cu.usbmodem* detection

### Port Naming Conventions

| Platform | Port Name Format | Example |
|----------|-----------------|---------|
| Windows | COMn | COM3, COM4 |
| Linux | /dev/ttyACM* or /dev/ttyUSB* | /dev/ttyACM0 |
| macOS | /dev/cu.usbmodem* | /dev/cu.usbmodem14201 |

### Error Messages

The module provides platform-specific error messages when the BRIDGEplate is not found:

**Windows:**
```
No COM port found with attached BRIDGEplate.
Platform: Windows
Please ensure:
  1. BRIDGEplate is connected via USB
  2. USB drivers are installed
```

**Linux:**
```
No serial port (usually /dev/ttyACM* or /dev/ttyUSB*) found with attached BRIDGEplate.
Platform: Linux
Please ensure:
  1. BRIDGEplate is connected via USB
  2. USB drivers are installed
  3. Your user is in the 'dialout' group: sudo usermod -a -G dialout $USER
     (logout and login required after adding to group)
```

**macOS:**
```
No serial port (usually /dev/cu.usbmodem* or /dev/tty.usbmodem*) found with attached BRIDGEplate.
Platform: Darwin
Please ensure:
  1. BRIDGEplate is connected via USB
  2. USB drivers are installed
  3. You may need to grant terminal permissions in System Preferences > Security & Privacy
```

---

## Additional Resources

- Pi-Plates Documentation: https://pi-plates.com/documentation/
- DAQCplate User's Guide: https://pi-plates.com/daqc-users-guide/
- DAQC2plate User's Guide: https://pi-plates.com/daqc2-users-guide/
- THERMOplate User's Guide: https://pi-plates.com/thermoplate-users-guide/
- RELAYplate User's Guide: https://pi-plates.com/relayplate-users-guide/
- Support: https://pi-plates.com/support/

---

**Document Version:** 2.1  
**Last Updated:** February 2026  
**Compatible with:** BRIDGEplate.py (using `from BRIDGEplate import *`)  
**Platform Support:** Windows, Linux, macOS  
**Based on:** Official Pi-Plates documentation from pi-plates.com
