import sys
import time
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
enter_daily_log(f'Snooze {off_delay} {snooze_time} back at {on_time}','newlogs/log')

bus = SMBus(i2c_bus)
high_byte = snooze_time >> 8
low_byte = snooze_time & 255
# will write four bytes: device, off_delay, 2 (for 2 bytes coming), high_byte, low_byte
for attempt in range(10):
    try:
        bus.write_block_data(i2c_dev,off_delay,[high_byte, low_byte])
    except OSError as e:
        enter_daily_log(f'Snooze encountered OSError {e}','newlogs/log')
        time.sleep(2)
    else:
        enter_daily_log(f'Snooze OK','newlogs/log')
bus.close()
