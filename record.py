from datetime import datetime
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Upload to Dropbox')
parser.add_argument('--token', required=True,
                    help='Access token '
                    '(see https://www.dropbox.com/developers/apps)')
args = parser.parse_args()

for ii in range(10000):
  fields_to_save = [4,6,7,11,14,15]
  call_signs = {}
  dt_now = datetime.now()
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
  subprocess.Popen(['python3','dropbox_upload.py','--token', args.token, '--file', filename])
