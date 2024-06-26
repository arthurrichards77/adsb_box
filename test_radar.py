import time
import socket
import argparse

test_data = """MSG,3,1,22745,4841A9,22745,2023/8/24,15:49:17.469,2023/8/24,15:49:17.469,,38000,,,50.40327,-1.06381,,,0,0,0,0
MSG,1,1,22709,48520A,22709,2023/8/24,15:49:17.525,2023/8/24,15:49:17.525,TRA26W,,,,,,,,,,,
MSG,3,1,22738,A255DD,22738,2023/8/24,15:49:17.532,2023/8/24,15:49:17.532,,23975,,,50.81363,-0.45813,,,0,1,0,0
MSG,3,1,22694,40769A,22694,2023/8/24,15:49:17.534,2023/8/24,15:49:17.534,,1650,,,51.38635,-2.62381,,,0,0,0,0
MSG,3,1,22723,501C0B,22723,2023/8/24,15:49:17.545,2023/8/24,15:49:17.545,,37000,,,50.85911,-1.44525,,,0,0,0,0
MSG,1,1,22726,A3DEFB,22726,2023/8/24,15:49:17.622,2023/8/24,15:49:17.622,CMB970,,,,,,,,,,,
MSG,3,1,22726,A3DEFB,22726,2023/8/24,15:49:17.642,2023/8/24,15:49:17.642,,38000,,,51.04197,-0.99564,,,0,0,0,0
MSG,1,1,22741,440C36,22741,2023/8/24,15:49:17.682,2023/8/24,15:49:17.682,EJU79ED,,,,,,,,,,,
MSG,1,1,22741,440C36,22741,2023/8/24,15:49:17.689,2023/8/24,15:49:17.689,EJU79ED,,,,,,,,,,,
MSG,3,1,22692,40717F,22692,2023/8/24,15:49:17.705,2023/8/24,15:49:17.705,,7675,,,51.49134,-2.18604,,,0,0,0,0
MSG,3,1,22681,407DA5,22681,2023/8/24,15:49:17.773,2023/8/24,15:49:17.773,,32700,,,51.84071,-3.67935,,,0,0,0,0
MSG,3,1,22746,4D02CD,22746,2023/8/24,15:49:17.785,2023/8/24,15:49:17.785,,20925,,,50.45555,-1.19952,,,0,0,0,0
MSG,1,1,22694,40769A,22694,2023/8/24,15:49:17.828,2023/8/24,15:49:17.828,TOM2J,,,,,,,,,,,
MSG,3,1,22735,405200,22735,2023/8/24,15:49:17.875,2023/8/24,15:49:17.875,,6200,,,51.05054,-1.38577,,,0,1,0,0
MSG,3,1,22714,40796B,22714,2023/8/24,15:49:17.886,2023/8/24,15:49:17.886,,18550,,,51.44888,-1.75308,,,0,0,0,0
MSG,1,1,22745,4841A9,22745,2023/8/24,15:49:17.909,2023/8/24,15:49:17.909,TRA6444,,,,,,,,,,,
MSG,3,1,22723,501C0B,22723,2023/8/24,15:49:17.945,2023/8/24,15:49:17.945,,37000,,,50.85855,-1.44586,,,0,0,0,0
MSG,1,1,22709,48520A,22709,2023/8/24,15:49:17.945,2023/8/24,15:49:17.945,TRA26W,,,,,,,,,,,
MSG,1,1,22695,4CA63A,22695,2023/8/24,15:49:17.950,2023/8/24,15:49:17.950,EIN165,,,,,,,,,,,
MSG,3,1,22709,48520A,22709,2023/8/24,15:49:17.965,2023/8/24,15:49:17.965,,37000,,,50.65503,-1.61157,,,0,0,0,0
MSG,3,1,22745,4841A9,22745,2023/8/24,15:49:17.969,2023/8/24,15:49:17.969,,38000,,,50.40430,-1.06308,,,0,0,0,0"""
#print(test_data)
test_msgs = test_data.split("\n")
#print(test_msgs)
#exit()

parser = argparse.ArgumentParser(description='Simulator for RadarCape Port 30003 data.  If port given, will wait for connection and serve via socket.  Otherwise will just print.')
parser.add_argument('-p','--port',type=int,
                    help='Port number to serve data on.')
parser.add_argument('-i','--ipaddr',default='127.0.0.1',
                    help='IP address of interface to serve data on.')
args = parser.parse_args()

s = None
conn = None
if args.port:
    print(f'Listening on {args.ipaddr}:{args.port}')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((args.ipaddr, args.port))
    s.listen()
    s.settimeout(2)

for ii in range(10000):
    if args.port:
        if not conn:
            try:
                print('Waiting for connection')
                conn, addr = s.accept()
                print(f"Connected by {addr}")
            except TimeoutError:
                conn = None
                continue
    try:
        for m in test_msgs:
            if conn:
                conn.sendall(m.encode())
                time.sleep(0.01) # has happy effect of flushing the socket
            else:
                print(m.strip())
                # time.sleep(0.01) # for some reason this stops the pipe from working
    except KeyboardInterrupt:
        break
    except ConnectionAbortedError:
        print("Lost client connection")
        conn = None
        pass

if conn:
    print('Closing connection')
    conn.close()

if s:
    print('Closing server')
    s.close()