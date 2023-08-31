"""
Ensure all files in current directory have 2 significant figures 
in their time stamps, i.e. _7_ becomes _07_
"""
import os
import re

file_list = os.listdir()
csv_file_list = [f for f in file_list if f.endswith('.csv')]
for file_name in csv_file_list:
    res = re.finditer('_[0-9][._]', file_name, )
    if res:
        new_file_name = file_name
        work_backwards = [r for r in res]
        work_backwards.reverse()
        for r in work_backwards:
            new_file_name = new_file_name[0:r.start()+1] + '0' + new_file_name[1+r.start():]
        print(f'Change {file_name} to {new_file_name}')
        os.rename(file_name,new_file_name)