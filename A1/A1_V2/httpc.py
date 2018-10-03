import socket
from urllib.parse import urlparse
import argparse
import MockHttp


def get(url, verbose=False):
    o = urlparse(url)
    host = o.netloc
    while(True):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, 80))
            request = MockHttp.HttpRequest(host, o.path, o.query, None)
            s.sendall(request.getGet())
            data = recvall(s)
        response = MockHttp.HttpResponse(data)

        if(response.code == MockHttp.HttpCode.redirect):
            host = response.location
        else:
            break
    
    if verbose:
        print(response.text)
    else:
        print (response.body)
    

def post(url, paras, format, verbose=False):
    o = urlparse(url)
    host = o.netloc
    
    while(True):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((o.netloc, 80))
            request = MockHttp.HttpRequest(host, o.path, paras, format)
            s.sendall(request.getPost())
            data = recvall(s)
        response = MockHttp.HttpResponse(data)

        if(response.code == MockHttp.HttpCode.redirect):
            host = response.location
        else:
            break

    if verbose:
        print(response.text)
    else:
        print (response.body)

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
    post(args.url, args.paras, args.format, args.v)
