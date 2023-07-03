import dropbox
import argparse

def main():
    parser = argparse.ArgumentParser(description='Upload to Dropbox')
    parser.add_argument('--token', required=True,
                        help='Access token '
                        '(see https://www.dropbox.com/developers/apps)')
    parser.add_argument('--file', required=True,
                        help='relative path to file')
    args = parser.parse_args()
    local_path = args.file
    dbx = dropbox.Dropbox(args.token)
    mode = dropbox.files.WriteMode.overwrite
    upload_path = '/' + local_path
    print(f'Will upload {local_path} to {upload_path}')
    with open(local_path, 'rb') as f:
        data = f.read()
    try:
        res = dbx.files_upload(data, upload_path, mode, mute=True)
    except dropbox.exceptions.ApiError as err:
        print('*** API error', err)
        return None
    res_path = res.name.encode('utf8')
    print(f'Uploaded as {res_path}')

main()