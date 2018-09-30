import socket
import threading
import argparse
import time


def run_server(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((host, port))
        listener.listen(5)
        print('Time server is listening at', port)
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    finally:
        listener.close()


def handle_client(conn, addr):
    print('New client from', addr)
    try:
        # Number of seconds elapsed from 1900 to 1970
        time1970 = 2208988800
        now = int(time.time()) + time1970
        # Must send uint32 in big-endian
        conn.sendall(now.to_bytes(4, byteorder='big'))
    finally:
        conn.close()


# Usage python echoserver.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="time server port", type=int, default=8037)
args = parser.parse_args()
run_server('', args.port)
