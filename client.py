import socket
import ssl
import argparse
import sys


def run_client(host, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect(("www.google.com", port))
        print("Type any thing then ENTER. Press Ctrl+C to terminate")
        while True:
            line = sys.stdin.readline(1024)
            request = line.encode("utf-8")
            #conn.sendall(request)
            conn.send("GET / HTTP/1.0\n\n")
            # MSG_WAITALL waits for full request or error
            response = conn.recv(len(request), socket.MSG_WAITALL)
            sys.stdout.write("Replied: " + response.decode("utf-8"))
    finally:
        conn.close()


# Usage: python echoclient.py --host host --port port
'''
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="server host", default="localhost")
parser.add_argument("--port", help="server port", type=int, default=80)
args = parser.parse_args()
run_client(args.host, args.port)
'''

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = ssl.wrap_socket(s)
    s.connect(('google.com', 443))
    request = b'GET google.com HTTP/1.1\n\n'
    s.send(request)
    print(s.recv(4096).decode())

main()
