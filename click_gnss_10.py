import serial

# access the GPS click using its USB port
port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)

while True:
    rcv = port.readline()
    print(rcv)