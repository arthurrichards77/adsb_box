"""Utilities to uploadef files to dropbox"""
from os import path, replace, listdir
from glob import glob
from argparse import ArgumentParser
import dropbox
from data_logging import enter_daily_log

def read_secret_file(fname):
    f = open('secrets/'+fname,'r')
    s = f.read()
    f.close()
    return s.strip()

def authorize():
    APP_KEY = read_secret_file('app_key.txt')
    APP_SECRET = read_secret_file('app_secret.txt')
    auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY,
                                                    consumer_secret=APP_SECRET,
                                                    token_access_type='offline')
    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click \"Allow\" (you might have to log in first).")
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()
    oauth_result = auth_flow.finish(auth_code)
    f = open('secrets/refresh_key.txt','w')
    f.write(oauth_result.refresh_token)
    f.close()
    print("Authorization complete")

def upload_file(file_name):
    APP_KEY = read_secret_file('app_key.txt')
    APP_SECRET = read_secret_file('app_secret.txt')
    REFRESH_TOKEN = read_secret_file('refresh_key.txt')
    full_local_path = path.abspath(file_name)
    target_name = '/' + path.basename(file_name)
    enter_daily_log(f'Uploading {full_local_path} to {target_name}','newlogs/log')
    with dropbox.Dropbox(oauth2_refresh_token=REFRESH_TOKEN,
                         app_key=APP_KEY,
                         app_secret=APP_SECRET) as dbx:
        with open(file_name,'rb') as f:
            data = f.read()
            res = dbx.files_upload(data,
                                   target_name,
                                   autorename=True)
            res_name = res.name.encode('utf8')
            enter_daily_log(f'Uploaded {full_local_path} as {res_name}','newlogs/log')

def upload_and_move_files(file_spec, dest_path=None, upload=True):
    if dest_path:
        assert path.isdir(dest_path)
    file_list = glob(file_spec)
    for f in file_list:
        #print(f)
        if path.isfile(f):
            if upload:
                try:
                    #print(f)
                    upload_file(f)
                except dropbox.exceptions.ApiError as e:
                    print(f'API error {e}')
                    enter_daily_log(f'ApiError uploading {f}',
                                    'newlogs/log')
                    continue
            if dest_path:
                new_path = path.join(dest_path,
                                    path.basename(f))
                enter_daily_log(f'Moving {path.abspath(f)} to {path.abspath(new_path)}',
                                'newlogs/log')
                try:
                    replace(f,new_path)
                except PermissionError:
                    enter_daily_log(f'Unable to move {path.abspath(f)}',
                                    'newlogs/log')

def main():
    parser = ArgumentParser(description = 'Upload utilities for dropbox')
    parser.add_argument('-u','--upload',help='Files to upload')
    parser.add_argument('-q','--queue',help='Files to queue for uploading.')
    parser.add_argument('-d','--dest',help='Destination folder for queueing or after uploading')
    args = parser.parse_args()
    if args.queue:
        assert args.dest is not None
        upload_and_move_files(args.queue,args.dest,upload=False)
    elif args.upload:
        upload_and_move_files(args.upload,args.dest,upload=True)
    else:
        authorize()

if __name__=='__main__':
    main()
