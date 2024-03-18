"""Utilities to uploadef files to dropbox"""
from os import path
from argparse import ArgumentParser
from dropbox import Dropbox, DropboxOAuth2FlowNoRedirect
from data_logging import enter_daily_log

def read_secret_file(fname):
    f = open('secrets/'+fname,'r')
    s = f.read()
    f.close()
    return s.strip()

def authorize():
    APP_KEY = read_secret_file('app_key.txt')
    APP_SECRET = read_secret_file('app_secret.txt')
    auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY,
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
    with Dropbox(oauth2_refresh_token=REFRESH_TOKEN,
                 app_key=APP_KEY,
                 app_secret=APP_SECRET) as dbx:
        with open(file_name,'rb') as f:
            data = f.read()
            res = dbx.files_upload(data,
                                   target_name)
            res_name = res.name.encode('utf8')
            enter_daily_log(f'Uploaded {full_local_path} as {res_name}','log')

def main():
    parser = ArgumentParser(description = 'Upload utilities for dropbox')
    parser.add_argument('-u','--upload',help='File to upload')
    args = parser.parse_args()
    if args.upload:
        upload_file(args.upload)
    else:
        authorize()

if __name__=='__main__':
    main()
