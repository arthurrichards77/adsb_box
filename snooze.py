import sys
from datetime import datetime,timedelta
from smbus import SMBus
from data_logging import enter_daily_log

i2c_bus = 1
i2c_dev = 4

#print(sys.argv)
assert len(sys.argv)==3

off_delay = int(sys.argv[1])
assert off_delay>0
assert off_delay<256

snooze_time = int(sys.argv[2])
assert snooze_time>0
assert snooze_time<65536

off_time = datetime.now()+timedelta(seconds=5*off_delay)
on_time = off_time + timedelta(seconds=5*snooze_time)
print(f'Off at {off_time}')
print(f'Back on at {on_time}')
enter_daily_log(f'Snooze {off_delay} {snooze_time}','newlogs/log')

bus = SMBus(i2c_bus)
bus.write_block_data(i2c_dev,off_delay,[snooze_time])
bus.close()
