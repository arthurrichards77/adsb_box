"""Driver and data recorder for the 4-20mA anemometer"""
from data_logging import enter_hourly_log
from argparse import ArgumentParser
from click_4_20ma import get_click_current
from click_gnss_10 import get_gps_position_time

class Anemometer:

    def __init__(self):
        pass

    def get_wind_speed(self):
        current = get_click_current()
        if current<3.8:
            return -1.0
        if current>20.2:
            return -1.0
        return 50.0*(current-4.0)/16.0
    
    def get_gps_position(self):
        lat,lon,gps_time = get_gps_position_time()
        return lat, lon, gps_time
    
    def log_wind(self,file_stub):
        enter_hourly_log(f'WND,{self.get_wind_speed()}',file_stub)

    def log_gps(self,file_stub):
        lat,lon,gps_time = self.get_gps_position()
        enter_hourly_log(f'GPS,{lat},{lon},{gps_time}',file_stub)

def main():
    parser = ArgumentParser(description='Get wind speed and position data from the anemometer and associated GPS')
    parser.add_argument('-w','--wind',help='Log file for wind speed measurement')
    parser.add_argument('-p','--pos',help='Log file for position measurement')
    args = parser.parse_args()
    anmtr = Anemometer()
    if args.wind:
        anmtr.log_wind(args.wind)
    if args.pos:
        anmtr.log_gps(args.pos)

if __name__=='__main__':
    main()
