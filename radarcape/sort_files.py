"""
Put files in folders sorted by days
Example:
data_2023_07_04_xx.csv goes into ../results-2023-07-04
"""
import os
import re

file_list = os.listdir()
data_file_list = [f for f in file_list if re.fullmatch('data_2023_[0-9][0-9]_[0-9][0-9]_[0-9][0-9]_[0-9][0-9]_[0-9][0-9].csv', f)]
for file_name in data_file_list:
    month = file_name[10:12]
    day = file_name[13:15]
    folder = f'../results-2023-{month}-{day}'
    print(f'Move {file_name} to {folder}')
    if not os.path.isdir(folder):
        print(f'Make dir {folder}')
        os.mkdir(folder)
    os.rename(file_name,folder+'/'+file_name)