"""Utilities for logging data to files
including splitting 
and timestamping files and entries"""
from datetime import datetime
from argparse import ArgumentParser
from sys import stdin

class DataLog:
    """
    file_stub : root of data log file name

    file_suffix : (optional) end of file name, default is '.txt'
    
    max_entries : (optional) split log across files with no more entries than this.
    
    file_stamp_format : (optional) file name time stamp format according to strftime

    """

    def __init__(self, file_stub, file_suffix = '.txt',max_entries = None, file_stamp_format = '%Y%m%d%H%M%S'):
        self.file_stub = file_stub
        self.file_suffix = file_suffix
        self.max_entries = max_entries
        self.time_stamp = datetime.now().strftime(file_stamp_format)
        self.file_count = 0
        self.entry_count = None
        self.file_handle = None
        self._refresh_file()

    def _refresh_file(self):
        if self.file_handle:
            self.file_handle.close()
        self.file_count += 1
        if self.max_entries:
            index_stamp = f'{self.file_count:06d}'
        else:
            index_stamp = ''
        file_name = f'{self.file_stub}{self.time_stamp}{index_stamp}{self.file_suffix}'
        self.file_handle = open(file_name,'at')
        self.entry_count = 0

    def log_entry(self, text):
        if self.max_entries:
            if self.entry_count==self.max_entries:
                self._refresh_file()
        time_stamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f')
        self.file_handle.write(f'{time_stamp},{text.strip()}\n')
        self.entry_count += 1

def enter_daily_log(text,file_stub):
    data_log = DataLog(file_stub=file_stub,
                       file_stamp_format='%Y%m%d')
    data_log.log_entry(text)

def enter_hourly_log(text,file_stub):
    data_log = DataLog(file_stub=file_stub,
                       file_stamp_format='%Y%m%d%H00')
    data_log.log_entry(text)

def stream_stdin_to_log(file_stub,max_entries=10000):
    data_log = DataLog(file_stub=file_stub,max_entries=max_entries)
    for line in stdin:
        data_log.log_entry(line)

def main():
    parser = ArgumentParser(description = 'Log text with timestamps')
    parser.add_argument('-f','--file_stub',help='Start of file name',
                        default='newlogs/log')
    parser.add_argument('-d','--daily',help='Text to add to daily log')
    parser.add_argument('-u','--hourly',help='Text to add to hourly log')
    parser.add_argument('-s','--stream',help='Stream from standard input to a running log'
                        action='store_true',default=False)
    args = parser.parse_args()
    if args.daily:
        enter_daily_log(args.daily, args.file_stub)
    if args.hourly:
        enter_hourly_log(args.hourly, args.file_stub)
    if args.stream:
        stream_stdin_to_log(args.file_stub)

if __name__=='__main__':
    main()