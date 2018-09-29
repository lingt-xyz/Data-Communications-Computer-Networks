import socket
import argparse
import sys


def run_client(host, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, port))
        print("Type any thing then ENTER. Press Ctrl+C to terminate")
        while True:
            line = sys.stdin.readline(1024)
            request = line.encode("utf-8")
            conn.sendall(request)
            # MSG_WAITALL waits for full request or error
            response = conn.recv(len(request), socket.MSG_WAITALL)
            sys.stdout.write("Replied: " + response.decode("utf-8"))
    finally:
        conn.close()


# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="server host", default="localhost")
parser.add_argument("--port", help="server port", type=int, default=8007)
args = parser.parse_args()
run_client(args.host, args.port)
