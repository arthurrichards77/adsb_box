import serial
from datetime import datetime

def degmin_to_decdeg(degmin,nsew):
    assert nsew in ['N','S','E','W']
    if nsew in ['N','E']:
        multiplier = 1.0
    else:
        multiplier = -1.0
    assert degmin >= 0
    return multiplier*(int(degmin/100) + (degmin%100)/60.0)

def decode_time_str(time_str):
    return datetime.strptime(time_str,'%H%M%S.%f')

def get_gps_position_time():
    port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)
    lat,lon,gps_time = None,None,None
    for _ in range(50):
        rcv = port.readline().decode('utf-8')
        if rcv.startswith('$GNGLL'):
            #print(rcv)
            fields = rcv.split(',')
            lat = degmin_to_decdeg(float(fields[1]),fields[2])
            lon = degmin_to_decdeg(float(fields[3]),fields[4])
            gps_time = decode_time_str(fields[5])
            break
    return lat,lon,gps_time
    
def main():
    # access the GPS click using its USB port
    port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)
    while True:
        rcv = port.readline().decode('utf-8')
        if rcv.startswith('$GNGLL'):
            fields = rcv.split(',')
            print(fields)
            lat = degmin_to_decdeg(float(fields[1]),fields[2])
            lon = degmin_to_decdeg(float(fields[3]),fields[4])
            print(lat,lon)
            gps_time = decode_time_str(fields[5])
            print(gps_time)
            
if __name__=='__main__':
    main()
