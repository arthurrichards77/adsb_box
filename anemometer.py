"""Driver and data recorder for the 4-20mA anemometer"""
from data_logging import enter_hourly_log
from argparse import ArgumentParser

class Anemometer:

    def __init__(self):
        pass

    def get_wind_speed(self):
        # fake for now
        return 24.2
    
    def get_gps_position(self):
        # fake for now
        return 51.47951494978535, -2.6046225943885166
    
    def log_wind(self,file_stub):
        enter_hourly_log(f'WND,{self.get_wind_speed()}',file_stub)

    def log_gps(self,file_stub):
        lat,lon = self.get_gps_position()
        enter_hourly_log(f'GPS,{lat},{lon}',file_stub)

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
