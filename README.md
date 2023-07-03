# Simple dropbox uploading

Written for caching ADSB data from remote box

Draws heavily on [https://github.com/dropbox/dropbox-sdk-python/blob/master/example/updown.py] 
but just uploads and overwrites a single file.

Need to create a scoped DropBox app following [https://www.dropbox.com/developers/apps] and then generate an access token for it.
The `simple_upload.py` script takes that token as an argument, or you can paste the token into `token.txt` and feed it in as in `test.ps1`.
