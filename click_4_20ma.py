import spidev
import time

def get_click_current(device_id=0):
    spi = spidev.SpiDev()
    spi.open(0,device_id)
    spi.max_speed_hz = 20000
    spi.mode = 0
    data = spi.readbytes(2)
    adc = ((data[0] & 0x1F) << 7) | (data[1] >> 1)
    curr_ma = adc/200
    print(f'Current {curr_ma} mA')
    return curr_ma

def main():
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = 20000
    spi.mode = 0
    while True:
        data = spi.readbytes(3)
        print(data)
        print(f'{data[0]:08b} {data[1]:08b} {data[2]:08b}')
        adc = int(data[0]*128 + data[1]/2)
        print('ADC',adc)
        adc2 = ((data[0] & 0x1F) << 7) | (data[1] >> 1)
        print('ADC2',adc2)
        volts = 2.048*adc/4096
        print('volts',volts)
        curr_ma = 1000*(volts/20)/4.99
        print('curr_ma',curr_ma)
        curr_ma2 = adc2/200
        print('curr_ma',curr_ma2)
        time.sleep(1)

if __name__=='__main__':
    main()
