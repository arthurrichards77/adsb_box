# script for retrieving Llanbedr data from Opensky

import os
from pyopensky.trino import Trino
from datetime import datetime, timedelta

# get yesterday 9am
now = datetime.now()
yesterday = now - timedelta(days=7)
yesterday_6am = yesterday.replace(hour=6, minute=0, second=0, microsecond=0)
print(f'Archiving data for 24 hours from {yesterday_6am}')

bounds_wsen = (-(5+35/60),
               52+35/60,
               -(3+55/60),
               53+10/60)
print(f'Area of interest {bounds_wsen}')

if 1<0:
    from pyopensky.config import opensky_config_dir, cache_dir, opensky_config_file, cache_path
    print(f'Config directory is {opensky_config_dir} ({opensky_config_file})')
    print(f'Cache directory is {cache_dir} ({cache_path})')

if 1<0:
    with open('opensky_settings.conf','r') as f:
        for line in f.readlines():
            if not line.startswith('['):
                line_bits = line.split('=')
                var_name = 'OPENSKY_' + line_bits[0].strip().upper()
                var_value = line_bits[1].strip()
                print(f'Setting {var_name} to {var_value}')
                os.environ[var_name] = var_value

trino = Trino()
print('Downloading history')
data = trino.history(start=yesterday_6am, bounds=bounds_wsen)

filename = 'outbox/llanbedr_' + yesterday_6am.isoformat().replace(':','-') + '_trino.csv'
print(f'Saving to {filename}')
data.to_csv(filename)
