import spidev
import time

spi = spidev.SpiDev()

spi.open(0,1)

spi.max_speed_hz = 20000
spi.mode = 0

while True:
    data = spi.readbytes(3)
    print(data)
    print(f'{data[0]:08b} {data[1]:08b} {data[2]:08b}')
    adc = int(data[0]*128 + data[1]/2)
    print(adc)
    adc2 = ((data[0] & 0x1F) << 7) | (data[1] >> 1)
    print(adc2)
    volts = 2.048*adc/4096
    print(volts)
    curr_ma = 1000*(volts/20)/4.99
    print(curr_ma)
    curr_ma2 = adc2/200
    print(curr_ma2)
    time.sleep(1)


