import serial
import re
import sys
import time
try:
    import serial.tools.list_ports
except ImportError:
    print("Error: pyserial package not found. Install with: pip install pyserial")
    sys.exit(1)

def extract_vid_pid_from_hwid(hwid):
    """Extract VID and PID from hardware ID string"""
    if not hwid:
        return None, None
    # Look for VID pattern
    vid_match = re.search(r'VID_([0-9A-Fa-f]{4})', hwid)
    lvid = vid_match.group(1).upper() if vid_match else None
    # Look for PID pattern
    pid_match = re.search(r'PID_([0-9A-Fa-f]{4})', hwid)
    lpid = pid_match.group(1).upper() if pid_match else None
    return lvid, lpid

def find_ports_by_vid_pid(target_vid, target_pid):
    """Find COM ports by VID and PID combination"""
    matching_ports = []
    
    try:
        available_ports = serial.tools.list_ports.comports()    
        for port in available_ports:
            vid = None
            pid = None
            # Try to get VID/PID directly from pyserial
            if hasattr(port, 'vid') and port.vid is not None:
                vid = f"{port.vid:04X}"
            if hasattr(port, 'pid') and port.pid is not None:
                pid = f"{port.pid:04X}"
            # If not available directly, parse from hardware ID
            if not vid or not pid:
                if port.hwid:
                    parsed_vid, parsed_pid = extract_vid_pid_from_hwid(port.hwid)
                    if parsed_vid and not vid:
                        vid = parsed_vid
                    if parsed_pid and not pid:
                        pid = parsed_pid
            
            # Check if this port matches the target VID/PID
            if vid == target_vid.upper() and pid == target_pid.upper():
                matching_ports=port.device 
    except Exception as e:
        print(f"Error searching COM ports: {e}") 
    return matching_ports

def CMD(cmd):
    #global ser
    cmd+="\n"							#add newline character
    ser.write(cmd.encode('utf-8'))
    #xresp = str(ser.read_until(expected='\n'),'utf-8')	#this cmd took WAY too long!
    xresp = str(ser.read_until(),'utf-8')
    xresp2=xresp.replace("\r", "")		#strip off CR if present
    xresp3=xresp2.replace("\n", "")		#strip off LF if present
    return xresp3

def printL(name, pList):
    print(name,end=' ')
    for i in range(7):
        print(pList[i],end='')
    print(pList[7])

def parseIt(cmd,args):
    #print(f"Received arguments: {args}")
    #print(f"Number of arguments: {len(args)}")
    argStr=', '.join(str(args) for args in args)
    #addr=args[0]
    cmdStr=cmd+"("+argStr+")"
    #print(cmdStr)
    comma_string=CMD(cmdStr)
    if ',' not in comma_string:		# No commas, so just convert to number if possible and return
        return convert_to_number(comma_string.strip())
    elements = [element.strip() for element in comma_string.split(',')]	# Split the string by commas and strip whitespace  
    # Convert each element to a number if possible
    converted_list = []
    for element in elements:
        converted_list.append(convert_to_number(element))
    return converted_list

def dispBlock(cmd):
    #global ser
    timeout=5.0
    cmd+="()\n"							#add newline character
    ser.write(cmd.encode('utf-8'))
    #Display output from the RP2350 until <<<END>>> is received
    buffer = ""
    #start_time = time.time()
    last_data_time = time.time()
    while True:
        if ser.in_waiting > 0:
            # Read and decode data
            data = ser.read(ser.in_waiting).decode('utf-8', errors='replace')
            buffer += data
            
            # Check if we've received the termination marker
            if "<<<END>>>" in buffer:
                end_pos = buffer.find("<<<END>>>")
                print(buffer[:end_pos], end='', flush=True)
                print("\n")
                break
            
            # Print data as it comes in
            print(data, end='', flush=True)
        if time.time() - last_data_time > timeout:
            if ser.in_waiting > 0:
                print(buffer, end='', flush=True)
            break            
        
        time.sleep(0.01)  # Small delay to prevent CPU spinning          


def convert_to_number(value):	#AIgenerated
    """
    Try to convert a value to int or float, otherwise keep as string.
    Args:
        value: The value to convert
    Returns:
        int, float, or original string
    """   
    try:	# Try converting to int first
        return int(value)
    except ValueError:
        pass
    
    try:	# Try converting to float
        return float(value)
    except ValueError:
        pass   
    # If both fail, return as string
    return value


"""
ADC class includes all 44 functions
Common Functions: getADDR, getID, getHWrev, getFWrev
LED Functions: setLED, clrLED, toggleLED
Basic ADC Functions: getADC, srTable, initADC, getADCall, getSall, getDall, getIall
Mode Functions: setMODE, getMODE
Input Configuration: configINPUT, enableINPUT, disableINPUT
Advanced ADC Read Functions: readSINGLE, startSINGLE, getSINGLE, readSCAN, startSCAN, getSCAN, getBLOCK, startBLOCK, startSTREAM, getSTREAM, stopSTREAM
Digital Input Functions: getDINbit, getDINall, enableDINevent, disableDINevent
Trigger Functions: configTRIG, startTRIG, stopTRIG, triggerFREQ, swTRIGGER, maxTRIGfreq
Event Functions: enableEVENTS, disableEVENTS, check4EVENTS, getEVENTS
"""

class ADC:
    def __init__(self):
        self.type="ADC"


    @staticmethod
    def getADDR(*args):
        myList = [*args]
        resp = parseIt("ADC.getADDR", myList)
        return resp
    
    @staticmethod
    def getID(*args):
        myList = [*args]
        resp = parseIt("ADC.getID", myList)
        return resp
    
    @staticmethod
    def getHWrev(*args):
        myList = [*args]
        resp = parseIt("ADC.getHWrev", myList)
        return resp
    
    @staticmethod
    def getFWrev(*args):
        myList = [*args]
        resp = parseIt("ADC.getFWrev", myList)
        return resp
    
    @staticmethod
    def setLED(*args):
        myList = [*args]
        resp = parseIt("ADC.setLED", myList)
        return resp
    
    @staticmethod
    def clrLED(*args):
        myList = [*args]
        resp = parseIt("ADC.clrLED", myList)
        return resp
    
    @staticmethod
    def toggleLED(*args):
        myList = [*args]
        resp = parseIt("ADC.toggleLED", myList)
        return resp
    
    @staticmethod
    def getADC(*args):
        myList = [*args]
        resp = parseIt("ADC.getADC", myList)
        return resp
    
    @staticmethod
    def srTable():
        dispBlock("ADC.srTable")
    
    @staticmethod
    def initADC(*args):
        myList = [*args]
        resp = parseIt("ADC.initADC", myList)
        return resp
    
    @staticmethod
    def enableEVENTS(*args):
        myList = [*args]
        resp = parseIt("ADC.enableEVENTS", myList)
        return resp
    
    @staticmethod
    def disableEVENTS(*args):
        myList = [*args]
        resp = parseIt("ADC.disableEVENTS", myList)
        return resp
    
    @staticmethod
    def check4EVENTS(*args):
        myList = [*args]
        resp = parseIt("ADC.check4EVENTS", myList)
        return resp
    
    @staticmethod
    def getEVENTS(*args):
        myList = [*args]
        resp = parseIt("ADC.getEVENTS", myList)
        return resp
    
    @staticmethod
    def getADCall(*args):
        myList = [*args]
        resp = parseIt("ADC.getADCall", myList)
        return resp
    
    @staticmethod
    def getSall(*args):
        myList = [*args]
        resp = parseIt("ADC.getSall", myList)
        return resp
    
    @staticmethod
    def getDall(*args):
        myList = [*args]
        resp = parseIt("ADC.getDall", myList)
        return resp
    
    @staticmethod
    def getIall(*args):
        myList = [*args]
        resp = parseIt("ADC.getIall", myList)
        return resp
    
    @staticmethod
    def setMODE(*args):
        myList = [*args]
        resp = parseIt("ADC.setMODE", myList)
        return resp
    
    @staticmethod
    def getMODE(*args):
        myList = [*args]
        resp = parseIt("ADC.getMODE", myList)
        return resp
    
    @staticmethod
    def configINPUT(*args):
        myList = [*args]
        resp = parseIt("ADC.configINPUT", myList)
        return resp
    
    @staticmethod
    def enableINPUT(*args):
        myList = [*args]
        resp = parseIt("ADC.enableINPUT", myList)
        return resp
    
    @staticmethod
    def disableINPUT(*args):
        myList = [*args]
        resp = parseIt("ADC.disableINPUT", myList)
        return resp
    
    @staticmethod
    def readSINGLE(*args):
        myList = [*args]
        resp = parseIt("ADC.readSINGLE", myList)
        return resp
    
    @staticmethod
    def startSINGLE(*args):
        myList = [*args]
        resp = parseIt("ADC.startSINGLE", myList)
        return resp
    
    @staticmethod
    def getSINGLE(*args):
        myList = [*args]
        resp = parseIt("ADC.getSINGLE", myList)
        return resp
    
    @staticmethod
    def readSCAN(*args):
        myList = [*args]
        resp = parseIt("ADC.readSCAN", myList)
        return resp
    
    @staticmethod
    def startSCAN(*args):
        myList = [*args]
        resp = parseIt("ADC.startSCAN", myList)
        return resp
    
    @staticmethod
    def getSCAN(*args):
        myList = [*args]
        resp = parseIt("ADC.getSCAN", myList)
        return resp
    
    @staticmethod
    def getBLOCK(*args):
        myList = [*args]
        resp = parseIt("ADC.getBLOCK", myList)
        return resp
    
    @staticmethod
    def startBLOCK(*args):
        myList = [*args]
        resp = parseIt("ADC.startBLOCK", myList)
        return resp
    
    @staticmethod
    def startSTREAM(*args):
        myList = [*args]
        resp = parseIt("ADC.startSTREAM", myList)
        return resp
    
    @staticmethod
    def getSTREAM(*args):
        myList = [*args]
        resp = parseIt("ADC.getSTREAM", myList)
        return resp
    
    @staticmethod
    def stopSTREAM(*args):
        myList = [*args]
        resp = parseIt("ADC.stopSTREAM", myList)
        return resp
    
    @staticmethod
    def getDINbit(*args):
        myList = [*args]
        resp = parseIt("ADC.getDINbit", myList)
        return resp
    
    @staticmethod
    def getDINall(*args):
        myList = [*args]
        resp = parseIt("ADC.getDINall", myList)
        return resp
    
    @staticmethod
    def enableDINevent(*args):
        myList = [*args]
        resp = parseIt("ADC.enableDINevent", myList)
        return resp
    
    @staticmethod
    def disableDINevent(*args):
        myList = [*args]
        resp = parseIt("ADC.disableDINevent", myList)
        return resp
    
    @staticmethod
    def configTRIG(*args):
        myList = [*args]
        resp = parseIt("ADC.configTRIG", myList)
        return resp
    
    @staticmethod
    def startTRIG(*args):
        myList = [*args]
        resp = parseIt("ADC.startTRIG", myList)
        return resp
    
    @staticmethod
    def stopTRIG(*args):
        myList = [*args]
        resp = parseIt("ADC.stopTRIG", myList)
        return resp
    
    @staticmethod
    def triggerFREQ(*args):
        myList = [*args]
        resp = parseIt("ADC.triggerFREQ", myList)
        return resp
    
    @staticmethod
    def swTRIGGER(*args):
        myList = [*args]
        resp = parseIt("ADC.swTRIGGER", myList)
        return resp
    
    @staticmethod
    def maxTRIGfreq(*args):
        myList = [*args]
        resp = parseIt("ADC.maxTRIGfreq", myList)
        return resp
    
    @staticmethod
    def help():
        dispBlock("ADC.help")

"""
BRIDGE class includes all 13 functions
Common Functions: getID, getHWrev, getFWrev
Stack Management: resetSTACK, getSRQ
Mode Configuration: setMODE
Digital Input Functions: getDIN, getDINall
Digital Output Functions: setDOUT, clrDOUT, toggleDOUT, setDOUTall
System Functions: resetBRIDGE
"""
class BRIDGE:
    def __init__(self):
        self.type = "BRIDGE"
    
    @staticmethod
    def getID(*args):
        myList = [*args]
        resp = parseIt("BRIDGE.getID", myList)
        return resp
    
    @staticmethod
    def getHWrev(*args):
        myList = [*args]
        resp = parseIt("BRIDGE.getHWrev", myList)
        return resp
    
    @staticmethod
    def getFWrev(*args):
        myList = [*args]
        resp = parseIt("BRIDGE.getFWrev", myList)
        return resp
    
    @staticmethod
    def resetSTACK(*args):
        myList = [*args]
        resp = parseIt("BRIDGE.resetSTACK", myList)
        return resp
    
    @staticmethod
    def getSRQ(*args):
        myList = [*args]
        resp = parseIt("BRIDGE.getSRQ", myList)
        return resp
    
#     @staticmethod
#     def setMODE(*args):
#         myList = [*args]
#         resp = parseIt("BRIDGE.setMODE", myList)
#         return resp
#     
#     @staticmethod
#     def getDIN(*args):
#         myList = [*args]
#         resp = parseIt("BRIDGE.getDIN", myList)
#         return resp
#     
#     @staticmethod
#     def getDINall(*args):
#         myList = [*args]
#         resp = parseIt("BRIDGE.getDINall", myList)
#         return resp
#     
#     @staticmethod
#     def setDOUT(*args):
#         myList = [*args]
#         resp = parseIt("BRIDGE.setDOUT", myList)
#         return resp
#     
#     @staticmethod
#     def clrDOUT(*args):
#         myList = [*args]
#         resp = parseIt("BRIDGE.clrDOUT", myList)
#         return resp
#     
#     @staticmethod
#     def toggleDOUT(*args):
#         myList = [*args]
#         resp = parseIt("BRIDGE.toggleDOUT", myList)
#         return resp
#     
#     @staticmethod
#     def setDOUTall(*args):
#         myList = [*args]
#         resp = parseIt("BRIDGE.setDOUTall", myList)
#         return resp
    
    @staticmethod
    def resetBRIDGE(*args):
        myList = [*args]
        resp = parseIt("BRIDGE.resetBRIDGE", myList)
        return resp

    @staticmethod
    def port():
        return matches
    
    @staticmethod
    def help():
        dispBlock("BRIDGE.help")    

"""
CURRENT class includes all 9 functions
Common Functions: getADDR, getID, getHWrev, getFWrev
LED Functions: setLED, clrLED, toggleLED
Current Measurement Functions: getI - Read single 4-20mA input channel (1-8), getIall - Read all 8 4-20mA input channels
"""
class CURRENT:
    def __init__(self):
        self.type = "CURRENT"
    
    @staticmethod
    def getADDR(*args):
        myList = [*args]
        resp = parseIt("CURRENT.getADDR", myList)
        return resp
    
    @staticmethod
    def getID(*args):
        myList = [*args]
        resp = parseIt("CURRENT.getID", myList)
        return resp
    
    @staticmethod
    def getHWrev(*args):
        myList = [*args]
        resp = parseIt("CURRENT.getHWrev", myList)
        return resp
    
    @staticmethod
    def getFWrev(*args):
        myList = [*args]
        resp = parseIt("CURRENT.getFWrev", myList)
        return resp
    
    @staticmethod
    def setLED(*args):
        myList = [*args]
        resp = parseIt("CURRENT.setLED", myList)
        return resp
    
    @staticmethod
    def clrLED(*args):
        myList = [*args]
        resp = parseIt("CURRENT.clrLED", myList)
        return resp
    
    @staticmethod
    def toggleLED(*args):
        myList = [*args]
        resp = parseIt("CURRENT.toggleLED", myList)
        return resp
    
    @staticmethod
    def getI(*args):
        myList = [*args]
        resp = parseIt("CURRENT.getI", myList)
        return resp
    
    @staticmethod
    def getIall(*args):
        myList = [*args]
        resp = parseIt("CURRENT.getIall", myList)
        return resp
    
    @staticmethod
    def help():
        dispBlock("CURRENT.help")    

"""
DAQC class includes all 27 functions
Common Functions: getADDR, getID, getHWrev, getFWrev
LED Functions: setLED, clrLED, toggleLED, getLED
ADC Functions: getADC - Read single ADC channel (0-8), getADCall - Read all 8 ADC channels
Digital Input Functions: getDINbit, getDINall, enableDINint, disableDINint
Temperature Functions: getTEMP - Read temperature sensor with scale (C/F/K)
Digital Output Functions: setDOUTbit, clrDOUTbit, setDOUTall, getDOUTbyte, toggleDOUTbit
PWM/DAC Functions: setPWM, getPWM, setDAC, getDAC
Range Finding Functions: getRANGE - Ultrasonic range measurement
Interrupt Functions: intENABLE, intDISABLE, getINTflags
"""
class DAQC:
    def __init__(self):
        self.type = "DAQC"
    
    @staticmethod
    def getADDR(*args):
        myList = [*args]
        resp = parseIt("DAQC.getADDR", myList)
        return resp
    
    @staticmethod
    def getID(*args):
        myList = [*args]
        resp = parseIt("DAQC.getID", myList)
        return resp
    
    @staticmethod
    def getHWrev(*args):
        myList = [*args]
        resp = parseIt("DAQC.getHWrev", myList)
        return resp
    
    @staticmethod
    def getFWrev(*args):
        myList = [*args]
        resp = parseIt("DAQC.getFWrev", myList)
        return resp
    
    @staticmethod
    def setLED(*args):
        myList = [*args]
        resp = parseIt("DAQC.setLED", myList)
        return resp
    
    @staticmethod
    def clrLED(*args):
        myList = [*args]
        resp = parseIt("DAQC.clrLED", myList)
        return resp
    
    @staticmethod
    def toggleLED(*args):
        myList = [*args]
        resp = parseIt("DAQC.toggleLED", myList)
        return resp
    
    @staticmethod
    def getLED(*args):
        myList = [*args]
        resp = parseIt("DAQC.getLED", myList)
        return resp
    
    @staticmethod
    def getADC(*args):
        myList = [*args]
        resp = parseIt("DAQC.getADC", myList)
        return resp
    
    @staticmethod
    def getADCall(*args):
        myList = [*args]
        resp = parseIt("DAQC.getADCall", myList)
        return resp
    
    @staticmethod
    def getDINbit(*args):
        myList = [*args]
        resp = parseIt("DAQC.getDINbit", myList)
        return resp
    
    @staticmethod
    def getDINall(*args):
        myList = [*args]
        resp = parseIt("DAQC.getDINall", myList)
        return resp
    
    @staticmethod
    def enableDINint(*args):
        myList = [*args]
        resp = parseIt("DAQC.enableDINint", myList)
        return resp
    
    @staticmethod
    def disableDINint(*args):
        myList = [*args]
        resp = parseIt("DAQC.disableDINint", myList)
        return resp
    
    @staticmethod
    def getTEMP(*args):
        myList = [*args]
        resp = parseIt("DAQC.getTEMP", myList)
        return resp
    
    @staticmethod
    def setDOUTbit(*args):
        myList = [*args]
        resp = parseIt("DAQC.setDOUTbit", myList)
        return resp
    
    @staticmethod
    def clrDOUTbit(*args):
        myList = [*args]
        resp = parseIt("DAQC.clrDOUTbit", myList)
        return resp
    
    @staticmethod
    def setDOUTall(*args):
        myList = [*args]
        resp = parseIt("DAQC.setDOUTall", myList)
        return resp
    
    @staticmethod
    def getDOUTbyte(*args):
        myList = [*args]
        resp = parseIt("DAQC.getDOUTbyte", myList)
        return resp
    
    @staticmethod
    def toggleDOUTbit(*args):
        myList = [*args]
        resp = parseIt("DAQC.toggleDOUTbit", myList)
        return resp
    
    @staticmethod
    def setPWM(*args):
        myList = [*args]
        resp = parseIt("DAQC.setPWM", myList)
        return resp
    
    @staticmethod
    def getPWM(*args):
        myList = [*args]
        resp = parseIt("DAQC.getPWM", myList)
        return resp
    
    @staticmethod
    def setDAC(*args):
        myList = [*args]
        resp = parseIt("DAQC.setDAC", myList)
        return resp
    
    @staticmethod
    def getDAC(*args):
        myList = [*args]
        resp = parseIt("DAQC.getDAC", myList)
        return resp
    
    @staticmethod
    def getRANGE(*args):
        myList = [*args]
        resp = parseIt("DAQC.getRANGE", myList)
        return resp
    
    @staticmethod
    def intENABLE(*args):
        myList = [*args]
        resp = parseIt("DAQC.intENABLE", myList)
        return resp
    
    @staticmethod
    def intDISABLE(*args):
        myList = [*args]
        resp = parseIt("DAQC.intDISABLE", myList)
        return resp
    
    @staticmethod
    def getINTflags(*args):
        myList = [*args]
        resp = parseIt("DAQC.getINTflags", myList)
        return resp
    
    @staticmethod
    def help():
        dispBlock("DAQC.help") 

"""
DAQC2 class includes all 54 functions
Common Functions: getADDR, getID, getHWrev, getFWrev, RESET
Interrupt Functions: intEnable, intDisable, getINTflags
Digital Output Functions: setDOUTbit, clrDOUTbit, toggleDOUTbit, setDOUTall, getDOUTbyte
Digital Input Functions: getDINbit, enableDINint, disableDINint, getDINall
ADC Functions: getADC - Read single ADC channel (0-8), getADCall - Read all 8 ADC channels
DAC Functions: setDAC, getDAC
LED Functions: setLED - Set LED color (off/red/green/yellow/blue/magenta/cyan/white), getLED
Frequency Functions: getFREQ, getSRQ, setSRQ, clrSRQ
PWM Functions: setPWM, getPWM
Function Generator Functions: fgON, fgOFF, fgFREQ, fgTYPE, fgLEVEL
Motor Control Functions: motorENABLE, motorDISABLE, motorMOVE, motorJOG, motorSTOP, motorDIR, motorRATE, motorOFF, motorINTenable, motorINTdisable
Oscilloscope Functions: startOSC, stopOSC, runOSC, setOSCchannel, setOSCsweep, getOSCtraces, setOSCtrigger, trigOSCnow
"""
class DAQC2:
    def __init__(self):
        self.type = "DAQC2"
    
    @staticmethod
    def getADDR(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getADDR", myList)
        return resp
    
    @staticmethod
    def getID(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getID", myList)
        return resp
    
    @staticmethod
    def getHWrev(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getHWrev", myList)
        return resp
    
    @staticmethod
    def getFWrev(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getFWrev", myList)
        return resp
    
    @staticmethod
    def intEnable(*args):
        myList = [*args]
        resp = parseIt("DAQC2.intEnable", myList)
        return resp
    
    @staticmethod
    def intDisable(*args):
        myList = [*args]
        resp = parseIt("DAQC2.intDisable", myList)
        return resp
    
    @staticmethod
    def getINTflags(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getINTflags", myList)
        return resp
    
    @staticmethod
    def RESET(*args):
        myList = [*args]
        resp = parseIt("DAQC2.RESET", myList)
        return resp
    
    @staticmethod
    def setDOUTbit(*args):
        myList = [*args]
        resp = parseIt("DAQC2.setDOUTbit", myList)
        return resp
    
    @staticmethod
    def clrDOUTbit(*args):
        myList = [*args]
        resp = parseIt("DAQC2.clrDOUTbit", myList)
        return resp
    
    @staticmethod
    def toggleDOUTbit(*args):
        myList = [*args]
        resp = parseIt("DAQC2.toggleDOUTbit", myList)
        return resp
    
    @staticmethod
    def setDOUTall(*args):
        myList = [*args]
        resp = parseIt("DAQC2.setDOUTall", myList)
        return resp
    
    @staticmethod
    def getDOUTbyte(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getDOUTbyte", myList)
        return resp
    
    @staticmethod
    def getDINbit(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getDINbit", myList)
        return resp
    
    @staticmethod
    def enableDINint(*args):
        myList = [*args]
        resp = parseIt("DAQC2.enableDINint", myList)
        return resp
    
    @staticmethod
    def disableDINint(*args):
        myList = [*args]
        resp = parseIt("DAQC2.disableDINint", myList)
        return resp
    
    @staticmethod
    def getDINall(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getDINall", myList)
        return resp
    
    @staticmethod
    def getADC(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getADC", myList)
        return resp
    
    @staticmethod
    def getADCall(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getADCall", myList)
        return resp
    
    @staticmethod
    def setDAC(*args):
        myList = [*args]
        resp = parseIt("DAQC2.setDAC", myList)
        return resp
    
    @staticmethod
    def getDAC(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getDAC", myList)
        return resp
    
    @staticmethod
    def setLED(*args):
        myList = [*args]
        resp = parseIt("DAQC2.setLED", myList)
        return resp
    
    @staticmethod
    def getLED(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getLED", myList)
        return resp
    
    @staticmethod
    def getSRQ(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getSRQ", myList)
        return resp
    
    @staticmethod
    def getFREQ(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getFREQ", myList)
        return resp
    
    @staticmethod
    def setPWM(*args):
        myList = [*args]
        resp = parseIt("DAQC2.setPWM", myList)
        return resp
    
    @staticmethod
    def getPWM(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getPWM", myList)
        return resp
    
    @staticmethod
    def fgON(*args):
        myList = [*args]
        resp = parseIt("DAQC2.fgON", myList)
        return resp
    
    @staticmethod
    def fgOFF(*args):
        myList = [*args]
        resp = parseIt("DAQC2.fgOFF", myList)
        return resp
    
    @staticmethod
    def fgFREQ(*args):
        myList = [*args]
        resp = parseIt("DAQC2.fgFREQ", myList)
        return resp
    
    @staticmethod
    def fgTYPE(*args):
        myList = [*args]
        resp = parseIt("DAQC2.fgTYPE", myList)
        return resp
    
    @staticmethod
    def fgLEVEL(*args):
        myList = [*args]
        resp = parseIt("DAQC2.fgLEVEL", myList)
        return resp
    
    @staticmethod
    def setSRQ(*args):
        myList = [*args]
        resp = parseIt("DAQC2.setSRQ", myList)
        return resp
    
    @staticmethod
    def clrSRQ(*args):
        myList = [*args]
        resp = parseIt("DAQC2.clrSRQ", myList)
        return resp
    
    @staticmethod
    def motorENABLE(*args):
        myList = [*args]
        resp = parseIt("DAQC2.motorENABLE", myList)
        return resp
    
    @staticmethod
    def motorDISABLE(*args):
        myList = [*args]
        resp = parseIt("DAQC2.motorDISABLE", myList)
        return resp
    
    @staticmethod
    def motorMOVE(*args):
        myList = [*args]
        resp = parseIt("DAQC2.motorMOVE", myList)
        return resp
    
    @staticmethod
    def motorJOG(*args):
        myList = [*args]
        resp = parseIt("DAQC2.motorJOG", myList)
        return resp
    
    @staticmethod
    def motorSTOP(*args):
        myList = [*args]
        resp = parseIt("DAQC2.motorSTOP", myList)
        return resp
    
    @staticmethod
    def motorDIR(*args):
        myList = [*args]
        resp = parseIt("DAQC2.motorDIR", myList)
        return resp
    
    @staticmethod
    def motorRATE(*args):
        myList = [*args]
        resp = parseIt("DAQC2.motorRATE", myList)
        return resp
    
    @staticmethod
    def motorOFF(*args):
        myList = [*args]
        resp = parseIt("DAQC2.motorOFF", myList)
        return resp
    
    @staticmethod
    def motorINTenable(*args):
        myList = [*args]
        resp = parseIt("DAQC2.motorINTenable", myList)
        return resp
    
    @staticmethod
    def motorINTdisable(*args):
        myList = [*args]
        resp = parseIt("DAQC2.motorINTdisable", myList)
        return resp
    
    @staticmethod
    def startOSC(*args):
        myList = [*args]
        resp = parseIt("DAQC2.startOSC", myList)
        return resp
    
    @staticmethod
    def stopOSC(*args):
        myList = [*args]
        resp = parseIt("DAQC2.stopOSC", myList)
        return resp
    
    @staticmethod
    def runOSC(*args):
        myList = [*args]
        resp = parseIt("DAQC2.runOSC", myList)
        return resp
    
    @staticmethod
    def setOSCchannel(*args):
        myList = [*args]
        resp = parseIt("DAQC2.setOSCchannel", myList)
        return resp
    
    @staticmethod
    def setOSCsweep(*args):
        myList = [*args]
        resp = parseIt("DAQC2.setOSCsweep", myList)
        return resp
    
    @staticmethod
    def getOSCtraces(*args):
        myList = [*args]
        resp = parseIt("DAQC2.getOSCtraces", myList)
        return resp
    
    @staticmethod
    def setOSCtrigger(*args):
        myList = [*args]
        resp = parseIt("DAQC2.setOSCtrigger", myList)
        return resp
    
    @staticmethod
    def trigOSCnow(*args):
        myList = [*args]
        resp = parseIt("DAQC2.trigOSCnow", myList)
        return resp
    
    @staticmethod
    def help():
        dispBlock("DAQC2.help")      

"""
DIGI class includes all 17 functions
Common Functions: getADDR, getID, getHWrev, getFWrev
LED Functions: setLED, clrLED, toggleLED
Digital Input Functions: getDINbit, getDINall, getFREQ, getFREQall
Event Functions: enableDINevent, disableDINevent, getEVENTS, check4EVENTS, eventEnable, eventDisable
"""
class DIGI:
    def __init__(self):
        self.type="DIGI"
    
    @staticmethod
    def getADDR(*args):
        myList = [*args]
        resp = parseIt("DIGI.getADDR", myList)
        return resp
    
    @staticmethod
    def getID(*args):
        myList = [*args]
        resp = parseIt("DIGI.getID", myList)
        return resp
    
    @staticmethod
    def getHWrev(*args):
        myList = [*args]
        resp = parseIt("DIGI.getHWrev", myList)
        return resp
    
    @staticmethod
    def getFWrev(*args):
        myList = [*args]
        resp = parseIt("DIGI.getFWrev", myList)
        return resp
    
    @staticmethod
    def setLED(*args):
        myList = [*args]
        resp = parseIt("DIGI.setLED", myList)
        return resp
    
    @staticmethod
    def clrLED(*args):
        myList = [*args]
        resp = parseIt("DIGI.clrLED", myList)
        return resp
    
    @staticmethod
    def toggleLED(*args):
        myList = [*args]
        resp = parseIt("DIGI.toggleLED", myList)
        return resp
    
    @staticmethod
    def getDINbit(*args):
        myList = [*args]
        resp = parseIt("DIGI.getDINbit", myList)
        return resp
    
    @staticmethod
    def getDINall(*args):
        myList = [*args]
        resp = parseIt("DIGI.getDINall", myList)
        return resp
    
    @staticmethod
    def getFREQ(*args):
        myList = [*args]
        resp = parseIt("DIGI.getFREQ", myList)
        return resp
    
    @staticmethod
    def getFREQall(*args):
        myList = [*args]
        resp = parseIt("DIGI.getFREQall", myList)
        return resp
    
    @staticmethod
    def enableDINevent(*args):
        myList = [*args]
        resp = parseIt("DIGI.enableDINevent", myList)
        return resp
    
    @staticmethod
    def disableDINevent(*args):
        myList = [*args]
        resp = parseIt("DIGI.disableDINevent", myList)
        return resp
    
    @staticmethod
    def getEVENTS(*args):
        myList = [*args]
        resp = parseIt("DIGI.getEVENTS", myList)
        return resp
    
    @staticmethod
    def check4EVENTS(*args):
        myList = [*args]
        resp = parseIt("DIGI.check4EVENTS", myList)
        return resp
    
    @staticmethod
    def eventEnable(*args):
        myList = [*args]
        resp = parseIt("DIGI.eventEnable", myList)
        return resp
    
    @staticmethod
    def eventDisable(*args):
        myList = [*args]
        resp = parseIt("DIGI.eventDisable", myList)
        return resp

"""
RELAY class includes all 12 functions
Common Functions: getADDR, getID, getHWrev, getFWrev
LED Functions: setLED, clrLED, toggleLED
Relay Control Functions:
relayON - Turn on relay (1-7)
relayOFF - Turn off relay (1-7)
relayTOGGLE - Toggle relay (1-7)
relayALL - Set all relays (0-127)
relaySTATE - Get current relay state
"""
class RELAY:
    def __init__(self):
        self.type = "RELAY"
    
    @staticmethod
    def getADDR(*args):
        myList = [*args]
        resp = parseIt("RELAY.getADDR", myList)
        return resp
    
    @staticmethod
    def getID(*args):
        myList = [*args]
        resp = parseIt("RELAY.getID", myList)
        return resp
    
    @staticmethod
    def getHWrev(*args):
        myList = [*args]
        resp = parseIt("RELAY.getHWrev", myList)
        return resp
    
    @staticmethod
    def getFWrev(*args):
        myList = [*args]
        resp = parseIt("RELAY.getFWrev", myList)
        return resp
    
    @staticmethod
    def setLED(*args):
        myList = [*args]
        resp = parseIt("RELAY.setLED", myList)
        return resp
    
    @staticmethod
    def clrLED(*args):
        myList = [*args]
        resp = parseIt("RELAY.clrLED", myList)
        return resp
    
    @staticmethod
    def toggleLED(*args):
        myList = [*args]
        resp = parseIt("RELAY.toggleLED", myList)
        return resp
    
    @staticmethod
    def relayON(*args):
        myList = [*args]
        resp = parseIt("RELAY.relayON", myList)
        return resp
    
    @staticmethod
    def relayOFF(*args):
        myList = [*args]
        resp = parseIt("RELAY.relayOFF", myList)
        return resp
    
    @staticmethod
    def relayTOGGLE(*args):
        myList = [*args]
        resp = parseIt("RELAY.relayTOGGLE", myList)
        return resp
    
    @staticmethod
    def relayALL(*args):
        myList = [*args]
        resp = parseIt("RELAY.relayALL", myList)
        return resp
    
    @staticmethod
    def relaySTATE(*args):
        myList = [*args]
        resp = parseIt("RELAY.relaySTATE", myList)
        return resp

"""
RELAY2 class includes all 12 functions
Common Functions: getADDR, getID, getHWrev, getFWrev
LED Functions: setLED, clrLED, toggleLED
Relay Control Functions:
relayON - Turn on relay (1-8)
relayOFF - Turn off relay (1-8)
relayTOGGLE - Toggle relay (1-8)
relayALL - Set all relays (0-255)
relaySTATE - Get current relay state
Note: RELAY2 supports 8 relays (1-8) compared to RELAY which supports 7 relays (1-7), and the relayALL value range is 0-255 instead of 0-127.
"""
class RELAY2:
    def __init__(self):
        self.type = "RELAY2"
        pass
    
    @staticmethod
    def getADDR(*args):
        myList = [*args]
        resp = parseIt("RELAY2.getADDR", myList)
        return resp
    
    @staticmethod
    def getID(*args):
        myList = [*args]
        resp = parseIt("RELAY2.getID", myList)
        return resp
    
    @staticmethod
    def getHWrev(*args):
        myList = [*args]
        resp = parseIt("RELAY2.getHWrev", myList)
        return resp
    
    @staticmethod
    def getFWrev(*args):
        myList = [*args]
        resp = parseIt("RELAY2.getFWrev", myList)
        return resp
    
    @staticmethod
    def setLED(*args):
        myList = [*args]
        resp = parseIt("RELAY2.setLED", myList)
        return resp
    
    @staticmethod
    def clrLED(*args):
        myList = [*args]
        resp = parseIt("RELAY2.clrLED", myList)
        return resp
    
    @staticmethod
    def toggleLED(*args):
        myList = [*args]
        resp = parseIt("RELAY2.toggleLED", myList)
        return resp
    
    @staticmethod
    def relayON(*args):
        myList = [*args]
        resp = parseIt("RELAY2.relayON", myList)
        return resp
    
    @staticmethod
    def relayOFF(*args):
        myList = [*args]
        resp = parseIt("RELAY2.relayOFF", myList)
        return resp
    
    @staticmethod
    def relayTOGGLE(*args):
        myList = [*args]
        resp = parseIt("RELAY2.relayTOGGLE", myList)
        return resp
    
    @staticmethod
    def relayALL(*args):
        myList = [*args]
        resp = parseIt("RELAY2.relayALL", myList)
        return resp
    
    @staticmethod
    def relaySTATE(*args):
        myList = [*args]
        resp = parseIt("RELAY2.relaySTATE", myList)
        return resp

"""
THERMO class includes all 24 functions
Common Functions: getADDR, getID, getHWrev, getFWrev, RESET
Interrupt Functions: intEnable, intDisable, getINTflags, setINTchannel, getSRQ, setINT, clrINT
LED Functions: setLED, clrLED, toggleLED
Temperature Measurement Functions:
getTEMP - Read temperature from channel (1-12) with scale (C/F/K)
getCOLD - Read cold junction temperature with scale (C/F/K)
getRAW - Read raw values from channel (1-8)
Configuration Functions:
setSCALE - Set temperature scale (C/F/K)
getSCALE - Get current temperature scale
setTYPE - Set thermocouple type (J/K) for channel (1-8)
getTYPE - Get thermocouple type for channel (1-8)
setLINEFREQ - Set line frequency (50/60 Hz)
setSMOOTH - Enable smoothing
clrSMOOTH - Disable smoothing
"""
class THERMO:
    def __init__(self):
        self.type = "THERMO"
        pass
    
    @staticmethod
    def getADDR(*args):
        myList = [*args]
        resp = parseIt("THERMO.getADDR", myList)
        return resp
    
    @staticmethod
    def getID(*args):
        myList = [*args]
        resp = parseIt("THERMO.getID", myList)
        return resp
    
    @staticmethod
    def getHWrev(*args):
        myList = [*args]
        resp = parseIt("THERMO.getHWrev", myList)
        return resp
    
    @staticmethod
    def getFWrev(*args):
        myList = [*args]
        resp = parseIt("THERMO.getFWrev", myList)
        return resp
    
    @staticmethod
    def intEnable(*args):
        myList = [*args]
        resp = parseIt("THERMO.intEnable", myList)
        return resp
    
    @staticmethod
    def intDisable(*args):
        myList = [*args]
        resp = parseIt("THERMO.intDisable", myList)
        return resp
    
    @staticmethod
    def getINTflags(*args):
        myList = [*args]
        resp = parseIt("THERMO.getINTflags", myList)
        return resp
    
    @staticmethod
    def setINTchannel(*args):
        myList = [*args]
        resp = parseIt("THERMO.setINTchannel", myList)
        return resp
    
    @staticmethod
    def setLED(*args):
        myList = [*args]
        resp = parseIt("THERMO.setLED", myList)
        return resp
    
    @staticmethod
    def clrLED(*args):
        myList = [*args]
        resp = parseIt("THERMO.clrLED", myList)
        return resp
    
    @staticmethod
    def toggleLED(*args):
        myList = [*args]
        resp = parseIt("THERMO.toggleLED", myList)
        return resp
    
    @staticmethod
    def getSRQ(*args):
        myList = [*args]
        resp = parseIt("THERMO.getSRQ", myList)
        return resp
    
    @staticmethod
    def getTEMP(*args):
        myList = [*args]
        resp = parseIt("THERMO.getTEMP", myList)
        return resp
    
    @staticmethod
    def getCOLD(*args):
        myList = [*args]
        resp = parseIt("THERMO.getCOLD", myList)
        return resp
    
    @staticmethod
    def getRAW(*args):
        myList = [*args]
        resp = parseIt("THERMO.getRAW", myList)
        return resp
    
    @staticmethod
    def setSCALE(*args):
        myList = [*args]
        resp = parseIt("THERMO.setSCALE", myList)
        return resp
    
    @staticmethod
    def getSCALE(*args):
        myList = [*args]
        resp = parseIt("THERMO.getSCALE", myList)
        return resp
    
    @staticmethod
    def setTYPE(*args):
        myList = [*args]
        resp = parseIt("THERMO.setTYPE", myList)
        return resp
    
    @staticmethod
    def getTYPE(*args):
        myList = [*args]
        resp = parseIt("THERMO.getTYPE", myList)
        return resp
    
    @staticmethod
    def setLINEFREQ(*args):
        myList = [*args]
        resp = parseIt("THERMO.setLINEFREQ", myList)
        return resp
    
    @staticmethod
    def setSMOOTH(*args):
        myList = [*args]
        resp = parseIt("THERMO.setSMOOTH", myList)
        return resp
    
    @staticmethod
    def clrSMOOTH(*args):
        myList = [*args]
        resp = parseIt("THERMO.clrSMOOTH", myList)
        return resp
    
    @staticmethod
    def RESET(*args):
        myList = [*args]
        resp = parseIt("THERMO.RESET", myList)
        return resp
    
    @staticmethod
    def setINT(*args):
        myList = [*args]
        resp = parseIt("THERMO.setINT", myList)
        return resp
    
    @staticmethod
    def clrINT(*args):
        myList = [*args]
        resp = parseIt("THERMO.clrINT", myList)
        return resp
    
def POLL():
    #global ser
    ADCplates=['-','-','-','-','-','-','-','-']
    CURRENTplates=['-','-','-','-','-','-','-','-']
    DAQCplates=['-','-','-','-','-','-','-','-']
    DAQC2plates=['-','-','-','-','-','-','-','-']
    DIGIplates=['-','-','-','-','-','-','-','-']
    #MOTORplates=['-','-','-','-','-','-','-','-']
    RELAYplates=['-','-','-','-','-','-','-','-']
    RELAYplate2s=['-','-','-','-','-','-','-','-']
    THERMOplates=['-','-','-','-','-','-','-','-']
    for i in range(8):
        resp=CMD("ADC.getADDR("+str(i)+")")
        if (resp[0]==str(i)):
            ADCplates[i]=str(i)
        resp=CMD("CURRENT.getADDR("+str(i)+")")
        if (resp[0]==str(i)):
            CURRENTplates[i]=str(i)
        resp=CMD("DAQC.getADDR("+str(i)+")")
        if (resp[0]==str(i)):
            DAQCplates[i]=str(i)            
        resp=CMD("DAQC2.getADDR("+str(i)+")")
        if (resp[0]==str(i)):
            DAQC2plates[i]=str(i)
        resp=CMD("DIGI.getADDR("+str(i)+")")
        if (resp[0]==str(i)):
            DIGIplates[i]=str(i)
#         resp=CMD("MOTOR.getADDR("+str(i)+")")
#         if (resp[0]==str(i)):
#             MOTORplates[i]=str(i)
        resp=CMD("RELAY.getADDR("+str(i)+")")
        if (resp[0]==str(i)):
            RELAYplates[i]=str(i)
        resp=CMD("RELAY2.getADDR("+str(i)+")")
        if (resp[0]==str(i)):
            RELAYplate2s[i]=str(i)
        resp=CMD("THERMO.getADDR("+str(i)+")")
        if (resp[0]==str(i)):
            THERMOplates[i]=str(i)            
    printL("ADCplates:    ",ADCplates)
    printL("CURRENTplates:",CURRENTplates)
    printL("DAQCplates:   ",DAQCplates)
    printL("DAQC2plates:  ",DAQC2plates)
    printL("DIGIplates:   ",DIGIplates)
    #printL("MOTORplates:  ",MOTORplates)
    printL("RELAYplates:  ",RELAYplates)
    printL("RELAYplate2s: ",RELAYplate2s)
    printL("THERMOplates: ",THERMOplates)
    return

pivid="2E8A"
pipid="10E3"
matches = find_ports_by_vid_pid(pivid,pipid)
if (matches):
    #print ("BRIDGEplate found on "+matches)
    ser = serial.Serial(matches, 115200, timeout=20) # Open port at 115200 baud, with a 20-second timeout (for slow ADCplate sample rates)
else:
    print ("No COM port found with an attached BRDGEplate.")

