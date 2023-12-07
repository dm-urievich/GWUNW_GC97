import serial
import time

serial_port = '/dev/ttyUSB0'

def getLong(data, addr):
    return data[addr]*256*256*256 + data[addr+1]*256*256 + data[addr+2]*256 + data[addr+3]

def getInt(data, addr):
    return data[addr]*256 + data[addr+1]
    
def pritnData(s):
    voltage = getLong(s, 8)
    current = getLong(s, 12)
    power = getLong(s, 25)
    charge = getLong(s, 17)
    charge_p = s[5]
    loadtime = getLong(s, 21)
    temperature = getInt(s, 6)
    power_decimal_point = s[29]
    # output readings to console
    print("Voltage:", voltage/100, "V")
    print("Current:", current/100, "A")
    power_div = pow(10, power_decimal_point)
    print("Power:", power/power_div, "W")
    print("isCharge:", s[16])
    print("Charge:", charge/1000, "Ah ", charge_p, "%")
    print("Loadtime:", loadtime,"min")
    print("Temperature:", temperature/10,"°C")

def isDataValid(data):
    if (len(data) >= 31 and data[0] == 0xfe and data[1] == 0xfe and data[2] == 0xfe and data[3] == 0xfe):
        check_sum = 0
        for i in data[0:30]:
            check_sum += i

        if check_sum % 256 == data[30]:
            return True
    
    #print("data not valid")
    return False

def startContinuousOutput(ser):
    print("Start Continuous Output Data")
    ser.write(bytes([0x77, 0x33, 0xC0, 0x42]))

ser = serial.Serial()
ser.baudrate = 19200
ser.port = serial_port
ser.timeout = 1
timeout_count = 0

try:
    while True:
        try:
            #print("try to open port")
            ser.open()
            # Start Continuous Output Data
            if ser.is_open:
                startContinuousOutput(ser)
            
            while True:
                ser.reset_input_buffer()
                s = ser.read(128)
                #print(len(s))
                #print(" ".join(hex(n) for n in s))
                
                if isDataValid(s):
                    print()
                    pritnData(s)

                if len(s) == 0:
                    timeout_count += 1

                    if timeout_count == 30:
                        startContinuousOutput(ser)
                        timeout_count = 0
                else:
                    timeout_count = 0
                #time.sleep(0.5)
                
        except serial.SerialException:
            print("30s delay to reconnect")
            if ser.is_open:
                ser.close()
            time.sleep(30)
            
except KeyboardInterrupt:
    print("Exit")

ser.close()    
