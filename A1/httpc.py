import socket
from urllib.parse import urlparse
import argparse


def get(url, verbose=False):
    o = urlparse(url)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((o.netloc, 80))
        request = ( "GET "+ o.path + "?" + o.query + " HTTP/1.0\r\n"
                    "Host:" + o.netloc + "\r\n\r\n")
        s.sendall(bytes(request, 'utf-8'))
        data = recvall(s)
    
    getCode(data.decode('utf-8'))
    
    if verbose:
        print(data.decode('utf-8'))
    else:
        responses = data.decode('utf-8').split("\r\n\r\n")
        print (responses[1])
    

def post(url, paras, format):
    o = urlparse(url)

    headers = ( "POST {path} HTTP/1.0\r\n"
                "{content_type}\r\n"
                "Content-Length: {content_length}\r\n"
                "Host: {host}\r\n"
                "User-Agent: Concordia-HTTP/1.0\r\n"
                "Connection: close\r\n\r\n")

    body_bytes = paras.encode('utf-8')                              
    header_bytes = headers.format(
        path=o.path,
        content_type=format,
        content_length=len(paras),
        host=o.netloc
    ).encode('utf-8')

    request = header_bytes + body_bytes

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((o.netloc, 80))
        s.sendall(request)
        data = recvall(s)
    print(data.decode('utf-8'))


def recvall(sock):
    BUFF_SIZE = 1024 # 1 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

def getCode(response):
    lines = response.split("\r\n")
    code = lines[0].split(" ")[1]
    location = lines[1]
    print(code + ":" + location)

URL1 = 'http://httpbin.org/status/418'
URL2 = 'http://httpbin.org/post'

ex1 = "http://httpbin.org/get?course=networking&assignment=1"

# get(URL1)

# post(URL2)

# get(ex1, True)

# Usage: python httpc.py (get|post) [-v] (-h "k:v")* [-d inline-data] [-f file] URL

# python3 httpc.py get 'http://httpbin.org/get?course=networking&assignment=1'
# python3 httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1'
# python3 httpc.py -header --d post http://httpbin.org/post '{"Assignment": 1}' Content-Type:application/json

parser = argparse.ArgumentParser()
parser.add_argument("-v", action='store_true')
parser.add_argument("-header", action='store_true')
parser.add_argument("--d", action='store_true')
parser.add_argument("method", choices=['get', 'post'], help="method")
parser.add_argument("url")
parser.add_argument("paras", nargs='?')
parser.add_argument("format", nargs='?')
args = parser.parse_args()
# print(args)

if args.method == 'get':
    get(args.url, args.v)

if args.method == 'post':
    post(args.url, args.paras, args.format)
