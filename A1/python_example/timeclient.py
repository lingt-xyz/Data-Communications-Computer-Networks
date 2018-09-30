import socket
import argparse
from datetime import datetime


def run_client(host, port):
    conn = socket.create_connection((host, port))
    try:
        buf = conn.recv(4, socket.MSG_WAITALL)
        # Number of seconds elapsed from 1900 to 1970
        time1970 = 2208988800
        rtime = int.from_bytes(buf, byteorder='big') - time1970
        print(datetime.fromtimestamp(rtime))
    finally:
        conn.close()


# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="time server host", default="localhost")
parser.add_argument("--port", help="time server port", type=int, default=8037)
args = parser.parse_args()
run_client(args.host, args.port)
