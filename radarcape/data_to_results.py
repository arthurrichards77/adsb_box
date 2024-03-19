"""
Convert raw port 30003 ADSB data in CSV files to processed CSV records
Import format documented at http://woodair.net/sbs/Article/Barebones42_Socket_Data.htm
Output format is Hex ID, date, time, altitude, lat, lon, callsign
There is an output row for every airborne position (msg 3) received
Callsign is looked up from the last received Identification message (msg 1) from the same Hex ID
"""
import os

current_dir = os.getcwd()
print(f'Processing {current_dir}')
target_dir = os.path.join(os.path.pardir,os.path.basename(current_dir).replace('data','results'))
print(f'Targeting {target_dir}')
if not os.path.isdir(target_dir):
    os.mkdir(target_dir)

fields_to_save = [4,6,7,11,14,15]
call_signs = {}

file_list = os.listdir()
csv_file_list = [f for f in file_list if f.endswith('.csv')]
for file_num, file_name in enumerate(csv_file_list):
    out_name = os.path.join(target_dir,f'data_{file_num:05d}.csv')
    print(f'Processing {file_name} into {out_name}')
    outfile = open(out_name, "w")
    with open(file_name) as fh:
        for line in fh:
            line_in = line.strip()
            fields = line_in.split(',')
            if len(fields)<10:
                continue
            if fields[1]=='1':
                call_signs[fields[4]] = fields[10]
            if fields[1]=='3':
                if fields[4] in call_signs:
                    line_out = ','.join([fields[ii] for ii in fields_to_save])+ "," + call_signs[fields[4]]+"\n"
                    #print(line_out)
                    outfile.write(line_out)
    outfile.close()

file_num = 0
while False:
  fields_to_save = [4,6,7,11,14,15]
  dt_now = datetime.now()
  if args.filestub:
    filename=f'{args.filestub}_{file_num:05d}.csv'
    file_num += 1
  else:
    filename = f'data_{dt_now.year}_{dt_now.month}_{dt_now.day}_{dt_now.hour}_{dt_now.minute}_{dt_now.second}.csv'
  f = open(filename, "w")
  print('Opened file {}'.format(filename))
  for jj in range(20000):
    line_in = input()
    fields = line_in.split(',')
    if fields[1]=='1':
      call_signs[fields[4]] = fields[10]
    if fields[1]=='3':
      if fields[4] in call_signs:
        f.write(','.join([fields[ii] for ii in fields_to_save])+ "," + call_signs[fields[4]]+"\n")
  f.close()
  print('Closed file {}'.format(filename))
